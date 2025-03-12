import datetime
import yaml


from airflow.decorators import dag, task
from airflow.providers.cncf.kubernetes.operators.job import KubernetesJobOperator


@task
def load_k8s_config():
    k8s_job_body = None
    with open("../k8s_job.yaml", "r") as file:
        k8s_job_body = yaml.safe_load(file)

    return k8s_job_body

@dag(
    start_date=datetime.datetime(2025, 3, 10),
    catchup=False,
    schedule_interval='0 12 * * *'
)
def run_kube_job():
    # https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/operators.html#id3
    KubernetesJobOperator(
        task_id='run_kube_job',
        namespace='default',
        config_file='/opt/airflow/kube/config',
        job_template_file='/opt/airflow/kube/k8s_job.yaml'
    )

run_kube_job()
