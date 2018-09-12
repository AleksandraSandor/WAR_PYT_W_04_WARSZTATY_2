import argparse
from controlers import connection
from models import users
from controlers import clcrypto
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--id", help="user id")
parser.add_argument("-u", "--username", help="user login")
parser.add_argument("-p", "--password", help="user password")
parser.add_argument("-m", "--mail", help="user mail")
parser.add_argument("-n", "--newpaswd", help="user new password")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="modify user password", action="store_true")

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)

if (args.username and args.password) and (not args.edit and not args.delete):
    usr = users.User()
    usr.username = args.username
    usr.email = args.mail
    usr.set_password(args.password, '12')
    conn = connection.create_connection("users_db")
    cursor = conn.cursor()
    usr.save_to_db(cursor)
    print(f"Create new user {args.username}.")

if args.username and args.password and args.edit:
    usr = users.User()
    conn = connection.create_connection("users_db")
    cursor = conn.cursor()
    searched_usr = usr.load_user_by_id(cursor, args.id)
    if clcrypto.check_password(args.password, searched_usr.hashed_password) and len(args.newpaswd) >= 8:
        searched_usr.set_password(args.newpaswd, '12')
        searched_usr.save_to_db(cursor)
        print("User updated")

if args.username and args.password and args.delete:
    usr = users.User()
    conn = connection.create_connection("users_db")
    cursor = conn.cursor()
    searched_usr = usr.load_user_by_id(cursor, args.id)
    if clcrypto.check_password(args.password, searched_usr.hashed_password):
        searched_usr.delete(cursor)
        print("User deleted")

if args.list:
    usr = users.User()
    conn = connection.create_connection("users_db")
    cursor = conn.cursor()
    users = usr.load_all_users(cursor)
    for user in users:
        print(user.id, user.username, user.email)

else:
    print("Upps error")
    parser.print_help()
