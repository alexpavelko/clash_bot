from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup

roles = {
    "leader": "глава",
    "co-leader": "соруководитель",
    "elder": "старейшина",
    "member": "участник",
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

kb_menu = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = InlineKeyboardButton('📝')
b2 = InlineKeyboardButton('👨‍💼')
b3 = InlineKeyboardButton('👑')
b4 = InlineKeyboardButton('⚔')
kb_menu.add(b1, b2).add(b3, b4)

panic_message = "Обнаружен нарушитель🥷! ВИУ-ВИУ-ВИУ🚨.\n\n" \
                "Чтобы стать порядочным гражданином чата 🙎‍♂, нажми 📝 на клавиатуре снизу и нажми на свой ник."