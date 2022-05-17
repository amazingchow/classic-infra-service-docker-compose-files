# -*- coding: utf-8 -*-
import faker
__Faker = faker.Faker()
import sys
import time
import tqdm
import uuid
from cassandra.cluster import Cluster


def insert(total_queries : int):
    try:
        cluster = Cluster(["127.0.0.1"], port=19042)
        session = cluster.connect()
        session.execute("CREATE KEYSPACE IF NOT EXISTS people WITH replication \
            = {'class': 'SimpleStrategy', 'replication_factor': '1' };")
        session.execute("USE people;")
        session.execute("CREATE TABLE IF NOT EXISTS people.eployees \
            (id uuid, name text, birth_day text, address text, job text, PRIMARY KEY (id));")
        prepared_insert = session.prepare("INSERT INTO people.eployees \
            (id, name, birth_day, address, job) VALUES (?, ?, ?, ?, ?);")
        for _ in tqdm.tqdm(range(total_queries)):
            session.execute(prepared_insert, (
                uuid.uuid4(), 
                __Faker.name(), 
                __Faker.date_of_birth(minimum_age=18).strftime("%Y-%m-%d"), 
                __Faker.address(), 
                __Faker.job()
            ))
            time.sleep(0.01)
    except Exception as e:
        print("failed to insert into cassandra cluster, err: {}".format(e))
        sys.exit(-1)


if __name__ == "__main__":
    TOTAL_QUERIES = 1000000

    st = time.time()
    insert(TOTAL_QUERIES)
    ed = time.time()
    print("finished executing {} inserts in {:.2f} seconds.".
        format(TOTAL_QUERIES, ed - st))
