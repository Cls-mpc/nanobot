import telebot
from telebot import types
import time
import threading
import os

TOKEN = os.getenv("8332636276:AAHunYZlJ7Vdw0fjM-9ScbKr4iepaWmkEfg")
OWNER_ID = 8746755745

bot = telebot.TeleBot(TOKEN)

users = {}
today_users = set()

banned_users = set()

message_links = {}

broadcast_wait = False
broadcast_text = ""

default_welcome = (
    "<i>Здравствуйте!\n\n"
    "Отправьте своё сообщение и мы ответим в ближайшее время.\n"
    "Это полностью анонимно 🎭</i>\n\n"
    "<blockquote><i>Создано с помощью @ReFatherBot</i></blockquote>"
)

welcome_text = default_welcome

waiting_name = False
waiting_welcome = False

banned_users = set()

broadcast_wait = False
broadcast_text = ""

def delete_after(chat, msg, sec=2):
    def task():
        time.sleep(sec)

        try:
            bot.delete_message(chat, msg)
        except:
            pass

    threading.Thread(target=task).start()

# START
@bot.message_handler(commands=["start"])
def start(message):

    user = message.from_user

    if user.id not in users:
        users[user.id] = {
            "username": user.username,
            "name": user.first_name
        }

        today_users.add(user.id)

    remove = types.ReplyKeyboardRemove()

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="HTML",
        reply_markup=remove
    )

    if message.chat.id == OWNER_ID:

        bot.send_message(
            message.chat.id,
            "пс: функционал бота является экспериментальным, при возникновении вопросов просьба писать в @clsMPC_bot.\n/help для получения полной информации о боте."
        )

# HELP
@bot.message_handler(commands=['help'])
def help_cmd(message):

    if message.chat.id != OWNER_ID:
        return

     
    text = (
    "<b>📝 FAQ для создателя:</b>\n\n"

    "<b>1. Ответ на сообщения.</b>\n"
    "• Чтобы ответить на сообщение, нужно просто свайпнуть его (провести пальцем справа налево) и отправить ответ.\n\n"

    "<b>2. Статистика, приветствие и название бота.</b>\n"
    "• Напишите /admin, чтобы открыть меню управления.\n\n"

    "<b>3. Блокировка пользователей.</b>\n"
    "• Напишите /ban, чс или бан в ответ на сообщение (описано в пункте 1) пользователя, чтобы его заблокировать.\n\n"

    "<b>4. Разблокировка пользователей.</b>\n"
    "• Напишите /unban, разбан в ответ на сообщение (описано в пункте 1) пользователя, чтобы его разблокировать.\n\n"

    "<b>5. Изменить аватарку/описание.</b>\n"
    "• Откройте профиль вашего бота (сначала диалог с ним, затем нажмите на название бота) и найдите кнопку редактирования (Изм. / Ред.).\n\n"

    "<b>6. Рассылка.</b>\n"
    "• Вы можете разослать сообщение всем пользователям вашего бота — используйте /broadcast и следуйте инструкции.\n\n"

    "<b>7. Привязать канал.</b>\n"
    "• Вы можете привязать свой канал к боту. Подробнее — /channel.\n\n"

    "<b>8. Добавить администратора.</b>\n"
    "• Создайте чат, добавьте туда бота и нужных пользователей.\n\n"

    "<blockquote>Информация будет дополняться.</blockquote>"
    )

    bot.send_message(
        message.chat.id, 
        text, 
        parse_mode="HTML"
    ) 

# ADMIN 
@bot.message_handler(commands=['admin'])
def admin(message):

    if message.chat.id != OWNER_ID:
        return

    markup = types.InlineKeyboardMarkup()
    
    markup.add(
        types.InlineKeyboardButton(
            "Настройки ⚙️",
            callback_data="settings"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "Статистика 📊",
            callback_data="stats"
        )
    )

    bot.send_message(
        message.chat.id,
        "Управление ботом.",
        reply_markup=markup
    )

# BAN
@bot.message_handler(commands=['ban'])
def ban_user(message):

    if message.chat.id != OWNER_ID:
        return

    if not message.reply_to_message:
        return

    msg_id = message.reply_to_message.message_id

    if msg_id in message_links:

        uid = message_links[msg_id]

        banned_users.add(uid)

        try:
            bot.send_message(
                uid,
                "⛔ Вас заблокировала администрация.\nТеперь ваши сообщения не будут доставляться владельцу бота."
            )
        except:
            pass

        bot.send_message(
            OWNER_ID,
            "✅ Пользователь заблокирован."
        )


