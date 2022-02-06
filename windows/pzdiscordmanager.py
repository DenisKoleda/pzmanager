import ast
from asyncio import tasks
from cmath import exp
from distutils.command.config import config
from distutils.log import error
from operator import imod
from random import random
from urllib import response
import discord
from discord.ext import commands, tasks
from dislash import InteractionClient, ActionRow, Button, ButtonStyle, SlashCommand
from discord.ext.commands import has_permissions
import random
from rcon import Client
from datetime import datetime
import requests
import configparser
import psutil
import subprocess
import os
import time
import threading
import urllib
import sys


config = configparser.ConfigParser()
config.read("config.ini")

url = "http://109.195.19.162/lic/ultserver"
file = urllib.request.urlopen(url)

for line in file:
	licence_key = line.decode("utf-8")

if licence_key != config.get("settings", "lic_key"):
    sys.exit("Лицензия недействительна")
else:
    print("Лицензия действительна")

reboot = False

def time_N():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;
      
def restart_server_timer():
    with Client(config.get("settings", "rcon_ip"), int(config.get("settings", "rcon_port")), passwd=config.get("settings", "rcon_password")) as client:
        global reboot
        reboot = True
        client.run('servermsg Server restart in five minutes',encoding="ISO-8859-1")
        time.sleep(240)
        client.run('servermsg Server restart in one minute',encoding="ISO-8859-1")
        bot.loop.create_task(msg_restart())
        time.sleep(60)
        client.run('quit',encoding="ISO-8859-1")
        time.sleep(60)
        if checkIfProcessRunning('java.exe'):
            print('Ошибка рестарта')
        else:
            bot.loop.create_task(msg_start())
            subprocess.Popen(config.get("settings", "server_path"), creationflags=subprocess.CREATE_NEW_CONSOLE)
            print('Успешный рестарт')
         
        reboot = False

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
 
intents = discord.Intents.all()
bot.remove_command("help")

inter_client = InteractionClient(bot)

@bot.event
async def on_ready():
    print("PZ Manager запущен!")
    print("Version 1.0 Windows")
    print("Special for UltimateSurvival")
    check_online.start()
    auto_restart.start()

async def msg_start():
    if config.get("settings", "event_channel") != 'None':
        my_channel = bot.get_channel(int(config.get("settings", "event_channel")))
        emb = discord.Embed(
            description = 
            f"""
            Сервер включён!
            """,
            colour = 0x2ecc67
        )
        emb.set_author(name = 'Статус сервера')
        await my_channel.send(embed = emb)  

async def msg_restart():
    if config.get("settings", "event_channel") != 'None':
        my_channel = bot.get_channel(int(config.get("settings", "event_channel")))
        emb = discord.Embed(
            description = 
            f"""
            Сервер перезапускается!
            """,
            colour = 0x2ecc67
        )
        emb.set_author(name = 'Статус сервера')
        await my_channel.send(embed = emb)  

@tasks.loop(minutes = 1)
async def auto_restart():
    global reboot
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    z = ast.literal_eval(config.get("settings", "restart_time"))
    if current_time in z and reboot == False:
        if checkIfProcessRunning('java.exe'):
            z = threading.Thread(target=restart_server_timer, daemon=True)
            if reboot == True:
                print('Перезапуск уже в процессе')
            else:
                z.start() 
                print('Автоматический рестарт сервера через 5 минут')
                if config.get("settings", "event_channel") != 'None':
                    my_channel = bot.get_channel(int(config.get("settings", "event_channel")))
                    emb = discord.Embed(
                        description = 
                        f"""
                        Сервер перезапуститься через 5 минут.
                        """,
                        colour = 0x2ecc67
                    )
                    emb.set_author(name = 'Автоматический рестарт сервера!')
                    await my_channel.send(embed = emb)  
        else:
            print('Авто-рестарт отменён. Сервер выключен.')
    
