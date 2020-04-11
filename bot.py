from fbchat import Client, log
from fbchat.models import *
import getpass
import random
import time

from fbchat import log, Client
people = {"100002271757479": "Aarush", "100021112489734": "Arul", "100022270536490": "Avyay", "100025774035153": "Karan"}
# Subclass fbchat.Client and override required methods
greetings = ['hello there', 'wassup', 'im aruls biggest fan']
class CustomClient(Client):
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, **kwargs):
        time.sleep(5)
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)
        person = ""
        text = ""
        if author_id in people:
            person = people[author_id]

        if person == "Arul":
            text = "@Arul Verma. I love you. Visit Stanford at stanford.edu!"
            
            final_message = Message(text=text, mentions=[Mention(thread_id=thread_id, offset=0, length=11)])
            self.send(final_message, thread_id=thread_id, thread_type=thread_type)
            self.reactToMessage(mid,MessageReaction.LOVE)
            self.changeThreadTitle("Arul Party Squad Hell Yea", thread_id=thread_id, thread_type=thread_type)
            time.sleep(10)
            self.changeThreadTitle("Legit Group #BKDJV", thread_id=thread_id, thread_type=thread_type)

        elif person == "Karan":
            self.sendRemoteImage("https://scontent-sjc3-1.xx.fbcdn.net/v/t1.15752-9/92789860_520272552260274_6942702805920514048_n.png?_nc_cat=111&_nc_sid=b96e70&_nc_oc=AQmDdjqWaPzXNlRv_uIZ9TX_V1k06-mUQQcGFiSFhZrqN7S5HGeXV3l6Yjx2CkYceo8&_nc_ht=scontent-sjc3-1.xx&oh=18f2fc90fce16f95d22dfb94b9ea0705&oe=5EB3F180", Message(text='Hehe Karan we will never forget!'), thread_id=thread_id, thread_type=thread_type)
        
        # elif person == "Aarush":
            
        elif author_id != self.uid:
            if 'arul' in message_object.text.lower():
                text = 'Did I just hear Arul? I love him! Go Arul!'
                final_message = Message(text=text)

                self.sendRemoteImage("https://identity.stanford.edu/img/block-s-2color.png", Message(text='Stanford?'), thread_id=thread_id, thread_type=thread_type)
                
                self.sendRemoteImage("https://upload.wikimedia.org/wikipedia/en/thumb/2/29/Harvard_shield_wreath.svg/1200px-Harvard_shield_wreath.svg.png", Message(text='Harvard?'), thread_id=thread_id, thread_type=thread_type)
                
                self.sendRemoteImage("https://i.pinimg.com/originals/b8/4f/0c/b84f0cfdee91f36c170a5e33bbc0ae66.jpg", Message(text='MIT?'), thread_id=thread_id, thread_type=thread_type)

                self.send(final_message, thread_id=thread_id, thread_type=thread_type)
                self.reactToMessage(mid,MessageReaction.LOVE)
            if 'azul' in message_object.text.lower():
                final_message = Message(text=random.choice(greetings))
                self.send(final_message, thread_id=thread_id, thread_type=thread_type)
            if 'i hate azul' in message_object.text.lower():
                final_message = Message(text="you killed me!")
                self.send(final_message, thread_id=thread_id, thread_type=thread_type)
                self.removeUserFromGroup(self.uid, thread_id=thread_id)

client = CustomClient('vermlaccc@gmail.com', getpass.getpass())
client.listen()
