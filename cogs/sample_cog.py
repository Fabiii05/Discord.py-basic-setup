from discord.ext import commands

#You can name the class as you want. Example: If you make admin commands, name the class Admin
class Test(commands.Cog):
    
    #The bot gets passed into the cog
    #All commands must now take a "self" parameter to allow usage of instance attributes that can be used to maintain state.
    def __init__(self, bot):
        self.bot = bot
    
    #Is not necessary. You can use it to see, if the class is ready
    #Every listener needs the "@commands.Cog.listener()" decorator
    @commands.Cog.listener()
    async def on_ready(self):
        print('Test ready!')

        
    #Every command needs the "@commands.commands()" decorator
    #"ctx" represents the context of the message. You also can write "message" instead
    #All commands start like line 21-22 if you want them to access with a prefix
    @commands.command()
    async def Example(self, ctx):
      await ctx.channel.send("Hello World!")
    
    #If you want the bot to answer on your message without using a prefix in front of the message use the following example
    @commands.Cog.listener()
    async def on_message(self, message):
      #first example
      if message.content == "test":
        await message.channel.send("test")
      #second example
      if message.content.startswith("test2"):
        await message.channel.send("test2")
        
      
        
#The word Test in "bot.add_cog(Test(bot))" is the name of the class you defined above
#The funktion registeres cogs with the "bot.add_cog()" call
def setup(bot):
    bot.add_cog(Test(bot))        
