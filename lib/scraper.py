import requests
import os
import time
import re

from alternative_item_names import alternative_item_names
from alternative_mob_names import alternative_mob_names
from alternative_move_names import alternative_move_names


class PokeAPIScraper():
    def __init__(self, api, cache_dir='translation_cache', limit=20, debug=False):
        self.api = api
        self.cache_directory = cache_dir
        self.api_limit = limit
        self.debug = debug
        self.api_mapping = {
            'mob': 'pokemon-species',
            'item': 'item',
            'move': 'move',
        }

    def setup(self):
        self.prepare_translation_cache()

        for object_type in ['mob', 'item', 'move']:
            self.create_mapping(object_type)
            self.fetch_objects(object_type)

    def prepare_translation_cache(self):
        available_languages = ['ja-Hrkt', 'roomaji', 'ko', 'zh-Hant',
                               'fr', 'de', 'en', 'es', 'it', 'cs', 'ja', 'zh-Hans', 'pt-BR']
        paths = ['mobs', 'moves', 'items']
        if not os.path.exists(self.cache_directory):
            os.mkdir(self.cache_directory)
        for path in paths:
            if not os.path.exists(f'{self.cache_directory}/{path}'):
                os.mkdir(f'{self.cache_directory}/{path}')
            for language in available_languages:
                if not os.path.exists(f'{self.cache_directory}/{path}/{language}'):
                    os.mkdir(f'{self.cache_directory}/{path}/{language}')

    def create_mapping(self, object_type):
        alternatives = {
            'mob': alternative_mob_names,
            'item': alternative_item_names,
            'move': alternative_move_names
        }
        raw_mapping_file = f'{self.cache_directory}/{object_type}_id.mapping.raw'
        finalized_mapping_file = f'{self.cache_directory}/{object_type}_id.mapping'
        if not os.path.exists(raw_mapping_file):
            offset = 0
            next_url = f'{self.api}/api/v2/{self.api_mapping.get(object_type)}?offset={offset}&limit={self.api_limit}'
            fetching = True
            if self.debug:
                print(
                    f'Fetching {object_type} lists from {self.api} with page limit {self.api_limit}. THIS MIGHT TAKE A WHILE!')
            if os.path.exists(raw_mapping_file):
                os.remove(raw_mapping_file)
            while fetching:
                response = requests.get(next_url)
                if not response.status_code == 200:
                    if self.debug:
                        print(
                            f'Unable to fetch Pokemon list {offset} to {offset+self.api_limit}')
                else:
                    for result in response.json().get('results'):
                        object_name = result.get('name')
                        object_id = result.get('url').split('/')[-2]
                        with open(raw_mapping_file, 'a') as mapping_file:
                            mapping_file.write(f'{object_name}|{object_id}\n')
                    next_url = response.json().get('next')
                    if not next_url:
                        fetching = False
                    else:
                        time.sleep(3)
        else:
            if self.debug:
                print(
                    f'Unfinalized mapping file {raw_mapping_file} exists, skipping fetch step')

        if not os.path.exists(finalized_mapping_file):
            final_lines = []
            with open(raw_mapping_file, 'r') as raw_mapping:
                lines = raw_mapping.readlines()
                for line in lines:
                    if line.split('|')[0].lower() in alternatives.get(object_type):
                        final_lines.append(alternatives.get(object_type).get(
                            line.split('|')[0]) + '|' + line.split('|')[1])
                    else:
                        final_lines.append(line)
                with open(finalized_mapping_file, 'w') as mapping:
                    mapping.writelines(final_lines)
        else:
            if self.debug:
                print(
                    f'Finalized mapping file {finalized_mapping_file} exists, skipping finalize step')

    def fetch_objects(self, object_type):
        with open(f'{self.cache_directory}/{object_type}_id.mapping', 'r') as object_id_map:
            for line in object_id_map.readlines():
                if len(line.strip()) > 1:
                    object_id = line.split('|')[1].strip()
                    # ignore-pattern for custom translations like 898b or 890a
                    pattern = re.compile("[A-Za-z]")
                    # checking cache for 'en' as it's the most completed translation
                    if not pattern.fullmatch(object_id[-1]) and not os.path.exists(f'{self.cache_directory}/{object_type}s/en/{object_type}_{object_id}.translation'):
                        if self.debug:
                            print(f'Missing cache for {object_type} {object_id}, trying to fetch from {self.api}')
                        try:
                            response = requests.get(
                                f'{self.api}/api/v2/{self.api_mapping.get(object_type)}/{object_id}')
                            if not response.status_code == 200:
                                if self.debug:
                                    print(
                                        f'Unable to fetch {object_type} {object_id}.')
                            else:
                                result = response.json()
                                result = result.get('names')
                                for translation in result:
                                    shortcode = translation.get(
                                        'language').get('name')
                                    with open(f'{self.cache_directory}/{object_type}s/{shortcode}/{object_type}_{object_id}.translation', 'w') as translation_file:
                                        translation_file.write(
                                            translation.get('name'))
                                        translation_file.write('\n')
                        except requests.exceptions.ConnectionError:
                            print(f'Unable to connect to {self.api}, skipping {object_id}')
