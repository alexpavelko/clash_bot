from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup

roles = {
    "leader": "глава",
    "co_leader": "соруководитель",
    "elder": "старейшина",
    "member": "участник",
}

roles_priority = {
    "leader": 1,
    "co-leader": 2,
    "elder": 3,
    "member": 4
}

shield_colors = {
    True: "✅",
    False: "❌"
}

war_result = {"tie": " ничья",
              "won": "победа!",
              "lost": "поражение",
              "winning": "побеждаем",
              "tied": "ничья",
              "losing": "поражение",
              "inWar": "определить не удалось",
              "warEnded": "определить не удалось"}

hello_message = "Привет, это clash of clans бот.Если ты не против, я буду напоминать тебе про атаки на кв. Если тебе это не надо - кинь меня в чс"

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
b1 = InlineKeyboardButton('📝')
b2 = InlineKeyboardButton('👨‍💼')
b3 = InlineKeyboardButton('👑')
kb_menu.add(b1, b2).add(b3)

panic_message = "Обнаружен нарушитель🥷! ВИУ-ВИУ-ВИУ🚨.\n\n" \
                "Чтобы стать порядочным гражданином чата 🙎‍♂, нажми 📝 на клавиатуре снизу и нажми на свой ник."
