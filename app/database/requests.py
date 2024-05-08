from app.database.models import async_session
from app.database.models import Date, Distance, Participant
from sqlalchemy import select


async def set_user(tg_id, fio, distance_id, date_id):
    async with async_session() as session:
        user = await session.scalar(select(Participant).where(Participant.tg_id == tg_id))

        if not user:
            distance_text = await session.scalar(select(Distance.distance).where(Distance.id == distance_id))
            date_text = await session.scalar(select(Date.date).where(Date.id == date_id))
            participant = Participant(tg_id=tg_id, fio=fio, distance=distance_text, date=date_text)
            session.add(participant)
            await session.commit()

async def get_distances():
    async with async_session() as session:
        return await session.scalars(select(Distance))

async def get_distance_date(distance_id):
    async with async_session() as session:
        return await session.scalars(select(Date).where(Date.distance == distance_id))