import argparse
from controlers import connection
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
    conn = connection.create_connection("users_db")
    cursor = conn.cursor()
    users = usr.load_all_users(cursor)
    messages = mes.load_all_messages_for_user(cursor)
    for user in users:
        for message in messages:
            print(user.id, user.username, user.email)


else:
    print("Upps error")
    parser.print_help()