@bot.message_handler(func=lambda m: m.text and m.text.lower() in ["бан", "чс"])
def ban_words(message):

    if message.chat.id != OWNER_ID:
        return

    if not message.reply_to_message:
        return

    msg_id = message.reply_to_message.message_id

    if msg_id in message_links:

        uid = message_links[msg_id]

        banned_users.add(uid)

        try:
            bot.send_message(
                uid,
                "⛔ Вас заблокировала администрация.\nТеперь ваши сообщения не будут доставляться владельцу бота."
            )
        except:
            pass

        bot.send_message(
            OWNER_ID,
            "✅ Пользователь заблокирован."
        )


# UNBAN
@bot.message_handler(commands=['unban'])
def unban_user(message):

    if message.chat.id != OWNER_ID:
        return

    if not message.reply_to_message:
        return

    msg_id = message.reply_to_message.message_id

    if msg_id in message_links:

        uid = message_links[msg_id]

        banned_users.discard(uid)

        try:
            bot.send_message(
                uid,
                "✅ Администрация сняла блокировку."
            )
        except:
            pass

        bot.send_message(
            OWNER_ID,
            "✅ Пользователь разблокирован."
        )


@bot.message_handler(func=lambda m: m.text and m.text.lower() == "разбан")
def unban_word(message):

    if message.chat.id != OWNER_ID:
        return

    if not message.reply_to_message:
        return

    msg_id = message.reply_to_message.message_id

    if msg_id in message_links:

        uid = message_links[msg_id]

        banned_users.discard(uid)

        try:
            bot.send_message(
                uid,
                "✅ Администрация сняла блокировку."
            )
        except:
            pass

        bot.send_message(
            OWNER_ID,
            "✅ Пользователь разблокирован."
        )

# BROADCAST
@bot.message_handler(commands=['broadcast'])
def broadcast(message):

    global broadcast_wait

    if message.chat.id != OWNER_ID:
        return

    broadcast_wait = True

    bot.send_message(
        OWNER_ID,
        "Пришлите сообщение, которое вы хотите отправить всем пользователям бота:"
    )
    
# CHANNEL
@bot.message_handler(commands=['channel'])
def channel(message):

    if message.chat.id != OWNER_ID:
        return

    text = (
        "Вы можете разрешить присылать вам сообщения только пользователям определенного канала.\n"
        "Чтобы активировать эту функцию - привяжите канал к боту, для этого необходимо назначить бота администратором канала с правами на добавление участников.\n"
        "➖ Для удобства используйте кнопку \"🏩 Выбрать канал\" на клавиатуре 👇"
    )

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    btn_channel = types.KeyboardButton(
        text="🏩 Выбрать канал",
        request_chat=types.KeyboardButtonRequestChat(
            request_id=1,
            chat_is_channel=True
        )
    )

    btn_cancel = types.KeyboardButton(
        "❌Отменить"
    )

    markup.add(btn_channel)
    markup.add(btn_cancel)

    bot.send_message(
        message.chat.id,
        text,
        reply_markup=markup
    )

# CALLBACK
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    global waiting_name
    global waiting_welcome
    global welcome_text

    chat = call.message.chat.id
    msg_id = call.message.message_id

    if call.data == "settings":

        waiting_name = False
        waiting_welcome = False

        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton(
                "🖋️Имя бота",
                callback_data="name"
            )
        )

        markup.add(
            types.InlineKeyboardButton(
                "👐Приветствия",
                callback_data="welcome"
            )
        )

        markup.add(
            types.InlineKeyboardButton(
                "⬅️Назад",
                callback_data="admin"
            )
        )

        bot.edit_message_text(
            "⚙️ Настройки",
            chat,
            msg_id,
            reply_markup=markup
        )

    elif call.data == "admin":

        waiting_name = False
        waiting_welcome = False

        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton(
                "Настройки ⚙️",
                callback_data="settings"
            )
        )

        markup.add(
            types.InlineKeyboardButton(
                "Статистика 📊",
                callback_data="stats"
            )
        )

        bot.edit_message_text(
            "Управление ботом.",
            chat,
            msg_id,
            reply_markup=markup
        )

    elif call.data == "stats":

        text = "📊 Статистика\n\n"

        text += f"Всего пользователей — {len(users)}\n"
        text += f"Новых пользователей — {len(today_users)}\n\n"

        for uid, data in users.items():

            text += (
                f"ID: {uid}\n"
                f"Username: @{data['username']}\n"
                f"Имя: {data['name']}\n\n"
            )

        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton(
                "⬅️Назад",
                callback_data="admin"
            )
        )

        bot.edit_message_text(
            text,
            chat,
            msg_id,
            reply_markup=markup
        )

    elif call.data == "name":

        waiting_name = True
        waiting_welcome = False

        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton(
                "❌ Отменить",
                callback_data="settings"
            )
        )

        bot.edit_message_text(
            "🖋️ Напишите новое имя для вашего бота (до 64 символов).",
            chat,
            msg_id,
            reply_markup=markup
        )

    elif call.data == "welcome":

        waiting_welcome = True
        waiting_name = False

        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton(
                "🗑️Удалить приветствие",
                callback_data="resetwelcome"
            )
        )

        bot.edit_message_text(
            "👋 Напишите новое приветствие для вашего бота (до 1024 символов).",
            chat,
            msg_id,
            reply_markup=markup
        )

    elif call.data == "resetwelcome":

        waiting_welcome = False
        welcome_text = default_welcome

        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton(
                "🖋️Имя бота",
                callback_data="name"
            )
        )

        markup.add(
            types.InlineKeyboardButton(
                "👐Приветствия",
                callback_data="welcome"
            )
        )

        markup.add(
            types.InlineKeyboardButton(
                "⬅️Назад",
                callback_data="admin"
            )
        )

        bot.edit_message_text(
            "⚙️ Настройки",
            chat,
            msg_id,
            reply_markup=markup
        )

    elif call.data == "start_broadcast":

        for uid in users:

            try:
                bot.send_message(uid, broadcast_text)
            except:
                pass

        bot.send_message(
            OWNER_ID,
            "Рассылка начата успешно!"
        )

        try:
            bot.delete_message(chat, msg_id)
        except:
            pass

    elif call.data == "cancel_broadcast":

        bot.send_message(
            OWNER_ID,
            "Действие отменено."
        )

        try:
            bot.delete_message(chat, msg_id)
        except:
            pass