@tasks.loop(minutes = 15)
async def check_online():
    if config.get("settings", "online_channel_id") != 'None':
        onlinech = bot.get_channel(int(config.get("settings", "online_channel_id")))
        response = requests.get(f'https://api.wargm.ru/server/get_info?api_key={config.get("settings", "wargm_api_key")}')
        online = str(response.content).split('"')
        if online[3] != "error" and online[3] != "blocked":
            online = online[41]
            await onlinech.edit(name=f'{config.get("settings", "online_channel_name")} : [{online}]', encoding="ISO-8859-1")
            print(f'{time_N()} online updated')
        else:
            print('online: WARGM API ERROR OR BLOCK')
            raise('WARGM BAD')
    if config.get("settings", "votes_wargm_channel_id") != 'None':        
        votech = bot.get_channel(int(config.get("settings", "votes_wargm_channel_id")))
        response = requests.get(f'https://api.wargm.ru/server/get_votes?api_key={config.get("settings", "wargm_api_key")}')
        votes = len(str(response.content).split('vote'))-1
        await votech.edit(name=f'{config.get("settings", "votes_wargm_channel_name")} : [{votes}]')
        print(f'{time_N()} wargm_votes updated')

@bot.event
async def on_command_error(ctx, error):
	print(error)

	if isinstance(error, commands.UserInputError):
		await ctx.send(embed = discord.Embed(
			color=0x2ecc67,
			description = f"Правильное использование команды: \n `{ctx.prefix}{ctx.command.usage}`"
		))

@bot.command(usage = "controlpanel")
@has_permissions(administrator=True)
async def controlpanel(ctx):
    emb = discord.Embed(
        description = 
        f"""
        Панель управления сервером через дискорд.
        """,
        colour = 0xffba42
    )
    emb.set_author(name = 'Панель управления')

    row = ActionRow(
        Button(
            style = ButtonStyle.grey,
            label = 'Статус',
            custom_id = 'status'
        ),
        Button(
            style = ButtonStyle.green,
            label = 'Запуск',
            custom_id = 'on'
        ),
        Button(
            style = ButtonStyle.red,
            label = 'Выключить',
            custom_id = 'off'
        ),
        Button(
            style = ButtonStyle.green,
            label = 'Перезапуск',
            custom_id = 'restart'
        ),
        Button(
            style = ButtonStyle.red,
            label = 'Убить',
            custom_id = 'kill'
        )
    )
    await ctx.send(embed = emb, components = [row])

@bot.command(usage = "adduser <@пользователь> <ник> <пароль(по желанию)>")
@has_permissions(administrator=True)
async def adduser(ctx, member: discord.Member, nickname, password = None):
    if password == None:
        chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        length = random.randint(6,8)
        for n in range(1):
            password =''
            for i in range(length):
                password += random.choice(chars)
    with Client(config.get("settings", "rcon_ip"), int(config.get("settings", "rcon_port")), passwd=config.get("settings", "rcon_password")) as client:
        response = client.run(f'adduser {nickname} {password}')
    print(response)
    if response != "A user with this name already exists":
        emb = discord.Embed(
            description = 
            f"Пользователь: {nickname} \n Пароль: {password} \n Cmd: {response}" , color=0x2ecc67
        )
        emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        emb.set_author(name = 'Добавление в White-List')
        await ctx.message.delete()
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(
            description = 
            f"Такой пользователь уже существует! \n Cmd: {response}" , color=0xec4b4b
        )
        emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        emb.set_author(name = 'Ошибка при добавлении в White-List')
        await ctx.message.delete()
        await ctx.send(embed = emb)
    emb = discord.Embed(
        description = 
        f"""
        Инофрмация для подключения: 

        **{config.get("settings", "server_name")}
        IP: {config.get("settings", "server_ip")}
        PORT: {config.get("settings", "server_port")}** 

        **Имя: {nickname} 
        Пароль: {password}** 
        """,
        colour = 0x2ecc67
    )
    emb.set_footer(text='Удачной игры на сервере!')
    emb.set_author(name = 'Вас добавили в WhiteList!')
    if config.get("settings", "add_wl_img") != 'None':
        emb.set_image(url = config.get("settings", "add_wl_img"))
    if response != "A user with this name already exists":
        print(f"{nickname} добавлен в WhiteList by {ctx.author.display_name}")
        await member.send(embed = emb)
        if config.get("settings", "add_wl_role_id") != 'None':
            role = ctx.guild.get_role(int(config.get("settings", "add_wl_role_id")))
            await member.add_roles(role)       
    else:
        print(f"Ошибка при добавлении в WhiteList by {ctx.author.display_name}")

