import logging
from typing import Optional
from shared.db import (
    execute_query, execute_one,
    execute_write, execute_write_returning
)

logger = logging.getLogger(__name__)


class BaseRepository:
    def __init__(self, conn):
        self.conn = conn

    def _query(
        self,
        sql: str,
        params: tuple = None
    ) -> list[dict]:
        logger.debug(f"Query: {sql[:100]}")
        return execute_query(self.conn, sql, params)

    def _query_one(
        self,
        sql: str,
        params: tuple = None
    ) -> Optional[dict]:
        logger.debug(f"Query one: {sql[:100]}")
        return execute_one(self.conn, sql, params)

    def _write(
        self,
        sql: str,
        params: tuple = None
    ) -> None:
        logger.debug(f"Write: {sql[:100]}")
        execute_write(self.conn, sql, params)

    def _write_returning(
        self,
        sql: str,
        params: tuple = None
    ) -> Optional[dict]:
        logger.debug(f"Write returning: {sql[:100]}")
        return execute_write_returning(
            self.conn, sql, params)
