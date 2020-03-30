create-net:
	docker network create component-net

list-net:
	docker network list

cassandra-cql:
	docker run -it --rm --network component-net cassandra:3.11.5 cqlsh cassandra_001
