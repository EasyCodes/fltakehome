# README
This project is for an interview with Flow Labs. All rights reserved to me, and/or them.


# Documentation


# Progress tracker

| id  | Deliverable Name                |             |
| --- | ------------------------------- | ----------- |
| 1   | C++ HMM-MMM                     |             |
| 2   | Python Wrapper for #1           | in progress |
| 3   | Python script to use #2         | in progress |
| 4   | Pulsar and Postgres integration | in progress |
| 5   | Docker                          | in progress |
| 6   | K8s                             |             |
| 7   | Airflow DAG                     |             |
| 8   | Documentation                   | in progress |


# Python Setup
- pip install 'apache-airflow[cncf.kubernetes]'

# Setup
- install Docker Desktoo
- Open Settings in Docker Desktop
    - open the Kubernetes tab, click the toggle for 'Enable Kubernetes'
    - Click 'Apply & Restart'

#TODO replace this with the 'correct thing to do' to configure, hopefully
- Copy Kube settings:
    - run: `kubectl config use-context docker-desktop
    - then: `kubectl config view --minify --raw > <path_to_project>/FlowLabs/airflow/kube/config`

# Run the App
- from the root directory run: `docker compose build & docker compose up -d`
- to run Airflow, from the same directory: `docker compose build -f airflow/compose.yaml & docker compose up -d -f airflow/compose.yaml`
- monitor terminal for results
