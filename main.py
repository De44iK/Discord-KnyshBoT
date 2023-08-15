# KnyshBoT Discord Project by @De44iK aka Denys Podolkhov
# Feel free to copy, use and modify this code
# Version: BotOS 0.31.3 User Experience Update

from secret import BOT_TOKEN_RELEASE, BOT_TOKEN_TESTING, WEATHER_API_KEY
from config import BOT_PREFIX, BOT_MODE
from discord.ui import Button, View
from discord import Embed, Color
from discord.ext import commands
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


intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)

color_list = [
    Color.default(),
    Color.teal(),
    Color.dark_teal(),
    Color.green(),
    Color.dark_green(),
    Color.blue(),
    Color.dark_blue(),
    Color.purple(),
    Color.dark_purple(),
    Color.magenta(),
    Color.dark_magenta(),
    Color.gold(),
    Color.dark_gold(),
    Color.orange(),
    Color.dark_orange(),
    Color.red(),
    Color.dark_red(),
    Color.lighter_grey(),
    Color.light_grey(),
    Color.dark_grey(),
    Color.darker_grey(),
    Color.blurple(),
    Color.greyple(),
    Color.red() 
]

embedCMDS = Embed(
    title="Команды KnyshBoT",
    description="Вот список доступных команд: ",
    color=Color.blue(),  # Blue color for the embed
)
embedCMDS.add_field(name="/menu", value="💬 Открыть стартовое меню", inline=False)
embedCMDS.add_field(name="/test", value="🟢 Проверить онлайн ли бот", inline=False)
embedCMDS.add_field(name="/ping", value="🌐 Проверить скорость соединения с ботом", inline=False)
embedCMDS.add_field(name="/qr", value="🔳 Создать qr-код с любой информацией", inline=False)
embedCMDS.add_field(name="/code", value="💻 Запустить код на Python прямо в чате", inline=False)
embedCMDS.add_field(name="/cmds", value="🧾 Открыть список команд в обход меню", inline=False)
embedCMDS.add_field(name="/advt", value="❗ Создать объявление от имени Главного Бота", inline=False)
embedCMDS.add_field(name="/cls", value="🎵 Очистить чат (только для музыкального чата)", inline=False)
embedCMDS.add_field(name="/tic", value="⭕ Сыграть в Крестики-Нолики", inline=False)
embedCMDS.add_field(name="/w", value="🌥 Узнать погоду в любом городе", inline=False)


@bot.command()
async def cmds(ctx):
    await ctx.send(embed=embedCMDS)


@bot.command()
async def test(ctx):
    testPhrases = [
        f"Я живой не парься, {ctx.author.mention}",
        "я тут",
        "шо надо",
        "я слушаю",
        "о да, админ в чате",
    ]
    await ctx.send(random.choice(testPhrases))


def create_error_embed(error_message):
    embed = discord.Embed(
        title="Error", description=error_message, color=discord.Color.red()
    )
    return embed


# Command: Run Python code
@bot.command()
async def code(ctx):
    await ctx.send("Write your code here and send to debug")

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
    # Calculate the bot's latency
    bot_latency = round(bot.latency * 1000)  # Convert to milliseconds

    # Record the time when the user's message was received
    start_time = time.time()

    # Send a temporary message to calculate round-trip time
    temp_message = await ctx.send("Calculating ping...")

    # Calculate round-trip time (time taken from sending to receiving the temporary message)
    round_trip_time = round((time.time() - start_time) * 1000)
    img = "🟢"
    if round_trip_time > 240:
        img = "🟡"
    if round_trip_time > 300:
        img = "🔴"
    # Edit the temporary message to display ping results
    await temp_message.edit(content=f"{img} Ping is: {round_trip_time}ms")


