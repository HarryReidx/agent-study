"""数据库初始化与会话管理。"""
from sqlmodel import SQLModel, Session, create_engine
from app.config.settings import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, echo=False)


def init_db() -> None:
    """创建全部表结构。"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI依赖：提供数据库会话。"""
    with Session(engine) as session:
        yield session
