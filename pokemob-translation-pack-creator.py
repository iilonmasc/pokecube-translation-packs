
import datetime
import os
import sys

import config
from lib.scraper import PokeAPIScraper
from lib.resourcepack import ResourcePack
from lib.extractor import BaseFileExtractor


date = datetime.datetime.now().strftime('%Y-%m-%d')
pokecube_jar = None

if len(sys.argv) > 1:
    arguments = sys.argv[1:]
    for argument in arguments:
        if '--debug' in argument:
            config.debug = True
        if '--jar' in argument:
            pokecube_jar = argument.split('=')[1]

scraper = PokeAPIScraper(
    config.api, cache_dir=config.cache_directory, limit=config.limit, debug=config.debug)

scraper.setup()
if config.debug:
    print('Scraper setup, done\n')


if pokecube_jar:
    if os.path.exists(pokecube_jar):
        extractor = BaseFileExtractor(pokecube_jar, config.debug)
        pokecube_version = extractor.get_archive_version()
        if config.debug:
            print(f'Found pokecube version {pokecube_version}')
        extractor.extract_base_files()
        for language in config.languages:
            resource_pack = ResourcePack(language, pokecube_version, date, config.debug)
            resource_pack.build_pack()
        extractor.cleanup_base_files()
    else:
        print(f'Could not find {pokecube_jar}!')
else:
    print('No jar file specified, please try again and include --jar=your-pokecube.jar')


# pokecube_version = '3.7.0'  # TODO: this will be taken from the jar later on
# # TODO: replace with JAR extractor
# if os.path.exists('base_mobs.json') and os.path.exists('base_moves.json'):
#     for language in config.languages:
#         resource_pack = ResourcePack(language, pokecube_version, date, config.debug)
#         resource_pack.build_pack()
