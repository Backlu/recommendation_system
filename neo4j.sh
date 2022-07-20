docker run \
    --name aaneo4j_ida \
    -p7471:7474 -p7681:7687 \
    -d \
    -e NEO4J_apoc_export_file_enabled=true \
    -e NEO4J_apoc_import_file_enabled=true \
    -e NEO4J_apoc_import_file_use__neo4j__config=true \
    -e NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.* \
    -e NEO4J_dbms_security_procedures_allowlist=gds.*,apoc.* \
    -v /Users/jayhsu/work/ws/neo4j/recommendation_system/data:/data \
    -v /Users/jayhsu/work/ws/neo4j/recommendation_system/logs:/logs \
    -v /Users/jayhsu/work/ws/neo4j/recommendation_system/import:/var/lib/neo4j/import \
    -v /Users/jayhsu/work/ws/neo4j/recommendation_system/plugins:/plugins \
    --env NEO4J_dbms_memory_heap_max__size=2g \
    --env NEO4J_dbms_memory_pagecache_size=2g \
    --env NEO4J_AUTH=neo4j/admin \
    neo4j:latest
