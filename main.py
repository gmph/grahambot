import StringIO
import json
import logging
import random
import urllib
import urllib2
import re

# For sending images:
from PIL import Image
import multipart


# For datastore of users and work status:
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.db import stats


# Standard app engine imports:
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2


# Telegram API and Admin Settings:
# Add a file private.py to the directory with the following code:
#
# token = 'YOUR_AUTH_TOKEN'
# admin = YOUR_CHAT_ID
#
# Note that your chat_id should be an int and your token should be a string.

from private import token, admin
BASE_URL = 'https://api.telegram.org/bot' + token + '/'
ADMIN_ON = True # Admin sees admin view by default, not user view
ADMIN_ID = admin

# Datastore Entities:

# For storing if/where I'm working:
class WorkStatus(db.Model):
    work_name = db.StringProperty(required=True)
    work_link = db.StringProperty(required=True)
    work_email = db.StringProperty(required=True)
    work_available = db.BooleanProperty(indexed=False)

# For storing extra custom messages that can be set by the admin:
class Messages(db.Model):
    message_name = db.StringProperty(required=True)
    message_content = db.StringProperty(required=True)

# For storing the details of people who use the bot:
class Contacts(db.Model):
    contact_firstname = db.StringProperty(required=True,multiline=True)
    contact_lastname = db.StringProperty(required=False,multiline=True)
    contact_id = db.StringProperty(required=True)
    contact_username = db.StringProperty(required=False)


# Work Status Functions:

def refreshWorkStatus():
    global WORK_NAME
    global WORK_LINK
    global WORK_EMAIL
    global WORK_AVAILABLE

    work_statuses = WorkStatus.all()
    work_status1 = work_statuses.fetch(1)

    for status in work_status1:
        WORK_NAME = status.work_name
        WORK_LINK = status.work_link
        WORK_EMAIL = status.work_email
        WORK_AVAILABLE = status.work_available


def setWorkStatus(name,link,email,available):
    global WORK_NAME
    global WORK_LINK
    global WORK_EMAIL
    global WORK_AVAILABLE

    if name != '':
        wnew = WorkStatus(key_name='main',
                       work_name=name,
                       work_link=WORK_LINK,
                       work_email=WORK_EMAIL,
                       work_available=WORK_AVAILABLE)
        wnew.put()
        WORK_NAME == name
    elif link != '':
        wnew = WorkStatus(key_name='main',
                       work_name=WORK_NAME,
                       work_link=link,
                       work_email=WORK_EMAIL,
                       work_available=available)
        wnew.put()
        WORK_LINK == link
    elif email != '':
        wnew = WorkStatus(key_name='main',
                       work_name=WORK_NAME,
                       work_link=WORK_LINK,
                       work_email=email,
                       work_available=WORK_AVAILABLE)
        wnew.put()
        WORK_EMAIL == email
    else:
        wnew = WorkStatus(key_name='main',
                       work_name=WORK_NAME,
                       work_link=WORK_LINK,
                       work_email=WORK_EMAIL,
                       work_available=available)
        wnew.put()
        WORK_AVAILABLE == available


# Message Functions:

def setMessage(name,content):
    mnew = Messages(key_name=name,
                   message_name = name,
                   message_content=content)
    mnew.put()


# Default Status and Handlers:

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)


def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))

class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))

class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))

# Fetch message when posted:

