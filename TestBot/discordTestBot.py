# -*- coding: utf-8 -*-
"""
Created on Thu May 21 16:48:05 2020

@author: josep
"""

import discord
from datetime import date
from time import time
client = discord.Client()
print('Run')

class UserDataPrefs:
    def __init__(self, name = '', discriminator = ''):
        self._name = name
        self._discriminator = discriminator
        self._chilis = 5
        self._in = True
        self._being_bullied = False
        self._being_bullied_since = time()
        
        self._bully_count = 0
        self._been_bullied_count = 0
        self._date_last_bullied_another = date(10,10,10) # Initialized to never.
        self._date_last_been_bullied = date(10,10,10)
    '''
    Chilis: 1-5. How high is this person's pain tolerance?
    
    '''
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        '''
        TODO: GIVE STRING REPRESENTATION OF THE DATA IN THIS OBJECT
        for reboot purposes
        '''
        pass
    
    def name(self):
        return self._name + "#"+ self._discriminator
    
    def set_chilis(self, chili_num):
        assert 1<= chili_num <= 5, "Invalid chili_num: " + str(chili_num)
        self._chilis = chili_num
        
    def bullyable(self):
        return self._in and self._date_last_been_bullied != date.today()
    
    def toggle_opt_in(self):
        self._in = not self._in
        
    def bully(self):
        self._bully_count += 1
        
    def be_bullied(self):
        self._been_bullied_count += 1
        self._being_bullied_since = time()
        
    def complete_bullying(self):
        self._date_last_been_bullied = date.today()
        
    def being_bullied(self):
        return self._being_bullied
    
    def toggle_being_bullied(self):
        self._being_bullied = not self._being_bullied
    
    def __eq__(self, other):
        return self._name == other._name
'''    
class Server:
    def __init__(self, channel=None, name='', users = ()):
        self._name=name
        self._users = list(users)
        self._channel = channel
        
    def set_channel(self, channel):
        self._channel = channel
    
    #member is the member name of the person to bully.
    
    def set_bully(self, member):
        assert type(member) == str, "Invalid member type: " + str(type(member))
        for user in self._users:
            if user._name == member:
                user.toggle_being_bullied()
                user.be_bullied()
                return
        return "Failed to bully: " + member

    def bully_targets(self, channel):
        for user in self._users:
            if user.being_bullied():
                bully(channel, user)
'''
                
async def bully(channel, user):
    await channel.send(user._name + ", you suck")
    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for user in client.users:
        newUser = UserDataPrefs(name = user.name, discriminator=user.discriminator)
        users.append(newUser)
        being_bullied.append(newUser)
        

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('ping'):
        await message.channel.send('Pong, Bitches!')
    if message.content == '!list':
        await message.channel.send(str(message.guild.members))
    else:
        await message.channel.send('No, fuck you.')
    
    for user in being_bullied:
        print(user.name(), message.author)
        if user.name() == str(message.author):
            print('FOUND SAME USER')
            await bully(message.channel, user)


users = []
being_bullied = []

client.run('NzEzMTI4MDg5NDMzMTQ1NDg0.Xsbmwg.2F8DiHDWPQZjCfY1PB43Dcge2BE')