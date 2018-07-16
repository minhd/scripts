#!/bin/bash

neo4jHOME=/Users/minhd/dev/ands/data/test/neo4j/
neo4jDOCKERHOME=/Users/minhd/dev/ands/docker/docker-dev

# deletes old swap.db
rm -rf $neo4jHOME/data/databases/swap.db

# do the import
cd $neo4jDOCKERHOME
docker-compose exec neo4j bin/neo4j-admin import \
    --database swap.db \
    --mode csv \
    --nodes import/nodes.csv \
    --nodes import/nodes-relatedInfo.csv \
    --relationships import/direct.csv \
    --relationships import/identical.csv \
    --relationships import/relations-relatedInfo.csv \
    --relationships import/primary.csv

rc=$?; if [[ $rc != 0 ]]; then exit $rc; fi

docker-compose stop neo4j
rm -rf $neo4jHOME/data/databases/graph.db.old
mv $neo4jHOME/data/databases/graph.db $neo4jHOME/data/databases/graph.db.old
mv $neo4jHOME/data/databases/swap.db $neo4jHOME/data/databases/graph.db
docker-compose start neo4j