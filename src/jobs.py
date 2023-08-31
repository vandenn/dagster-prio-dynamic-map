from dagster import job

from src import ops


@job
def non_dynamic_job():
    pokemon_list = ops.get_all_data()
    pokemon_list = ops.expensive_transformation_1(pokemon_list)
    ops.pseudo_load_to_db(pokemon_list)
