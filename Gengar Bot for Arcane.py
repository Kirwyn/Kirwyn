from __future__ import print_function
import discord
from discord.ext import tasks, commands
from discord import Embed
from datetime import datetime, timedelta
import random
import re
import asyncio
import os.path
from random import randint
#googlesheets
import httplib2
import requests
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient import discovery

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

spreadsheetId = 'Spreadsheetid'
rangeName = 'Sheet!A:D'
listchannelid = 0
attchannelid = 0
guildid = 0


def get_credentials():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
    	creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)
    # Call the Sheets AP
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    return creds

description = '''Bot created by Kyou.'''

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.reactions = True


bot = commands.Bot(command_prefix='!', description=description, intents=intents)

creds = get_credentials()
service = build('sheets', 'v4', credentials=creds)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="Chilling Out"))
	
	
async def downimg(pic_url):	
	with open('sig.png', 'wb') as handle:
		response = requests.get(pic_url, stream=True)

		if not response.ok:
			print(response)

		for block in response.iter_content(1024):
			if not block:
				break
			handle.write(block)	
	
	
@bot.command(description='add Snowball role')
async def snowball(ctx):
	"""Add or remove snowballers role."""
	member = ctx.message.author
	role = discord.utils.get(ctx.guild.roles, name="SnowBallers")
	if role in member.roles:
		await member.remove_roles(role)
		embed = discord.Embed(title="Snowball Event:", description="Snowball role removed succesfully!", color=0xFF0000)
		await ctx.send(embed=embed)
	else:
		await member.add_roles(role)
		embed = discord.Embed(title="Snowball Event:", description="Snowball role added succesfully!", color=0xFF83FA)
		await ctx.send(embed=embed)

@bot.command(description='Shows signature of character, using !sig <charname>')
async def sig(ctx, *char : str):
	"""Shows the signature of your char."""
	pos = 0
	amb = 0
	nome = char[0]
	for i in char[1:]:
		nome = nome + '_' + i
	indice = nome.find('/')
	if (indice != -1):
		if nome[indice-1].isdigit and nome[indice+1].isdigit:
			pos = 1
			amb = 1
			if nome[indice-2] != '_':
				amb = 2
			if indice+3 == len(nome):
				pos = 2
			await downimg('https://www.novaragnarok.com/ROChargenPHP/newsig/' + nome[0:indice-amb].replace(' ','_') + '/' + nome[indice-amb:indice] + '/' + nome[indice+1:indice+pos+1])
			await ctx.send(file=discord.File('sig.png'))
		else:
			embed = discord.Embed(title="Error", description="Unsupported Format, try !sig <char name> <amb>/<pos>", color=0x546e7a)
			await ctx.send(embed=embed)		
	else:
		await downimg('https://www.novaragnarok.com/ROChargenPHP/newsig/' + nome.replace(' ','_') + '/1/0')
		await ctx.send(file=discord.File('sig.png'))
	#await ctx.send('https://www.novaragnarok.com/ROChargenPHP/newsig/' + nome.replace(' ','_') + '/1/0')	
	
@bot.command(description='Shows random signature of character, using !sig <charname>')
async def sigr(ctx, *char : str):
	"""Shows the signature of your char."""
	nome = char[0]
	for i in char[1:]:
		nome = nome + '_' + i
	await downimg('https://www.novaragnarok.com/ROChargenPHP/newsig/' + nome.replace(' ','_') + '/' + str(randint(1,11)) + '/' + str(randint(0,26)))	
	await ctx.send(file=discord.File('sig.png'))
	#await ctx.send('https://www.novaragnarok.com/ROChargenPHP/newsig/' + nome.replace(' ','_') + '/' + str(randint(1,11)) + '/' + str(randint(0,26)))	
	
