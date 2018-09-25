import argparse
from controlers.connection import create_connection, execute_single_sql, execute_sql
from models import users
from models import messages
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="user login")
parser.add_argument("-p", "--password", help="user password")
parser.add_argument("-l", "--list", help="list all messages")
parser.add_argument("-t", "--to", help="email aderes of reciepient")
parser.add_argument("-s", "--send", help="sent message")

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

if args.list and (args.username and args.password):
    mes = messages.Message()
    usr = users.User()
    conn = create_connection("users_db")
    cursor = conn.cursor()
    users = usr.load_all_users(cursor)
    messages = mes.load_all_messages_for_user(cursor)
    for user in users:
        list = []
        for message in messages:
            list.append(messages)
            print(list.sort())

if args.send and (args.username and args.password and args.to):
    mes = messages.Message()
    usr = users.User()
    conn = create_connection("users_db")
    cursor = conn.cursor()
    users = usr.load_all_users(cursor)
    messages = mes.save_to_db(cursor)
    print(f'Message to {messages[1]} from {messages[0]}. Sent on {messages[3]}. Text: "{messages[2]}"')

else:
    print("Upps error")
    parser.print_help()
