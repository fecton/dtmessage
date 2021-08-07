#!/usr/bin/python3
# -*- encoding: utf-8 -*-

__version__ = "1.0"

import webbrowser
import discord
import telebot

from tkinter import *
from tkinter import messagebox

try:
    with open("config", encoding="UTF-8") as config:
        data = {
            "TELEGRAM-TOKEN": "",
            "DISCORD-TOKEN": "",
            "TELEGRAM-CHANNEL": "",
            "DISCORD-CHANNEL": ""
        }

        for line in config.readlines():
            data[line[:line.find(":")]] = line[line.find(":") + 1:].strip("\n")
except FileNotFoundError:
    with open("config", "w", encoding="UTF-8") as config:
        config.write("""TELEGRAM-TOKEN:\nDISCORD-TOKEN:\nTELEGRAM-CHANNEL:\nDISCORD-CHANNEL:""")
    messagebox.showwarning(title="Конфиг", message="Заполните конфиг!")
    exit()


def empty_fields_are():
    count = 0
    for variable in [TELEGRAM_TOKEN, DISCORD_TOKEN, TELEGRAM_CHANNEL, DISCORD_CHANNEL]:
        if not variable:
            count += 1
    if count:
        messagebox.showerror(title="Пустой конфиг", message=f"{count} полей в конфиге пусты!")
        return False
    return True


def start_sending():
    # message = 1 (if checked)
    # announcement = 2 1 (if checked)
    # else = 0

    link_checked = is_message.get() + is_announcement.get()
    user_text = str(user_text_entry.get("1.0", END))

    if user_text.strip(" ").strip("\n"):
        if link_checked == 2:
            first_string = "🎮  "
            added_strings = """
            Twitch: https://www.twitch.tv/morrak_direnni
            YouTube: https://www.youtube.com/channel/UCcKlsRIryUaszsHgxhWtlzw
            GoodGame: https://goodgame.ru/channel/Morrak
            ВКонтакте: https://vk.com/public201736906
            """
            send_text = first_string + user_text + added_strings
        elif link_checked == 1:
            send_text = "Моррак вещает: " + user_text
        elif link_checked == 0:
            send_text = user_text
        else:
            messagebox.showwarning(title="Хм...", message="Чего-то слишком много, не так ли?")
            return

        telegram_bot = telebot.TeleBot(TELEGRAM_TOKEN)
        telegram_bot.send_message(TELEGRAM_CHANNEL, send_text)

        discord_bot = discord.Client()

        @discord_bot.event
        async def on_ready():
            channel = discord_bot.get_channel(DISCORD_CHANNEL)
            if channel is None:
                messagebox.showerror(title="Ошибка", message="Канал не найден!")
                return
            else:
                await channel.send(send_text)
                messagebox.showwarning(title="Успешно", message="Сообщение отправлено ботами!")
                await discord_bot.close()
        discord_bot.run(DISCORD_TOKEN)
        exit()
    else:
        messagebox.showerror(title="Ошибка", message="Пустые поля!")
        return


TELEGRAM_TOKEN = data["TELEGRAM-TOKEN"]
DISCORD_TOKEN = data["DISCORD-TOKEN"]

TELEGRAM_CHANNEL = int(data["TELEGRAM-CHANNEL"])
DISCORD_CHANNEL = int(data["DISCORD-CHANNEL"])

empty_fields_are()

window = Tk()
window.title("Message sender")
window.geometry("660x300")
window.resizable(False, False)

is_message = IntVar()
is_announcement = IntVar()

logo = PhotoImage(file='icon.png')
window.call('wm', 'iconphoto', window._w, logo)

window.configure(bg="#6cc6d3")

canvas = Canvas(window, bg="#3A7FF6", height=800, width=260, bd=0, highlightthickness=0, relief="ridge")
canvas.place(x=0, y=0)
canvas.create_rectangle(0, 0, 10, 10, fill="#0900ff", outline="")

canvas.create_oval(-50, -50, 200, 200, fill="#4989f7", outline="")
canvas.create_oval(90, 200, 290, 400, fill="#4989f7", outline="")
canvas.create_oval(20, 400, 170, 550, fill="#4989f7", outline="")

generate_btn_img = PhotoImage(file="github.png", height=50, width=50)
generate_btn = Button(image=generate_btn_img, borderwidth=0, highlightthickness=0,
                      command=lambda: webbrowser.open_new("https://github.com/Fecton"), relief="flat")
generate_btn.place(x=20, y=10, width=50, height=50)

title = Label(text="GitHub", bg="#4989f7", fg="white", font=("Arial-BoldMT", int(16.0)))
title.place(x=13, y=60)

user_text_entry = Text(bd=0, bg="#F6F7F9", highlightthickness=0, font=("Arial-BoldMT", int(12.0)))
user_text_entry.place(x=280, y=50, width=360, height=135)
user_text_entry.focus()

checkbox_is_message = Checkbutton(window, text="Сообщение", variable=is_message, onvalue=1, offvalue=0, height=3,
                                  width=10)
checkbox_is_message.place(x=155, y=55)

checkbox_is_announcement = Checkbutton(window, text="Анонс", variable=is_announcement, onvalue=2, offvalue=0, height=3,
                                       width=10)
checkbox_is_announcement.place(x=155, y=115)

generate_btn = Button(text="Отправить", borderwidth=0, highlightthickness=0, command=start_sending, relief="flat")
generate_btn.place(x=380, y=210, width=180, height=55)

window.mainloop()
