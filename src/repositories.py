from dagster import repository

from src.jobs import dynamic_job, prio_dynamic_job, static_job


@repository
def dagster_prio_dynamic_map():
    return {
        "jobs": {
            "static_job": static_job,
            "dynamic_job": dynamic_job,
            "prio_dynamic_job": prio_dynamic_job,
        }
    }
