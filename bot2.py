import discord
from discord.ext import commands
import datetime
import asyncio
import time
from discord.utils import  get
import  requests
from  PIL import  Image, ImageFont, ImageDraw
import io

intents = discord.Intents.default()
intents.members = True


async def on_message(massage):
    await client.process_commands(massage)
    msg = massage.content.lower()


PREFIX = '?'
bad_words = [ 'котак', 'гандон', 'пидор', 'пидр', 'иди на хуй', 'иди на хер', 'хуй', 'член', 'шлюха', 'дешевая шлюха',
              'пидорска', 'мудак', 'хуй ', 'пизда ', 'ебать ', 'блядь ', 'блять ', 'Fuck ', 'Fuck you ', 'Bitch ', ' Nigger',
              'Fucking shit ',  'Fucking idiot', 'Fucking fool ', 'Nerd ', 'Son of a bitch ',
              'заебал', 'негр ', 'слитый бот ', 'бот ', 'ботяра', 'гей', 'отебись от сюда', 'у сука', 'я тебя трахну', 'го ебаться',
              'сука' ]

client = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
client.remove_command('help')


@client.event
async def on_ready():
    print('BOT connected')

    await  client.change_presence( status = discord.Status.online, activity= discord.Game( 'NoctaCraft' ) )

@client.command()
async def on_command_error(ctx, error):
    pass


@client.event
async def on_member_join(member):
    channel = client.get_channel(853136551349190686)

    role = discord.utils.get(member.guild.roles, id=853146515168952320)

    await member.add_roles(role)
    await channel.send(
        embed=discord.Embed(description=f'Привет  {member.name},  приятного отдыха!', color=0x0c0c0c))


@client.event
async  def on_message( message ):
    await  client.process_commands( message )

    msg = message.content.lower()

    if msg in bad_words:
        await  message.delete()
        await  message.author.send( f'{message.author.name}, не надо тут такое писать! в следущий раз будет бан!')

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)

async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

    await ctx.send( embed=discord.Embed(description=f':white_check_mark: Удалено {amount} сообщений', color=0x0c0c0c))


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='kick', color=discord.Color.red())
    await  ctx.channel.purge(limit=1)

    await  member.kick(reason=reason)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='kick user', value='Kick user: {}'.format(member.mention))

    await  ctx.send(embed=emb)


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    emb = discord.Embed(title='Ban', colour=discord.Color.red())
    await ctx.channel.purge(limit=1)

    await member.ban(reason=reason)

    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Ban user', value='Baned user : {}'.format(member.mention))
    emb.set_footer(text='Был забанин Админом {}'.format(ctx.author.name), icon_url=ctx.author.avatar_url)

    await ctx.send(embed=emb)


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):

    await  ctx.channel.purge(limit=1)

    banned_users = await ctx.guild.bans()


    for ban_entry in banned_users:
        user = ban_entry.user

        await  ctx.guild.unban(user)

        return






@client.command()

async  def help( ctx ):
    emb = discord.Embed( title= 'Команды сервера' )

    emb.add_field(name='{}clear'.format(PREFIX), value='Очиска чата')
    emb.add_field(name='{}kick'.format(PREFIX), value='Удаление участника с сервера')
    emb.add_field(name='{}ban'.format(PREFIX), value='Бан участника')
    emb.add_field(name='{}unban'.format(PREFIX), value='Разбанить учатника')
    emb.add_field(name='{}time'.format(PREFIX), value='Время (Москва) ')
    emb.add_field(name='{}mute'.format(PREFIX), value='Мут участнику ')
    emb.add_field(name='{}unmute'.format(PREFIX), value='Убрать мут участнику ')
    emb.add_field(name='{}join'.format(PREFIX), value='подключение бота к голосовому чату ')
    emb.add_field(name='{}leave'.format(PREFIX), value='отключение бота к голосовому чату')
    emb.add_field(name='{}server'.format(PREFIX), value='узнать айпи майнкрафт сервера')
    emb.add_field(name='{}role'.format(PREFIX), value='Назначить роль участнику')
    emb.add_field(name='{}unrole'.format(PREFIX), value='Забрать роль у участника ')

    await  ctx.send( embed = emb )


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def time(ctx):
    emb = discord.Embed(title='Your title', description='Вы сможете узнать текущее время в Москве',
                        colour=discord.Color.green(), url='https://time100.ru/Moscow')

    emb.set_author(name=client.user.name, icon_url=client.user.avatar_url)
    emb.set_footer(text='Спасибо за использование нашего бота!')
    # emb.set_image( url = 'https://st2.depositphotos.com/2020021/7591/v/600/depositphotos_75910375-stock-illustration-time-is-money-time-management.jpg' )
    emb.set_thumbnail(
        url='https://st2.depositphotos.com/2020021/7591/v/600/depositphotos_75910375-stock-illustration-time-is-money-time-management.jpg ')

    now_date = datetime.datetime.now()

    emb.add_field(name='Time', value='Time : {}'.format(now_date))

    await  ctx.send(embed=emb)


