from dagster import repository

from src.jobs import non_dynamic_job


@repository
def dagster_prio_dynamic_map():
    return {"jobs": {"non_dynamic_job": non_dynamic_job}}
