from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram import Router
from aiogram.filters.command import Command

from os import getenv
from db_connection import get_db_connection

router = Router()


@router.message(Command("rand"))
async def command_random_quote(message: Message) -> None:
    connection = get_db_connection()
    cursor = connection.cursor()
    table_name = 'quotes_star_wars'
    cursor.execute(f'SELECT * FROM {table_name} ORDER BY RAND() LIMIT 1;')
    doc = cursor.fetchone()

    await message.answer(f'<b>Quote</b>:\n{doc["quote"]}\n©{doc["author_en"]}\n\n<b>Цитата</b>:\n<tg-spoiler>{doc["quote_translation"]}\n{doc["author_ru"]}</tg-spoiler>')
    await message.bot.send_message(getenv('ADMIN_ID'), f'{message.from_user.full_name} command rand\nGot: {doc["quote"]}')
    connection.close()
    cursor.close()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f'Hello, {hbold(message.from_user.full_name)}!')
