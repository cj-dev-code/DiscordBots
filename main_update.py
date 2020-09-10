import discord
import random

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.author.id == self.user.id:
            return

        if message.content.startswith('!hello'):
            message.content.lower()
            possible_responses = ["That must be the work of dark reunion.", "it appears that we've been attacked with a new stand power", "I only wanted…to be friends with Saiki-kun.", "I won't allow that to happen. I will protect the world! For I am The Jet-Black Wings!", "A dark force called 'Black Beat' dwells in my right arm", "I don't care about your past. What matters is who you are now and who you'll be in the future!", "Take this! Meteor spark genocide ball! ooph!"]
        await message.channel.send(random.choice(possible_responses))

client = MyClient()
client.run('NzUzNTYwOTUwMzIxMzE1ODUw.X1n-Uw.tssa2cmHZVpwWnXtUra_fGtF30Q')