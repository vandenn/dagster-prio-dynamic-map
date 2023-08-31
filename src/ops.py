import csv
import time

from dagster import op


@op
def get_all_data(context):
    with open("./data/pokemon.csv", "r") as data_file:
        data_reader = csv.DictReader(data_file)
        pokemon = list(data_reader)
        context.log.info(f"{len(pokemon)} records retrieved.")
    return pokemon


@op
def expensive_transformation_1(context, pokemon_list):
    time.sleep(1)
    return [
        {
            "name": pokemon["name"],
            "generation": pokemon["generation"],
            "type1": pokemon["type1"],
            "type2": pokemon["type2"],
        }
        for pokemon in pokemon_list
    ]


@op
def pseudo_load_to_db(context, pokemon_list):
    for pokemon in pokemon_list:
        context.log.info(f"Pushing {pokemon['name']} to DB..")