@bot.command()
async def advt(ctx: commands.Context, *, args):
    try:
        result = str(args)
        channel = ctx.channel

        async for message in channel.history(limit=1):
            await message.delete()
        phrases = ["Объявление от: ", "С любовью, ваш ", "Это написал ", "Вас уведомляет ", "Пишет админчик "]
        await ctx.send(
            embed=discord.Embed(
                title=f"{result}",
                description= random.choice(phrases)+f"{ctx.author.name}",
                color=random.choice(color_list)
            )
        )
    except Exception:
        embed = discord.Embed(
            title="Ошибка",
            description='Обьявления доступны только для каналов на серверах',
            color=0xFC2403,
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
        embed = discord.Embed(
            title="Ошибка",
            description='Пожалуйста, предоставтье значение для qr-кода после команды.\nПример: "/qr www.example.com"',
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
            content = "Ходит чел с О:"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "Ходит чел с Х:"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "Победил Х!"
            elif winner == view.O:
                content = "Победил чел с О!"
            else:
                content = "Ничья, победила дружба!!"

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


def get_weather_data(city):
    # Make API request to OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()


def translate_weather(value):
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


button1 = Button(label="Инфо", style=discord.ButtonStyle.green)
button2 = Button(label="Команды", style=discord.ButtonStyle.green)
button3 = Button(label="Статистика", style=discord.ButtonStyle.green)


@bot.command()
async def menu(ctx):
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
        embed.add_field(name="BotOS Version", value="**ver. 0.31.2** User Experience Silent Update", inline=False)
        embed.add_field(name="GitHub Repository", value="https://github.com/De44iK/Discord-KnyshBoT")
        embed.add_field(name='Discord.Py Library Version', value=library_version, inline=False)
        await ctx.send(embed=embed)

    async def button2_callback(interaction):
        await interaction.response.edit_message(content="ㅤ", view=None)
        await message.delete()  # Delete the menu message

        await ctx.send(embed=embedCMDS)

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
async def cls(ctx):
    if ctx.channel.id == 996721226166841424:
        # Fetch the channel to clear messages from
        channel = ctx.channel

        # Fetch and delete messages in batches
        messages_deleted = 0
        async for message in channel.history(limit=None):
            await message.delete()
            messages_deleted += 1

        await ctx.send(f"Channel cleared. Deleted {messages_deleted} messages.")
    else:
        await ctx.send("Эта команда только для музыкального чата")


@bot.command()
async def tic(ctx: commands.Context):
    """Starts a tic-tac-toe game with yourself."""
    await ctx.send("Крестики-нолики: Х ходит первым", view=TicTacToe())

# buttonA = Button(label="A", style=discord.ButtonStyle.green)
# buttonB = Button(label="B", style=discord.ButtonStyle.green)
# buttonC = Button(label="C", style=discord.ButtonStyle.green)

# @bot.command()
# async def cls1(ctx):
#     chanid = ctx.channel.id
#     clearchat()
#     async def clearchat():
#         if chanid == 996721226166841424:
#             # Fetch the channel to clear messages from
#             channel = ctx.channel

#             # Fetch and delete messages in batches
#             messages_deleted = 0
#             async for message in channel.history(limit=None):
#                 await message.delete()
#                 messages_deleted += 1

#             await ctx.send(f"Channel cleared. Deleted {messages_deleted} messages.")
#         else:
#             await ctx.send("Эта команда только для музыкального чата. Введите Админский пароль что бы очистить этот чат")
#             password = []
#             view = View()
#             view.add_item(buttonA)
#             view.add_item(buttonB)
#             view.add_item(buttonC)
#             message = await ctx.send("Меню KnyshBoT: \nВыберите один из пунктов: ", view=view)
#             def buttonA_callback(interaction):
#                 password.append("A")
#                 if "".join(password) == "AABC":
#                     print("Password is correct!!!!")
#             def buttonB_callback(interaction):
#                 password.append("B")
#                 if "".join(password) == "AABC":
#                     print("Password is correct!!!!")
#             def buttonC_callback(interaction):
#                 password.append("C")
#                 if "".join(password) == "AABC":
#                     chanid = 996721226166841424
#                     clearchat()
#         buttonA.callback = buttonA_callback
#         buttonB.callback = buttonB_callback
#         buttonC.callback = buttonC_callback

@bot.event
async def on_ready():
    print("\033[1;32;40m"+f"Logged in SUCESSFULLY as {bot.user.name}#{bot.user.discriminator}" + "\033[0m")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.playing,
            name="/menu | Ver 0.31.3",
            # details="none",
            # state="© 2023 D44K Local Software Corp",
        )
    )

async def main():
    # await load_cogs()
    if BOT_MODE == "RELEASE":
        await bot.start(BOT_TOKEN_RELEASE)
    elif BOT_MODE == "TESTING":
        await bot.start(BOT_TOKEN_TESTING)
    else:
        print(f"> ERROR!\nINCORRECT BOT MODE IS SELECTED: {BOT_MODE}")

if __name__ == "__main__":
    asyncio.run(main())


#damn this code became long asf