@bot.command(description='Shows character image, using !char <charname>')
async def char(ctx, *char : str):		
	"""Shows the picture of your character."""
	pos = 0
	amb = 0
	nome = char[0]
	for i in char[1:]:
		nome = nome + '_' + i
	indice = nome.find('/')
	if (indice != -1):
		if nome[indice-1].isdigit and nome[indice+1].isdigit:
			pos = 1
			amb = 1
			if nome[indice-2] != '_':
				amb = 2
			if indice+3 == len(nome):
				pos = 2
			await downimg('https://www.novaragnarok.com/ROChargenPHP/character/' + nome[0:indice-amb].replace(' ','_') + '/' + nome[indice-amb:indice] + '/' + nome[indice+1:indice+pos+1])
			await ctx.send(file=discord.File('sig.png'))
		else:
			embed = discord.Embed(title="Error", description="Unsupported Format, try !sig <char name> <amb>/<pos>", color=0x546e7a)
			await ctx.send(embed=embed)		
	else:
		await downimg('https://www.novaragnarok.com/ROChargenPHP/character/' + nome.replace(' ','_') + '/0/0')
		await ctx.send(file=discord.File('sig.png'))
	#await ctx.send('https://www.novaragnarok.com/ROChargenPHP/character/' + nome.replace(' ','_'))
	
@bot.command(pass_context=True, description='Reset attendance list')
@commands.has_role("pepega")
async def resetatt(ctx):
	if (ctx.message.guild.id == guildid):
		if (str(ctx.message.channel).strip() == str(ctx.guild.get_channel(attchannelid)).strip()):
			value_range_body = {}
			request = service.spreadsheets().values().clear(spreadsheetId=spreadsheetId, range='Sheet1!C4:C60', body=value_range_body)
			response = request.execute()
			await UpdateList(ctx)
			embed = discord.Embed(title="Reset Att", description="Attendance reset", color=0x546e7a)
			await ctx.send(embed=embed)

async def get_next_weekday(startdate, weekday):
    """
    @startdate: given date, in format '2013-05-25'
    @weekday: week day as a integer, between 0 (Monday) to 6 (Sunday)
    """
    t = timedelta((7 + weekday - startdate.weekday()) % 7)
    return (startdate + t)
    
