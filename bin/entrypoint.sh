#!/bin/bash

REPO_BASE=$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." && pwd )

/usr/local/bin/python ${REPO_BASE}/Grafana/elasticsearch2elastic.py
