from asyncio import tasks
from cmath import exp
from distutils.log import error
from operator import imod
from random import random
from urllib import response
import discord
from discord.ext import commands, tasks
from dislash import InteractionClient, ActionRow, Button, ButtonStyle, SlashCommand
from PIL import Image,ImageFilter,ImageDraw,ImageFont
from discord.ext.commands import has_permissions, has_any_role
import paramiko
import random
from rcon import Client
from datetime import datetime
import requests

host = "127.0.0.1"
port = 22
username = "pzserver1"
password = "JopaSRuchkoi"

def genid():
    id = random.randint(1,10000)
    return str(id)

def time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time 

 
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
 
intents = discord.Intents.all()
bot.remove_command("help")

inter_client = InteractionClient(bot)

@bot.event
async def on_ready():
    # my_channel = bot.get_channel(938594910985138257)
    # emb = discord.Embed(
    #     description = 
    #     f"""
    #     Панель управления сервером через дискорд.
    #     """,
    #     colour = 0xffba42
    # )
    # emb.set_author(name = 'Панель управления')

    # row = ActionRow(
    #     Button(
    #         style = ButtonStyle.grey,
    #         label = 'Статус',
    #         custom_id = 'status'
    #     ),
    #     Button(
    #         style = ButtonStyle.green,
    #         label = 'Запуск',
    #         custom_id = 'on'
    #     ),
    #     Button(
    #         style = ButtonStyle.red,
    #         label = 'Выключить',
    #         custom_id = 'off'
    #     ),
    #     Button(
    #         style = ButtonStyle.green,
    #         label = 'Перезапуск',
    #         custom_id = 'restart'
    #     ),
    #     Button(
    #         style = ButtonStyle.red,
    #         label = 'Убить',
    #         custom_id = 'kill'
    #     )
    # )
    # await my_channel.send(embed = emb, components = [row])
    print("Бот запущен")
    check_online.start()

@tasks.loop(minutes = 15)
async def check_online():
    channel = bot.get_channel(936696285866631279)
    response = requests.get('https://api.wargm.ru/server/get_info?api_key=CwWeii7Wq0LZ7AmE_ogIRYCzUeuwPJ55')
    online = str(response.content).split('"')[41]
    await channel.edit(name=f'🟢・𝓞𝓷𝓵𝓲𝓷𝓮 : [{online}]')
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f'{current_time} online upd')
    channel = bot.get_channel(939372575228825690)
    response = requests.get('https://api.wargm.ru/server/get_votes?api_key=CwWeii7Wq0LZ7AmE_ogIRYCzUeuwPJ55')
    votes = len(str(response.content).split('vote'))-1
    await channel.edit(name=f'📌・ 𝓥𝓸𝓽𝓮𝓼 : [{votes}]')

@bot.event
async def on_member_join(member):
    if role := member.guild.get_role(928823976321511434):
        await member.add_roles(role)

@bot.event
async def on_voice_state_update(member,before,after):
    if after.channel != None:
        if after.channel.id == 936706603401482291:
            maincategory = discord.utils.get(member.guild.categories, id=928666080929542198)
            channel2 = await member.guild.create_voice_channel(name=f'🔊・{member.display_name}',category = maincategory)
            await channel2.set_permissions(member,connect=True, speak=True, manage_channels=True)
            try:
                await member.move_to(channel2)
            except:
                await channel2.delete()
            def check(x,y,z):
                return len(channel2.members) == 0
            await bot.wait_for('voice_state_update',check=check)
            await channel2.delete()

@bot.event
async def on_command_error(ctx, error):
	print(error)

	if isinstance(error, commands.UserInputError):
		await ctx.send(embed = discord.Embed(
			color=0xffba42,
			description = f"Правильное использование команды: \n `{ctx.prefix}{ctx.command.usage}`"
		))

