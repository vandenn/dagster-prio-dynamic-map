from dagster import job

from src import ops_no_prio, ops_with_prio


@job
def non_dynamic_job():
    pokemon_list = ops_no_prio.non_dynamic_extract()
    pokemon_list = ops_no_prio.non_prio_transform_1(pokemon_list)
    pokemon_list = ops_no_prio.non_prio_transform_2(pokemon_list)
    ops_no_prio.non_prio_load(pokemon_list)


# max_concurrent is not really necessary here -- it's used to show the difference of prio vs. non-prio for beefier machines
@job(config={"execution": {"config": {"multiprocess": {"max_concurrent": 4}}}})
def dynamic_job():
    def _for_each(pokemon_batch):
        pokemon_batch = ops_no_prio.non_prio_transform_1(pokemon_batch)
        pokemon_batch = ops_no_prio.non_prio_transform_2(pokemon_batch)
        ops_no_prio.non_prio_load(pokemon_batch)

    pokemon_list = ops_no_prio.non_prio_dynamic_extract()
    pokemon_list.map(_for_each)


# max_concurrent is not really necessary here -- it's used to show the difference of prio vs. non-prio for beefier machines
@job(config={"execution": {"config": {"multiprocess": {"max_concurrent": 4}}}})
def prio_dynamic_job():
    def _for_each(pokemon_batch):
        pokemon_batch = ops_with_prio.prio_transform_1(pokemon_batch)
        pokemon_batch = ops_with_prio.prio_transform_2(pokemon_batch)
        ops_with_prio.prio_load(pokemon_batch)

    pokemon_list = ops_with_prio.prio_dynamic_extract()
    pokemon_list.map(_for_each)
