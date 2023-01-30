import csv

from telethon.sync import events
from telethon.sync import TelegramClient

from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty

from utils.artwork import ascii
from utils.printcolors import printout


banner = lambda color: print(printout(ascii, color))
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


result = client(GetDialogsRequest(
    offset_date=None,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=500,
    hash=0,
))
for group in result.chats:
    try:
        if group.megagroup == True:
            groups.append(group)
    except:
        continue

val = 0
for group in groups:
    print(printout(f'[{val}] {group.title}', 'green'))
    val += 1

group = groups[int(input(printout('Choose group number: ', 'green')))]

print('Fetching Members...')
all_participants = []
all_participants = client.get_participants(group, aggressive=True)

print(printout('Saving In file...', 'green'))
with open('output/members.csv', 'w', encoding='UTF-8') as f:
    writer = csv.writer(f, delimiter=",", lineterminator="\n")
    writer.writerow(['username', 'user id', 'access hash',
                    'name', 'group', 'group id'])
    for user in all_participants:
        if user.username:
            username = user.username
        else:
            username = ''
        if user.first_name:
            first_name = user.first_name
        else:
            first_name = ''
        if user.last_name:
            last_name = user.last_name
        else:
            last_name = ''
        name = (first_name + ' ' + last_name).strip()
        writer.writerow([username, user.id, user.access_hash,
                        name, group.title, group.id])
print(printout('Members scraped successfully.', 'yellow'))


