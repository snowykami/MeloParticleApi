import os
from typing import List

from PIL import Image

from .event import MCFunction


class Save(object):
    def __init__(self,
                 path: str,
                 datapack: str,
                 resourcepack: str,
                 namespace: str,
                 ):
        if not os.path.exists(os.path.join(path, 'level.dat')):
            raise FileNotFoundError('level.dat not found')

        self.path = path
        self.datapack = datapack
        self.resourcepack = resourcepack
        self.namespace = namespace
        self.event_count = 0

        self.function_list: List[MCFunction] = []

    def add_function(self,
                     function: MCFunction
                     ) -> MCFunction:
        function.namespace = self.namespace
        self.function_list.append(function)
        return function

    @property
    def game_root(self) -> str:
        return os.path.abspath(os.path.join(self.path, '../..'))

    @property
    def game_resourcepack(self):
        return os.path.join(self.game_root, 'resourcepacks', self.resourcepack)

    def output(self):
        for mcfunction in self.function_list:
            func_path = f'{self.path}/datapacks/{self.datapack}/data/{self.namespace}/functions'
            function_path = f'{self.path}/datapacks/{self.datapack}/data/{self.namespace}/functions/{mcfunction.name}.mcfunction'
            if not os.path.exists(os.path.dirname(function_path)):
                os.makedirs(os.path.dirname(function_path), exist_ok=True)
            with open(file=f'{self.path}/datapacks/{self.datapack}/data/{self.namespace}/functions/{mcfunction.name}.mcfunction',
                      mode='w',
                      encoding='utf-8') as f:
                f.write('\n'.join(mcfunction.commands))
        print('Output complete')

    def __del__(self):
        self.output()


class ResourcePack(object):
    def __init__(self,
                 path: str,
                 namespace: str,
                 ):
        self.path = path
        self.namespace = namespace

    def add_texture_block(
            self,
            image: str | Image.Image,
            path: str,
            emissive: bool = False
    ):
        """
        Add a block texture to the resource pack.
        :param emissive:
        :param image:
        :param path: without .png
        :return:
        """
        file_path = os.path.join(self.path, 'assets', self.namespace, 'textures/block', path + '.png')
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

        if isinstance(image, str):
            image = Image.open(image)
        image.save(file_path)

        if emissive:
            emissive_properties = os.path.join(self.path, 'assets', self.namespace, 'optifine/emissive.properties')
            if not os.path.exists(emissive_properties):
                os.makedirs(os.path.dirname(emissive_properties), exist_ok=True)
                with open(emissive_properties, 'a') as f:
                    f.write('suffix.emissive=_e\n')
            image.save(file_path.replace('.png', '_e.png'))
