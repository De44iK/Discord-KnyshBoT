# KnyshBoT Discord Project by @De44iK aka Denys Podolkhov
# Feel free to copy, use and modify this code
# Version: BotOS 0.78 Big AF Update

from secret import BOT_TOKEN_RELEASE, BOT_TOKEN_TESTING, WEATHER_API_KEY
from config import BOT_PREFIX, BOT_MODE
from discord.ui import Button, View
from discord import Embed, Color
from discord.ext import commands
from datetime import datetime
from typing import List
import contextlib
import traceback
import requests
import datetime
import discord
import asyncio
import qrcode
import random
import time
import json
import os
import io

stop_deletion = False
# Load music configuration from JSON file
def load_music_config():
    try:
        with open('music_config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Save music configuration to JSON file
def save_music_config(config):
    with open('music_config.json', 'w') as f:
        json.dump(config, f, indent=4)




# Load configuration from JSON file
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Save configuration to JSON file
def save_config(config):
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_message(message):
    if message.content.startswith('s!play'):
        play_messages = load_music_config()

        play_messages.append({"content": message.content, "timestamp": str(datetime.utcnow())})
        play_messages = play_messages[-20:]  # Limit to 20 items

        save_music_config(play_messages)

    await bot.process_commands(message)  # Process other commands

@bot.command()
async def music(ctx):
    play_messages = load_music_config()

    if play_messages:
        embed = discord.Embed(title="Music Commands", color=0x00ff00)
        for idx, play_message in enumerate(play_messages, start=1):
            embed.add_field(name=f"Track {idx}", value=play_message["content"], inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("No music play messages found.")


# Define all the colors

cool_quotes = [
    {"quote": "Будущее принадлежит тем, кто верит в красоту своих мечтаний.", "author": "Элеонор Рузвельт"},
    {"quote": "В середине трудностей рождается возможность.", "author": "Альберт Эйнштейн"},
    {"quote": "Поверь, что ты можешь, и ты уже на полпути к цели.", "author": "Теодор Рузвельт"},
    {"quote": "Не смотри на часы; делай то, что они делают. Продолжай двигаться.", "author": "Сэм Левенсон"},
    {"quote": "Успех не является конечной точкой, неудача не смертельна: важно только смело продолжать.", "author": "Уинстон Черчилль"},
    {"quote": "Трудности часто готовят обычных людей к необычной судьбе.", "author": "Клайв С. Льюис"},
    {"quote": "Единственное ограничение для нашего завтрашнего успеха — это сомнения сегодняшнего дня.", "author": "Франклин Д. Рузвельт"},
    {"quote": "То, что ты получишь, достигнув своих целей, не так важно, как то, чем ты станешь, достигая своих целей.", "author": "Зиг Зиглар"},
    {"quote": "Верь в себя и во всё, что ты есть. Знай, внутри тебя есть что-то большее, чем любое препятствие.", "author": "Кристиан Д. Ларсон"},
    {"quote": "Успех — это не ключ к счастью. Счастье — это ключ к успеху. Если ты любишь то, что ты делаешь, ты будешь успешным.", "author": "Альберт Швейцер"},
    {"quote": "Единственный способ делать великую работу — это любить то, что ты делаешь.", "author": "Стив Джобс"},
    {"quote": "Дорога к успеху и дорога к неудаче почти идентичны.", "author": "Колин Р. Дэвис"},
    {"quote": "Успех обычно приходит к тем, кто слишком занят, чтобы искать его.", "author": "Генри Дэвид Торо"},
    {"quote": "Я замечаю, что чем усерднее я работаю, тем больше мне везет.", "author": "Томас Джефферсон"},
    {"quote": "Секрет достижения — начать.", "author": "Марк Твен"},
    {"quote": "Единственное место, где успех идет перед трудом, это словарь.", "author": "Видал Сассун"},
    {"quote": "Успех — это хождение от неудачи к неудаче, не потеряв энтузиазма.", "author": "Уинстон Черчилль"},
    {"quote": "Успех — это не только заработать деньги. Это оказать влияние.", "author": "Неизвестный"},
    {"quote": "Успех — это не результат спонтанного горения. Ты должен поджечь себя сам.", "author": "Арнольд Х. Гласоу"},
    {"quote": "Единственное, что стоит между вами и вашей мечтой, это желание попробовать и вера в то, что это действительно возможно.", "author": "Джоэл Браун"},
    {"quote": "Ваше время ограничено, не тратьте его на жизнь другого человека.", "author": "Стив Джобс"},
    {"quote": "Не давайте страхам в вашем разуме управлять вами. Пусть вами руководят мечты в вашем сердце.", "author": "Рой Т. Беннетт"},
]
cool_quotes_en = [
    {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"quote": "In the middle of difficulties lies opportunity.", "author": "Albert Einstein"},
    {"quote": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
    {"quote": "Don't watch the clock; do what it does. Keep going.", "author": "Sam Levenson"},
    {"quote": "Success is not final, failure is not fatal: It is the courage to continue that counts.", "author": "Winston Churchill"},
    {"quote": "Hardships often prepare ordinary people for an extraordinary destiny.", "author": "C.S. Lewis"},
    {"quote": "The only limit to our realization of tomorrow will be our doubts of today.", "author": "Franklin D. Roosevelt"},
    {"quote": "What you get by achieving your goals is not as important as what you become by achieving your goals.", "author": "Zig Ziglar"},
    {"quote": "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.", "author": "Christian D. Larson"},
    {"quote": "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful.", "author": "Albert Schweitzer"},
    {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"quote": "The road to success and the road to failure are almost exactly the same.", "author": "Colin R. Davis"},
    {"quote": "Success usually comes to those who are too busy to be looking for it.", "author": "Henry David Thoreau"},
    {"quote": "I find that the harder I work, the more luck I seem to have.", "author": "Thomas Jefferson"},
    {"quote": "The secret to getting ahead is getting started.", "author": "Mark Twain"},
    {"quote": "The only place where success comes before work is in the dictionary.", "author": "Vidal Sassoon"},
    {"quote": "Success is walking from failure to failure with no loss of enthusiasm.", "author": "Winston Churchill"},
    {"quote": "Success is not only about making money. It's about making a difference.", "author": "Unknown"},
    {"quote": "Success is not the result of spontaneous combustion. You must set yourself on fire.", "author": "Arnold H. Glasow"},
    {"quote": "The only thing standing between you and your dream is the will to try and the belief that it is actually possible.", "author": "Joel Brown"},
    {"quote": "Your time is limited, don't waste it living someone else's life.", "author": "Steve Jobs"},
    {"quote": "Don't let the fear of what could happen make nothing happen.", "author": "Roy T. Bennett"},
]


DEFAULT = Color.default()
TEAL = Color.teal()
DARK_TEAL = Color.dark_teal()
GREEN = Color.green()
DARK_GREEN = Color.dark_green()
BLUE = Color.blue()
DARK_BLUE = Color.dark_blue()
PURPLE = Color.purple()
DARK_PURPLE = Color.dark_purple()
MAGENTA = Color.magenta()
DARK_MAGENTA = Color.dark_magenta()
GOLD = Color.gold()
DARK_GOLD = Color.dark_gold()
ORANGE = Color.orange()
DARK_ORANGE = Color.dark_orange()
RED = Color.red()
DARK_RED = Color.dark_red()
LIGHTER_GREY = Color.lighter_grey()
LIGHT_GREY = Color.light_grey()
DARK_GREY = Color.dark_grey()
DARKER_GREY = Color.darker_grey()
BLURPLE = Color.blurple()
GREYPLE = Color.greyple()

color_list = [
    DEFAULT,
    TEAL,
    DARK_TEAL,
    GREEN,
    DARK_GREEN,
    BLUE,
    DARK_BLUE,
    PURPLE,
    DARK_PURPLE,
    MAGENTA,
    DARK_MAGENTA,
    GOLD,
    DARK_GOLD,
    ORANGE,
    DARK_ORANGE,
    RED,
    DARK_RED,
    LIGHTER_GREY,
    LIGHT_GREY,
    DARK_GREY,
    DARKER_GREY,
    BLURPLE,
    GREYPLE,
]

en_users = []
ru_users = []


@bot.command()
async def cmds(ctx):
    await help_embed(ctx)


async def help_embed(ctx):
    embed = Embed(title="Команды/Помощь", description="Используйте реакции снизу для навигации по списку", color=0x00ff00)
    message = await ctx.send(embed=embed)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")


    @bot.event
    async def on_reaction_add(reaction, user):
        if user == bot.user:
            return
        if reaction.emoji == "1️⃣":
            embed = discord.Embed(title="1️⃣Команды", description="**Инструменты и функции**", color=0x00ff00)
            embed.add_field(name="--> /menu", value="💬 **Открыть стартовое меню**", inline=False)
            embed.add_field(name="--> /cmds", value="🧾 **Открыть этот список команд в обход меню**", inline=False)
            embed.add_field(name="--> /ping", value="🌐 **Проверить скорость соединения с ботом**", inline=False)
            embed.add_field(name="--> /test", value="🟢 **Проверить онлайн ли бот**", inline=False)
            embed.add_field(name="--> /qr", value="🔳 **Создать qr-код с любой информацией**\nИспользование: /qr www.example.com", inline=False)
            embed.add_field(name="--> /code", value="💻 **Запустить код на Python прямо в чате**", inline=False)
            embed.add_field(name="--> /advt", value="❗ **Создать объявление в канале сервера**\nИспользование: /advt [Содержание обьявления]", inline=False)
            embed.add_field(name="--> /test", value="🟢 **Проверить онлайн ли бот**", inline=False)
            embed.add_field(name="--> /cls", value="**🗑️ Очистить чат**\nИспользование: /cls [кол-во сообщений для удаления]\nВведите /cls all что бы очистить весь чат\n\"/stop\" останавливает удаление сообщений", inline=False)
            embed.add_field(name="--> /pic", value="**🖼️ Прислать аватар пользователя с ссылкой на скачивание**\nИспользование: /pic @пользователь", inline=False)
            
            await reaction.message.edit(embed=embed)
        elif reaction.emoji == "2️⃣":
            embed = discord.Embed(title="2️⃣Команды", description="Игры и развлечения", color=0x00ff00)
            embed.add_field(name="--> /tic", value="Начать игру в крестики-нолики", inline=False)
            embed.add_field(name="--> /num", value="Игра: Угадай число", inline=False)
            embed.add_field(name="Page 3", value="Help page 3", inline=False)
            await reaction.message.edit(embed=embed)
        elif reaction.emoji == "3️⃣":
            embed = discord.Embed(title="3️⃣Команды", description="Прочее", color=0x00ff00)
            embed.add_field(name="--> /lang", value="**🅰️ Сменить язык бота для пользователя**\nИспользование: /pic @пользователь", inline=False)
            embed.add_field(name="--> /music", value="🎵 **Показать историю проигранной музыки**", inline=False)
            embed.add_field(name="Page 3", value="Help page 3", inline=False)
            await reaction.message.edit(embed=embed)
        try:
            await reaction.remove(user)
        except Exception as e:
            pass


@bot.command()
async def test(ctx):
    try:
        user_config = load_config()
        user_id = str(ctx.author.id)
        if str(ctx.author.id) not in user_config:
                user_config[str(ctx.author.id)] = "ru"
                save_config(user_config)
        if user_config[user_id] == "ru":
            testPhrases = [
                f"Я живой не парься, {ctx.author.mention}",
                "я тут",
                "шо надо",
                "я слушаю",
                "о да, админ в чате",
            ]
            await ctx.send(random.choice(testPhrases))
        elif user_config[user_id] == "en":
            testPhrases = [
                f"I am alive, {ctx.author.mention}",
                "bro, I am here, why?",
                "what do you need, my man?",
                "How can I assist you today?",
                "Oh yes, admin is in the chat",
            ]
            await ctx.send(random.choice(testPhrases))
        
    except Exception as e:
        print(e)


@bot.command()
async def code(ctx):
    user_config = load_config()
    user_id = str(ctx.author.id)
    if str(ctx.author.id) not in user_config:
            user_config[str(ctx.author.id)] = "ru"
            save_config(user_config)
    def create_error_embed(error_message):
        if user_config[user_id] == "ru":
            label = "Возникла Ошибка"
        else:
            label = "Error Occured"
        embed = discord.Embed(
            title=label, description=error_message, color=discord.Color.red()
        )
        return embed


    if user_config[user_id] == "ru":
        label = "Пишите свой код здесь и отправтье для отладки"
    else:
        label = "Write your code and send it for debugging."

    await ctx.send(label)

    def check(msg):
        return msg.author == ctx.author and msg.content != "/code"

    code_msg = await bot.wait_for("message", check=check)

    # Create an environment to capture stdout
    old_stdout = io.StringIO()
    new_stdout = io.StringIO()
    code = code_msg.content

    try:
        with contextlib.redirect_stdout(new_stdout):
            exec(code)

        stdout_value = new_stdout.getvalue()
        if stdout_value:
            await ctx.send(stdout_value)
    except Exception as e:
        traceback_msg = traceback.format_exception(type(e), e, e.__traceback__)
        traceback_str = "".join(traceback_msg)

        # Create and send the error embed
        error_embed = create_error_embed(f"\n```\n{traceback_str}\n```")
        await ctx.send(embed=error_embed)


@bot.command()
async def ping(ctx):
    user_config = load_config()
    user_id = str(ctx.author.id)
    if str(ctx.author.id) not in user_config:
            user_config[str(ctx.author.id)] = "ru"
            save_config(user_config)
    # Record the time when the user's message was received
    start_time = time.time()

    # Send a temporary message to calculate round-trip time
    if user_config[user_id] == "ru":
        label = "Вычисляем пинг..."
    else: 
        label = "Calculating Ping.."
    temp_message = await ctx.send(label)

    # Calculate round-trip time (time taken from sending to receiving the temporary message)
    round_trip_time = round((time.time() - start_time) * 1000)
    img = "🟢"
    if round_trip_time > 240:
        img = "🟡"
    if round_trip_time > 300:
        img = "🔴"
    # Edit the temporary message to display ping results
    if user_config[user_id] == "ru":
        label = "Пинг бота: "
    else:
        label = "Bot latency is:"
    await temp_message.edit(content=f"{img} {label} {round_trip_time}ms")


@bot.command()
async def advt(ctx: commands.Context, *, args):
    try:
        result = str(args)
        channel = ctx.channel
        user_config = load_config()
        user_id = str(ctx.author.id)
        if str(ctx.author.id) not in user_config:
                user_config[str(ctx.author.id)] = "ru"
                save_config(user_config)
        await ctx.message.delete()
        if user_config[user_id] == "ru":
            phrases = ["Объявление от: ", "С любовью, ваш ", "Это написал ", "Вас уведомляет ", "Пишет админчик "]
        else: 
            phrases = ["An advertisement from: ", "With love, your: ", "This was written by: ", "You are being notified by: ", "Written by admin "]
        await ctx.send(
            embed=discord.Embed(
                title=f"{result}",
                description= random.choice(phrases)+f"{ctx.author.name}",
                color=random.choice(color_list)
            )
        )
    except Exception as e:
        if user_config[user_id] == "ru":
            title = "Ошибка"
            desc = "Объявления доступны только для каналов на серверах"
        else:
            title="Error"
            desc ="Advertisements are available only for channels on servers."

        embed = discord.Embed(
            title=title,
            description=desc,
            color=RED,
        )
        await ctx.send(embed=embed)

@bot.command()
async def qr(ctx, *, args):
    data = str(args).replace(" ", "_")

    # Generate the QR code image
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create a discord.File object from the QR code image
    qr_image = qr.make_image(fill_color="black", back_color="white")
    qr_filename = "qr_code.png"
    qr_image.save(qr_filename)
    qr_file = discord.File(qr_filename)

    # Send the QR code image as a message
    await ctx.send(file=qr_file)

    # Delete the temporary QR code image file
    qr_image.close()
    os.remove(qr_filename)


@qr.error
async def make_qr_code_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        user_config = load_config()
        user_id = str(ctx.author.id)
        if str(ctx.author.id) not in user_config:
                user_config[str(ctx.author.id)] = "ru"
                save_config(user_config)
        if user_config[user_id] == "ru":
            title = "Ошибка"
            description='Пожалуйста, предоставтье значение для qr-кода после команды.\nПример: "/qr www.example.com"'
        else:
            title="Error"
            description = 'Make sure you provided required data for a qr-code\nUsage: /qr www.example.com'
            
        embed = discord.Embed(
            title=title,
            description=description,
            color=0xFC2403,
        )
        await ctx.send(embed=embed)


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y
        

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: discord.Interaction):

        # user_config = load_config()
        # user_id = str(ctx.author.id)
        # if str(ctx.author.id) not in user_config:
        #         user_config[str(ctx.author.id)] = "ru"
        #         save_config(user_config)
        # if user_config[user_id] == "ru":
        #     contextX = "Ходит X"
        #     contextO = "Ходит O"
        #     contextWinX = 'Победил "X"'
        #     contextWinO = 'Победил "O"'
        #     contextDraw = 'Ничья!'
        # else:
        #     contextX='Plays X'
        #     contextO ='Plays O'
        #     contextWinX ="Won by \"X\""
        #     contextWinO ="Won by \"O\""
        #     contextDraw = 'It\'s draw!'
        
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = ""
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = ""

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = ""
            elif winner == view.O:
                content = ""
            else:
                content = ""

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(discord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

@bot.command(name="w")
async def weather(ctx, *, city_name):

    def get_weather_data(city):
    # Make API request to OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        return response.json()
    
    def translate_weather(value):
        user_config = load_config()
        user_id = str(ctx.author.id)
        if str(ctx.author.id) not in user_config:
                user_config[str(ctx.author.id)] = "ru"
                save_config(user_config)
        if user_config[user_id] == "ru":
            match value:
                case "clear sky":
                    a = "Ясно ☀️"
                case "few clouds":
                    a = "Немного облачно 🌤"
                case "scattered clouds":
                    a = "Рассеянные облака ☁️"
                case "broken clouds":
                    a = "Облачно с прояснениями ☁️"
                case "overcast clouds":
                    a = "Пасмурно ☁️"
                case "mist":
                    a = "Туман 🌫️"
                case "fog":
                    a = "Туман 🌫️"
                case "haze":
                    a = "Мгла 🌫️"
                case "smoke":
                    a = "Дымка 🔥"
                case "dust":
                    a = "Пыль 💨"
                case "sand":
                    a = "Песчаная буря 🌪️"
                case "ash":
                    a = "Пепел ☠️"
                case "squalls":
                    a = "Шквалы 💨"
                case "tornado":
                    a = "Торнадо 🌪️"
                case "tropical storm":
                    a = "Тропический шторм 🌀"
                case "hurricane":
                    a = "Ураган 🌀"
                case "light rain":
                    a = "Легкий дождь 🌧️"
                case "moderate rain":
                    a = "Умеренный дождь 🌧️"
                case "heavy rain":
                    a = "Сильный дождь 🌧️"
                case "shower rain":
                    a = "Ливневый дождь 🌧️"
                case "light snow":
                    a = "Легкий снег 🌨️"
                case "moderate snow":
                    a = "Умеренный снег 🌨️"
                case "heavy snow":
                    a = "Сильный снег 🌨️"
                case "sleet":
                    a = "Дождь со снегом 🌨️"
                case "shower sleet":
                    a = "Ливневый дождь со снегом 🌨️"
                case "light rain and snow":
                    a = "Легкий дождь и снег 🌧️❄️"
                case "moderate rain and snow":
                    a = "Умеренный дождь и снег 🌧️❄️"
                case "light shower snow":
                    a = "Легкий ливневый снег 🌨️"
                case "thunderstorm with light rain":
                    a = "Гроза с небольшим дождем ⛈️🌧️"
                case "thunderstorm with rain":
                    a = "Гроза с дождем ⛈️🌧️"
                case "thunderstorm with heavy rain":
                    a = "Гроза с сильным дождем ⛈️🌧️"
                case "light thunderstorm":
                    a = "Легкая гроза ⛈️"
                case "moderate thunderstorm":
                    a = "Умеренная гроза ⛈️"
                case "heavy thunderstorm":
                    a = "Сильная гроза ⛈️"
                case "ragged thunderstorm":
                    a = "Неровная гроза ⛈️"
                case "thunderstorm with light drizzle":
                    a = "Гроза с моросящим дождем и молниями ⛈️🌧️"
                case "thunderstorm with drizzle":
                    a = "Гроза с моросящим дождем ⛈️🌧️"
                case "thunderstorm with heavy drizzle":
                    a = "Гроза с сильным моросящим дождем ⛈️🌧️"
                case _:
                    a = "Неизвестно ❓"
        else:
            match value:
                case "clear sky":
                    a = "Clear sky ☀️"
                case "few clouds":
                    a = "Few clouds 🌤️"
                case "scattered clouds":
                    a = "Scattered clouds ☁️"
                case "broken clouds":
                    a = "Broken clouds ☁️"
                case "overcast clouds":
                    a = "Overcast clouds ☁️"
                case "mist":
                    a = "Mist 🌫️"
                case "fog":
                    a = "Fog 🌫️"
                case "haze":
                    a = "Haze 🌫️"
                case "smoke":
                    a = "Smoke 🔥"
                case "dust":
                    a = "Dust 💨"
                case "sand":
                    a = "Sandstorm 🌪️"
                case "ash":
                    a = "Ash ☠️"
                case "squalls":
                    a = "Squalls 💨"
                case "tornado":
                    a = "Tornado 🌪️"
                case "tropical storm":
                    a = "Tropical storm 🌀"
                case "hurricane":
                    a = "Hurricane 🌀"
                case "light rain":
                    a = "Light rain 🌧️"
                case "moderate rain":
                    a = "Moderate rain 🌧️"
                case "heavy rain":
                    a = "Heavy rain 🌧️"
                case "shower rain":
                    a = "Shower rain 🌧️"
                case "light snow":
                    a = "Light snow 🌨️"
                case "moderate snow":
                    a = "Moderate snow 🌨️"
                case "heavy snow":
                    a = "Heavy snow 🌨️"
                case "sleet":
                    a = "Sleet 🌨️"
                case "shower sleet":
                    a = "Shower sleet 🌨️"
                case "light rain and snow":
                    a = "Light rain and snow 🌧️❄️"
                case "moderate rain and snow":
                    a = "Moderate rain and snow 🌧️❄️"
                case "light shower snow":
                    a = "Light shower snow 🌨️"
                case "thunderstorm with light rain":
                    a = "Thunderstorm with light rain ⛈️🌧️"
                case "thunderstorm with rain":
                    a = "Thunderstorm with rain ⛈️🌧️"
                case "thunderstorm with heavy rain":
                    a = "Thunderstorm with heavy rain ⛈️🌧️"
                case "light thunderstorm":
                    a = "Light thunderstorm ⛈️"
                case "moderate thunderstorm":
                    a = "Moderate thunderstorm ⛈️"
                case "heavy thunderstorm":
                    a = "Heavy thunderstorm ⛈️"
                case "ragged thunderstorm":
                    a = "Ragged thunderstorm ⛈️"
                case "thunderstorm with light drizzle":
                    a = "Thunderstorm with light drizzle ⛈️🌧️"
                case "thunderstorm with drizzle":
                    a = "Thunderstorm with drizzle ⛈️🌧️"
                case "thunderstorm with heavy drizzle":
                    a = "Thunderstorm with heavy drizzle ⛈️🌧️"
                case _:
                    a = "Unknown ❓"
        return a

    def create_weather_embed(data):
    # Create and return a Discord embed for weather data
        embed = discord.Embed(
            title=f"Погода в городе: {data['name']}",
            description=translate_weather(data["weather"][0]["description"]),
            color=0x3498DB,
        )
        embed.add_field(name="Температура", value=f"{data['main']['temp']}°C")
        embed.add_field(name="Влажность", value=f"{data['main']['humidity']}%")
        embed.add_field(name="Скорость ветра", value=f"{data['wind']['speed']} m/s")
        return embed

    def create_more_info_embed(data):
        # Create and return a Discord embed with more info

        embed = discord.Embed(
            title=f"Больше информации о погоде в: {data['name']}",
            description=translate_weather(data["weather"][0]["description"]),
            color=0x3498DB,
        )

        embed.add_field(name="Температура", value=f"{data['main']['temp']}°C")
        embed.add_field(name="Влажность", value=f"{data['main']['humidity']}%")
        embed.add_field(name="Скорость ветра", value=f"{data['wind']['speed']} m/s")
        embed.add_field(name="Давление", value=f"{data['main']['pressure']} hPa")

        return embed


    try:
        weather_data = get_weather_data(city_name)
        embed = create_weather_embed(weather_data)
        message = await ctx.send(embed=embed)

        async def more_info_callback(interaction, message=message):
            more_info_embed = create_more_info_embed(weather_data)
            await message.edit(embed=more_info_embed, view=None)

        more_info_button = Button(label="More Info", style=discord.ButtonStyle.green)
        more_info_button.callback = more_info_callback

        view = View()
        view.add_item(more_info_button)

        await message.edit(view=view)

        def check(interaction):
            return interaction.message.id == message.id

        try:
            interaction = await bot.wait_for("button_click", check=check, timeout=3600)
            await more_info_callback(interaction)
        except asyncio.TimeoutError:
            view.clear_items()
            await message.edit(view=view)

    except discord.Forbidden:
        await ctx.send(
            "Я не могу отправить вам приватное сообщение. Поалуйста, разрешите мне писать вам."
        )


@bot.command()
async def menu(ctx):
    button1 = Button(label="Инфо", style=discord.ButtonStyle.green)
    button2 = Button(label="Команды", style=discord.ButtonStyle.green)
    button3 = Button(label="Статистика", style=discord.ButtonStyle.green)

    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)

    message = await ctx.send("Меню KnyshBoT: \nВыберите один из пунктов: ", view=view)

    async def button1_callback(interaction):
        await interaction.response.edit_message(content="ㅤ", view=None)
        await message.delete()  # Delete the menu message
        library_version = discord.__version__
        # Send an embed
        embed = discord.Embed(
            title="Информация о KnyshBot",
            description="© 2023 D44K Local Software Corp",
            color=discord.Color.green(),
        )
        embed.add_field(name="BotOS Version", value="**ver. 0.33** Safety Features Silent Update", inline=False)
        embed.add_field(name="GitHub Repository", value="https://github.com/De44iK/Discord-KnyshBoT")
        embed.add_field(name='Discord.Py Library Version', value=library_version, inline=False)
        await ctx.send(embed=embed)

    async def button2_callback(interaction):
        await interaction.response.edit_message(content="ㅤ", view=None)
        await message.delete()  # Delete the menu message

        await help_embed(ctx)

    async def button3_callback(interaction):
        try:
            await interaction.response.edit_message(content="ㅤ", view=None)
            await message.delete()  # Delete the menu message
            server_count = len(bot.guilds)
            user_count = sum(guild.member_count for guild in bot.guilds)
            now = datetime.datetime.now(datetime.timezone.utc)
            uptime = now - bot.user.created_at
            

            days = uptime.days
            # Send an embed
            embed = discord.Embed(
                title="📈 Статистика KnyshBoT",
                description="Вот некоторые показатели прогресса: ",
                color=discord.Color.green(),
            )
            embed.add_field(name=f'🌐 Кол-во Серверов с этим ботом: {server_count}', value='', inline=False)
            embed.add_field(name=f'👤 Всего пользователей бота: {user_count}', value='', inline=False)
            embed.add_field(name= f"🌈 Цветов для обьявлений: {len(color_list)}",value='', inline=False)
            embed.add_field(name=f'📆 Бот существует уже: {str(days)} д.', value='', inline=False)
            embed.add_field(name= f"💻 Количество Команд: {len(bot.commands)}", value='', inline=False)
            
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    button1.callback = button1_callback
    button2.callback = button2_callback
    button3.callback = button3_callback


@bot.command()
async def cls(ctx, limit):
    try:
        # Fetch the channel to clear messages from
        channel = ctx.channel
        global stop_deletion
        stop_deletion = False  # Flag to stop message deletion
        messages_deleted = 0
        if limit.lower() == "all":
            await ctx.send("Are you sure you want to delete all messages in this channel? (yes/no)")

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() in ["yes", "no", "/stop"]

            response = await bot.wait_for("message", check=check)

            if response.content.lower() == "yes":
                
                async for message in channel.history():
                    
                    if stop_deletion:
                        break
                    await message.delete()
                    messages_deleted += 1
                await ctx.send(f"Channel cleared. Deleted {messages_deleted} messages.")
            elif response.content.lower() == "/stop":
                await ctx.send("Channel clearing canceled.")
                stop_deletion = True
            else:
                await ctx.send("Channel clearing canceled.")

        else:
            lim = int(limit)
            async for message in channel.history():
                    
                if stop_deletion or lim < 0:
                    break
                await message.delete()
                lim -= 1
                messages_deleted += 1
            await ctx.send(f"Channel cleared. Deleted {messages_deleted -1 } messages.")

    except Exception as e:
        print(e)


@bot.command()
async def stop(ctx):
    global stop_deletion
    stop_deletion = True
    await ctx.send("Message deletion has been stopped.")


@bot.command()
async def tic(ctx: commands.Context):
    """Starts a tic-tac-toe game with yourself."""
    await ctx.send(content="", view=TicTacToe())


@bot.command()
async def num(ctx):

    target_number = random.randint(1, 50)
    remaining_tries = 7
    embed = discord.Embed(
            title="Игра: Угадай Число",
            description="Загадано число от 1 до 50. Напиши свое предположение в чат\nДано 6 попыток",
            color=BLUE
        )
    await ctx.send(embed=embed)
    while remaining_tries > 0:
        try:
            message = await bot.wait_for("message", timeout=30, check=lambda m: m.author == ctx.author)
            guess = int(message.content)

            if guess <= 1 or guess >= 50:
                embed = discord.Embed(
                    title="🟥 Ошибка",
                    description="Значение находится в рамках от 1 до 50.\nПопытка не засчитана, попробуйте опять",
                    color=RED
                )

            if guess < target_number:
                embed = discord.Embed(
                    title="⬆️ Больше!",
                    description="Загаданный случайный номер больше {}.".format(guess),
                    color=ORANGE
                )
                await ctx.send(embed=embed)
            elif guess > target_number:
                embed = discord.Embed(
                    title="⬇️ Меньше!",
                    description="Загаданный случайный номер меньше {}.".format(guess),
                    color=BLURPLE
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="✅ Победа!",
                    description="Загаданный номер: {}.".format(guess) + f"\n Попыток оставалось: {remaining_tries}",
                    color=GREEN
                )
                await ctx.send(embed=embed)
                break

            remaining_tries -= 1

        except ValueError:
            embed = discord.Embed(
                    title="🟥 Ошибка",
                    description="Введенное значение не является номером.\nОстанавливаем игру...",
                    color=RED
                )
            await ctx.send(embed=embed)
            break
        except asyncio.TimeoutError:
            embed = discord.Embed(
                    title="🟥 Ошибка",
                    description="🕑 Время на попытку вышло\nОстанавливаем игру...",
                    color=RED
                )
            await ctx.send(embed=embed)
            break
    if remaining_tries == 0:
        embed = discord.Embed(
                        title="😥 Поражение",
                        description="Количество попыток закончилось...",
                        color=RED
                    )
        embed.add_field(name=f"Загаданное число: {target_number}", value="")
        await ctx.send(embed=embed)

@bot.command()
async def quote(ctx):
    try:
        user_config = load_config()
        user_id = str(ctx.author.id)
        if str(ctx.author.id) not in user_config:
                user_config[str(ctx.author.id)] = "ru"
                save_config(user_config)
        try:
            await ctx.message.delete()
        except:
            pass
        
        user = ctx.message.author
        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        if user_config[user_id] == "ru":
            label = "Запрошено пользователем: "
            random_quote = random.choice(cool_quotes)
            author = random_quote["author"]
            quote = random_quote["quote"]
            requester = ctx.author.display_name


            embed = discord.Embed(title=quote, description=f"- {author}", color=GREEN)
        else:
            label = "Requested by: "
            random_quote = random.choice(cool_quotes_en)
            author = random_quote["author"]
            quote = random_quote["quote"]
            requester = ctx.author.display_name


            embed = discord.Embed(title=quote, description=f"- {author}", color=GREEN)
        embed.set_footer(text=f"{label} {requester}", icon_url=avatar_url)
        embed.set_thumbnail(url="https://memepedia.ru/wp-content/uploads/2022/10/mudroe-tainstvennoe-derevo-mem-25.jpg")

        await ctx.send(embed=embed)
    except Exception as e:
        print(e)
        
@bot.command()
async def pic(ctx, member: discord.Member = None):
    try:
        user_config = load_config()
        user_id = str(ctx.author.id)
        if str(ctx.author.id) not in user_config:
                user_config[str(ctx.author.id)] = "ru"
                save_config(user_config)
        if member is None:
            member = ctx.author
            
        avatar_url = member.avatar.url
        png_link = f"[PNG]({avatar_url})"
        jpg_link = f"[JPG]({avatar_url.replace('.png', '.jpg')})"
        webp_link = f"[WebP]({avatar_url.replace('.png', '.webp')})"
        if user_config[user_id] == "ru":
            label = "Аватарка пользователя: "
            dwn = "Скачать в форматах:"
        else:
            label = 'Avatar of the User: '
            dwn = "Download formats:"
        embed = discord.Embed(title=f"{label} {member.display_name}")
        embed.set_image(url=avatar_url)
        embed.description = f"{dwn} \n{png_link} | {jpg_link} | {webp_link}"
        
        await ctx.send(embed=embed)
    except Exception as e:
        print(e)


@bot.command()
async def lang(ctx, selected_language):
    try:
        selected_language = selected_language.lower()

        if selected_language == "en":
            user_config = load_config()
            
            user_config[str(ctx.author.id)] = "en"
            save_config(user_config)
            await ctx.send(f'{ctx.author.display_name}, Your bot response language in now US English💥 🦅 🇺🇸 🦅 🇺🇸')
        
        elif selected_language == "ru":
            user_config = load_config()
            
            user_config[str(ctx.author.id)] = "ru"
            save_config(user_config)
            await ctx.send(f'{ctx.author.display_name}, Ответы вашего бота теперь будут на русском')
        
        else:
            await ctx.send('Invalid language choice.')
    except Exception as e:
        print(e)


# @bot.command()
# async def vote(ctx, *, vote_input):
#     try:
#         vote_parts = vote_input.split("&")
#         if len(vote_parts) < 3:
#             await ctx.send("Usage: `/vote Topic & Option1 & Option2 & Option3 ...`")
#             return

#         topic = vote_parts[0].strip()
#         options = [option.strip() for option in vote_parts[1:]]


#         embed = discord.Embed(title=f"🗳️ Vote: {topic}", color=0x3498db)
#         for idx, option in enumerate(options, start=1):
#             embed.add_field(name=f"Option {idx}", value=option, inline=False)
#         user = ctx.message.author
#         avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
#         embed.set_footer(text=f"Vote initiated by {ctx.author.display_name}", icon_url=avatar_url)

#         message = await ctx.send(embed=embed)

#         for idx in range(len(options)):
#             await message.add_reaction(f"{idx + 1}\N{COMBINING ENCLOSING KEYCAP}")
#     except Exception as e:
#         print(e)


@bot.event
async def on_ready():
    print("\033[1;32;40m"+f"Logged in SUCESSFULLY as {bot.user.name}#{bot.user.discriminator}" + "\033[0m")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="/menu | Ver. 0.78 AF",
        )
    )

def decrypt(encrypted_text, shift):
    decrypted_text = ""
    for char in encrypted_text:
        if char.isalpha():
            is_upper = char.isupper()
            shifted_char = chr(((ord(char) - ord('A' if is_upper else 'a') - shift) % 26) + ord('A' if is_upper else 'a'))
            decrypted_text += shifted_char
        else:
            decrypted_text += char
    return decrypted_text

async def main():

    if BOT_MODE == 1:
        await bot.start(decrypt(BOT_TOKEN_RELEASE, 23))
    elif BOT_MODE == 0:
        await bot.start(decrypt(BOT_TOKEN_TESTING, 23))
    else:
        print(f"> ERROR!\nINCORRECT BOT MODE IS SELECTED: {BOT_MODE}")


if __name__ == "__main__":
    asyncio.run(main())


#damn this code became long asf