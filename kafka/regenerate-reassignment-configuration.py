# -*- coding: utf-8 -*-
import copy
import json


def next_permutation(arr):
    l = len(arr)
    x = arr[0]
    arr[:l-1] = arr[1:l]
    arr[l-1] = x


def resort_reassignment_configuration():
    f = open("./reassignment-configuration.json", "r")
    d = json.load(f)
    f.close()
    
    d["partitions"] = sorted(d["partitions"], key = lambda x: (x["topic"], x["partition"]))
    
    f = open("./resort-reassignment-configuration.json", "w")
    json.dump(d, f)
    f.close()


def regenerate_reassignment_configuration():
    f = open("./resort-reassignment-configuration.json", "r")
    d = json.load(f)
    f.close()
    
    replicas = [1001, 1002, 1003, 1004, 1005]
    for idx, _ in enumerate(d["partitions"]):
        tmp = copy.copy(replicas)
        d["partitions"][idx]["replicas"] = tmp
        d["partitions"][idx]["log_dirs"].append("any")
        d["partitions"][idx]["log_dirs"].append("any")
        next_permutation(replicas)
    
    f = open("./regenerate-reassignment-configuration.json", "w")
    json.dump(d, f)
    f.close()


if __name__ == "__main__":
    resort_reassignment_configuration()
    regenerate_reassignment_configuration()
