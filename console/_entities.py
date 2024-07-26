import json

from typing import List

from _utils import data_file_path, get_json_from_file


def get_entity_file_name(entity) -> str:
    kind = entity['kind']
    provider = entity['metadata']['provider']
    namespace = entity['metadata']['namespace'] if 'namespace' in entity['metadata'] else 'default'
    name = entity['metadata']['name']

    ref = f'{kind}_{provider}_{namespace}_{name}'.lower()

    return f'{ref}.json'

def get_individual_entity_files() -> List[str]:
    '''Create a new file in the temp directory for each entity in entities.json.'''
    entities = get_json_from_file()

    file_paths = []

    # create a new file in temp for each entity
    for entity in entities:
        file_name = get_entity_file_name(entity)
        file_path = data_file_path(f'temp/{file_path}')

        with open(f'data/temp/{file_name}', 'w') as f:
            json.dump(entity, f)
            file_paths.append(f.name)

    return file_paths
