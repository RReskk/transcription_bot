from aiogram import types, executor, Dispatcher, Bot
from bs4 import BeautifulSoup
import requests


def main():
    bot = Bot(bot_token)
    disp = Dispatcher(bot)

    @disp.message_handler(commands=['start'])
    async def start(message: types.Message):
        await bot.send_message(message.chat.id, 'Отправь мне слово на английском языке.')

    @disp.message_handler(content_types=['text'])
    async def parser(message: types.Message):
        request = requests.get(URL + message.text.strip())
        soup = BeautifulSoup(request.text, 'html.parser')
        try:
            transcription_block = soup.find('div', class_='trans_sound')
            transcription = transcription_block.find('span')
            sound = transcription_block.find('source')
            await bot.send_message(message.chat.id, transcription.text)
            await bot.send_voice(message.chat.id, f'https://wooordhunt.ru{sound["src"]}')
        except AttributeError:
            await bot.send_message(message.chat.id, 'К сожалению, данное слово не было найдено.')
        print('someone was used bot just now')
    executor.start_polling(disp)


if __name__ == '__main__':
    bot_token = 'TOKEN'
    URL = 'https://wooordhunt.ru/word/'
    main()