@bot.command(usage = "adduser <@пользователь> <ник> <пароль(по желанию)>")
@has_any_role(933519639349198868,936716382920380416,931521179045490698,928823247993192458,936725774713618493)
async def adduser(ctx, member: discord.Member, nickname, password = None):
    if password == None:
        chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
        length = random.randint(6,8)
        for n in range(1):
            password =''
            for i in range(length):
                password += random.choice(chars)
    with Client('127.0.0.1', 27015, passwd='8TNvxsxJDp') as client:
        response = client.run(f'adduser {nickname} {password}')
    print(response)
    emb = discord.Embed(
        description = 
        f"Пользователь: {nickname} \n Пароль: {password} \n Cmd: {response}" , color=0xffba42
    )
    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    emb.set_author(name = 'Добавление в White-List')
    await ctx.message.delete()
    await ctx.send(embed = emb)
    emb = discord.Embed(
        description = 
        f"""
        Инофрмация для подключения: 

        **The Dead City 
        IP: 109.195.19.162 
        PORT: 16261** 

        **Имя: {nickname} 
        Пароль: {password}** 
        """,
        colour = 0xffba42
    )
    emb.set_footer(text='Удачной игры на сервере!')
    emb.set_author(name = 'Вас добавили в White-List!')
    emb.set_image(url = 'https://cdn.discordapp.com/attachments/938944433448173648/938945542673817620/ezgif.com-gif-maker.gif')
    if response != "A user with this name already exists":
        await member.send(embed = emb)
        role = ctx.guild.get_role(939139025883762728)
        await member.add_roles(role)

@bot.command(usage = "deluser <никнейм>")
@has_any_role(933519639349198868,936716382920380416,931521179045490698,928823247993192458,936725774713618493)
async def deluser(ctx, nick):
    with Client('127.0.0.1', 27015, passwd='8TNvxsxJDp') as client:
        response = client.run(f'removeuserfromwhitelist {nick}')
    emb = discord.Embed(
        description = response, color=0xffba42
    )
    emb.set_footer(text=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    await ctx.message.delete()    
    emb.set_author(name = f'Удаление из White-List')
    await ctx.send(embed = emb)

@bot.event
async def on_button_click(inter):
    guild = bot.get_guild(inter.guild.id)
    if inter.component.id == "verif_button":
        verif = guild.get_role(928823976321511434)
        member = inter.author
        if verif in member.roles:
            res = 'Вы уже верифицированы 😉'
        else:
            res = 'Вы успешно верифицировались!'
            await member.add_roles(verif)
        await inter.reply(res, ephemeral = True)
    if inter.component.id == "status":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        command = "pzserver status"
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        str1 = ''.join(lines)
        id = genid()
        cmdtime = time()
        print(id + ' - ' + cmdtime + ' - ' + str1)
        ssh.close
        await inter.reply(str1, ephemeral = True)
    if inter.component.id == "on":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        command = "pzserver start"
        ssh.exec_command(command)
        ssh.close
        await inter.reply('Запускаю сервер! 📡', ephemeral = True)
    if inter.component.id == "off":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        command = "pzserver stop"
        ssh.exec_command(command)
        ssh.close
        await inter.reply('Выключаю сервер! 📡', ephemeral = True)
    if inter.component.id == "kill":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        command = "pzserver kill"
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        str1 = ''.join(lines)
        id = genid()
        cmdtime = time()
        print(id + ' - ' + cmdtime + ' - ' + str1)
        ssh.close
        await inter.reply(str1, ephemeral = True)
    if inter.component.id == "restart":
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        command = "pzserver restart"
        ssh.exec_command(command)
        ssh.close
        await inter.reply('Перезапускаю сервер! 📡', ephemeral = True)
        my_channel = bot.get_channel(936698972561637496)
        emb = discord.Embed(
            description = 
            f"""
            Сервер перезапуститься через 15 минут.
            """,
            colour = 0xffba42
        )
        emb.set_author(name = 'Перезапуск сервера!')
        await my_channel.send(embed = emb)  

@bot.command(usage = "serf <@пользователь>")
async def serf(ctx, member: discord.Member):
    base = Image.open("ser.png").convert("RGBA")
    txt = Image.new("RGBA", base.size, (255,255,255,0))
    fnt = ImageFont.truetype("Monotype Corsiva.ttf", 25)
    d = ImageDraw.Draw(txt)
    if len(member.name) == 11:
        d.text((150,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))
    if len(member.name) == 4:
        d.text((185,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))
    if len(member.name) == 5:
        d.text((185,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))
    if len(member.name) == 6:
        d.text((180,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))
    if len(member.name) == 7:
        d.text((175,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))
    if len(member.name) == 8:
        d.text((170,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))
    if len(member.name) == 9:
        d.text((165,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))
    if len(member.name) == 10:
        d.text((160,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))
    if len(member.name) == 12:
        d.text((155,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))
    if len(member.name) > 12:
        d.text((150,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))
    if len(member.name) == 3:
        d.text((185,225), str(member.name), font = fnt, fill = (90,81,52))
        out = Image.alpha_composite(base, txt)
        out.save('user.png')
        await ctx.send(file = discord.File(fp = 'user.png'))

bot.run("OTM4MzY1NjkwMzQyMTY2NTU4.YfpPJg.0T0WIBPx8KL7wyb3W6WIXFdaWSw")