import telebot
import json
from config import token
from datetime import datetime
from threading import Thread

bot = telebot.TeleBot(token)

with open('card.json', 'r') as f:
    card = json.load(f)

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
        db[str(message.chat.id)]['balance'] = 10
        db[str(message.chat.id)]['tasks'] = []
        db[str(message.chat.id)]['privichka'] = []
        db[str(message.chat.id)]['inventory'] = []
    markup = telebot.types.InlineKeyboardMarkup()
    About_button = telebot.types.InlineKeyboardButton(text='About', callback_data='about')
    Task_button = telebot.types.InlineKeyboardButton(text='Task', callback_data='task')
    Inventory_button = telebot.types.InlineKeyboardButton(text='Inventory', callback_data='inventory')
    Store_button = telebot.types.InlineKeyboardButton(text='Store', callback_data='store')
    markup.add(Task_button, About_button, Inventory_button, Store_button)
    bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}!\nYou have {db[str(message.chat.id)]["balance"]} money.', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "about":
            bot.send_message(call.message.chat.id, "Teamlead and programmer: @neko18\n")
        elif call.data == "task":
            markup = telebot.types.InlineKeyboardMarkup()
            Create_button = telebot.types.InlineKeyboardButton(text='Create', callback_data='create')
            Show_button = telebot.types.InlineKeyboardButton(text='Show', callback_data='show')
            Delete_button = telebot.types.InlineKeyboardButton(text='Delete', callback_data='delete')
            Doit_button = telebot.types.InlineKeyboardButton(text='Done', callback_data='done')
            markup.add(Create_button, Show_button, Delete_button, Doit_button)
            bot.send_message(call.message.chat.id, "What do you want to do?", reply_markup=markup)
        elif call.data == "create":
            One_day_button = telebot.types.InlineKeyboardButton(text='One day', callback_data='one')
            Every_day_button = telebot.types.InlineKeyboardButton(text="Every day", callback_data='every')
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(One_day_button, Every_day_button)
            bot.send_message(call.message.chat.id, "Is this a task that you will complete once or every day?", reply_markup=markup)
        elif call.data == "show":
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
        elif call.data == "delete":
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
        elif call.data == "done":
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
        elif call.data == "one":
            bot.send_message(call.message.chat.id, "What is the task?")
            bot.register_next_step_handler(call.message, add_task)
        elif call.data == "every":
            bot.send_message(call.message.chat.id, "What is the task?")
            bot.register_next_step_handler(call.message, add_every_task)
        elif call.data == "one_task":
            bot.send_message(call.message.chat.id, "What is the task?")
            bot.register_next_step_handler(call.message, do_task)
        elif call.data == "every_task":
            bot.send_message(call.message.chat.id, "What is the task?")
            bot.register_next_step_handler(call.message, do_every_task)
        elif call.data == "del_one":
            bot.send_message(call.message.chat.id, "What task do you want to delete?")
            bot.register_next_step_handler(call.message, del_fucking_task)
        elif call.data == "del_every":
            bot.send_message(call.message.chat.id, "What task do you want to delete?")
            bot.register_next_step_handler(call.message, del_fucking_every_task)
        elif call.data == "store":
            markup = telebot.types.InlineKeyboardMarkup()
            for i in card:
                print(i)
                markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
            bot.send_message(call.message.chat.id, "Select the character you want to watch:", reply_markup=markup)
        elif call.data in card:
            buy_person_button = telebot.types.InlineKeyboardButton(text='Buy person', callback_data=f"{call.data}.buy")
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(buy_person_button)
            f = open(f"C:/Users/qube2/Project/RPG_MOTIVATOR/image/{call.data}.jpg", "rb")
            bot.send_photo(call.message.chat.id, f, caption=f"{call.data}\nSpeed: {card[call.data]['Speed']}\nAttack: {card[call.data]['Attack']}\nDefense: {card[call.data]['Defense']}\nPrice: {card[call.data]['price']}", reply_markup=markup)
            f.close()
        elif "buy" in call.data:
            if call.data[:-4] not in db[str(call.message.chat.id)]['inventory'] and db[str(call.message.chat.id)]['balance'] >= card[(call.data)[:-4]]['price']:
                db[str(call.message.chat.id)]['inventory'].append((call.data)[:-4])
                db[str(call.message.chat.id)]['balance'] -= card[(call.data)[:-4]]['price']
                bot.send_message(call.message.chat.id, f"{(call.data)[:-4]} bought!")
            else:
                bot.send_message(call.message.chat.id, f"You can't buy {(call.data)[:-4]}")
        elif call.data == "inventory":
            markup = telebot.types.InlineKeyboardMarkup()
            for i in db[str(call.message.chat.id)]['inventory']:
                markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=f"{i}.inventory"))
            bot.send_message(call.message.chat.id, "Select character", reply_markup=markup)
        elif "inventory" in call.data:
            f = open(f"C:/Users/qube2/Project/RPG_MOTIVATOR/image/{(call.data)[:-10]}.jpg", "rb")
            data = card[(call.data)[:-10]]
            bot.send_photo(call.message.chat.id, f, caption=f"{(call.data)[:-10]}\nSpeed: {data['Speed']}\nAttack: {data['Attack']}\nDefense: {data['Defense']}")
            f.close()
bot.polling(none_stop=True)
with open("db.json", "w") as f:
    json.dump(db, f)

