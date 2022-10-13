#Импортируем необходимые библиотеки
from dataclasses import replace
import requests
import datetime
from config import tg_bot_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import login_spyer
from config import token_spyer

#Назначаем диспатчер и указываем путь к токену
bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

# Бот ожидает команду "Старт" от юзера и передает ему кнопки клавиатуры
@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup()
    button_1 = types.KeyboardButton(text="Soccer")
    keyboard.add(button_1)
    button_2 = "Basketball"
    keyboard.add(button_2)
    await message.answer("Привет! Выбери вид спорта", reply_markup=keyboard)

#Выполняем запрос
@dp.message_handler()
async def get_score(message: types.Message):
    try:
        r = requests.get(
            f'https://spoyer.ru/api/get.php?login={login_spyer}&token={token_spyer}&task=livedata&sport={message.text}'
        )
        data = r.json()
        #pprint(data) # Данная функция выполняет вывод информации в формате json
        
        # Назначем переменные для полученных объектов json
        number_match1 = data['games_live'][0]['game_id']
        number_match2 = data['games_live'][1]['game_id']
        number_match3 = data['games_live'][2]['game_id']
        #data_game1 = datetime.fromtimestamp(data['games_live'][0]['time'])
        #data_game2 = datetime.datetime.fromtimestamp(data['games_live'][1]['time'])
        #data_game3 = datetime.datetime.fromtimestamp(data['games_live'][2]['time'])
        league1 = data['games_live'][0]['league']['name']
        league2 = data['games_live'][1]['league']['name']
        league3 = data['games_live'][2]['league']['name']
        home1 = data['games_live'][0]['home']['name']
        home2 = data['games_live'][1]['home']['name']
        home3 = data['games_live'][2]['home']['name']
        away1 = data['games_live'][0]['away']['name']
        away2 = data['games_live'][1]['away']['name']
        away3 = data['games_live'][2]['away']['name']
        score1 = data['games_live'][0]['score']
        score2 = data['games_live'][1]['score']
        score3 = data['games_live'][2]['score']

        # Выводим сообщение по назначенным ключам
        await message.reply(f'Номер матча: {number_match1}\nЛига: {league1}\nХозяева: {home1}\nГости: {away1}\nСчет: {score1}\n')
        await message.reply(f'Номер матча: {number_match2}\nЛига: {league2}\nХозяева: {home2}\nГости: {away2}\nСчет: {score2}\n')
        await message.reply(f'Номер матча: {number_match3}\nЛига: {league3}\nХозяева: {home3}\nГости: {away3}\nСчет: {score3}\n')

        # Если пользователь ввел текст самостоятельно, то выводим ошибку
    except:
        await message.reply('😢Такого спорта не существует😢')

        # Позволяет боту работать без перезапуска после каждого запроса
if __name__ == '__main__':
    executor.start_polling(dp)