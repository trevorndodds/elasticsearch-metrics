#!/usr/bin/env python
import datetime
import urllib, json
import requests

def fetch_clusterhealth():
    utc_datetime = datetime.datetime.utcnow()
    urlData = "http://192.168.1.54:9200/_cluster/health"
    response = urllib.urlopen(urlData)
    jsonData = json.loads(response.read())
    clusterName = jsonData['cluster_name']
    jsonData['@timestamp'] = str(utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
    post_data(jsonData)
    return clusterName


def fetch_clusterstats():
    utc_datetime = datetime.datetime.utcnow()
    urlData = "http://192.168.1.54:9200/_cluster/stats"
    response = urllib.urlopen(urlData)
    jsonData = json.loads(response.read())
    jsonData['@timestamp'] = str(utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
    post_data(jsonData)


def fetch_nodestats(clusterName):
    utc_datetime = datetime.datetime.utcnow()
    urlData = "http://192.168.1.54:9200/_cat/nodes?v&h=n"
    response = urllib.urlopen(urlData)
    nodes = response.read()[ 1:-1].strip().split('\n')
    for node  in nodes:
        urlData = "http://192.168.1.54:9200/_nodes/%s/stats" % node.rstrip()
        response = urllib.urlopen(urlData)
        jsonData = json.loads(response.read())
        nodeID = jsonData['nodes'].keys()
        jsonData['nodes']['%s' %nodeID[0]]['@timestamp'] = str(utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
        jsonData['nodes']['%s' % nodeID[0]]['cluster_name'] = clusterName
        newJsonData = jsonData['nodes']['%s' %nodeID[0]]
        post_data(newJsonData)
    #   print json.dumps(newJsonData, indent = 5)


def fetch_indexstats(clusterName):
    utc_datetime = datetime.datetime.utcnow()
    urlData = "http://192.168.1.54:9200/_stats"
    response = urllib.urlopen(urlData)
    jsonData = json.loads(response.read())
    jsonData['_all']['@timestamp'] = str(utc_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3])
    jsonData['_all']['cluster_name'] = clusterName
    post_data(jsonData['_all'])


def post_data(data):
    utc_datetime = datetime.datetime.utcnow()
    utc_datetime.strftime("%Y-%m-%d")
    url = 'http://192.168.1.54:9200/trev/message'
    headers = {'content-type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print  response.elapsed
    except Exception as e:
        print "Error:  {}".format(str(e))


def main():
    clusterName = fetch_clusterhealth()
    fetch_clusterstats()
    fetch_nodestats(clusterName)
    fetch_indexstats(clusterName)

if __name__ == '__main__':
   #main(sys.argv[1])
    main()


   # scratch
   #    output =  response.json()
   # print output['_id']
   #
