import os
import asyncpg
from typing import Optional

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/alunos_db")

class Database:
    def __init__(self):
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        if not self.pool:
            self.pool = await asyncpg.create_pool(dsn=DATABASE_URL)

    async def disconnect(self):
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def get_connection(self):
        if not self.pool:
            raise Exception("Database pool is not initialized")
        return self.pool.acquire()

db = Database()
