import csv
import time
import uuid


def get_all_data(context):
    with open("./data/pokemon.csv", "r") as data_file:
        data_reader = csv.DictReader(data_file)
        pokemon = list(data_reader)
        context.log.info(f"{len(pokemon)} records retrieved.")
    return pokemon


def dynamic_get_all_data(context):
    with open("./data/pokemon.csv", "r") as data_file:
        data_reader = csv.DictReader(data_file)
        pokemon = list(data_reader)

        # Simulate batch retrieval of data from an API
        batch_size = 100
        total = len(pokemon)
        for offset in range(0, total, batch_size):
            context.log.info(
                f"{min(offset + batch_size, total)}/{total} records retrieved."
            )
            yield pokemon[offset : offset + batch_size], offset


def expensive_transformation_1(pokemon_list):
    time.sleep(1)  # Simulate long transformation time
    return [
        {
            "name": pokemon["name"],
            "generation": pokemon["generation"],
            "type1": pokemon["type1"],
            "type2": pokemon["type2"],
        }
        for pokemon in pokemon_list
    ]


def expensive_transformation_2(pokemon_list):
    time.sleep(1)  # Simulate long transformation time
    return [{"internal_id": uuid.uuid4(), **pokemon} for pokemon in pokemon_list]


def pseudo_load_to_db(context, pokemon_list):
    for pokemon in pokemon_list:
        context.log.info(
            f"Pushing {pokemon['name']} ({pokemon['internal_id']}) to DB.."
        )
