# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 14:08:39 2020

@author: josep
"""

import discord

def get_member_by_discord_name(guild, discord_name):
    for member in guild.members:
        if member.name + "#" + member.discriminator == discord_name:
            return member
    return False

class Club: # Creates a club category channel with CLUB MEMBER role read and write permissions for club members and CLI access for club convenors
    Convenor_abstract_permissions = None
    convenor_color = discord.Colour.blue()
    Member_abstract_permissions = None
    def __init__(self, guild, convener, clubName):
        # Make a cli where commands from club conveners here can shape club below.
        # Have list of all voice and text channels owned by the club.
        # Can only influence voice/text channels owned by this club object.
        # Clubs are the only things that can act on the server. Conveners can act
        # on club objects.

        #Auto give at least one person convener access to the club.
        # Needs functionality to give other ECStudents convener roles.
        self._guild = guild
        self._convener = convener
        self._clubName = 'c-' + clubName
                
        
    async def _init(self):
        '''
        CREATE & ASSIGN ROLES. (Expandable to include mods, operators, etc.)
        '''
        # Create convenor role 
        self._convener_role = await self._guild.create_role(name=self._clubName + " Convener", colour=Club.convenor_color)
        # assign convener role
        await self._convener.add_roles(self._convener_role)
        
        # Create member role
        self._member_role = await self._guild.create_role(name=self._clubName + " Member")

        '''
        CREATE HOLDER FOR CLUB ASSOCIATED STUDENT ROLES
        '''            
        self._club_roles = [self._convener_role, self._member_role]
        
        '''
        CREATE CATEGORY CHANNEL W/ CLUB ASSOCIATED STUDENT ROLES PARTICIPATION PRIVILEDGES
        '''
        # Create  channel
        self._category = await self._guild.create_category(name=self._clubName)
        for role in self._guild.roles:
            await self._category.set_permissions(role, read_messages=False, send_messages=False)
        for role in self._club_roles:
            await self._category.set_permissions(role, read_messages=True, send_messages=True, connect=True, speak=True)
        '''
        CREATE CATEGORY DEFAULT TEXT CHANNELS
        '''
        # Create CLI text channel
        self._cli = await self._category.create_text_channel(self._clubName + "-convenor-command-line")
        # And make it private to all but conveners
        for role in self._guild.roles:
            await self._cli.set_permissions(role, read_messages=False, send_messages=False)
        await self._cli.edit(topic = 'Only Conveners can use this channel')
        await self._cli.set_permissions(self._convener_role, read_messages=True, send_messages=True)
        await self._cli.send(ClubSuite.get_help_message(self._cli))       
        
        
        # Only Conveners of this club can post in this channel
        # textchannel.set_permissions(rolename, read_messages=True, write_messages=True)
#        self._cli_channel_id = None # Cli channel for the club

        # Conveners and members of this club can post in this channel. (Use textchannel.set_permissions)
    def __repr__(self):
        return self._cli_channel_id
    

class ClubSuite:
    def get_all_clubs(guild): # returns list of club categories
        roleNames= []
        for role in guild.roles:
            roleNames.append(role.name)
        return filter(lambda x: x.name + ' Convener' in roleNames, guild.channels)
    
    '''
    Resolve club category from club category name
    '''
    def get_club(clubs, name):
        for club in clubs:
            if club.name.lower() == name.lower():
                return club
        return None
    
    def get_club_roles(club):
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
    
    '''
    Returns club category that matches proposed cli if there is one.
    '''
    def is_cli(clubs, channel):
        for club in clubs:
            if club.name.lower() + "-convenor-command-line" == channel.name:
                return club
        return False
    '''
    Returns the cli for the given club category channel
    '''
    
    def get_cli(category):
        for channel in category.channels:
            if category.name.lower() + '-convenor-command-line' == channel.name.lower():
                return channel
        return False

    '''
    Create a new role for the club.
    Club - a guild category
    role_name: a string of the new role name. Ex: Organizer
    permissions: Permissions item to give the role
    '''
    async def add_role(club, role_name, permissions):
        await club.guild.create_role(club.name + ' ' + role_name, permissions) # Unstable.

    async def add_role_to_user(club, member, role):
        await member.add_roles(ClubSuite.get_role(club, role))
    # Add new convener to the club
    async def add_convener(club, member, convener_role_name=None):
        if convener_role_name == None:
            convener_role_name = club.name + ' Convener'
        await member.add_roles(ClubSuite.get_role(club, convener_role_name))

    # Add new members to the club
    async def add_member(club, member, member_role_name=None):
        if member_role_name == None:
            member_role_name = club.name + ' Member'
        await member.add_roles(ClubSuite.get_role(club, member_role_name))
    
    async def kick_member(club, member, member_role_name=None):
        if member_role_name == None:
            member_role_name = club.name + ' Member'
        await member.remove_roles(ClubSuite.get_role(club, member_role_name))
        
    async def ban_member(self, member):
        # permaban member from the club
        # do not allow join if on a list, i guess
        pass
    def unban_member(self, member):
        # unban member from the club
        # remove from the list, i guess
        pass
    
    '''
    add text channel to resolved club category channel
    '''
    async def add_text_channel(club, channelName):
        # add a text channel to this category.
        await club.create_text_channel(channelName)
    
    async def remove_text_channel(club, channel_name):
        channel_name = channel_name.lower()
        #remove text channel from category
        for channel in club.text_channels:
            if channel.name.lower() == channel_name:
                await channel.delete()
                return True
        return False
    
    async def get_text_channel(club, channel_name):
        channel_name = channel_name.lower()
        #remove text channel from category
        for channel in club.text_channels:
            if channel.name.lower() == channel_name:
                return channel
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
        for role in ClubSuite.get_club_roles(club):
            await role.delete()
        
        await club.delete()

    def get_club_commands():
        return ['!describe description - Registers your club description. You can put spaces in description.', 
                '!pin channel-to-pin-to-in-club message-to-pin - Pins message-to-pin to channel-to-pin-to-in-club',
                '!unpin channel-to-unpin-from-in-club copypaste-message-to-unpin - unpins the message copy pasted from pinned messages from channel-to-unpin-from-in-club',
                '!requestbot What you want your bot to do - Ask the Manager Bot Developers to make your club a bot! (They will get back to you with questions)',
                '!kick member - Removes a member',
                '!addvoicechannel name - Adds a voice channel',
                '!addtextchannel name - Adds a text channel',
                '!addconvener member - Makes member a convener', 
                '!ban member - Unimplemented', '!unban member - Unimplemented',
                '!closeclub - Closes your club',
                '!removevoicechannel name - Remove voice channel',
                '!removetextchannel name - Remove text channel',
                '!convenerhelp - Displays this message']
    
    def get_club_command_examples():
        return # not implemented
    
    def get_help_message(channel):
        commands = ClubSuite.get_club_commands()
        send_text = 'Convener Commands in ' + channel.name + ' are:\n\t'
        for command in commands:
            send_text += command + '\n\t'
        return send_text
    
    async def processes_inc_command(message):
        content = message.content.lower()
        try:
            maybe_club = ClubSuite.is_cli(ClubSuite.get_all_clubs(message.channel.guild), message.channel) #''' This will break the program later. message.channel can be a DM channel. find a way to make it so that that wont break the channel'''
            if maybe_club == False:
                print(content)
                if content.startswith('!describeclub'):
                    cli = ClubSuite.get_cli(ClubSuite.get_club(ClubSuite.get_all_clubs(message.channel.guild), 'C-' + content[len('!describeclub '):]))
                    if cli != False:
                        for pin in await cli.pins():
                            if pin.content.startswith('DESCRIPTION SET TO: '):
                                await message.channel.send(content[len('!describeclub '):] + '\'s description is: ' + pin.content[len('DESCRIPTION SET TO: '):])
                                return True
                        await message.channel.send('Aww... ' + content[len('!describeclub '):] + ' hasn\'t set a description yet. Check back later!')
                        return True
                return False
        except:                
            print('could not find guild')
            return False
        
        if content.startswith('!addtextchannel '): # Add club text channel
            await ClubSuite.add_text_channel(maybe_club, content[len('!addtextchannel '):]); return True
        elif content.startswith('!removetextchannel'): # remove club text channel
            await ClubSuite.remove_text_channel(maybe_club, content[len('!removetextchannel '):]); return True
        elif content.startswith('!addvoicechannel'): #add club voice channel
            await ClubSuite.add_voice_channel(maybe_club, content[len('!addvoicechannel '):]); return True
        elif content.startswith('!removevoicechannel'): # remove club voice channel
            await ClubSuite.remove_voice_channel(maybe_club, content[len('!removevoicechannel '):]); return True
        elif content.startswith('!closeclub'):
            await ClubSuite.delete_category(maybe_club); return True
        elif content.startswith('!addmember'):
            member = get_member_by_discord_name(message.guild, content[len('!addmember '):])
            await ClubSuite.add_member(maybe_club, member); return True
        elif content.startswith('!addconvener'):
            member = get_member_by_discord_name(message.guild, content[len('!addconvener '):])#'''ADDCONVENER NEEDS SOME WORK'''
            await ClubSuite.add_convener(maybe_club, member); return True
        elif content.startswith('!kick'):
            member = get_member_by_discord_name(message.guild, content[len('!kick '):])
            await ClubSuite.kick_member(maybe_club, member); return True
        elif content.startswith('!convenerhelp'):
            await message.channel.send(ClubSuite.get_help_message(message.channel)); return True
        elif content.startswith('!describe'):
            await (await message.channel.send('DESCRIPTION SET TO: ' + content[len('!describe '):])).pin()
            return True
        elif content.startswith('!pin'):
            terms = content.split(' ')
            if len(terms) < 3:
                await message.channel.send('!pin requires 3 things! Here\'s an example: !pin MyClubTextChannel what I want to pin and you can include spaces here', delete_after = 10)
            channel = await ClubSuite.get_text_channel(maybe_club, terms[1])
            if channel != False:
                await (await channel.send(' '.join(terms[2:]))).pin()
        elif content.startswith('!unpin'):
            terms = content.split(' ')
            if len(terms) < 3:
                await message.channel.send('!pin requires 3 things! Here\'s an example: !pin MyClubTextChannel what I want to pin and you can include spaces here', delete_after = 10)
            channel = await ClubSuite.get_text_channel(maybe_club, terms[1])
            content = ' '.join(terms[2:])
            if channel != False:
                for pin in await channel.pins():
                    if pin.content == content:
                        await pin.unpin()
                        return True
            await message.channel.send('!unpin requires 3 things! Here\'s an example: !pin TheClubChannelYourPinisin And what text copy pasted is in that pinned message', delete_after = 10)
        elif content.startswith('!requestbot'):
            await message.channel.send('We will get back to you soon with questions and information about your bot!')
            return True#unimplemented. To implement Soon
        return False
        