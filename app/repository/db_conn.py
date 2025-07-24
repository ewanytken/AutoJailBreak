from pathlib import Path
from typing import Optional

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseConnection:
    def __init__(self, database_name: Optional[str] = "postgresql"):

        database_path = Path(__file__).parent.parent.parent / 'config.yaml'
        with open(database_path, 'r') as file:
            database_parameters = yaml.safe_load(file)

        self.user = database_parameters['database_parameters']['user']
        self.password = database_parameters['database_parameters']['password']
        self.host = database_parameters['database_parameters']['host']
        self.port = database_parameters['database_parameters']['port']
        self.database = database_parameters['database_parameters']['database']

        SQLALCHEMY_DATABASE_URL = f"{database_name}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        self.engine = create_engine(SQLALCHEMY_DATABASE_URL)
        self.session = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)

    def get_session(self):
        try:
            yield self.session()
        finally:
            self.session().close()