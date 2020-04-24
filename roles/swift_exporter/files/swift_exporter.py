#!/usr/bin/python3
import swiftclient
import yaml
import logging
import sys
from prometheus_client import start_http_server, Gauge
from collections import defaultdict, namedtuple
import time

#Define prometheus_metrics
gauge_container_count = Gauge('swift_container_count','Number of container in an account', ['account'])
gauge_object_count = Gauge('swift_object_count', 'Number of object in an account', ['account'])
gauge_used_bytes = Gauge('swift_used_bytes', 'Used bytes in an account', ['account'])
gauge_quota_bytes = Gauge('swift_quota_bytes', 'quota bytes in an account', ['account'])
gauge_container_connect = Gauge('swift_container_connect', 'Connection to container', ['account'])

## Read yaml config
def get_config(configfile):
    with open(configfile, 'r') as stream:
        try:
            config_obj = yaml.safe_load(stream)
            return config_obj
        except yaml.YAMLError as exc:
            logging.critical("Error reading yaml config file %s", exc)
            sys.exit(1)
        except OSError as exc:
            logging.critical(" yaml config file Not found %s", exc)
            sys.exit(1)

## Connect with swift object storage
def swift_connect(user,key,authurl):
    try:
        conn = swiftclient.Connection(
            user=user,
            key=key,
            authurl=authurl,
        )
        resp_headers, containers = conn.get_account()
    except Exception as exc:
        logging.critical(" Exception during connecting to object storage %s", exc)
        resp_headers=None
        containers= None
    return resp_headers,containers

## Get container size        
def get_account_stats(resp_headers,containers):
    container_count = resp_headers['x-account-container-count']
    object_count = resp_headers['x-account-object-count']
    used_bytes = resp_headers['x-account-bytes-used']
    quota_bytes = resp_headers['x-account-meta-quota-bytes']
    container_obj =  namedtuple('_',['container_count', 'object_count', 'used_bytes', 'quota_bytes'])(container_count, object_count, used_bytes, quota_bytes)
    return container_obj

## Prometheus_metrics conversion
def prometheus_metrics(container_obj,tag,can_connect):
    if can_connect == 1:
        gauge_container_count.labels(account=tag).set(10)
        gauge_object_count.labels(account=tag).set(container_obj.object_count)
        gauge_used_bytes.labels(account=tag).set(container_obj.used_bytes)
        gauge_quota_bytes.labels(account=tag).set(container_obj.quota_bytes)
        gauge_container_connect.labels(account=tag).set(can_connect)
    else:
        gauge_container_connect.labels(account=tag).set(can_connect)

# Main Funtion
if __name__ == "__main__": 
    configfile="/etc/swift_accounts.yaml"
    config_obj = get_config(configfile)
    start_http_server(config_obj['listen_port'])
    logging.info("Starting swift exporter on port : %s", config_obj['listen_port']) 

    while True:
        for obj in config_obj['swift_accounts']:
            resp_headers, containers = swift_connect(obj['user'], obj['key'], obj['authurl'])
            if resp_headers and containers:
                can_connect = 1
                container_obj = get_account_stats(resp_headers, containers)
                prometheus_metrics(container_obj,obj['tag'],can_connect)
        time.sleep(300)
