from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Distance(Base):
    __tablename__ = 'distances'

    id: Mapped[int] = mapped_column(primary_key=True)
    distance: Mapped[str] = mapped_column(String(20))

class Date(Base):
    __tablename__ = 'dates'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column(String(20))
    distance: Mapped[int] = mapped_column(ForeignKey('distances.id'))

class Participant(Base):
    __tablename__ = 'participants'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    fio: Mapped[str] = mapped_column(String(40))
    distance: Mapped[str] = mapped_column(String(20))
    date: Mapped[str] = mapped_column(String(20))

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)