# -*- coding: utf-8 -*-
import faker
__Faker = faker.Faker()
import kafka
import tqdm
import ujson as json
from google.protobuf.json_format import Parse

import sys
import os
sys.path.append(os.path.abspath('./gen'))
from gen.pb_python.people_pb2 import Person

__KAFKA_BROKERS = ["127.0.0.1:9091", "127.0.0.1:9092", "127.0.0.1:9093"]
__PRODUCER = kafka.KafkaProducer(bootstrap_servers=__KAFKA_BROKERS)

def produce(send_times : int, topic : str):
    for _ in tqdm.tqdm(range(send_times)):
        person_in_json_format = {
            "name": __Faker.name(),
            "birth_day": __Faker.date_of_birth(minimum_age=18).strftime("%Y-%m-%d"),
            "address": __Faker.address(),
            "job": __Faker.job()
        }
        person = Parse(json.dumps(person_in_json_format), Person())
        try:
            __PRODUCER.send(topic, person.SerializeToString())
        except Exception as e:
            print("failed to produce message into '{}', err: {}".format(topic, e))
            sys.exit(-1)


if __name__ == "__main__":
    topic_list = ["topic-1", "topic-2", "topic-3"]
    send_times = 100000
    for topic in topic_list:
        print("produce messages for '{}'".format(topic))
        produce(send_times, topic)
