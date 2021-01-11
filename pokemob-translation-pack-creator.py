
import datetime
import os
import sys

import config
from lib.scraper import PokeAPIScraper
from lib.resourcepack import ResourcePack


pokecube_version = '3.7.0'  # TODO: this will be taken from the jar later on
date = datetime.datetime.now().strftime('%Y-%m-%d')

if len(sys.argv) > 1:
    arguments = sys.argv[1:]
    for argument in arguments:
        if '--debug' in argument:
            config.debug = True
        if '--version' in argument:
            pokecube_version = argument.split('=')[1]

scraper = PokeAPIScraper(
    config.api, cache_dir=config.cache_directory, limit=config.limit, debug=config.debug)

scraper.setup()
if config.debug:
    print('Scraper setup, done')


# TODO: replace with JAR extractor
if os.path.exists('base_mobs.json') and os.path.exists('base_moves.json'):
    for language in config.languages:
        resource_pack = ResourcePack(language, pokecube_version, date, config.debug)
        resource_pack.build_pack()
