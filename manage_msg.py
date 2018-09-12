import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="user login")
parser.add_argument("-l", "--list", help="list all messages")
parser.add_argument("-t", "--to", help="email aderes of reciepient")
parser.add_argument("-s", "--send", help="sent message")

try:
    args = parser.parse_args()
except:
    parser.print_help()
    sys.exit(0)