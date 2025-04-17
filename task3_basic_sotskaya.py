import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram import F
import asyncio

API_TOKEN = 'token'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

with open('C:/Users/User/Downloads/faq.json', encoding='utf-8') as f:
    data = json.load(f)

keywords = {
    "цены": ["цены", "стоимость", "заказ", "оплата"],
    "часы работы": ["часы работы", "время работы", "доступность"],
    "доставка": ["доставка", "сроки доставки", "стоимость доставки", "отслеживание"],
    "возврат": ["возврат", "обмен", "возврат товара", "гарантия"],
    "контакты": ["связаться", "телефон", "email", "адрес"]
}

def find_answer(user_message):
    for category, words in keywords.items():
        for word in words:
            if word in user_message.lower():
                for item in data['faq']:
                    if word in item['question'].lower():
                        return item['answer']
    return "Извините, я не понял ваш вопрос."

kb = [
    [
        KeyboardButton(text="О компании"), 
        KeyboardButton(text="Связаться с оператором")
    ]
]

keyboard = ReplyKeyboardMarkup(
    keyboard=kb,  
    resize_keyboard=True,
    input_field_placeholder="Выберите действие"
)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я бот, который поможет вам с часто задаваемыми вопросами. Задайте свой вопрос или выберите одну из кнопок ниже.", reply_markup=keyboard)

@dp.message(F.text == "О компании")
async def about_company(message: types.Message):
    await message.answer("Наша компания занимается доставкой товаров по всей стране.")

@dp.message(F.text == "Связаться с оператором")
async def contact_operator(message: types.Message):
    await message.answer("Перевожу на оператора...")

@dp.message()
async def handle_message(message: types.Message):
    answer = find_answer(message.text)
    await message.reply(answer)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())