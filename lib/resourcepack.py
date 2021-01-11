import shutil
import os
import json
import config

from lib.apiobject import APIObject
from alternative_language_names import alternative_language_names

class ResourcePack():
    def __init__(self, language, pokecube_version, date, debug=False):
        self.language = language
        self.pokecube_version = pokecube_version
        self.date = date
        self.debug = debug
        self.name = f'pokecube-translation-{self.language}-{self.pokecube_version}-{self.date}'

        self.translations = {
            'mob': {
                'total': 0,
                'missing': 0
            },
            'item': {
                'total': 0,
                'missing': 0
            },
            'move': {
                'total': 0,
                'missing': 0
            }
        }

        self.create_resource_pack_structure()

    def create_resource_pack_structure(self):
        paths = [
            config.dist_directory,
            f'{self.name}',
            f'{self.name}/assets',
            f'{self.name}/assets/pokecube_mobs',
            f'{self.name}/assets/pokecube_mobs/lang',
            f'{self.name}/assets/pokecube_moves',
            f'{self.name}/assets/pokecube_moves/lang',
        ]
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

    def create_language_files(self):
        for object_type in ['mobs', 'moves']:
            if self.debug:
                print(f'Starting to write {object_type} translations')
            if object_type == 'mobs':
                asset_path = f'{self.name}/assets/pokecube_mobs/lang/en_us.json'
            elif object_type == 'moves':
                asset_path = f'{self.name}/assets/pokecube_moves/lang/en_us.json'

            asset_file = open(asset_path, 'w')
            asset_file.write('{\n')

            if object_type == 'moves':
                if os.path.exists(f'hardcoded_translations/{self.language}_messages.json'):
                    base_message_file_path = f'hardcoded_translations/{self.language}_messages.json'
                else:
                    if self.debug:
                        print(
                            f'Could not find "{self.language}" move base messages, falling back to english')
                    base_message_file_path = f'hardcoded_translations/en_messages.json'
                base_message_file = open(base_message_file_path, 'r')
                base_message_data = json.load(base_message_file)
                base_message_file.close()
                for key in base_message_data:
                    asset_file.write(
                        f'  "{key}": "{base_message_data[key]}",\n')

            base_file = open(f'base_{object_type}.json', 'r')
            base_file_data = json.load(base_file)
            base_file.close()
            for key in base_file_data:
                if key.lower() != '_comment':
                    api_object = APIObject(
                        object_type, base_file_data.get(key), key, self.language)
                    if not api_object.id:
                        self.translations[object_type[:-1]]['missing'] += 1
                        if self.debug:
                            print(
                                f'Could not find id for {api_object.fallback_name}, falling back to english name')
                    elif not api_object.translation:
                        self.translations[object_type[:-1]]['missing'] += 1
                        if self.debug:
                            print(
                                f'Could not find "{api_object.target_language}" translation for {api_object.fallback_name}, falling back to english name')
                        api_object.translation = api_object.fallback_name
                    asset_file.write(
                        '  ' + api_object.get_string_presentation() + '\n')
                    self.translations[object_type[:-1]]['total'] += 1
            asset_file.write('}\n')
            asset_file.close()
            self.finalize_language_file(asset_path)
            if self.debug:
                print(f'Done writing {object_type} translations')
            api_object = None

    def finalize_language_file(self, file_path):
        with open(file_path, 'r') as output_file:
            lines = output_file.readlines()
            final_line = lines[-2][:-2] + '\n'
        with open(file_path, 'w') as output_file:
            lines[-2] = final_line
            output_file.writelines(lines)
        self.copy_localisation(file_path)

    def copy_localisation(self, asset_path):
        asset_directory = '/'.join(asset_path.split('/')[:-1])
        for language in alternative_language_names:
            asset_file=f'{asset_directory}/{alternative_language_names.get(language)}.json'
            if asset_path != asset_file:
                shutil.copyfile(asset_path, asset_file)


    def create_resource_pack_archive(self):
        shutil.make_archive(f'dist/{self.name}', 'zip', self.name)
        if self.debug:
            print(f'Created archive: dist/{self.name}.zip')

    def write_pack_meta(self):
        with open(f'{self.name}/pack.mcmeta', 'w') as meta_file:
            meta_file.write('{\n')
            meta_file.write('  "pack": {\n')
            meta_file.write('    "pack_format": 6,\n')
            meta_file.write(
                f'    "description": "Pokecube Translation Pack - {self.language}"\n')
            meta_file.write('  },\n')
            meta_file.write('  "language": {}\n')
            meta_file.write('}\n')

    def perform_cleanup(self):
        shutil.rmtree(self.name)

    def print_summary(self):
        print(f"""
{'-'*10} Build Summary {self.name} {'-'*10}

        Missing mobs  : {self.translations.get('mob')['missing']}/{self.translations.get('mob')['total']}
        Missing items : {self.translations.get('item')['missing']}/{self.translations.get('item')['total']}
        Missing moves : {self.translations.get('move')['missing']}/{self.translations.get('move')['total']}

Total translations missing: {sum([self.translations.get(key)['missing'] for key in ['mob', 'item', 'move']])}/{sum([self.translations.get(key)['total'] for key in ['mob', 'item', 'move']])}
""")

    def build_pack(self):
        self.create_language_files()
        self.write_pack_meta()
        self.create_resource_pack_archive()
        self.perform_cleanup()
        self.print_summary()
