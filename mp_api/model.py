import os


class World(object):
    def __init__(self, path: str, datapack: str, namespace: str):
        self.path = path
        self.datapack = datapack
        self.namespace = namespace
        # test for datapack
        if not os.path.exists(os.path.join(path, 'datapacks', datapack)):
            os.makedirs(os.path.join(path, 'datapacks', datapack))
            pack_mcmeta = open(os.path.join(), 'w', encoding='utf-8')
