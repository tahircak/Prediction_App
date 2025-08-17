import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from db import init_db, get_session
from models import User
from routers import auth as auth_router
from routers import matches as matches_router
from routers import admin as admin_router
from auth import get_password_hash


def get_cors_origins():
    origins_env = os.getenv("CORS_ORIGINS", "*")
    if origins_env == "*":
        return ["*"]
    return [o.strip() for o in origins_env.split(",") if o.strip()]


app = FastAPI(title="Predictions API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(matches_router.router)
app.include_router(admin_router.router)


@app.on_event("startup")
def on_startup():
    init_db()
    # Admin kullanıcısını oluştur veya admin yap
    admin_email = "admin@betapp.com"
    with next(get_session()) as session:  # type: ignore
        existing = session.exec(select(User).where(User.email == admin_email)).first()
        if existing:
            # Kullanıcı varsa admin yap
            if not existing.is_admin:
                existing.is_admin = True
                session.commit()
                print(f"✅ {admin_email} admin yapıldı")
        else:
            # Kullanıcı yoksa oluştur
            user = User(
                email=admin_email,
                password_hash=get_password_hash("admin123"),
                is_admin=True,
            )
            session.add(user)
            session.commit()
            print(f"✅ Admin kullanıcısı oluşturuldu: {admin_email}")
