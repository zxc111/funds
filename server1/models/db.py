# coding: utf8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Config, Base


class InitDB:
    def __init__(self, env):
        config = Config.get_db(env)
        from .funds import Fund, FundStatistics
        engine = create_engine(
            'mysql+pymysql://{username}:{passwd}@{host}/{db}?charset=utf8mb4'.format(**config),
            echo=False,
        )
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