# ОБЩИЙ ОБРАБОТЧИК
@bot.message_handler(func=lambda m: True)
def messages(message):

    global waiting_name
    global waiting_welcome
    global welcome_text
    global broadcast_wait
    global broadcast_text

    # ВЛАДЕЛЕЦ БОТА
    if message.chat.id == OWNER_ID:

        if message.text == "❌Отменить":

            remove = types.ReplyKeyboardRemove()

            bot.send_message(
                OWNER_ID,
                "Действие отменено.",
                reply_markup=remove
            )

            return
        
        if broadcast_wait:

            broadcast_wait = False
            broadcast_text = message.text

            markup = types.InlineKeyboardMarkup()

            markup.add(
                types.InlineKeyboardButton(
                    "Начать рассылку",
                    callback_data="start_broadcast"
                )
            )

            markup.add(
                types.InlineKeyboardButton(
                    "Отменить",
                    callback_data="cancel_broadcast"
                )
            )

            bot.send_message(
                OWNER_ID,
                'Это сообщение будет отправлено всем пользователям вашего бота.\n\nЕсли вы уверены, нажмите "Начать рассылку" либо "Отмена" для завершения.',
                reply_markup=markup
            )

            return
        
        if waiting_name:

            waiting_name = False

            new_name = message.text[:64]

            try:
                bot.set_my_name(new_name)
            except:
                pass

            bot.send_message(
                OWNER_ID,
                f'🖋️Имя вашего бота изменено на "{new_name}"\n\nЧтобы увидеть его, подождите или перезагрузите Telegram.'
            )

            return

        
        if waiting_welcome:

            waiting_welcome = False

            welcome_text = message.text

            bot.send_message(
                OWNER_ID,
                "✅ Приветствие обновлено"
            )

            return

        # ответ пользователю через свайп
        if message.reply_to_message:

            replied_id = message.reply_to_message.message_id

            if replied_id in message_links:

                user_id = message_links[replied_id]

                bot.send_message(
                    user_id,
                    message.text
                )

                msg = bot.send_message(
                    OWNER_ID,
                    "✅ Ваш ответ успешно отправлен"
                )

                delete_after(
                    OWNER_ID,
                    msg.message_id
                )

        return

    if message.from_user.id in banned_users:
        return
    
    # ПОЛЬЗОВАТЕЛЬ
    user = message.from_user

    text = (
        "<i>💬 У тебя новое анонимное сообщение!</i>\n\n"
        f"<blockquote>{message.text}</blockquote>\n\n"
        "<i>⬅️ Свайпни для ответа.</i>"
    )

    msg = bot.send_message(
        OWNER_ID,
        text,
        parse_mode="HTML"
    )

    message_links[msg.message_id] = user.id

    bot.send_message(
    OWNER_ID,
    (
        f"<i>ID:</i> {user.id}  |  "
        f"<i>Username:</i> @{user.username}  |  "
        f"<i>Имя:</i> {user.first_name}"
    ),
    parse_mode="HTML"
    )

    confirm = bot.send_message(
        message.chat.id,
        "✅ Сообщение успешно отправлено"
    )

    delete_after(
        message.chat.id,
        confirm.message_id
    )

bot.infinity_polling()
