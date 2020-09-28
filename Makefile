prepare:
	docker network create component-net

cassandra-cql:
	docker run -it --rm --network component-net cassandra:3.11.5 cqlsh cassandra_001
