from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from llama_index.llms.ollama import Ollama

storage = MemoryStorage()

llm = Ollama(model='llama3')

load_dotenv()
token = os.getenv('TOKEN')

bot = Bot(token=token)
dispatcher = Dispatcher(bot, storage=storage)
