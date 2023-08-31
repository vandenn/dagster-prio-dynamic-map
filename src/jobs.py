from dagster import job

from src import ops


@job
def non_dynamic_job():
    pokemon_list = ops.get_all_data()
    pokemon_list = ops.expensive_transformation_1(pokemon_list)
    pokemon_list = ops.expensive_transformation_2(pokemon_list)
    ops.pseudo_load_to_db(pokemon_list)


@job(config={"execution": {"config": {"multiprocess": {"max_concurrent": 4}}}})
def dynamic_job():
    def _for_each(pokemon_batch):
        pokemon_batch = ops.expensive_transformation_1(pokemon_batch)
        pokemon_batch = ops.expensive_transformation_2(pokemon_batch)
        ops.pseudo_load_to_db(pokemon_batch)

    pokemon_list = ops.dynamic_get_all_data()
    pokemon_list.map(_for_each)