@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
    emb = discord.Embed(title='Мут', colour=discord.Color.purple())
    await ctx.channel.purge(limit=1)

    mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')

    await member.add_roles(mute_role)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='Мут участнику', value='Мут выдан : {}'.format(member.mention))

    await ctx.send(embed=emb)


@client.command()
@commands.has_permissions(administrator=True)

async def unmute(ctx, member: discord.Member):
    emb = discord.Embed(title='Убрали Мут', colour=discord.Color.blue())
    await ctx.channel.purge(limit=1)


    mute_role = discord.utils.get(ctx.message.guild.roles, name='mute')

    await member.remove_roles(mute_role)
    emb.set_author(name=member.name, icon_url=member.avatar_url)
    emb.add_field(name='UnMute', value='Мут убрали : {}'.format(member.mention))

    await ctx.send(embed=emb)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{ctx.author.name}, обезательно укажите аргумент!')

    if isinstance( error, commands.MissingPermissions ):
        await  ctx.send( f'{ ctx.author.name}, у вас не достаточно прав!')



@ban.error
async def ban_error(ctx, error):
    if isinstance( error, commands.MissingPermissions ):
        await  ctx.send( f'{ ctx.author.name}, у вас не достаточно прав!')


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await  ctx.send(f'{ctx.author.name}, у вас не достаточно прав!')

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await  ctx.send(f'{ctx.author.name}, у вас не достаточно прав!')

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await  ctx.send(f'{ctx.author.name}, у вас не достаточно прав!')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await  ctx.send(f'{ctx.author.name}, у вас не достаточно прав!')\



@client.command()
async  def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await  ctx.send(f'Бот присоеденился к каналу: {channel}')

@client.command()
async  def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        voice = await  channel.connect()
        await  ctx.send(f'Бот отключился от канала {channel}')


@client.command()
async def server(ctx):
    await  ctx.send ('Тут будет ip майнкрафт сервера*')

@client.command()
@commands.has_permissions(administrator=True)
async def role(ctx, member: discord.Member, role: discord.Role):

    await ctx.message.delete()
    role_name = discord.utils.get(ctx.message.guild.roles, name=f'{role}')
    await member.add_roles(role_name)
    await ctx.send(f'{ctx.message.author.mention} Выдал роль {role} участнику {member.mention}')
    print(f'{ctx.message.author} Выдал роль {role} участнику {member}')

@client.command()
@commands.has_permissions(administrator=True)
async def unrole(ctx, member: discord.Member, role: discord.Role):
    await ctx.message.delete()
    role_name = discord.utils.get(ctx.message.guild.roles, name=f'{role}')
    await member.remove_roles(role_name)
    await ctx.send(f'{ctx.message.author.mention} Забрал роль  {role} участника {member.mention}')
    print(f'{ctx.message.author} Забрал роль {role} участника {member}')

@role.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await  ctx.send(f'{ctx.author.name}, у вас не достаточно прав!')

@unrole.error
async def unrole_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await  ctx.send(f'{ctx.author.name}, у вас не достаточно прав!')



token = open('token.txt', 'r').readline()

client.run(token)
