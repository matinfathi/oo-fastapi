from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import select

from fastapi.middleware.gzip import GZipMiddleware

from app.user.router import user_router
from app.user.models import Role, OoUserModel as User
from app.core.config import settings
from app.core.security import core_router, get_password_hash
from app.core.database_async import init_db, AsyncSessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.role == "SuperAdmin"))
        existing = result.scalar_one_or_none()

        if not existing:
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin"),
                role=Role.SuperAdmin,
            )
            session.add(admin)
            await session.commit()

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan,
)

app.add_middleware(GZipMiddleware, minimum_size=500)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(core_router, prefix="", tags=["Security"])


@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
