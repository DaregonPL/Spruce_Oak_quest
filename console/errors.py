class InvalidMapFormatError(Exception):
    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return 'The Map is invalid'

class NonExistingSceneCalledError(Exception):
    def __init__(self, scenename, Map):
        self.scenename = scenename
        self.map = Map

    def __str__(self):
        return f'There is no {self.scenename} in map {self.Map}'
