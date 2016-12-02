#!/usr/bin/env python
import datetime
import time
import urllib
import json
import urllib2
import os
import sys

# ElasticSearch Cluster to Monitor
elasticServer = "server1"
interval = 60

# ElasticSearch Cluster to Send Metrics
elasticIndex = "elasticsearch_metrics"
elasticMonitoringCluster = "server2"


def fetch_clusterhealth():
    utc_datetime = datetime.datetime.utcnow()
    endpoint = "/_cluster/health"
    urlData = elasticServer + endpoint
    response = urllib.urlopen(urlData)
    jsonData = json.loads(response.read())
    clusterName = jsonData['cluster_name']
    jsonData['@timestamp'] = str(utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
    post_data(jsonData)
    return clusterName


def fetch_clusterstats():
    utc_datetime = datetime.datetime.utcnow()
    endpoint = "/_cluster/stats"
    urlData = elasticServer + endpoint
    response = urllib.urlopen(urlData)
    jsonData = json.loads(response.read())
    jsonData['@timestamp'] = str(utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
    post_data(jsonData)


def fetch_nodestats(clusterName):
    utc_datetime = datetime.datetime.utcnow()
    endpoint = "/_cat/nodes?v&h=n"
    urlData = elasticServer + endpoint
    response = urllib.urlopen(urlData)
    nodes = response.read()[1:-1].strip().split('\n')
    for node in nodes:
        endpoint = "/_nodes/%s/stats" % node.rstrip()
        urlData = elasticServer + endpoint
        response = urllib.urlopen(urlData)
        jsonData = json.loads(response.read())
        nodeID = jsonData['nodes'].keys()
        jsonData['nodes'][nodeID[0]]['@timestamp'] = str(utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
        jsonData['nodes'][nodeID[0]]['cluster_name'] = clusterName
        newJsonData = jsonData['nodes'][nodeID[0]]
        post_data(newJsonData)


def fetch_indexstats(clusterName):
    utc_datetime = datetime.datetime.utcnow()
    endpoint = "/_stats"
    urlData = elasticServer + endpoint
    response = urllib.urlopen(urlData)
    jsonData = json.loads(response.read())
    jsonData['_all']['@timestamp'] = str(utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
    jsonData['_all']['cluster_name'] = clusterName
    post_data(jsonData['_all'])


def post_data(data):
    utc_datetime = datetime.datetime.utcnow()
    url_parameters = {
        'cluster': elasticMonitoringCluster,
        'index': elasticIndex,
        'index_period': utc_datetime.strftime("%Y.%m.%d"),
    }
    url = "%(cluster)s/%(index)s_%(index_period)s/message" % url_parameters
    headers = {'content-type': 'application/json'}
    try:
        req = urllib2.Request(url, headers=headers, data=json.dumps(data))
        f = urllib2.urlopen(req)
    except Exception as e:
        print "Error:  {}".format(str(e))


def main():
    clusterName = fetch_clusterhealth()
    fetch_clusterstats()
    fetch_nodestats(clusterName)
    fetch_indexstats(clusterName)

if __name__ == '__main__':
    try:
        nextRun = 0
        while True:
                if time.time() >= nextRun:
                        nextRun = time.time() + interval
                        now = time.time()
                        main()
                        elapsed = time.time() - now
                        print "Total Elapsed Time: %s" % elapsed
                        timeDiff = nextRun - time.time()
                        time.sleep(timeDiff)
    except KeyboardInterrupt:
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
