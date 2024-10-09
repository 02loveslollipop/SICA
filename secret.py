import yaml

class Secret:
    def __init__(self,path: str = None) -> None:
        if path is None:
            path = 'secret'
        with open(path) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            self.uri = config['uri']