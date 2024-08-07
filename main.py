import telebot
import json
from config import token
from datetime import datetime
from threading import Thread

bot = telebot.TeleBot(token)

with open('db.json', 'r') as f:
    db = json.load(f)
print(db)
backup_time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]

def napominanie():
    while True:
        if datetime.now().hour == 12 and datetime.now().minute == 0:
            for i in db:
                if db[str(i)]['privichka'] is not None:
                    bot.send_message(i, "Go to work!")
        if datetime.now().hour in backup_time and (datetime.now().minute == 2 or datetime.now().minute == 30):
            with open("db.json", "w") as f:
                json.dump(db, f)

t1 = Thread(target=napominanie)
t1.start()

def do_every_task(message):
    try:
        text = message.text
        bot.send_message(message.chat.id, "Great!")
        db[str(message.chat.id)]['balance'] += 1
        start(message)
    except:
        bot.send_message(message.chat.id, "Error: You stupid")

def add_every_task(message):
    text = message.text
    db[str(message.chat.id)]['privichka'].append(text)
    bot.send_message(message.chat.id, "Great!")
    start(message)


def add_task(message):
    text = message.text
    db[str(message.chat.id)]['tasks'].append(text)
    bot.send_message(message.chat.id, "Great!")
    start(message)

def del_fucking_task(message):
    try:
        text = message.text
        db[str(message.chat.id)]['tasks'].pop(int(message.text) - 1)
        bot.send_message(message.chat.id, "Great!")
        start(message)
    except:
        bot.send_message(message.chat.id, "Error: You stupid")

def del_fucking_every_task(message):
    try:
        text = message.text
        db[str(message.chat.id)]['privichka'].pop(int(message.text) - 1)
        bot.send_message(message.chat.id, "Great!")
        start(message)
    except:
        bot.send_message(message.chat.id, "Error: You stupid")


def do_task(message):
    try:
        text = message.text
        db[str(message.chat.id)]['tasks'].pop(int(message.text) - 1)
        bot.send_message(message.chat.id, "Great!")
        db[str(message.chat.id)]['balance'] += 1
        start(message)
    except:
        bot.send_message(message.chat.id, "Error: You stupid")


@bot.message_handler(commands=['start'])
def start(message):
    if str(message.chat.id) not in db:
        db[str(message.chat.id)] = {}
        db[str(message.chat.id)]['username'] = message.from_user.username
        db[str(message.chat.id)]['balance'] = 0
        db[str(message.chat.id)]['tasks'] = []
        db[str(message.chat.id)]['privichka'] = []
    markup = telebot.types.InlineKeyboardMarkup()
    About_button = telebot.types.InlineKeyboardButton(text='About', callback_data='about')
    Task_button = telebot.types.InlineKeyboardButton(text='Task', callback_data='task')
    markup.add(Task_button, About_button)
    bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}!\nYou have {db[str(message.chat.id)]["balance"]} money.', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "about":
            bot.send_message(call.message.chat.id, "Teamlead and programmer: @neko18")
        if call.data == "task":
            markup = telebot.types.InlineKeyboardMarkup()
            Create_button = telebot.types.InlineKeyboardButton(text='Create', callback_data='create')
            Show_button = telebot.types.InlineKeyboardButton(text='Show', callback_data='show')
            Delete_button = telebot.types.InlineKeyboardButton(text='Delete', callback_data='delete')
            Doit_button = telebot.types.InlineKeyboardButton(text='Done', callback_data='done')
            markup.add(Create_button, Show_button, Delete_button, Doit_button)
            bot.send_message(call.message.chat.id, "What do you want to do?", reply_markup=markup)
        if call.data == "create":
            One_day_button = telebot.types.InlineKeyboardButton(text='One day', callback_data='one')
            Every_day_button = telebot.types.InlineKeyboardButton(text="Every day", callback_data='every')
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(One_day_button, Every_day_button)
            bot.send_message(call.message.chat.id, "Is this a task that you will complete once or every day?", reply_markup=markup)
        if call.data == "show":
            e = 0
            q = 0
            w = ''
            w += f"You have {len(db[str(call.message.chat.id)]['tasks'])} tasks of the type 'One day'\n"
            for i in db[str(call.message.chat.id)]['tasks']:
                q += 1
                w += f"{q}. {i}\n"
            w += f"And you have {len(db[str(call.message.chat.id)]['privichka'])} tasks of the type 'Every day'\n"
            for i in db[str(call.message.chat.id)]['privichka']:
                e += 1
                w +=f"{e}. {i}\n"
            bot.send_message(call.message.chat.id, w)
        if call.data == "delete":
            q = 0
            e = 0
            w = ''
            w += f"You have {len(db[str(call.message.chat.id)]['tasks'])} tasks of the type 'One day'\n"
            for i in db[str(call.message.chat.id)]['tasks']:
                q += 1
                w += f"{q}. {i}\n"
            w += f"And you have {len(db[str(call.message.chat.id)]['privichka'])} tasks of the type 'Every day'\n"
            for i in db[str(call.message.chat.id)]['privichka']:
                e += 1
                w +=f"{e}. {i}\n"
            One_day_button = telebot.types.InlineKeyboardButton(text='One day', callback_data='del_one')
            Every_day_button = telebot.types.InlineKeyboardButton(text="Every day", callback_data='del_every')
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(One_day_button, Every_day_button)
            bot.send_message(call.message.chat.id, w, reply_markup=markup)
        if call.data == "done":
            q = 0
            e = 0
            w = ''
            w += f"You have {len(db[str(call.message.chat.id)]['tasks'])} tasks of the type 'One day'\n"
            for i in db[str(call.message.chat.id)]['tasks']:
                q += 1
                w += f"{q}. {i}\n"
            w += f"And you have {len(db[str(call.message.chat.id)]['privichka'])} tasks of the type 'Every day'\n"
            for i in db[str(call.message.chat.id)]['privichka']:
                e += 1
                w +=f"{e}. {i}\n"
            One_day_button = telebot.types.InlineKeyboardButton(text='One day', callback_data='one_task')
            Every_day_button = telebot.types.InlineKeyboardButton(text="Every day", callback_data='every_task')
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(One_day_button, Every_day_button)
            bot.send_message(call.message.chat.id, w, reply_markup=markup)
        if call.data == "one":
            bot.send_message(call.message.chat.id, "What is the task?")
            bot.register_next_step_handler(call.message, add_task)
        if call.data == "every":
            bot.send_message(call.message.chat.id, "What is the task?")
            bot.register_next_step_handler(call.message, add_every_task)
        if call.data == "one_task":
            bot.send_message(call.message.chat.id, "What is the task?")
            bot.register_next_step_handler(call.message, do_task)
        if call.data == "every_task":
            bot.send_message(call.message.chat.id, "What is the task?")
            bot.register_next_step_handler(call.message, do_every_task)
        if call.data == "del_one":
            bot.send_message(call.message.chat.id, "What task do you want to delete?")
            bot.register_next_step_handler(call.message, del_fucking_task)
        if call.data == "del_every":
            bot.send_message(call.message.chat.id, "What task do you want to delete?")
            bot.register_next_step_handler(call.message, del_fucking_every_task)


bot.polling(none_stop=True)
with open("db.json", "w") as f:
    json.dump(db, f)
#Аллах вас не простит
