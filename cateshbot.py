import os, random
import requests
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

bot = commands.Bot(command_prefix='$')
slash = SlashCommand(bot, sync_commands=True)
bot_guild_ids = []

def makeids() :
  global bot_guild_ids
  for guild in bot.guilds :
    bot_guild_ids.append(guild.id)

# -------------------------------------------
# defining the lists

allcats = {
  'catesh': ['Catesh', []],
  'thurston': ['Thurston Waffles', []],
  'catswhoyell': ['Yelling Cats', []],
  'catsareassholes': ['Asshole Cats', []],
  'bigfloppa': ['Big Floppa', []],
  'illegallysmolcats': ['Illegally Smol Cats', []],
  'catswithjobs': ['Cats With Jobs', []], 
  'petthedamncat': ['Cats that want Petting', []],
  'catsareliquid': ['Liquid Cats', []],
  'catshuggingthings': ['Cats Hugging Things', []],
  'catblep': ['Blepping Cats', []],
  'catloaf': ['Cats Like Loaves', []],
  'catsstandingup': ['Cats Standing Up', []],
  'startledcats': ['Startled Cats', []],
  'supermodelcats': ['Supermodel Cats', []],
  'bottlebrush': ['Cats With Bottlebrush Tails', []],
  'feelinglucky': ['Feeling Lucky Cat', []],
}
cmd_choices = []

# reading the list of cat links

for categ in allcats :
  if (categ != 'feelinglucky') :
    with open(f'/home/pi/cateshbot/res/{categ}.txt', 'r') as catlist :
      clist = eval(catlist.read())
      allcats[categ][1] = clist.copy()
      allcats['feelinglucky'][1].extend(clist.copy())
  cmd_choices.append(create_choice(
    name=allcats[categ][0],
    value=categ
  ))

# when the bot is running

@bot.event
async def on_ready() :
  print(f'Logged in as {bot.user}')
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='/help and /cat'))

@bot.event
async def on_guild_join(guild) :
  makeids()

# registering the slash commands

@slash.slash(
  name='catesh',
  description='A command to send pictures/videos of cute cats!',
  options=[
    create_option(
      name='category',
      description='Choose which cat to get a picture/video of!',
      required=False,
      option_type=3,
      choices=cmd_choices
    ),
    create_option(
      name='count',
      description='Count of pictures/videos (must not be more than 10)',
      required=False,
      option_type=4,
    )
  ],
)
async def _cat(ctx: SlashContext, category: str = 'feelinglucky', count: int = 1) :
  if (count <= 10) :
    clist = allcats[category][1].copy()
    await ctx.defer()
    for i in range(count) :
      wurl = clist.pop(random.randrange(0, len(clist)))
      print(wurl)
      if (wurl.startswith('https://www.reddit.com/') or wurl.startswith('https://www.gyfcat.com/') or wurl.startswith('https://www.imgur.com/')) :
        await ctx.send(f'Cute {allcats[category][0]}: {wurl}')
      elif ('sinaimg' in wurl):
        print(wurl) 
        response = requests.get(wurl)
        extension=wurl.split('.')[-1]
# Check if the request was successful
        if response.status_code == 200:
          
    # Save the image to a file
          with open(f"image.{extension}", "wb") as f:
            f.write(response.content)
            print('success')
          if os.path.exists(f'image.{extension}'):
            with open(f'image.{extension}','rb') as f:
              picture = discord.File(f)
              await ctx.send('Cute Catesh',file=picture)
        else:
          pass
      else :
        cembed = discord.Embed(title=f'Cute {allcats[category][0]}')
        cembed.set_image(url=wurl)
        cembed.set_footer(text='Catesh Bot', icon_url='https://cdn.discordapp.com/avatars/890941783113076757/4f334efe53eff369bb93ccd234af9b5c.webp?size=240')
        await ctx.send(embed=cembed)
  else :
    await ctx.send('Only 10 or less pictures/videos can be sent at a time!')

@slash.slash(
  name='help',
  description='A command for help on how to use this bot!'
)
async def _help(ctx: SlashContext) :
  wembed = discord.Embed(title='Help • Catesh Bot')
  wdescription = 'Catesh Bot brings to you a wide variety of images of the cutest cats!\nUse `/cat` to see such pictures.\n\nThe `/cat` command asks for a `category`,  which needs to be the category of image you ask for. The categories are as follows:\n\n'
  for categ in allcats :
    wdescription += '• '+allcats[categ][0]+'\n'
  wembed.description = wdescription
  wembed.set_footer(text='Catesh Bot', icon_url='https://cdn.discordapp.com/avatars/890941783113076757/4f334efe53eff369bb93ccd234af9b5c.webp?size=240')
  await ctx.send(embed=wembed)

bot.run("MTA2MDE3MzgzMzI5MTcwMjM3NA.GVqO5U.uX3ZLGUimUIvsRXDfdNrGMjLgJ3dDs8ZOkGmyw")
