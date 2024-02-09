import os
from typing import List

from .event import MCFunction


class Save(object):
    def __init__(self,
                 path: str,
                 datapack: str,
                 namespace: str
                 ):
        if not os.path.exists(os.path.join(path, 'level.dat')):
            raise FileNotFoundError('level.dat not found')

        self.path = path
        self.datapack = datapack
        self.namespace = namespace
        self.event_count = 0

        self.function_list: List[MCFunction] = []

    def add_function(self,
                     function: MCFunction
                     ):
        self.function_list.append(function)

    def output(self):
        for mcfunction in self.function_list:
            with open(file=f'{self.path}/datapacks/{self.datapack}/data/{self.namespace}/functions/{mcfunction.name}.mcfunction',
                      mode='w',
                      encoding='utf-8') as f:
                f.write('\n'.join(mcfunction.commands))

    def __del__(self):
        self.output()
        print('-------------------\n',
              f'{self.event_count} Events\n',
              '-------------------\n')
