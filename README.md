# elasticsearch-metrics

https://grafana.net/dashboards/878

Run either as a standalone script or docker container.

To build the container:

```bash
git clone https://github.com/trevorndodds/elasticsearch-metrics.git es-monitor
cd es-monitor
docker build -t <user>/es-monitor:latest .
```

To run it:

```bash
docker run -d -e ES_METRICS_CLUSTER_URL=http://search1.example.net:9200 \
-e ES_METRICS_INDEX_NAME=elasticsearch_metrics-search1 \
-e ES_METRICS_MONITORING_CLUSTER_URL=http://es-monitor.example.net:9200 \
<user>/es-monitor:latest
```
