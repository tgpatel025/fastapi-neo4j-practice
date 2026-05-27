import os
from collections.abc import Iterator
from contextlib import contextmanager

from dotenv import load_dotenv
from neo4j import Driver
from neomodel import db, get_config


load_dotenv()
DEFAULT_DATABASE_URL = "bolt://neo4j:password@localhost:7687"
_shared_driver: Driver | None = None


def configure_database() -> None:
    config = get_config()
    config.database_url = os.getenv("NEOMODEL_DATABASE_URL", DEFAULT_DATABASE_URL)


def connect_database() -> None:
    global _shared_driver

    if _shared_driver is None:
        db.set_connection(url=get_config().database_url)
        _shared_driver = db.driver
    elif db.driver is None:
        db.set_connection(driver=_shared_driver)


def close_database() -> None:
    global _shared_driver

    if _shared_driver is not None and db.driver is not _shared_driver:
        _shared_driver.close()
    db.close_connection()
    _shared_driver = None


@contextmanager
def read_transaction() -> Iterator[None]:
    connect_database()
    with db.read_transaction:
        yield


@contextmanager
def write_transaction() -> Iterator[None]:
    connect_database()
    with db.write_transaction:
        yield