@bot.command(usage = "deluser <никнейм>")
@has_permissions(administrator=True)
async def deluser(ctx, nick):
    with Client(config.get("settings", "rcon_ip"), int(config.get("settings", "rcon_port")), passwd=config.get("settings", "rcon_password")) as client:
        response = client.run(f'removeuserfromwhitelist {nick}')
    emb = discord.Embed(
        description = response, color=0x2ecc67
    )
    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.message.delete()    
    emb.set_author(name = f'Удаление из WhiteList')
    await ctx.send(embed = emb)
    print(f"{response} by {ctx.author.display_name}")

@bot.event
async def on_button_click(inter):
    if inter.component.id == "status":
        if checkIfProcessRunning('java.exe'):
            status = 'Сервер включен'
            print(status)
        else:
            status = 'Сервер выключен'
            print(status)
        await inter.reply(status, ephemeral = True)
    if inter.component.id == "on":
        if checkIfProcessRunning('java.exe'):
            await inter.reply('Сервер уже запущен! 📡', ephemeral = True)
        else:
            x = config.get("settings", "server_path")
            subprocess.Popen(config.get("settings", "server_path"), creationflags=subprocess.CREATE_NEW_CONSOLE)
            await inter.reply('Запускаю сервер! 📡', ephemeral = True)
            if config.get("settings", "event_channel") != 'None':
                my_channel = bot.get_channel(int(config.get("settings", "event_channel")))
                emb = discord.Embed(
                    description = 
                    f"""
                    Сервер включён!
                    """,
                    colour = 0x2ecc67
                )
                emb.set_author(name = 'Статус сервера')
                await my_channel.send(embed = emb)
    if inter.component.id == "off":
        if checkIfProcessRunning('java.exe'):
            with Client(config.get("settings", "rcon_ip"), int(config.get("settings", "rcon_port")), passwd=config.get("settings", "rcon_password")) as client:
                client.run('quit')
            await inter.reply('Выключаю сервер! 📡', ephemeral = True)
            if config.get("settings", "event_channel") != 'None':
                my_channel = bot.get_channel(int(config.get("settings", "event_channel")))
                emb = discord.Embed(
                    description = 
                    f"""
                    Сервер выключен!
                    """,
                    colour = 0x2ecc67
                )
                emb.set_author(name = 'Статус сервера')
                await my_channel.send(embed = emb)
        else:
            await inter.reply('Сервер уже выключен! 📡', ephemeral = True)
    if inter.component.id == "kill":
        if checkIfProcessRunning('java.exe'):
            os.system("taskkill /im java.exe /f")
            await inter.reply('Процесс убит! 📡', ephemeral = True)
        else:
            await inter.reply('Сервер уже выключен! 📡', ephemeral = True)
    if inter.component.id == "restart":
        if checkIfProcessRunning('java.exe'):
            z = threading.Thread(target=restart_server_timer, daemon=True)
            global reboot
            if reboot == True:
                await inter.reply('Перезапуск уже в процессе! 📡', ephemeral = True)
            else:
                z.start() 
                await inter.reply('Перезапуск запущен! 📡', ephemeral = True)
            if config.get("settings", "event_channel") != 'None':
                my_channel = bot.get_channel(int(config.get("settings", "event_channel")))
                emb = discord.Embed(
                    description = 
                    f"""
                    Сервер перезапуститься через 5 минут.
                    """,
                    colour = 0x2ecc67
                )
                emb.set_author(name = 'Перезапуск сервера!')
                await my_channel.send(embed = emb)  
        else:
            await inter.reply('Сервер выключен! 📡', ephemeral = True)


bot.run("OTM5NjcxMDA5Nzk4Mjg3Mzkw.Yf8O0g.tMyjdrC7vVcVvmlkKTKIG3-obdg")