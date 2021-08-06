CONTAINER_ID=50dcad20c122
TOPIC=topic-1

create-topics:
	@docker exec -it $(CONTAINER_ID) /bin/bash -c \
		"kafka-topics.sh --create --replication-factor 3 --partitions 32 --topic topic-1 --zookeeper zk_node0:2181,zk_node1:2181,zk_node2:2181/"
	@docker exec -it $(CONTAINER_ID) /bin/bash -c \
		"kafka-topics.sh --create --replication-factor 3 --partitions 32 --topic topic-2 --zookeeper zk_node0:2181,zk_node1:2181,zk_node2:2181/"
	@docker exec -it $(CONTAINER_ID) /bin/bash -c \
		"kafka-topics.sh --create --replication-factor 3 --partitions 32 --topic topic-3 --zookeeper zk_node0:2181,zk_node1:2181,zk_node2:2181/"

list-topics:
	@docker exec -it $(CONTAINER_ID) /bin/bash -c \
		"kafka-topics.sh --list --zookeeper zk_node0:2181,zk_node1:2181,zk_node2:2181/"

describe-topic:
	@docker exec -it $(CONTAINER_ID) /bin/bash -c \
		"kafka-topics.sh --describe --topic ${TOPIC} --zookeeper zk_node0:2181,zk_node1:2181,zk_node2:2181/"

# 1. 进入某个kafka节点容器里面
# 2. 新建/kafka/topics-to-move.json
# 3. 执行如下指令
# 4. 保存"Proposed partition reassignment configuration"输出为reassignment-configuration.json
reassign-partitions-step1:
	kafka-reassign-partitions.sh --zookeeper zk_node0:2181,zk_node1:2181,zk_node2:2181/ \
		--topics-to-move-json-file /kafka/topics-to-move.json --broker-list 1001,1002,1003 --generate

# 1. 执行如下指令
# 2. 保存输出为regenerate-reassignment-configuration.json
reassign-partitions-step2:
	python regenerate-reassignment-configuration.py

# 1. 进入某个kafka节点容器里面
# 2. 新建/kafka/regenerate-reassignment-configuration.json
# 3. 执行如下指令
reassign-partitions-step3:
	kafka-reassign-partitions.sh --zookeeper zk_node0:2181,zk_node1:2181,zk_node2:2181/ \
		--reassignment-json-file /kafka/regenerate-reassignment-configuration.json --bootstrap-server localhost:9092 --execute

	kafka-reassign-partitions.sh --zookeeper zk_node0:2181,zk_node1:2181,zk_node2:2181/ \
		--reassignment-json-file /kafka/regenerate-reassignment-configuration.json --bootstrap-server localhost:9092 --verify
