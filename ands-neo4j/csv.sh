#!/bin/bash

importPath=/Users/minhd/dev/ands/data/test/neo4j/import/

start=$(date +'%s')
echo "exporting started... $importPath"
cd ~/dev/ands/registry
for module in 'nodes' 'direct' 'relatedInfoNodes' 'relatedInfoRelations' 'identical' 'primary'
do
   php ands.php export:csv --importPath=$importPath --$module -q &
done
wait
echo "exporting finished ... It took $(($(date +'%s') - $start)) seconds"