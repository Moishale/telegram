import sys
import csv
import traceback
import time
import random

from telethon.sync import events
from telethon.sync import TelegramClient

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser

from telethon.errors import *

from utils.artwork import ascii
from utils.printcolors import printout

from time import sleep


banner = lambda color: print(printout(ascii, color))
writeout = lambda text: print(printout(text, 'red'))

groups = []
banner('green')

try:
    import configparser
    config = configparser.ConfigParser()
    config.read('config\credentials.ini')
    api_hash = config['Credentials']['api_hash']
    api_id = config['Credentials']['api_id']
    phone = config['Credentials']['phone']
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
except ValueError:
    print(printout('set credentials before running!', 'red'))

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input(printout('Enter Login Code:', 'green')))


users = []
with open('output\members.csv', encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        user['id'] = int(row[1])
        user['access_hash'] = int(row[2])
        user['name'] = row[3]
        users.append(user)

result = client(GetDialogsRequest(
    offset_date=None,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=500,
    hash=0,
))
for group in result.chats:
    try:

        groups.append(group)
    except:
        continue

val = 0
for group in groups:
    print(printout(f'[{val}] {group.title}', 'green'))
    val += 1

group = groups[int(input(printout('Choose group number: ', 'green')))]

target_group_entity = InputPeerChannel(
    group.id, group.access_hash)

mode = int(input("Enter 1 to add by username or 2 to add by ID: "))

error_count = 0

for user in users:
    try:
        print(printout('Adding {}'.format(user['username']), 'green'))
        if mode == 1:
            if user['username'] == '':
                continue
            user_to_add = client.get_input_entity(user['username'])
        elif mode == 2:
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
        else:
            sys.exit('Invalid Mode Selected. Please Try Again.')
        client(InviteToChannelRequest(target_group_entity, [user_to_add]))
    except FloodWaitError:
        writeout('Getting Flood Error from telegram. Script is stopping now. Please try again after some time.')
    except UserPrivacyRestrictedError:
        writeout('The users privacy settings do not allow you to do this. Skipping.')
    except:
        traceback.print_exc()
        writeout('Unexpected Error')
        error_count += 1
        if error_count > 10:
            sys.exit('too many errors')
        continue
    print('Waiting 10-60 seconds before adding another member')
    sleep(random.randint(10,61))


