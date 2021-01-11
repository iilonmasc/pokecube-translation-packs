import os

import config


class APIObject():
    def __init__(self, object_type, fallback_name, resource_id, target_language):
        self.fallback_name = fallback_name
        self.target_language = target_language
        self.object_type = object_type
        self.resource_id = resource_id
        self.id = self.get_id()
        if not self.id:
            self.translation = self.fallback_name
        else:
            self.translation = self.get_translation()

    def get_translation(self):
        translation_file = f'{config.cache_directory}/{self.object_type}/{self.target_language}/{self.object_type[:-1]}_{self.id}.translation'
        if os.path.exists(translation_file):
            with open(translation_file, 'r') as translation_reader:
                translation = ''.join(translation_reader.readlines()).strip()
                return translation if len(translation) >= 1 else None
        return None

    def get_id(self):
        with open(f'{config.cache_directory}/{self.object_type[:-1]}_id.mapping', 'r') as mapping:
            sanitized_name = self.fallback_name.replace(
                ' ', '-').replace('\'', '').replace('’', '').lower()
            for line in mapping.readlines():
                object_name = line.split('|')[0].lower()
                object_id = line.split('|')[1].lower().strip()
                # print(object_name,sanitized_name)
                if object_name == self.fallback_name.lower():
                    return object_id
                if (self.object_type == 'moves' and (object_name == self.fallback_name.lower() or object_name == sanitized_name or object_name == sanitized_name + '--physical')):
                    return object_id
            return None

    def get_string_presentation(self):
        return f'"{self.resource_id}": "{self.translation if self.translation != None else self.fallback_name}",'
