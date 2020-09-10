# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 14:34:41 2020

@author: josep
"""

# Restricted Channel:
#   Channels where people must get moderator approval to add new text 
#   and voice channels

import discord

# Public Channels are areas where people can make text and voice channels
# Whenever they want to

class RestrictChan: # Creates a restricted category channel with CLUB MEMBER role read and write permissions for club members and CLI access for club convenors
    # Is the same as a public channel, except that 
    Convenor_abstract_permissions = None
    convenor_color = discord.Colour.red()
    Member_abstract_permissions = None
    def __init__(self, guild, moderator, channelName):
        # Make a cli where commands from club conveners here can shape club below.
        # Have list of all voice and text channels owned by the club.
        # Can only influence voice/text channels owned by this club object.
        # Clubs are the only things that can act on the server. Conveners can act
        # on club objects.

        #Auto give at least one person convener access to the club.
        # Needs functionality to give other ECStudents convener roles.
        self._guild = guild
        self._moderator = moderator
        self._channelName = 'r-' + channelName
                
        
    async def _init(self):
        '''
        CREATE & ASSIGN ROLES. (Expandable to include mods, operators, etc.)
        '''
        # Create convenor role 
        self._convener_role = await self._guild.create_role(name=self._channelName + " Moderator_", colour=RestrictChan.convenor_color)
        # assign convener role
        await self._moderator.add_roles(self._convener_role)

        '''
        CREATE HOLDER FOR CLUB ASSOCIATED STUDENT ROLES
        '''            
        self._club_roles = [self._convener_role] + [role for role in self._guild.roles if role.name in ['ECStudent', 'ECFaculty']]
        
        '''
        CREATE CATEGORY CHANNEL W/ CLUB ASSOCIATED STUDENT ROLES PARTICIPATION PRIVILEDGES
        '''
        # Create  channel
        self._category = await self._guild.create_category(name=self._channelName)
        for role in self._guild.roles:
            await self._category.set_permissions(role, read_messages=False, send_messages=False)
        for role in self._club_roles:
            await self._category.set_permissions(role, read_messages=True, send_messages=True, connect=True, speak=True)
        
        '''
        CREATE CATEGORY DEFAULT TEXT CHANNELS
        '''
        # Create CLI text channel
        self._cli = await self._category.create_text_channel(self._channelName + "-moderator_-command-line")
        # And make it private to all but conveners
        for role in self._guild.roles:
            await self._cli.set_permissions(role, read_messages=False, send_messages=False)
        await self._cli.edit(topic = 'Only Moderators can use this channel')
        await self._cli.set_permissions(self._convener_role, read_messages=True, send_messages=True)
        await self._cli.send(RestrictChanSuite.get_help_message(self._cli))       
        
        
        # Only Conveners of this club can post in this channel
        # textchannel.set_permissions(rolename, read_messages=True, write_messages=True)
#        self._cli_channel_id = None # Cli channel for the club

        # Conveners and members of this club can post in this channel. (Use textchannel.set_permissions)
    def __repr__(self):
        return self._cli_channel_id
    
class RestrictChanSuite:
    def get_all_restrictchans(guild): # returns list of club categories
        roleNames= []
        for role in guild.roles:
            roleNames.append(role.name)
        return filter(lambda x: x.name + ' Moderator_' in roleNames, guild.channels)
    
    '''
    Resolve club category from club category name
    '''
    def get_restrictchan(clubs, name):
        for club in clubs:
            if club.name == name:
                return club
        return None
    
    def get_restrictchan_roles(club):
        roles = []
        for role in club.guild.roles:
            if role.name.startswith(club.name):
                roles.append(role)
        return roles
    
    '''
    Resolve club role from club and full role name
    '''
    def get_role(club, roleName):
        for role in club.guild.roles:
            print(role.name, roleName)
            if role.name == roleName:
                return role
        return None
    
    def get_cli(category):
        for channel in category.channels:
            if category.name.lower() + '-moderator_-command-line' == channel.name.lower():
                return channel
        return False
    
    '''
    Returns club category that matches proposed cli if there is one.
    '''
    def is_cli(clubs, channel):
        for club in clubs:
            if club.name.lower() + "-moderator_-command-line" == channel.name:
                return club
        return False

    '''
    Create a new role for the club.
    Club - a guild category
    role_name: a string of the new role name. Ex: Organizer
    permissions: Permissions item to give the role
    '''
    async def add_role(club, role_name, permissions):
        raise NotImplementedError('Not Applicable Here')
        #await club.guild.create_role(club.name + ' ' + role_name, permissions) # Unstable.

    async def add_role_to_user(club, member, role):
        await member.add_roles(RestrictChanSuite.get_role(club, role))
    # Add new convener to the club
    async def add_moderator(club, member, moderator_role_name=None):
        if moderator_role_name == None:
            moderator_role_name = club.name + ' Moderator_'
        await member.add_roles(RestrictChanSuite.get_role(club, moderator_role_name))

    async def ban_member(self, member):
        # permaban member from the pubchannel
        # do not allow join if on a list, i guess
        pass
    def unban_member(self, member):
        # unban member from the pubchannel
        # remove from the list, i guess
        pass
    
    '''
    add text channel to resolved club category channel
    '''
    async def add_text_channel(club, channelName):
        # add a text channel to this category.
        await club.create_text_channel(channelName)
    
    async def remove_text_channel(club, channel_name):
        #remove text channel from category
        channel_name = channel_name.lower()
        for channel in club.text_channels:
            if channel.name.lower() == channel_name:
                await channel.delete()
                return True
        return False
    
    '''
    add text channel to resolved club category channel
    '''
    async def add_voice_channel(club, channelName):
        #add voice channel to category
        await club.create_voice_channel(channelName)
        
    async def remove_voice_channel(club, channel_name):
        #remove voice channel from this category
        channel_name = channel_name.lower()
        for channel in club.voice_channels:
            if channel.name == channel_name:
                await channel.delete()
                return True
        return False
    
    async def delete_category(club): # Provide your category
        # Ask "are you sure" in the discord cli. if yes, delete the category.
        # if no, don't. Return true or false if category was successfully/unsuccessfully deleted, respectively.
        # Remove the clubnameX roles from the discord.        
        
        '''
        TAKE LOG OF ALL PRIOR ACTIVITY FROM ALL EXISTING TEXT CHANNELS
        '''
        #TODO
        
        '''
        DELETE ASSOCIATED CHANNELS & CATEGORIES
        '''        
        for channel in club.text_channels + club.voice_channels:
            await channel.delete()
            
        
        '''
        DELETE ASSOCIATED CLUB ROLES
        '''
        for role in RestrictChanSuite.get_pubchan_roles(club):
            await role.delete()
        
        await club.delete()

    def get_restrictchan_commands():
        return ['!addrole - notimplemented','!addmember [member]- adds a member','!kick [member] - removes a member','!addvoicechannel [name] - adds a voice channel','!addtextchannel [name] - adds a text channel','!addconvener [member] - makes [member] a convener', '!ban [member] - unimplemented', '!unban [member] - unimplemented', '!closeclub - closes your club',
                '!removevoicechannel [name] - remove voice channel', '!removetextchannel [name] - remove text channel']
    def get_restrictchan_command_examples():
        return # not implemented
    
    def get_help_message(channel):
        commands = RestrictChanSuite.get_restrictchan_commands()
        send_text = 'Moderator_ Commands in ' + channel.name + ' are:\n\t'
        for command in commands:
            send_text += command + '\n\t'
        return send_text
    async def process_commands(message):
        content = message.content.lower()
        try:
            maybe_restrict_chan = RestrictChanSuite.is_cli(RestrictChanSuite.get_all_restrictchans(message.channel.guild), message.channel) #''' This will break the program later. message.channel can be a DM channel. find a way to make it so that that wont break the channel'''
            if content.startswith('!addtextchannel'):
                await RestrictChanSuite.add_text_channel(maybe_restrict_chan, content[len('!addtextchannel '):])
            elif content.startswith('!removetextchannel'):
                await RestrictChanSuite.remove_text_channel(maybe_restrict_chan, content[len('!removetextchannel '):])
            elif content.startswith('!addvoicechannel'):
                await RestrictChanSuite.add_voice_channel(maybe_restrict_chan, content[len('!addvoicechannel '):])
            elif content.startswith('!removevoicechannel'):
                await RestrictChanSuite.add_voice_channel(maybe_restrict_chan, content[len('!removevoicechannel '):])
            return True
        except:
            print('could not find restrictchannelcommandline'); return False
            

        try:
            command, chanName, name = content.split(' ')
        except:
            await message.channel.send('Invalid command: ' + message.content, delete_after = 5)
            return 
        rschan = RestrictChanSuite.get_restrictchan(RestrictChanSuite.get_all_restrictchans(message.channel.guild), chanName.upper())
        rschan_cli = RestrictChanSuite.get_cli(rschan)
        if rschan:
            if content.startswith('!addtextchannel'):
                await rschan_cli.send(message.author.name + ' would like to add a text channel to this restricted group: ' + name + '. Would anyone like to take care of that?')
                # remove a text channel from a hangout space.
            elif content.startswith('!removetextchannel'):
                await rschan_cli.send(message.author.name + ' would like to remove a text channel to this restricted group: ' + name + '. Would anyone like to take care of that?')
            elif content.startswith('!addvoicechannel'):
                await rschan_cli.send(message.author.name + ' would like to add a voice channel to this restricted group: ' + name + '. Would anyone like to take care of that?')
            elif content.startswith('!removevoicechannel'):
                await rschan_cli.send(message.author.name + ' would like to remove a voice channel to this restricted group: ' + name + '. Would anyone like to take care of that?')
            await message.channel.send('We heard your request. Our moderators will respond to your request soon :)', delete_after = 5)
            return True
        else:
            message.channel.send('There is no restricted channel called: ' + chanName + '! Try again! We hope to help you in some way!')
            