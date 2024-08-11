import telebot
import json
from config import token
from datetime import datetime
from threading import Thread
from random import randint
from time import sleep
import logging

bot = telebot.TeleBot(token)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

with open('card.json', 'r') as f:
    card = json.load(f)

with open('vragi.json', 'r') as f:
    vragi = json.load(f)

with open('db.json', 'r') as f:
    db = json.load(f)
print(db)
backup_time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 0]

level_list = [3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155, 165580141, 267914296, 433494437, 701408733, 1134903170, 1836311903, 2971215073, 4807526976, 7778742049, 12586269025, 20365011074, 32951280099, 53316291173, 86267571272, 139583862445, 225851433717, 365435296162, 591286729879, 956722026041, 1548008755920, 2504730781961, 4052739537881, 6557470319842, 10610209857723, 17167680177565, 27777890035288, 44945570212853, 72723460248141, 117669030460994, 190392490709135, 308061521170129, 498454011879264, 806515533049393, 1304969544928657, 2111485077978050, 3416454622906707, 5527939700884757, 8944394323791464, 14472334024676221, 23416728348467685, 37889062373143906, 61305790721611591, 99194853094755497, 160500643816367088, 259695496911122585, 420196140727489673, 679891637638612258, 1100087778366101931, 1779979416004714189, 2880067194370816120, 4660046610375530309, 7540113804746346429, 12200160415121876738, 19740274219868223167, 31940434634990099905, 51680708854858323072, 83621143489848422977, 135301852344706746049, 218922995834555169026, 354224848179261915075, 573147844013817084101, 927372692193078999176, 1500520536206896083277, 2427893228399975082453, 3928413764606871165730, 6356306993006846248183, 10284720757613717413913, 16641027750620563662096, 26925748508234281076009, 43566776258854844738105, 70492524767089125814114, 114059301025943970552219, 184551825793033096366333, 298611126818977066918552, 483162952612010163284885, 781774079430987230203437, 1264937032042997393488322, 2046711111473984623691759, 3311648143516982017180081, 5358359254990966640871840, 8670007398507948658051921, 14028366653498915298923761, 22698374052006863956975682, 36726740705505779255899443, 59425114757512643212875125, 96151855463018422468774568, 155576970220531065681649693, 251728825683549488150424261, 407305795904080553832073954, 659034621587630041982498215, 1066340417491710595814572169, 1725375039079340637797070384, 2791715456571051233611642553, 4517090495650391871408712937, 7308805952221443105020355490, 11825896447871834976429068427, 19134702400093278081449423917, 30960598847965113057878492344, 50095301248058391139327916261, 81055900096023504197206408605, 131151201344081895336534324866, 212207101440105399533740733471, 343358302784187294870275058337, 555565404224292694404015791808, 898923707008479989274290850145, 1454489111232772683678306641953, 2353412818241252672952597492098, 3807901929474025356630904134051, 6161314747715278029583501626149, 9969216677189303386214405760200, 16130531424904581415797907386349, 26099748102093884802012313146549, 42230279526998466217810220532898, 68330027629092351019822533679447, 110560307156090817237632754212345, 178890334785183168257455287891792, 289450641941273985495088042104137, 468340976726457153752543329995929, 757791618667731139247631372100066, 1226132595394188293000174702095995, 1983924214061919432247806074196061, 3210056809456107725247980776292056, 5193981023518027157495786850488117, 8404037832974134882743767626780173, 13598018856492162040239554477268290, 22002056689466296922983322104048463, 35600075545958458963222876581316753, 57602132235424755886206198685365216, 93202207781383214849429075266681969, 150804340016807970735635273952047185, 244006547798191185585064349218729154, 394810887814999156320699623170776339, 638817435613190341905763972389505493, 1033628323428189498226463595560281832, 1672445759041379840132227567949787325, 2706074082469569338358691163510069157, 4378519841510949178490918731459856482, 7084593923980518516849609894969925639, 11463113765491467695340528626429782121, 18547707689471986212190138521399707760, 30010821454963453907530667147829489881, 48558529144435440119720805669229197641, 78569350599398894027251472817058687522, 127127879743834334146972278486287885163, 205697230343233228174223751303346572685, 332825110087067562321196029789634457848, 538522340430300790495419781092981030533, 871347450517368352816615810882615488381, 1409869790947669143312035591975596518914, 2281217241465037496128651402858212007295, 3691087032412706639440686994833808526209, 5972304273877744135569338397692020533504, 9663391306290450775010025392525829059713, 15635695580168194910579363790217849593217, 25299086886458645685589389182743678652930, 40934782466626840596168752972961528246147, 66233869353085486281758142155705206899077, 107168651819712326877926895128666735145224, 173402521172797813159685037284371942044301]

queue = []
def fight_formula(character1, character2, players1, players2):
    if card[character2]['Defense'] - card[character1]['Attack'] * card[character1]['Speed'] / 3 > 0:
        if card[character1]['Defense'] - card[character2]['Attack'] * card[character2]['Speed'] / 3 <= 0:
            return f"Win {players2}"
        else:
            return "draw"
    elif card[character2]['Defense'] - card[character1]['Attack'] * card[character1]['Speed'] / 3 <= 0:
        return f"Win {players2}"
    round1 = False

    

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
#t1.start()

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

