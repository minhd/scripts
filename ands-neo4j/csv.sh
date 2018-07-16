#!/bin/bash

importPath=/Users/minhd/dev/ands/data/test/neo4j/import/
registryHome=~/dev/ands/registry

start=$(date +'%s')
echo "exporting started... $importPath"
echo "registry: $registryHome"
echo "import: $importPath"

cd $registryHome
for module in 'nodes' 'direct' 'relatedInfoNodes' 'relatedInfoRelations' 'identical' 'primary'
do
   php ands.php export:csv --importPath=$importPath --$module -q &
done
wait
echo "exporting finished ... It took $(($(date +'%s') - $start)) seconds"