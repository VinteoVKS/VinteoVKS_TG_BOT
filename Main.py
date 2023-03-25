import Db_core as Db
import telebot
from telebot import types

bot = telebot.TeleBot("API-TG")

connect = Db.connect
cursor = Db.cursor

@bot.message_handler(commands=['start'])
def Start(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        company_btn = types.KeyboardButton("О компании")
        subdivision_btn = types.KeyboardButton("Подразделения")
        workers_btn = types.KeyboardButton("Сотрудники")
        help_btn = types.KeyboardButton("Горячая линия")
        markup.add(company_btn, subdivision_btn, workers_btn, help_btn)
        bot.send_message(message.chat.id,
                         "Привет, {0.first_name}! Я помогу тебе соориентироваться в нашей компании".format(
                             message.from_user), reply_markup=markup)

    except:
        bot.send_message(message.chat.id, "Что-то пошло не так!")


@bot.message_handler(content_types=['text'])
def Bot_work(message):

    try:

        if (message.text == "Горячая линия"):
            bot.send_message(message.chat.id, "Техподдержка:"
                                              "\n8-800-333-40-16 звонок по России бесплатный"
                                              "\ne-mail: support@vinteo.ru"
                                              "\nПн-пт: 10:00-19:00"
                                              "\nСб-вс: выходной")

        elif (message.text == "О компании"):
            bot.send_message(message.chat.id, "Vinteo – российский производитель серверных решений видеоконференцсвязи,"
                                              " обеспечивающих до 90% совместимости со всеми стандартными протоколами ВКС."
                                              "\n\n100% отечественная компания с собственным штатом разработчиков")

        elif message.text == "Сотрудники":

            cursor.execute(
                "SELECT Worker.Id, Worker.FirstName, Worker.MiddleName, Worker.LastName, Worker.Number, Worker.Telegram, Post.Name"
                " FROM Worker, Post, WorkerHasPost"
                " WHERE WorkerHasPost.WorkerId = Worker.Id AND WorkerHasPost.PostId = Post.Id")

            info = []
            info = cursor.fetchall()

            kb = types.InlineKeyboardMarkup(row_width=1)

            for row in info:
                fio = str(row[0]) + ". " + row[1] + "\t" + row[2] + "\t" + str(row[3])

                kb.add(types.InlineKeyboardButton(text=fio, callback_data=str(row[0])))

            bot.send_message(message.chat.id, "Список всех сотрудников:", reply_markup=kb)

        elif(message.text == "Подразделения"):

            cursor.execute(
                "SELECT *"
                " FROM Subdivision")

            info = []
            info = cursor.fetchall()

            kb = types.InlineKeyboardMarkup(row_width=1)

            for row in info:
                fio = str(row[0]) + ". " + row[1]

                kb.add(types.InlineKeyboardButton(text=fio, callback_data=row[1]))

            bot.send_message(message.chat.id, "Список всех подразделений:", reply_markup=kb)
        else:
            bot.send_message(message.chat.id,"Такой команды не знаю(")
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так!")

@bot.callback_query_handler(func=lambda call: True)
def Worker_info(call):
    try:
        info = []
        kb = types.InlineKeyboardMarkup(row_width=1)

        cursor.execute(
            "SELECT Worker.Id, Worker.FirstName, Worker.MiddleName, Worker.LastName, Worker.Number, Worker.Telegram, Post.Name"
            " FROM Worker, Post, WorkerHasPost"
            " WHERE WorkerHasPost.WorkerId = Worker.Id AND WorkerHasPost.PostId = Post.Id")

        if(call.data == "Тестирование"):
            cursor.execute(
                "SELECT Worker.Id, Worker.FirstName, Worker.MiddleName, Worker.LastName, Worker.Number, Worker.Telegram, Post.Name"
                " FROM Worker, Post, WorkerHasPost, Subdivision, PostHasSubdivision"
                " WHERE WorkerHasPost.WorkerId = Worker.Id AND WorkerHasPost.PostId = Post.Id AND PostHasSubdivision.SubdivisionId = Subdivision.Id"
                " AND Subdivision.Id = 1 AND PostHasSubdivision.PostId = Post.Id")
            info = cursor.fetchall()
            for row in info:
                fio = row[1] + "\t" + row[2] + "\t" + str(row[3])
                kb.add(types.InlineKeyboardButton(text=fio, callback_data=str(row[0])))
            bot.send_message(call.message.chat.id, "Сотрудники подразделения 'Тестирование':", reply_markup=kb)

        if (call.data == "Frontend разработка"):
            cursor.execute(
                "SELECT Worker.Id, Worker.FirstName, Worker.MiddleName, Worker.LastName, Worker.Number, Worker.Telegram, Post.Name"
                " FROM Worker, Post, WorkerHasPost, Subdivision, PostHasSubdivision"
                " WHERE WorkerHasPost.WorkerId = Worker.Id AND WorkerHasPost.PostId = Post.Id AND PostHasSubdivision.SubdivisionId = Subdivision.Id"
                " AND Subdivision.Id = 2 AND PostHasSubdivision.PostId = Post.Id")
            info = cursor.fetchall()
            for row in info:
                fio = row[1] + "\t" + row[2] + "\t" + str(row[3])
                kb.add(types.InlineKeyboardButton(text=fio, callback_data=str(row[0])))
            bot.send_message(call.message.chat.id, "Сотрудники подразделения 'Frontend разрааботка':", reply_markup=kb)

        if (call.data == "Backend разработка"):
            cursor.execute(
                "SELECT Worker.Id, Worker.FirstName, Worker.MiddleName, Worker.LastName, Worker.Number, Worker.Telegram, Post.Name"
                " FROM Worker, Post, WorkerHasPost, Subdivision, PostHasSubdivision"
                " WHERE WorkerHasPost.WorkerId = Worker.Id AND WorkerHasPost.PostId = Post.Id AND PostHasSubdivision.SubdivisionId = Subdivision.Id"
                " AND Subdivision.Id = 3 AND PostHasSubdivision.PostId = Post.Id")
            info = cursor.fetchall()
            for row in info:
                fio = row[1] + "\t" + row[2] + "\t" + str(row[3])
                kb.add(types.InlineKeyboardButton(text=fio, callback_data=str(row[0])))
            bot.send_message(call.message.chat.id, "Сотрудники подразделения 'Backend разработка':", reply_markup=kb)

        if (call.data == "Техподдержка"):
            cursor.execute(
                "SELECT Worker.Id, Worker.FirstName, Worker.MiddleName, Worker.LastName, Worker.Number, Worker.Telegram, Post.Name"
                " FROM Worker, Post, WorkerHasPost, Subdivision, PostHasSubdivision"
                " WHERE WorkerHasPost.WorkerId = Worker.Id AND WorkerHasPost.PostId = Post.Id AND PostHasSubdivision.SubdivisionId = Subdivision.Id"
                " AND Subdivision.Id = 4 AND PostHasSubdivision.PostId = Post.Id")
            info = cursor.fetchall()
            for row in info:
                fio = row[1] + "\t" + row[2] + "\t" + str(row[3])
                kb.add(types.InlineKeyboardButton(text=fio, callback_data=str(row[0])))
            bot.send_message(call.message.chat.id, "Сотрудники подразделения 'Техподдержка':", reply_markup=kb)

        info = cursor.fetchall()
        for row in info:
            if call.data == str(row[0]):
                fio ="ФИО: " + row[1] + "\t" + row[2] + "\t" + row[3] + "\nНомер телефона: " + str(row[4]) + "\nTelegram: " + row[5] + "\nПродукт ответственности: " + row[6]
                bot.send_message(call.message.chat.id,fio)

    except:
        bot.send_message(call.message.chat.id, "Что-то пошло не так!")
bot.polling(none_stop=True)
