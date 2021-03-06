import logging

from aiogram import types, Bot
from decouple import config

from messages_controller import extract_user_object, extract_message_object, extract_chat_object
from controllers.glpi import glpi

bot = Bot(token= config('API_TOKEN'))

class BeltisBot:
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher
        self.bot = bot
        self.glpi = glpi()
        self.run_bot()

    def run_bot(self):
        @self.dispatcher.message_handler(commands=['start', 'help'])
        async def send_welcome(message: types.Message):
            await message.reply("""Beltis TI bot. 
 *AINDA EM PRODUÇÃO*

 Available commands:
  - /help: Provides the command list;
  - /getid: Returns the user id, used to setup the zabbix notifications;
  - /ticket ID: Returns information about the ticket provided 
""")

        @self.dispatcher.message_handler(commands=['getid'])
        async def return_user_id(message: types.Message):
            msg = extract_user_object(message)
            await message.reply(msg.telegram_id)

        @self.dispatcher.message_handler(commands=['ticket'])
        async def ticket_handler(message: types.Message):
            if (len(message.text) > 7):
                ticket_id = message.text.split(' ')[1]
                ticket_status =  self.glpi.getTicket(ticket_id)
                await message.reply(ticket_status)
            else:
                await message.reply("Criar ticket")

        
        @self.dispatcher.message_handler(commands=['teste'])
        async def testMessage(message: types.Message):
            print(message)
            await message.reply(message)
    
        @self.dispatcher.message_handler(commands=['validateGLPI'])
        async def validate_glpi_api(message: types.Message):
            await message.reply("App-Token: {}\nSession-Token: {}".format(self.glpi.app_token,self.glpi.session_token))
    
