from dagster import DynamicOut, DynamicOutput, op

from src import logic


@op(out=DynamicOut(), tags={"dagster/priority": 0})
def prio_dynamic_extract(context):
    for batch, offset in logic.dynamic_get_all_data(context):
        yield DynamicOutput(batch, mapping_key=f"{offset}")


@op(tags={"dagster/priority": 1})
def prio_transform_1(context, pokemon_list):
    return logic.expensive_transformation_1(pokemon_list)


@op(tags={"dagster/priority": 2})
def prio_transform_2(context, pokemon_list):
    return logic.expensive_transformation_2(pokemon_list)


@op(tags={"dagster/priority": 3})
def prio_load(context, pokemon_list):
    logic.pseudo_load_to_db(context, pokemon_list)
