# pokecube-translation-packs

Are you using any of the pokecube mods for minecraft?

Are you used to the german/french/italian/spanish monster names but playing minecraft in english because you are used to the item/block names?

Well then this pack/repository is for you!

This pack is a translation resource pack for the pokecube mod to translate (most) mobs and moves to your language while still playing minecraft in english.

## Which pack to choose?

Packs are built for specific versions of pokecube, you can find your pack by taking a look at the name of the zip file.

E.g. a german pack built for pokecube 3.7.0 would look like this `pokecube-translation-de-3.7.0.zip`

[Take a look at the releases page to find a pack for you!](https://github.com/iilonmasc/pokecube-translation-packs/releases)

## Development

The scripts in this repository are used to generate the zip files found under releases. Aside from the `requests` library the project is pure python3 so all you need after cloning this repository to set yourself up:

1. `pip install requests` to be able to use the `requests` library
2. Copy `config.py.temp` to `config.py` and take a look at it to configure your scripts.
3. Drop the pokecube.jar in the directory so the scripts can extract necessary information from the mod
4. Run `python3 pokemob-translation-pack-creator.py --jar=your-pokecube-file.jar` to start generating your own resource packs!

_Note:_ running the pack-creator for the first time might take a while since it scrapes the configure pokeapi instance for all the data needed to translate mobs/moves/items

#### DO NOT configure the official pokeapi instance as your API!
Please set up a self-hosted pokeapi instance for the data-scraper! [Take a look at the github page for pokeapi how to setup your own instance.](https://github.com/PokeAPI/pokeapi#setup-)

These scripts generate many requests and you wouldn't want to bombard the official pokeapi servers, would you?
