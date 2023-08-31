from dagster import job

from src import ops_no_prio, ops_with_prio


@job
def non_dynamic_job():
    pokemon_list = ops_no_prio.get_all_data()
    pokemon_list = ops_no_prio.expensive_transformation_1(pokemon_list)
    pokemon_list = ops_no_prio.expensive_transformation_2(pokemon_list)
    ops_no_prio.pseudo_load_to_db(pokemon_list)


@job(config={"execution": {"config": {"multiprocess": {"max_concurrent": 4}}}})
def dynamic_job():
    def _for_each(pokemon_batch):
        pokemon_batch = ops_no_prio.expensive_transformation_1(pokemon_batch)
        pokemon_batch = ops_no_prio.expensive_transformation_2(pokemon_batch)
        ops_no_prio.pseudo_load_to_db(pokemon_batch)

    pokemon_list = ops_no_prio.dynamic_get_all_data()
    pokemon_list.map(_for_each)


@job(config={"execution": {"config": {"multiprocess": {"max_concurrent": 4}}}})
def prio_dynamic_job():
    def _for_each(pokemon_batch):
        pokemon_batch = ops_with_prio.expensive_transformation_1_prio(pokemon_batch)
        pokemon_batch = ops_with_prio.expensive_transformation_2_prio(pokemon_batch)
        ops_with_prio.pseudo_load_to_db_prio(pokemon_batch)

    pokemon_list = ops_with_prio.dynamic_get_all_data_prio()
    pokemon_list.map(_for_each)
