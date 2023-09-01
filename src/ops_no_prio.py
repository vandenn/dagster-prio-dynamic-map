from dagster import DynamicOut, DynamicOutput, op

from src import logic


@op
def static_extract(context):
    return logic.get_all_data(context)


@op(out=DynamicOut())
def non_prio_dynamic_extract(context):
    for batch, offset in logic.dynamic_get_all_data(context):
        yield DynamicOutput(batch, mapping_key=f"{offset}")


@op
def non_prio_transform_1(context, pokemon_list):
    return logic.expensive_transformation_1(pokemon_list)


@op
def non_prio_transform_2(context, pokemon_list):
    return logic.expensive_transformation_2(pokemon_list)


@op
def non_prio_load(context, pokemon_list):
    logic.pseudo_load_to_db(context, pokemon_list)