async def UpdateList(ctx):
	channel = ctx.guild.get_channel(listchannelid)
	msg = await channel.history(limit=2).flatten()
	if (len(msg) != 0):
		async for message in channel.history(limit=100):
			if message.author == discord.User.name:
				messageid = message.id
			msge = await channel.fetch_message(message.id)
			await msge.delete()
	result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
	values = result.get('values', [])
	Nomes = ''
	Presencas = ''
	Roles = ''
	GNomes = ''
	GPresencas = ''
	GRoles = ''
	Gyescount = 0
	Gnocount = 0
	yescount = 0
	nocount = 0
	guests = 0
	for row in values:
		if len(row) > 0:
			if row[0].strip() == 'GUESTS':
				guests = 1
			else:
				if(row[0].strip() != ''):
					if guests == 0:
						Nomes = Nomes + row[0] + '\n'
					else:
						GNomes = GNomes + row[0] + '\n'
					if len(row) > 1:
						if (row[1].strip() == ''):
							if guests == 0:
								Presencas = Presencas + '- \n'
							else:
								GPresencas = GPresencas + '- \n'
						else:
							if (row[1].strip().lower() == 'yes'):
								if guests == 0:
									yescount = yescount + 1
								else:
									Gyescount = Gyescount + 1
							else:
								if guests == 0:
									nocount = nocount + 1
								else:
									Gnocount = Gnocount + 1
							if guests == 0:
								Presencas = Presencas + row[1] + '\n'
							else:
								GPresencas = GPresencas + row[1] + '\n'
								
						if len(row) > 2:
							if (row[2].strip() == ''):
								if guests == 0:
									Roles = Roles + ' - \n'
								else:
									GRoles = GRoles + ' - \n'	
							else:
								if guests == 0:
									Roles = Roles + row[2] + '\n'
								else:
									GRoles = GRoles + row[2] + '\n'
						else:
							if guests == 0:
								Roles = Roles + ' - \n'
							else:
								GRoles = GRoles + ' - \n'
					else:
						if guests == 0:
							Presencas = Presencas + '- \n'
							Roles = Roles + ' - \n'
						else:
							GPresencas = GPresencas + '- \n'
							GRoles = GRoles + ' - \n'
	data = await get_next_weekday(datetime.now() + timedelta(days=1),5)
	embed2 = discord.Embed(title="Attendance", description="WoE Date: " + str(data.month) + '/' + str(data.day) + '/' + str(data.year), color=0xff0000)
	embed2.set_thumbnail(url='https://cdn.discordapp.com/attachments/829776739130671157/833069377372422204/emperium_2_4x.png')
	#embed2 = discord.Embed(title="Attendance", color=0x992d22)
	embed2.add_field(name="Name", value=Nomes, inline=True)
	embed2.add_field(name="Presence", value=Presencas, inline=True)
	embed2.add_field(name="Role", value=Roles, inline=True)
	embed2.set_footer(text=str(yescount) + " said yes and " + str(nocount) + " said no")
	await channel.send(embed=embed2)
	Gdata = data
	Gembed2 = discord.Embed(title="Guest Attendance", description="WoE Date: " + str(data.month) + '/' + str(data.day) + '/' + str(data.year), color=0x0000ff)
	Gembed2.set_thumbnail(url=ctx.guild.icon_url)
	#embed2 = discord.Embed(title="Attendance", color=0x992d22)
	Gembed2.add_field(name="Name", value=GNomes, inline=True)
	Gembed2.add_field(name="Presence", value=GPresencas, inline=True)
	Gembed2.add_field(name="Role", value=GRoles, inline=True)
	Gembed2.set_footer(text=str(Gyescount) + " said yes and " + str(Gnocount) + " said no")
	await channel.send(embed=Gembed2)
	

@bot.command(pass_context=True, description='Set attendance for WoE, using !setatt yes/no <yourrole>')
@commands.has_role("Core")	
async def setatt(ctx, *char : str):
	"""Set your presence status on the sheet."""
	presenca = char[len(char)-1]
	nome = '';
	nome2 = '';
	for i in char[0:len(char)-1]:
		nome = nome + ' ' + i
	nome = nome.strip();
	if nome == '':
		if ctx.message.author.nick is None:
			nome = ctx.message.author.name
		else:
			nome = ctx.message.author.name
			nome2 = ctx.message.author.nick
	if (ctx.message.guild.id == guildid):
		if (str(ctx.message.channel).strip() == str(ctx.guild.get_channel(attchannelid)).strip()):
			if (presenca.lower() != 'yes') & (presenca.lower() != 'no'):
				embed = discord.Embed(title="Error", description= presenca + "  is not a valid choice, try yes or no", color=0x546e7a)
			else:
				result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
				values = result.get('values', [])
				count = 4;
				teste = '';
				for row in values:
					if len(row) > 0:
						if row[0].strip().lower() == nome.lower() or row[0].strip().lower() == nome2.lower():
							teste = 'found'
							break
					count = count + 1
				if teste != 'found':
					if nome2 == '':
						embed = discord.Embed(title="Error", description=nome + " was not found on sheet, you can try !setatt <name_on_sheet> <yes/no>", color=0x546e7a)
					else:
						embed = discord.Embed(title="Error", description=nome + "/" + nome2 + " was not found on sheet, you can try !setatt <name_on_sheet> <yes/no>", color=0x546e7a)
				else:
					value_input_option = 'USER_ENTERED'
					value_range_body = {
						"range": "Sheet1!C" + str(count),
						"values": [[presenca]]
					}
					request = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range='Sheet1!C' + str(count), valueInputOption=value_input_option, body=value_range_body)
					response = request.execute()
					embed = discord.Embed(title="Attendance set", color=0x992d22)
					if nome2 == '':
						embed.add_field(name="Name", value=nome, inline=True)
					else:
						embed.add_field(name="Name", value=nome + "/" + nome2, inline=True)
					embed.add_field(name="Presence", value=presenca, inline=True)
					await UpdateList(ctx)
		await ctx.send(embed=embed)	
	
