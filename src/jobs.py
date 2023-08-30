from dagster import job

from src import ops


@job
def non_dynamic_job():
    ops.get_all_data()
