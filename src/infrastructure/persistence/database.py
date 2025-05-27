"""Database connection and operations."""

import asyncpg
from asyncpg import Connection, Record
from asyncpg.pool import Pool
import os
from typing import Any, Dict, List, Optional

class Database:
    """Database connection and operations."""

    def __init__(self, dsn: str):
        """Initialize the database connection pool."""
        self.dsn = dsn
        self.pool: Optional[Pool] = None

    async def connect(self) -> None:
        """Establish a connection pool to the database."""
        self.pool = await asyncpg.create_pool(dsn=self.dsn)

    async def disconnect(self) -> None:
        """Close the connection pool."""
        if self.pool:
            await self.pool.close()

    async def execute(self, query: str, *args: Any) -> str:
        """Execute a query that doesn't return rows."""
        async with self.pool.acquire() as connection:
            return await connection.execute(query, *args)

    async def fetch(self, query: str, *args: Any) -> List[Record]:
        """Execute a query that returns rows."""
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def fetchrow(self, query: str, *args: Any) -> Record:
        """Execute a query that returns a single row."""
        async with self.pool.acquire() as connection:
            return await connection.fetchrow(query, *args)

    async def save_flujo_ejecutado(self, flujo: Dict[str, Any]) -> int:
        """Save a FlujoEjecutado record to the database."""
        query = """
        INSERT INTO flujo_ejecutado (id, data, status, created_at, updated_at)
        VALUES ($1, $2, $3, NOW(), NOW())
        RETURNING id
        """
        return await self.execute(query, flujo["id"], flujo["data"], flujo["status"])

    async def update_flujo_ejecutado(self, flujo: Dict[str, Any]) -> None:
        """Update a FlujoEjecutado record in the database."""
        query = """
        UPDATE flujo_ejecutado
        SET data = $2, status = $3, updated_at = NOW()
        WHERE id = $1
        """
        await self.execute(query, flujo["id"], flujo["data"], flujo["status"])

# Initialize the database connection
db = Database(os.getenv("AUDIT_DB_URL", "postgresql://user:password@localhost:5432/audit_db"))

async def init_db():
    """Initialize the database connection."""
    await db.connect()

async def close_db():
    """Close the database connection."""
    await db.disconnect()