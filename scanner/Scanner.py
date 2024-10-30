class Scanner:
    def __init__(self, api: str, db_path: str, api_key: str = None):
        self.api = api
        self.db_path = db_path
        self.api_key = api_key
