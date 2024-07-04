from aiogram.utils import executor
from initialisation import dispatcher as dp
from client import client_handlers
import aiofiles
import datetime


async def on_startup(_):
    async with aiofiles.open(file="log.txt",
                             mode="a",
                             encoding="utf-8") as f:
        await f.write(f"[SYSTEM] | {str(datetime.datetime.now())[:-7]} | Бот запущен успешно\n")


async def on_shutdown(_):
    async with aiofiles.open(file="log.txt",
                             mode="a",
                             encoding="utf-8") as f:
        await f.write(f"[SYSTEM] | {str(datetime.datetime.now())[:-7]} | Бот выключен\n")


if __name__ == "__main__":
    client_handlers(dp)

    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup,
                           on_shutdown=on_shutdown)
