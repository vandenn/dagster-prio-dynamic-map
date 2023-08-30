from dagster import op


@op
def get_all_data(context):
    data = []
    context.log.info("Data retrieved.")
    return data
