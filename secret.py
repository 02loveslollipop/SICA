import yaml

class Secret:
    def __init__(self,path: str = None) -> None:
        if path is None:
            path = 'secret'
        with open(path) as file:
            config = yaml.load(file, Loader=yaml.FullLoader)
            self.uri = config['MongoDB']['uri']
            self.dbName = config['MongoDB']['dbName']
            self.providerCollection = config['MongoDB']['providerCollection']
            self.token_ttl = config['API']['token_ttl']
            self.secret = config['API']['secret']