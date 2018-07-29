# coding: utf8

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Config:

    db = dict(
        dev=dict(
            host="127.0.0.1",
            username="root",
            passwd="root",
            db="funds",
        )
    )

    @classmethod
    def get_db(cls, env):
        return cls.db[env]
