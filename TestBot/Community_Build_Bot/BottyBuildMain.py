# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 14:09:29 2020

@author: josep
"""

import discord
import smtplib, ssl
from datetime import datetime
from random import random
from asyncio import create_task, sleep, run

from PublicChannel import PubChanSuite, PublicChan
from ClubChannel import ClubSuite, Club
from restrictedchannel import RestrictChan, RestrictChanSuite
from handles import User, ECMember, ECStudent, ECFaculty, Organizer, Convener, Admin, SuperAdmin



def get_member_by_discord_name(guild, discord_name):
    for member in guild.members:
        if member.name + "#" + member.discriminator == discord_name:
            return member
    return False

def is_auth(channel, auth_channel_name):
    print(channel.name)
    return channel.name == auth_channel_name
    #for channel in guild.text_channels:
    #    if channel.name == auth_channel_name:
    #        return channel
    #return False


auth_channel = 'auth'
domain_dest = '@earlham.edu'
send_account_email='earlhamhackerscontrol@gmail.com'
account_password = 'Z1iCriDx$16yBjf1!2#8JH'

student_role_name = 'ECStudent'
faculty_role_name = 'ECFaculty'

clubs = []
users = []

client = discord.Client()


async def make_new_member(member):
    new_member = User(member.guild, member)
    await new_member._init(authChannel=auth_channel)
    users.append(new_member)
    return new_member

@client.event
async def on_member_join(member):
    await make_new_member(member)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    #await message.channel.send('received', delete_after=3)
    # Is it a command? if it's not a command, ignore. Otherwise, proceed.
    
    content = message.content.lower()
    if content.startswith('!'):
        '''
        Check if channel is server's auth channel. If so, allow auth commands.
        '''
        try: 
            maybe_auth = is_auth(message.channel, auth_channel)#''' This will break the program later. message.channel can be a DM channel. find a way to make it so that that wont break the channel'''
        except:
            print('could not find auth channel')
            return
        print('got auth channel: ' + str(maybe_auth))
        if maybe_auth:
            # Get the user to do auth stuff with
            auth_user = None
            for user in users:
                if user._member.id == message.author.id:
                    auth_user = user
                    break
            if auth_user == None:
                
                print("Failed to find user: " + message.author.name + ". Making new one")
                auth_user = await make_new_member(get_member_by_discord_name(message.channel.guild, message.author.name + "#" + message.author.discriminator))

            '''
            AUTH COMMANDS GO HERE
            '''
            print('made it to auth commands')
            #killer = create_task(kill_after_n(3, message)) # messages in this channel expire after 3 seconds
            if content.startswith('!auth'): # this allows users to put in their codes
                if await auth_user.authenticate(content[len('!auth '):].upper(), student_role_name, faculty_role_name) == True:
                    users.remove(auth_user)
                    await message.channel.send('Authenticatoin succeeded... Moving to Full Discord', delete_after = 3)
                else:
                    await message.channel.send('Authentication failed... ' + content[len('!auth '):] + ' is not the correct auth code', delete_after = 3)
            else: #anything else is ![prefix] which files an email attempt
                print('sent email to ' + content[len('!'):])
                auth_user.send_auth_email_to_addr(content[len('!'):], domain_dest,send_account_email, account_password)
                await message.channel.send('Send auth code to: ' + content[len('!'):], delete_after = 3)
            #run(killer)
            await message.delete(delay=3)
            return
        '''
        Check if the channel mentioned is a cli for a pubchan. If so, perform pubchan commands.
        '''
        try:
            is_admin = message.channel.name == 'admin'
            #maybe_pubchan = PubChanSuite.is_cli(PubChanSuite.get_all_pubchans(message.channel.guild, message.channel))
        except:
            is_admin = False
        if is_admin:
            '''
            moderator commands go here
            '''
            # Add, remove hangout spaces
            if content.startswith('!addpubchan'):
                clubName = content[len('!addpubchan '):].upper()
                clubs = list(PubChanSuite.get_all_pubchans(message.channel.guild))
                # make sure we're not making a duplicate club
                for i in range(len(clubs)):
                    clubs[i] = clubs[i].name
                if clubName in clubs:
                    await message.channel.send('Sorry, that pubchan name is already taken. try a different one?', delete_after = 5)
                    return
                # and make the club if not a duplicate
                newClub = PublicChan(message.guild, message.author, clubName)
                await newClub._init()
                return
            '''
            Restricted Channel commands go here
            '''
            if content.startswith('!addrestrictedchan'):
                clubName = content[len('!addrestrictedchan '):].upper()
                clubs = list(RestrictChanSuite.get_all_restrictchans(message.channel.guild))
                # make sure we're not making a duplicate club
                for i in range(len(clubs)):
                    clubs[i] = clubs[i].name
                if clubName in clubs:
                    await message.channel.send('Sorry, that restrictedchannel name is already taken. try a different one?', delete_after = 5)
                    return
                # and make the club if not a duplicate
                newClub = RestrictChan(message.guild, message.author, clubName)
                await newClub._init()
                return
            
        '''
        Check if the channel mentioned is a cli for a club. if so, perform club commands.
        '''
        # try catch around this boy
        if await ClubSuite.processes_inc_command(message):
            await message.channel.send('Succeeded...', delete_after=3)
            return
        
        '''
            GENERAL COMMANDS GO HERE
        '''
        if content.startswith('!makeclub'):
            clubName = content[len('!makeclub '):].upper()
            clubs = list(ClubSuite.get_all_clubs(message.channel.guild))
            # make sure we're not making a duplicate club
            for i in range(len(clubs)):
                clubs[i] = clubs[i].name.lower()
            if clubName in clubs:
                await message.channel.send('Sorry, that clubname is already taken. try a different one?', delete_after = 5)
                return
            # and make the club if not a duplicate
            newClub = Club(message.guild, message.author, clubName)
            await newClub._init()
            return
        elif content.startswith('!joinclub'):
            target = ('c-' + content[len('!joinclub '):]).upper()
            print('registered joinclub for' + target)
            target_club = ClubSuite.get_club(ClubSuite.get_all_clubs(message.channel.guild), target)
            await ClubSuite.add_member(target_club, message.author)

            return
            # Find club category
            # if there is a role called category [member], add the person to the role]
        elif content.startswith('!leaveclub'):
            target = ('c-' + content[len('!leaveclub '):]).upper()
            print('registered leaveclub for' + target)
            target_club = ClubSuite.get_club(ClubSuite.get_all_clubs(message.channel.guild), target)
            await ClubSuite.kick_member(target_club, message.author)
            return 
        elif content.startswith('!MAKESTUDENT'):
            student = ECStudent(get_member_by_discord_name(message.channel.guild, content[len('!MAKESTUDENT '):]))
            await student._init(role_name=student_role_name)
            return 
        elif content.startswith('!clublist'):
            clubs = ClubSuite.get_all_clubs(message.channel.guild)
            send_text = 'The clubs in ' + message.channel.guild.name + ' are: \n\t'
            for club in clubs:
                send_text += club.name[2:] + '\n\t'
            await message.channel.send(send_text)
        elif content.startswith('!examples'):
            commands = ['!clublist\n\t\t - lists all clubs in ' + message.channel.guild.name,
                        '!joinclub ECHackers\n\t\t - Joins the ECHackers Club',
                        '!leaveclub ECHackers\n\t\t - Leaves the ECHackers Club',
                        '!makeclub JelloLicking\n\t\t - Makes the JelloLicking club',
                        '!admin\n\t\t - (does nothing now) Opens a channel with you and admins', 
                        '!report person reason\n\t\t - (does nothing now) Sends a report on a person to an admin or club convener.',
                        '!addtextchannel Problems-with-admin Friend-Houses\n\t\t - Adds the Friend-Houses text channel to Problems-with-admin',
                        '!removetextchannel Problems-with-admin Friend-Houses\n\t\t - Removes the Friend-Houses text channel from Problems-with-admin (if you made it)',
                        '!addvoicechannel Problems-with-admin Friend-Houses\n\t\t - Adds the Friend-Houses voice channel to Problems-with-admin',
                        '!removevoicechannel Problems-with-admin Friend-Houses\n\t\t - Removes the Friend-Houses voice channel from Problems-with-admin (if you made it)',]
            send_text = 'Examples of commands ' + message.channel.guild.name + ' are (In order):\n\t'
            for command in commands:
                send_text += command + '\n\t'
            await message.channel.send(send_text)
            return 
        elif content.startswith('!help'):
            commands = ['!clublist\n\t\t - Lists all clubs in ' + message.channel.guild.name, '!describeclub Clubname\n\t\t - Gives a Clubname\'s self-provided description', '!joinclub Clubname\n\t\t - Joins the club Clubname', '!leaveclub\n\t\t - Leaves a server\'s club',
                        '!makeclub Clubname\n\t\t - Makes a club with the clubname Clubname','!admin\n\t\t - Opens a channel with you and admins', '!report person reason\n\t\t - Sends a report on a person to an admin or club convener.',
                        '!addtextchannel The-name-of-the-public-category The-new-channel\'s-name\n\t\t - Adds a new public text channel in a category', 
                        '!removetextchannel The-name-of-the-public-category The-new-channel\'s-name\n\t\t - Removes the public text channel YOU MADE from the category. Doesn\'t work for other people\'s channels',
                        '!addvoicechannel The-name-of-the-public-category The-new-channel\'s-name\n\t\t - Adds a new public voice channel in a category', 
                        '!removevoicechannel The-name-of-the-public-category The-new-channel\'s-name\n\t\t - Removes the public voice channel YOU MADE from the category. Doesn\'t work for other people\'s channels',]
            send_text = 'Commands in ' + message.channel.guild.name + ' are:\n\t'
            for command in commands:
                send_text += command + '\n\t'
            await message.channel.send(send_text)
            return 
        elif content.startswith('!admin'):
            await message.channel.send('not yet implemented...')
            raise NotImplementedError()
        elif content.startswith('!report'):
            await message.channel.send('not yet implemented...')
            raise NotImplementedError()
        # Try to process remaining commands as hangoutspace commands:
        if await PubChanSuite.process_commands(message):
            await message.channel.send('Succeeded... ', delete_after = 3);return
        # or as restricted suite petitions
        if await RestrictChanSuite.process_commands(message):
            await message.channel.send('Succeeded... ', delete_after = 3)
            return
        await message.channel.send('Sorry. We didn\'t process your command. Will you check for typos or ask for help and try again?', delete_after=10)
        
    # Check if a message comes in from a CLI channel. 
    #   if in a CLI channel, 
        # is it an admin channel?
        # is it a convener channel?
        # is it a ____ channel?
        #Process according to context.
    
    # Check if the message is a general command. Process accordingly.
    
    
    # moderation
    # policing
# Down the line:
# In meet & greet lobbies, link to games, shows, 
# and movies after 15 min of people talking.
# We NEED to be able to host remote events. Convocation, Speaker events, and more
client.run()