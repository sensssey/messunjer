from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.database import engine, Base
from src.auth.routes import auth_router
from src.posts.routes import posts_router
from src.profile.logikaprofilya import pr_router
from src.config import BASE_DIR
app = FastAPI()

app.include_router(auth_router)
app.include_router(posts_router)
app.include_router(pr_router)

@app.on_event("startup")
async def startup():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database connection established")
    except Exception as e:
        print(f"Database connection failed: {e}")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print(BASE_DIR)