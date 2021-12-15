import discord
import asyncio
import json




#The token for the bot to start will be loaded from the token.json file
#Don't forget to replace "Enter your token here" in the token.json with your token
with open('token.json', 'r') as f:
    data = json.load(f)
    token = data["TOKEN"]


    
#The prefixes of the guilds your bot is in will be grabbed from the prefixes.json file and returned
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


  
#The prefix of the bot for the guilds will be set by the get_prefix funcion
bot = commands.Bot(command_prefix = get_prefix)



#Prints a text to the console, when the bot started and the status task gets looped
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    bot.loop.create_task(status_task())


    
#If your bot joins a guild, the guild id will be written to the prefix.json file and the prefix for it will be ;
#You can change the prefix with the prefix command below
@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = ";"

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)


#If your bot leaves a guild, the guild id and the prefix will be deleted off the prefix.json file
@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)        
        

        
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game('prefix + help'), status=discord.Status.online)
        await asyncio.sleep(5)
        await bot.change_presence(activity=discord.Game('Discord Bot'), status=discord.Status.online)
        await asyncio.sleep(5)
  

  
#If the command you typed in the discord channel doesn't exist, this error message will be send in the channel 
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command does not exist!') 
 

#Funktions to load and unload the cogs. 
#Example: ";unload Example" --> unloads the Example class in cogs/Example.py
@bot.command()
@commands.has_permissions(administrator = True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

#Example: ";load Example" --> loads the Example class in cogs/Example.py
@bot.command()
@commands.has_permissions(administrator = True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

    
#Adds the scripts with the end named .py from the cogs folder
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        


#Command for changing the prefix of the guild the command gets send in
#@commands.has_permissions(administrator = True) <-- can be deleted if you want that everyone can change the prefix, not just the member with administrator rights
@bot.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent = 4)

    await ctx.send(f'Prefix changed to: {prefix}')

#Sends error message if someone is running the command with missing permissions    
@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You are missing the required permissions to run this command!')
     
    
#Your bot gets logged in    
bot.run(token)
