prepare:
	docker network create component-net

cassandra-cql:
	docker run -it --rm --network component-net cassandra:3.11.5 cqlsh cassandra_001
	# CREATE KEYSPACE IF NOT EXISTS leader_elect_test WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'} AND durable_writes = true;