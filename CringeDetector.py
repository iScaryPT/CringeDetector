import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

class CringeDetector(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.trigger = "<:CringeDetector:838460709524209684>"
        self.yes_emoji = "<:HmmmYes:838429420716818463>"
        self.no_emoji = "<:AngryBeja:895806455452663819>"
        self.tagged_messages = {}
        self.poll_msgs = {}
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()
        
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        
        if(user.bot):
            return 
        
        #if its guimas cringe detector emogi
        if(str(reaction.emoji) == self.trigger):
        
            #the cring detector cannot cringe lmao
            if(reaction.message.author.bot):
                return
            
            #we cant cringe detect on polls or on current/past messages
            if(reaction.message.id not in self.poll_msgs.keys() and reaction.message.id not in self.tagged_messages.keys()):
                
                #create poll
                poll_msg = await reaction.message.reply("I smell cringe around here... Should we arrest this fag? You have 1 minute to decide... <:CringeDetector:838460709524209684>", mention_author=True);
                await poll_msg.add_reaction(self.yes_emoji)
                await poll_msg.add_reaction(self.no_emoji)
                self.poll_msgs[poll_msg.id] = reaction.message.id
                
                #add info about the new poll 
                self.tagged_messages[reaction.message.id] = { "poll": poll_msg, "author": reaction.message.author, "yes":0, "no":0 }
                
                #schedule the penalty appliance
                self.scheduler.add_job(self.apply_penalty, 'date', run_date= datetime.now() + timedelta(seconds=5),  args = [reaction.message.id,])
        
        #if its yes or no message reacting on a active poll
        elif(str(reaction.emoji) == self.yes_emoji or str(reaction.emoji) == self.no_emoji):
            
            if(reaction.message.id in self.poll_msgs.keys()):
                
                if(str(reaction.emoji) == self.yes_emoji):
                    self.tagged_messages[self.poll_msgs[reaction.message.id]]["yes"] += 1
                else:
                    self.tagged_messages[self.poll_msgs[reaction.message.id]]["no"] += 1
                
            
            
    async def apply_penalty(self, msg_id):
           

        yes = self.tagged_messages[msg_id]["yes"]
        no = self.tagged_messages[msg_id]["no"]
        
        #reply the result of the poll
        result_msg = await self.tagged_messages[msg_id]["poll"].reply("Result -> " + str(yes) + " yes and " + str(no) + " no.")
        
        self.poll_msgs.pop(self.tagged_messages[msg_id]["poll"].id)
        self.tagged_messages.pop(msg_id, None)

       