class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        message = body['message']
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        chat = message['chat']
        chat_id = chat['id']
        fr_username = fr.get('username')
        fr_firstname = fr.get('first_name')
        fr_lastname = fr.get('last_name')

        if not text:
            logging.info('no text')
            return

        # Message Sending Functions:

        def fwdToMe(frchatid,msgid):
            resp = urllib2.urlopen(BASE_URL + 'forwardMessage', urllib.urlencode({
                'chat_id': str(ADMIN_ID), # @grahammacphee's chat_id
                'from_chat_id': frchatid,
                'message_id': msgid,
            }))

        def replyWithBot(tochatid,msg):
            message = "Direct from Graham: " + msg
            resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                'chat_id': tochatid,
                'text': message.encode('utf-8'),
            }))

        def reply(msg=None, img=None):
            if msg:
                resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                    'chat_id': str(chat_id),
                    'text': msg.encode('utf-8'),
                    'disable_web_page_preview': 'true',
                })).read()
            elif img:
                resp = multipart.post_multipart(BASE_URL + 'sendPhoto', [
                    ('chat_id', str(chat_id)),
                    ('reply_to_message_id', str(message_id)),
                ], [
                    ('photo', 'image.jpg', img),
                ])
            else:
                logging.error('No message or image specified.')
                resp = None

            logging.info('Send response:')
            logging.info(resp)

        # For each message that arrives:

        refreshWorkStatus()

        # Type / to enable and disable admin view:

        if (chat_id == ADMIN_ID):
            global ADMIN_ON
            if text == "/":
                ADMIN_ON = not ADMIN_ON
                reply("Admin: " + str(ADMIN_ON))

        # Admin Commands:

        if (chat_id == ADMIN_ID) and (ADMIN_ON):

            global WORK_AVAILABLE
            global WORK_NAME
            global WORK_LINK
            global WORK_EMAIL

            # Basic Start and Stop Admin Commands:

            if text == "/start":
                reply("Type /set and I'll remind you what I can update for you, or type /check to see what info I have currently. If you want to see who's messaged me recently type /contacts. To set a welcome message, type /message welcome followed by your extra message for new users.")

            elif text == '/stop':
                reply('Have a lovely day!')
                setEnabled(chat_id, False)

            # Set Admin Command for Work Status:

            elif text == "/set":
                reply("Type /set available true | false to set work availability. Type /set employer followed by a name to set your employer. Type /set link followed by a URL to set the link to your employer's site. Type /set email followed by an address to set your work email.")

            elif text.startswith('/set available'):
                if text[len('/set available')+1:len(text)] == 'true':
                    setWorkStatus('','','',True)
                    reply("Okay, I've noted that you are now available for work.")
                else:
                    setWorkStatus('','','',False)
                    reply("Got it! I'll tell people you're not looking for new opportunities just now.")

            elif text.startswith('/set employer'):
                setWorkStatus(text[len('/set employer')+1:len(text)],'','',False)
                reply("Great, I've noted that you're now working at " + text[len('/set employer')+1:len(text)] + ".")

            elif text.startswith('/set link'):
                setWorkStatus('',text[len('/set link')+1:len(text)],'',False)
                reply("Cool, I'll link people to " + WORK_NAME + " at " + text[len('/set link')+1:len(text)] + " now when they ask about your availability.")

            elif text.startswith('/set email'):
                setWorkStatus('','',text[len('/set email')+1:len(text)],False)
                reply("Okay, I'll tell people they can contact you at "+ text[len('/set email')+1:len(text)] + " if they'd like to discuss " + WORK_NAME + ".")

            # Check Admin Command for Work Status:

            elif text == '/check':
                reply("Here are your current details: \nEmployer: " + WORK_NAME + "\nLink: " + WORK_LINK + "\nEmail: " + WORK_EMAIL + "\nAvailable: " + str(WORK_AVAILABLE).lower())

            # Recent Contacts Admin Command:

            elif text == '/contacts':
                contacts = Contacts.all()
                recentcontacts = contacts.fetch(20)
                contactlist = ""

                for contact in recentcontacts:
                    if contact.contact_id != str(ADMIN_ID):
                        if contact.contact_username == None:
                            contactlist += ("\n"+re.sub('[^0-9a-zA-Z]+', '*', contact.contact_firstname)+": "+contact.contact_id)
                        else:
                            contactlist += ("\n"+re.sub('[^0-9a-zA-Z]+', '*', contact.contact_firstname)+": "+contact.contact_id+" @"+contact.contact_username)

                reply("Recent contacts:" + contactlist)
                reply("Type /msgid followed by a user's ID then your message and I'll pass it along to them.")

            # Message ID Admin Command:

            elif text == '/msgid':
                reply("Type /msgid followed by a user's ID then your message and I'll pass it along to them.")

            elif text.startswith('/msgid'):
                content = text[7:len(text)]
                splitcontent = content.split(' ')
                toid = splitcontent[0]
                msg = content[len(splitcontent[0])+1:len(content)]
                replyWithBot(toid,msg)
                reply("Sent to "+toid+"!")

            elif text == '/message':
                reply("To set a welcome message, type /message welcome followed by your extra message for new users.")

            elif text.startswith('/message'):
                content = text[len('/message')+1:len(text)]
                splitcontent = content.split(' ')
                messagename = splitcontent[0]
                messagecontent = content[len(splitcontent[0])+1:len(content)]
                setMessage(messagename,messagecontent)
                reply("Set '"+messagename+"' message: "+messagecontent)

            else:
                reply("Type /set and I'll remind you what I can update for you, or type /check to see what info I have currently. If you want to see who's messaged me recently type /contacts. To set a welcome message, type /message welcome followed by your extra message for new users.")

        # Standard User Commands:

        else:

            # Create display-safe name variables:

            fr_firstname_safe = re.sub('[^0-9a-zA-Z]+', '*', fr_firstname)
            if fr_lastname !=None:
                fr_lastname_safe = re.sub('[^0-9a-zA-Z]+', '*', fr_lastname)
            else:
                fr_lastname_safe = None

            # Store the current contact and update data:

            cnew = Contacts(key_name=str(chat_id),
                           contact_firstname=fr_firstname_safe,
                           contact_lastname=fr_lastname_safe,
                           contact_id=str(chat_id),
                           contact_username=fr_username)
            cnew.put()

            if text.startswith('/'):

                # Basic Start and Stop Commands:

                if text == '/start':
                    reply("Hey "+fr_firstname_safe+"! How can I help you? Type /feedback to share your thoughts on something Graham's worked on, /enquiry to check his availability for work, or /info to find out more about him.")
                    setEnabled(chat_id, True)

                    # Add in extra welcome message if provided:

                    messages = Messages.all()
                    for message in messages:
                        if (message.message_name == 'welcome') and ((message.message_content != '') and (message.message_content.lower() != 'none')):
                            reply(message.message_content)

                elif text == '/stop':
                    reply('Have a lovely day!')
                    setEnabled(chat_id, False)

                # Feedback Command:

                elif text.startswith('/feedback'):
                    if text == '/feedback':
                        reply("Type /feedback followed by your feedback in a single message. Let me know what you think of any of Graham's work and I'll forward your message to him. Try to link to it if you have the URL to hand.")
                    else:
                        fwdToMe(chat_id,message_id)
                        reply("Thanks for your help! I've forwarded this on to Graham so he can have a look. If you'd like to say something else type /feedback again followed by a message.")

                # Enquiry Command:

                elif text == '/enquiry':
                    if WORK_AVAILABLE:
                        reply("Good news! Graham's currently seeking a position at an interesting startup. He specialises in UI and UX design, and front-end web development. Have a look at his portfolio at grahammacphee.co.uk. You can email Graham at hi@grahammacphee.co.uk or message him here @grahammacphee directly for a more informal chat about any opportunities.")
                    else:
                        reply("Graham is currently unavailable for design work. He's having fun working with the team at "+WORK_NAME+" ("+WORK_LINK+") on some interesting products. You can email him at "+WORK_EMAIL+" if you'd like to discuss "+WORK_NAME+". To stay up-to-date, follow him on Twitter: twitter.com/gmph.")

                # Info Command:

                elif text == '/info':
                    reply("Type /info followed by what you're looking for. I can help you find Graham's social profiles, blog, email address, portfolio, or tell you a little bit about him.")

                # Respond in order with all matching criteria:

                elif text.startswith('/info'):
                    replied = False
                    if 'social' in text.lower():
                        reply("Type /info followed by the profile(s) you're looking for, e.g. Twitter, Dribbble, GitHub...")
                        replied = True
                    if 'twitter' in text.lower():
                        reply("Twitter: twitter.com/gmph")
                        replied = True
                    if 'dribbble' in text.lower():
                        reply("Dribbble: dribbble.com/gmph")
                        replied = True
                    if 'github' in text.lower():
                        reply("GitHub: github.com/gmph")
                        replied = True
                    if 'facebook' in text.lower():
                        reply("Facebook: facebook.com/grahammacphee")
                        replied = True
                    if 'telegram' in text.lower():
                        reply("Telegram: please use /feedback here if you'd like to message Graham.")
                        replied = True
                    if 'foursquare' in text.lower():
                        reply("Foursquare: foursquare.com/gmph")
                        replied = True
                    if 'google' in text.lower():
                        reply("Google+: google.com/+grahammacphee")
                        replied = True
                    if 'email' in text.lower():
                        reply("Email: hi@grahammacphee.co.uk")
                        replied = True
                    if ('website' in text.lower()) or ('portfolio' in text.lower()):
                        reply("Portfolio: grahammacphee.co.uk")
                        replied = True
                    if 'blog' in text.lower():
                        reply("Blog: thinks.grahammacphee.co.uk")
                        replied = True
                    if 'about' in text.lower():
                        reply("Graham is a Designer and Front-end Developer from Scotland. He enjoys photography, nature, singing and playing ukulele. He always gets caught up building little projects like me on the weekends!")
                        replied = True
                    if replied == False:
                        reply("Sorry, I'm not sure what you're looking for. I can help you find Graham's social profiles, blog, email address, portfolio, or tell you a little bit about him. Type /info followed by what you're looking for.")

                else:
                    reply("I can take feedback, enquiries and tell you about Graham. Type /feedback to send some feedback on something Graham's worked on, /enquiry to check his availability for work, or /info to find out more about him.")

            # Just to acknowledge politeness:

            elif ('thanks' in text.lower()) or ('thank you' in text.lower()):
                reply("I'm glad I could help! Is there anything else I can do for you? Type /feedback to send some feedback on something Graham's worked on, /enquiry to check his availability for work, or /info to find out more about him.")

            elif 'who are you' in text.lower():
                reply("I'm Graham Macphee's preprogrammed assistant. Graham is a Designer from Scotland. Find him on Twitter @gmph: twitter.com/gmph")

            else:
                reply("I can take feedback, enquiries and tell you about Graham. Type /feedback to send some feedback on something Graham's worked on, /enquiry to check his availability for work, or /info to find out more about him.")


app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