@bot.command(pass_context=True, description='Set role that is playing for WoE, using !setrole <name_on_sheet> <yourrole>')
@commands.has_role("Core")	
async def setrole(ctx, nome, role=""):
	"""Set your role on the sheet."""
	if role.strip() == '':
		role = nome
		if ctx.message.author.nick is None:
			nome = ctx.message.author.name
		else:
			nome = ctx.message.author.nick
	if (ctx.message.guild.id == guildid):
		if (str(ctx.message.channel).strip() == str(ctx.guild.get_channel(attchannelid)).strip()):
				result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
				values = result.get('values', [])
				count = 4;
				teste = '';
				for row in values:
					if len(row) > 0:
						if row[0].strip().lower() == nome.lower():
							teste = 'found'
							break
					count = count + 1
				if teste != 'found':
					embed = discord.Embed(title="Error", description="Discord name not found on sheet, you can try !setrole <name_on_sheet> <role>", color=0x546e7a)
				else:
					value_input_option = 'USER_ENTERED'
					value_range_body = {
						"range": "Sheet1!D" + str(count),
						"values": [[role]]
					}
					request = service.spreadsheets().values().update(spreadsheetId=spreadsheetId, range='Sheet1!D' + str(count), valueInputOption=value_input_option, body=value_range_body)
					response = request.execute()
					embed = discord.Embed(title="Role set", color=0x992d22)
					embed.add_field(name="Name", value=nome, inline=True)
					embed.add_field(name="Role", value=role, inline=True)
				await UpdateList(ctx)
	await ctx.send(embed=embed)		

	
@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))
    
@bot.command(description='Show the profile pic of person')
async def pic(ctx, *char: str):
	"""Shows the picture of person !pic <name>."""
	nome = " ".join(char)
	flag = True
	for membro in ctx.guild.members:
   		if str(membro.name).strip().lower() == nome.strip().lower() or str(membro.nick).strip().lower() == nome.strip().lower():
   			await ctx.send(membro.avatar_url)
   			flag = False
   			break
	if flag:
   		embed = discord.Embed(title="Error", description="Discord name not found", color=0x546e7a)
   		await ctx.send(embed=embed)
   		
@bot.command(description='Show how long to next woe')
async def woe(ctx):
	"""Shows how long to next woe"""
	data = await get_next_weekday(datetime.now(),5)
	woe = datetime(year=data.year,month=data.month,day=data.day,hour=12)
	if (datetime.now() > woe):
		data = await get_next_weekday(datetime.now() + timedelta(days=1),5)
		woe = datetime(year=data.year,month=data.month,day=data.day,hour=12)
	woet = woe - (datetime.now() - timedelta(hours = 3))
	await ctx.send("Woe starts in " + str(woet.days) + " days " + str(woet.seconds//3600) + " hours and " + str((woet.seconds//60)%60) + " minutes ")
    

async def my_background_task():
	await bot.wait_until_ready()
	channel = bot.get_channel(0)
	while True:
		agora = datetime.now()
		agora = agora - timedelta(hours = 3)
		h = agora.hour
		m = agora.minute
		if(h == 11 or h == 16 or h == 22 or h == 4):
			if(m == 25):
				await channel.send("<@&0> Snowball event starting in 5 minutes!")
				#embed = discord.Embed(title="Snowball Event:", description="<@&915644510996930681> Snowball Event is starting in 5 minutes!", color=0xFF83FA)
				#await channel.send(embed=embed)
				await asyncio.sleep(17700)
			else:
				await asyncio.sleep(60)
		else:
			await asyncio.sleep(60)

#bot.loop.create_task(my_background_task())
bot.run('bottoken')
