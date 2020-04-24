#!/usr/bin/python3
import swiftclient
import yaml
import logging
import sys
from prometheus_client import start_http_server, Gauge
from collections import defaultdict
import time

#Define prometheus_metrics
gauge_container_count = Gauge('swift_container_count','Number of container in an account', ['account_tags'])
gauge_object_count = Gauge('swift_object_count', 'Number of object in an account', ['account_tags'])
gauge_used_bytes = Gauge('swift_used_bytes', 'Used bytes in an account', ['account_tags'])
gauge_quota_bytes = Gauge('swift_quota_bytes', 'quota bytes in an account', ['account_tags'])
gauge_container_connect = Gauge('swift_container_connect', 'Connection to container', ['account_tags'])

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
def calculate_container_size(resp_headers,containers):
        container_count = resp_headers['x-account-container-count']
        object_count = resp_headers['x-account-object-count']
        used_bytes = resp_headers['x-account-bytes-used']
        quota_bytes = resp_headers['x-account-meta-quota-bytes']
        return container_count, object_count, used_bytes, quota_bytes    

## Prometheus_metrics conversion
def prometheus_metrics(container_obj):
    for tag, account in container_obj:
        if account['can_connect'] == 1:
            gauge_container_count.labels(account_tags=tag).set(account['container_count'])
            gauge_object_count.labels(account_tags=tag).set(account['object_count'])
            gauge_used_bytes.labels(account_tags=tag).set(account['used_bytes'])
            gauge_quota_bytes.labels(account_tags=tag).set(account['quota_bytes'])
            gauge_container_connect.labels(account_tags=tag).set(account['can_connect'])
        else:
            gauge_container_connect.labels(account_tags=tag).set(account['can_connect'])

# Main Funtion
if __name__ == "__main__": 
    configfile="/etc/swift_accounts.yaml"
    config_obj = get_config(configfile)
    start_http_server(config_obj['listen_port'])
    logging.info("Starting swift exporter on port : %s", config_obj['listen_port']) 

    while True:
        container_dict = defaultdict(list)
        for obj in config_obj['swift_accounts']:
            jsonobj = defaultdict(list)
            resp_headers, containers = swift_connect(obj['user'], obj['key'], obj['authurl'])
            if resp_headers and containers:
                container_count, object_count, used_bytes, quota_bytes = calculate_container_size(resp_headers, containers)
                jsonobj['object_count'] = object_count
                jsonobj['container_count'] = container_count
                jsonobj['used_bytes'] =  used_bytes
                jsonobj['quota_bytes'] = quota_bytes
                jsonobj['can_connect'] = 1
                container_dict[obj['tag']] =jsonobj
            else: 
                jsonobj['can_connect'] = 0
                container_dict[obj['tag']] =jsonobj
        prometheus_metrics(container_dict)
        time.sleep(20)
