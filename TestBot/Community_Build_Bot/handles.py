# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 14:05:37 2020

@author: josep
"""
import discord
import smtplib, ssl
from datetime import datetime
from random import random


auth_channel = 'auth'
domain_dest = '@earlham.edu'
send_account_email='earlhamhackerscontrol@gmail.com'
account_password = 'Z1iCriDx$16yBjf1!2#8JH'

student_role_name = 'ECStudent'
faculty_role_name = 'ECFaculty'

clubs = []
users = []


class User:
    def __init__(self, guild, member):
        #send a message to the user asking for their pre-@earlham.edu email part
        # send an auth code
        # if they get the code right, delete them from this class and add them to the ECMember class
        # If after 24 hours they are not an ECMember, kick them out of the server.
        
        self._guild = guild
        self._member = member

        # Get the auth role from the guild.
        
        
        
        
        #Record the time
        #self._time = None
        
        #their authcode:
        self._authcode = 'AUTH' + str(random())
        
        # and their email prefix.
        self._email_prefix = None
    async def _init(self, authRole = 'auth', authChannel = 'please authenticate'):
        '''
        Assert there is an Auth Role in the server. If there is no auth role, immediately kick the user out of the server/
        Assert there is an Auth Channel in the server. If there is no such auth channel, immediately kick the user out of the server/
        
        '''
        # TODO
        self._authRole = None
        self._authChannel = None
        for role in self._guild.roles:
            if role.name == authRole:
                self._authRole = role
                break
        for channel in self._guild.text_channels:
            if channel.name == authChannel:
                self._authChannel = channel
                break
        if self._authRole == None:
            self._authRole = await self._guild.create_role(name=authRole, colour=discord.Colour.from_rgb(255,255,255))
            #raise AssertionError("THERE IS NO AUTH ROLE IN THE SERVER... KICKED NEW USER")
        if self._authChannel == None:
            self._authChannel = await self._guild.create_text_channel(authChannel)
            await self._authChannel.set_permissions(self._guild.default_role, read_messages = False)
            await self._authChannel.set_permissions(self._authRole, read_messages=True, send_messages=True)
            await self._authChannel.send('''Welcome! To get started, please type in an '!' followed by your Zimbra username, minus the @earlham.edu\n
Ex. !jnislam18\n
You should see an email from earlhamhackerscontrol@gmail.com in your zimbra email. Enter the code into the chat.
                                         ''')
            #raise AssertionError("THERE IS NO AUTH CHANNEL IN THE SERVER... KICKED NEW USER")
        
        '''Give the new user authentication priviledges'''
        await self._member.add_roles(self._authRole)
        
        '''AND AUTHENTICATE'''
        # Record authentication start time
        self._now = datetime.now()
        # Send message asking for their pre-earlham@earlham.edu email part (Do i want to do this?)
        
    def send_auth_email_to_addr(self, email_prefix, domain_dest,send_account_email, account_password):
        self._email_prefix = email_prefix
        port = 465
        password = account_password
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("earlhamhackerscontrol@gmail.com", password)
            # TODO: Send email here
            sender_email = send_account_email#"@gmail.com"
            receiver_email = email_prefix + domain_dest
            message = 'From:'+ sender_email + '\r\nTo: '+receiver_email + """\r\nSubject: Time to join the ECDigitalCommunity...\r\n\r\n
            
            Hello """ + self._member.name + """,
                Copy \"!auth """+ self._authcode + """\" into the auth discord channel to join the ECDigitalCommunity."""
            server.sendmail(sender_email, receiver_email, message)
            server.close()
    def getResponse(self):
        # Get all messages. If not number of digits in the authcode, it's an address.
        # Send email out.
        # otherwise, it's an authcode. attempt authorization.
        pass
    async def authenticate(self, authcode, student_role_name, faculty_role_name):
        # Get their user information. Make an ECMember object and return it with their creds
        '''AUTHENTICATE. FIGURE OUT WHETHER STUDENT OR FACULTY LATER'''
        '''NOT FINISHED. MUST FIX TO BE MORE GENERAL, BUT FOR FUTURE RENDITIONS'''
        if authcode == self._authcode:
            #make an ecmember,
            print('successfully authenticated')
            new_member, role_name = (ECStudent(self._member), student_role_name) if User.valid_student_email(self._email_prefix) else (ECFaculty(self._member),faculty_role_name) # FIX TO BE MORE GENERAL LATER
            await self._member.remove_roles(self._authRole)
            await new_member._init(role_name=role_name)
            return True
        # post message of failed authentication
        # wait three seconds and then delete message of failed authentication
        
        return False #ECMember()
    
    async def attempt_kick(self):
        # kick them out if the time is >= 24 hours after self._now.
        # Deletes them from the server.
        # returns true if kicked. False otherwise.
        timedelta = datetime.now() - self._now
        if timedelta.days >= 1:
            await self._member.kick()
            
    def is_int(string):
        try:
            return int(string)
        except:
            return False
    
    def valid_student_email(earlham_email_handle):
        year = User.is_int(earlham_email_handle[-2:])
        return (year and 17 <= year <= 20)
