from fbchat import Client, log
from fbchat.models import *
import getpass
import random
import time
from fbchat import log, Client

people = {"100002271757479": "Aarush", 
          "100021112489734": "Arul", 
          "100022270536490": "Avyay",
          "100025774035153": "Karan"}

# Subclass fbchat.Client and override required methods
greetings = ['hello there', 'wassup', 'im aruls biggest fan']

class Poll:
    
    def __init__(self, name, options):
        self.key_to_options = {}
        self.individualVotes = {}
        self.name = name
        for option in options:
            self.key_to_options[option] = []
            
    def get_summary(self):
        self.key_to_options = sorted(self.key_to_options.items(), key=lambda x: x[1], reverse = True)
        message_text = self.name + "\n"
        for option in self.key_to_options.keys():
            message_text += option + " " + str(self.key_to_options[option]) + "\n"
        return message_text
        
class CustomClient(Client):
    polls = []
    arul_on = False
    def arul(self, text, mid, thread_id, thread_type):
        time.sleep(3)
        final_message = Message(text=text)
        time.sleep(3)
        self.sendRemoteImage("https://identity.stanford.edu/img/block-s-2color.png", Message(text='Stanford?'), thread_id=thread_id, thread_type=thread_type)
        time.sleep(3)
        self.sendRemoteImage("https://upload.wikimedia.org/wikipedia/en/thumb/2/29/Harvard_shield_wreath.svg/1200px-Harvard_shield_wreath.svg.png", Message(text='Harvard?'), thread_id=thread_id, thread_type=thread_type)
        time.sleep(3)
        self.sendRemoteImage("https://i.pinimg.com/originals/b8/4f/0c/b84f0cfdee91f36c170a5e33bbc0ae66.jpg", Message(text='MIT?'), thread_id=thread_id, thread_type=thread_type)
        time.sleep(3)
        self.send(final_message, thread_id=thread_id, thread_type=thread_type)
        time.sleep(3)
        self.reactToMessage(mid, MessageReaction.LOVE)
    def countFrequency(self, my_dictionary): 
        # Creating an empty dictionary  
        freq = {} 
        for item in my_dictionary.values(): 
            if (item in freq): 
                freq[item] += 1
            else: 
                freq[item] = 1
        return freq 
    def remove(self, text, mid, thread_id, thread_type):
        time.sleep(3)
        final_message = Message(text=text)
        time.sleep(3)
        self.send(final_message, thread_id=thread_id, thread_type=thread_type)
        time.sleep(3)
        self.reactToMessage(mid, MessageReaction.ANGRY)
        time.sleep(3)
        self.removeUserFromGroup(self.uid, thread_id=thread_id)
        
    def add(self, thread_id, thread_type, member_id):
        time.sleep(3)
        self.addUsersToGroup(member_id, thread_id=thread_id)
        
    def say(self, text, mid, thread_id, thread_type):
        time.sleep(3)
        final_message = Message(text=text)
        self.send(final_message, thread_id=thread_id, thread_type=thread_type)
    
    def create_poll(self, text, mid, thread_id, thread_type):
        time.sleep(3)
        messy_poll_data = text.split(" ")
        name_of_poll = messy_poll_data[1]
        choices = messy_poll_data[2:]
        poll_summary = name_of_poll.upper() + "\n"
        for choice in choices:
            poll_summary += choice + "\n"
        self.say(poll_summary, mid, thread_id, thread_type)
        time.sleep(3)
        self.polls.append(Poll(name=name_of_poll, options=choices))

    def respond_to_poll(self, text, author_id,  mid, thread_id, thread_type):
        time.sleep(3)
        messy_poll_data = text.split(" ")
        name_of_poll = messy_poll_data[1]
        choice = messy_poll_data[2].lower()
        for poll in self.polls:
            if poll.name == name_of_poll:           
                if author_id not in poll.individualVotes.keys() :
                    poll.individualVotes.append(author_id, choice)
                    frequencies = countFrequency(poll.individualVotes)
                    poll.key_to_options[choice] = frequencies[choice]
                else :
                    poll.individualVotes[author_id] = choice
                    frequencies = countFrequency(poll.individualVotes)
                    poll.key_to_options[choice] = frequencies[choice]
                self.say(poll.get_summary(), mid, thread_id, thread_type)
                break
                
    def onPersonRemoved(self, removed_id, author_id, thread_id, **kwargs):
        if thread_id == "1736268456466047":
            if removed_id != self.uid:
                self.addUsersToGroup(removed_id, thread_id=thread_id)    
            
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, **kwargs):
        time.sleep(3)
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        message_text = message_object.text.lower()
        person_speaking = ""
        
        if author_id in people:
            person_speaking = people[author_id]
        
        if author_id != self.uid:
            
            if message_text == "spam on":
                self.arul_on = True
            if message_text == "spam off":
                self.arul_on = False

            if message_text == "kick ma dude":
                self.remove("i hate u!", mid, thread_id, thread_type)
                
            elif message_text[0:4] == "poll":
                self.create_poll(message_text, mid, thread_id, thread_type)
            
            elif message_text[0:8] == "fillpoll":
                self.respond_to_poll(message_text, author_id, mid, thread_id, thread_type)
            
            elif "arul" in message_text.lower() and self.arul_on == True:
                self.arul("heyyy arul ;)", mid, thread_id, thread_type)
                  
                
client = CustomClient('legomations10@gmail.com', getpass.getpass())

client.listen()