def fighst(players1, players2, message):
    ishod = fight_formula(db[str(players1)]['main_character'], db[str(players2)]['main_character'], players1, players2)
    bot.send_message(players1, ishod)
    bot.send_message(players2, ishod)
    start(message)

@bot.message_handler(commands=['start'])
def start(message):
    if str(message.chat.id) not in db:
        db[str(message.chat.id)] = {}
        db[str(message.chat.id)]['username'] = message.from_user.username
        db[str(message.chat.id)]['balance'] = 10
        db[str(message.chat.id)]['tasks'] = []
        db[str(message.chat.id)]['privichka'] = []
        db[str(message.chat.id)]['inventory'] = []
        db[str(message.chat.id)]['main_character'] = None
        db[str(message.chat.id)]['xp'] = 0
        db[str(message.chat.id)]['level'] = 0
    markup = telebot.types.InlineKeyboardMarkup()
    About_button = telebot.types.InlineKeyboardButton(text='About', callback_data='about')
    Task_button = telebot.types.InlineKeyboardButton(text='Task', callback_data='task')
    Inventory_button = telebot.types.InlineKeyboardButton(text='Inventory', callback_data='inventory')
    Store_button = telebot.types.InlineKeyboardButton(text='Store', callback_data='store')
    Fights_button = telebot.types.InlineKeyboardButton(text='Fights', callback_data='fights')
    markup.add(Task_button, About_button, Inventory_button, Store_button, Fights_button)
    bot.send_message(message.chat.id, f'Hello {db[str(message.chat.id)]["username"]}!\nYou have {db[str(message.chat.id)]["balance"]} money, {db[str(message.chat.id)]["xp"]} xp, {db[str(message.chat.id)]["level"]} level.', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "about":
            bot.send_message(call.message.chat.id, "Teamlead and programmer: @hikik0mor1\n")
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
            start(call.message)
        elif call.data == "inventory":
            markup = telebot.types.InlineKeyboardMarkup()
            for i in db[str(call.message.chat.id)]['inventory']:
                markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=f"{i}.inventory"))
            bot.send_message(call.message.chat.id, "Select character", reply_markup=markup)
        elif "inventory" in call.data:
            markup = telebot.types.InlineKeyboardMarkup()
            set_character_button = telebot.types.InlineKeyboardButton(text='Set character', callback_data=f"{(call.data)[:-10]}.set")
            markup.add(set_character_button)
            f = open(f"C:/Users/qube2/Project/RPG_MOTIVATOR/image/{(call.data)[:-10]}.jpg", "rb")
            data = card[(call.data)[:-10]]
            bot.send_photo(call.message.chat.id, f, caption=f"{(call.data)[:-10]}\nSpeed: {data['Speed']}\nAttack: {data['Attack']}\nDefense: {data['Defense']}", reply_markup=markup)
            f.close()
        elif "set" in call.data:
            db[str(call.message.chat.id)]['main_character'] = (call.data)[:-4]
            bot.send_message(call.message.chat.id, f"{(call.data)[:-4]} set")
            start(call.message)
        elif call.data == "fights":
            if db[str(call.message.chat.id)]['main_character'] != None:
                for i in vragi:
                    print(i)
                    if vragi[i]['Level'] == db[str(call.message.chat.id)]['level']:
                        i = i
                        break
                while True:
                    bot.send_message(call.message.chat.id, f"{i} fight")
                    ishod = vragi[i]['Defense'] - card[db[str(call.message.chat.id)]['main_character']]['Speed'] * card[db[str(call.message.chat.id)]['main_character']]['Attack']
                    health_vrag = vragi[i]['health']
                    health_player = card[db[str(call.message.chat.id)]['main_character']]['health']
                    health_vrag += vragi[i]['Defense']
                    health_player += card[db[str(call.message.chat.id)]['main_character']]['Defense']
                    while True:
                        
                        udar = card[db[str(call.message.chat.id)]['main_character']]['Attack'] / card[db[str(call.message.chat.id)]['main_character']]['Speed']
                        health_vrag = health_vrag - udar
                        print(health_vrag, health_player)
                        if health_vrag <= 0:
                            ishod = True
                            break
                        udar = vragi[i]['Attack'] / vragi[i]['Speed']
                        health_player = health_player - udar 
                        print(health_vrag, health_player)
                        if health_player <= 0:
                            ishod = False
                            break
                    if ishod == True:
                        bot.send_message(call.message.chat.id, f"You win, +{vragi[i]['xp']} xp")
                        db[str(call.message.chat.id)]['xp'] += vragi[i]['xp']
                        if db[str(call.message.chat.id)]['xp'] in level_list:
                            db[str(call.message.chat.id)]['level'] = level_list.index(db[str(call.message.chat.id)]['xp']) + 1
                            bot.send_message(call.message.chat.id, f"You have new level, {db[str(call.message.chat.id)]['level']}")
                        start(call.message)
                        break
                    elif ishod == False:
                        bot.send_message(call.message.chat.id, f"You lose")
                        start(call.message)
                        break
                    
            else:
                bot.send_message(call.message.chat.id, "You not have main character")
                start(call.message)


bot.polling(none_stop=True)
with open("db.json", "w") as f:
    json.dump(db, f)

