import zipfile
import os
import json

class BaseFileExtractor():
    def __init__(self, archive, debug=False):
        self.archive_path = archive
        self.archive = zipfile.ZipFile(self.archive_path)
        self.debug = debug
        self.asset_files = {
            'base_mobs.json': 'assets/pokecube_mobs/lang/en_us.json',
            'base_moves.json': 'assets/pokecube_moves/lang/en_us.json',
        }

    def extract_base_files(self):
        for asset_file in self.asset_files:
            self.extract_base_file(self.asset_files.get(asset_file), asset_file)

    def clear_base_move_file(self):
        ignore_fields=[
    "_comment",
    "pokemob.status.curse.user",
    "pokemob.status.flinch.user",
    "pokemob.status.confuse.add.user",
    "pokemob.status.confuse.remove.user",
    "pokemob.status.confusion.user",
    "pokemob.status.infatuate.user",
    "pokemob.move.stat.fail.user",
    "pokemob.status.curse.target",
    "pokemob.status.flinch.target",
    "pokemob.status.confuse.add.target",
    "pokemob.status.confuse.remove.target",
    "pokemob.status.confusion.target",
    "pokemob.status.infatuate.target",
    "pokemob.move.stat.fail.target",
    "pokemob.move.super.effective.user",
    "pokemob.move.not.very.effective.user",
    "pokemob.move.doesnt.affect.user",
    "pokemob.move.critical.hit.user",
    "pokemob.move.super.effective.target",
    "pokemob.move.not.very.effective.target",
    "pokemob.move.doesnt.affect.target",
    "pokemob.move.critical.hit.target",
    "pokemob.move.used.user",
    "pokemob.move.used.target",
    "pokemob.move.stat.fail.user",
    "pokemob.move.stat.rise1.user",
    "pokemob.move.stat.rise2.user",
    "pokemob.move.stat.rise3.user",
    "pokemob.move.stat.fall1.user",
    "pokemob.move.stat.fall2.user",
    "pokemob.move.stat.fall3.user",
    "pokemob.move.stat.fail.target",
    "pokemob.move.stat.rise1.target",
    "pokemob.move.stat.rise2.target",
    "pokemob.move.stat.rise3.target",
    "pokemob.move.stat.fall1.target",
    "pokemob.move.stat.fall2.target",
    "pokemob.move.stat.fall3.target",
    "pokemob.move.stat1",
    "pokemob.move.stat2",
    "pokemob.move.stat3",
    "pokemob.move.stat4",
    "pokemob.move.stat5",
    "pokemob.move.stat6",
    "pokemob.move.stat7",
    "pokemob.move.notify.learn",
    "pokemob.move.terraindamage",
    "pokemob.move.missed.user",
    "pokemob.move.missed.target",
    "pokemob.move.failed.user",
    "pokemob.move.failed.target",
    "pokemob.move.isfrozen.user",
    "pokemob.move.issleeping.user",
    "pokemob.move.isfullyparalyzed.user",
    "pokemob.move.paralyzed.user",
    "pokemob.move.isburned.user",
    "pokemob.move.ispoisoned.user",
    "pokemob.move.isbadlypoisoned.user",
    "pokemob.move.isfrozen.target",
    "pokemob.move.issleeping.target",
    "pokemob.move.isfullyparalyzed.target",
    "pokemob.move.paralyzed.target",
    "pokemob.move.isburned.target",
    "pokemob.move.ispoisoned.target",
    "pokemob.move.isbadlypoisoned.target",
    "pokemob.move.sketched",
    "pokemob.move.cooldown",
        ]
        with open('base_moves.json', 'r') as base_moves_file:
            base_moves_data = json.load(base_moves_file)
        for key in ignore_fields:
            if base_moves_data.get(key):
                base_moves_data.pop(key)
        base_moves_data['_comment'] = '#Move Names'
        with open('base_moves.json', 'w') as base_moves_file:
            json.dump(base_moves_data, base_moves_file)

    def cleanup_base_files(self):
        self.archive.close()
        if self.debug:
            print(f'Closed {self.archive_path} zipfile handler')
        for asset_file in self.asset_files:
            if os.path.exists(asset_file):
                if self.debug:
                    print(f'Removed {asset_file}')
                os.remove(asset_file)

    def extract_base_file(self, path, target):
        if self.debug:
            print('Extracting', path, 'to', target)
        with self.archive.open(path, 'r') as archive_file:
            with open(target, 'w') as target_file:
                for line in archive_file.readlines():
                    target_file.write(line.decode('utf-8'))
        if target == 'base_moves.json':
            self.clear_base_move_file()

    def get_archive_version(self):
        manifest = self.archive.open('META-INF/MANIFEST.MF', 'r') # Implementation-Version: X.X.X
        for line in manifest:
            if line.decode('utf-8').split(':')[0].lower() == 'implementation-version':
                return line.decode('utf-8').split(':')[1].lower().strip()
            if line.decode('utf-8').split(':')[0].lower() == 'specification-version':
                return line.decode('utf-8').split(':')[1].lower().strip()
        return '0.0.0'