class ECMember:
    def __init__(self):
        # give them access to information channel and meet & greet channels.
        #   Give them access to read messages in digital advertisement text channel.
        # Give them ability to dm users, see user roles
        pass
    
class ECStudent(ECMember):
    def __init__(self, member):
        # Give them ability to join and start clubs.
        ECMember.__init__(self)    
        self._member = member
    async def _init(self, role_name='ECSTUDENT', role_color='Magenta'):
        ''' 
        Assert there is an ECSTUDENT ROLE. if there isn't, make one.
        and add general member permissions to said role.
        '''
        student_role_name = role_name
        student_role_color= role_color
        guild = self._member.guild
        student_role = None
        for role in guild.roles:
            if role.name == student_role_name:
                student_role = role
                break
        if student_role == None:
            # make the role and add general permissions
            student_role = await guild.create_role(name=student_role_name, colour=discord.Colour.magenta()) # FIX TO ACTUALLY SUPPORT COLORS LATER
            #await student_role.set_permissions( blah blah)
        await self._member.add_roles(student_role) 
        
        
        # Give the member the ECSTUDENT role    
        # Give the ECStudent Role
        
        # permissions for botty commands will line up based on the user's object type
        #   Play games

class ECFaculty(ECMember):
    def __init__(self, member):
        # Give them the ability to join and advise clubs.
        ECMember.__init__(self)    
        self._member = member
    
    async def _init(self, role_name='ECFACULTY', role_color='teal'):
        ''' 
        Assert there is an ECFACULTY ROLE. if there isn't, make one.
        and add general member permissions to said role.
        '''
        faculty_role_name = role_name
        faculty_role_color = role_color
        guild = self._member.guild
        faculty_role = None
        for role in guild.roles:
            if role.name == faculty_role_name:
                faculty_role = role
                break
        if faculty_role == None:
            # make the role and add general permissions
            faculty_role = await guild.create_role(name=faculty_role_name, colour=discord.Colour.teal()) # FIX TO ACTUALLY SUPPORT COLORS LATER
            #await faculty_role.set_permissions( blah blah)
        await self._member.add_roles(faculty_role) 


class Organizer(ECStudent):
    def __init__(self):
        # Allow access to post in digital advertisement message channel
        pass

class Convener(ECStudent):
    def __init__(self):
        # Give them the ability to kick, ban members from club text, call channels
        # Give them club text, call channels.
        # Give them ability to post in Digital Advertisement Board.
        # Give them channel to issue bot commands for their club:
        #   Approve members
        #   Kick, ban, mute, deafen, etc different members.
        #   Make a new spinoff text channel for their club
        #   Make a new spinoff voice/video channel for their club
        #   Delete spinoff channels from their club.
        #   Request addition of new bots to server for their club.
        #   Manage new bot locations and permissions.
        pass        
        # Give the member the ECFACULTY role
class Admin(ECMember):
    def __init__(self):
        # Give them the admin role.
        # Give them ability to kick, ban, mute, users across channels.
        ECMember.__init__(self)
        
class SuperAdmin(Admin):
    def __init__(self):
        # Give ability to close, open new text & voice channels.
        Admin.__init__(self)
