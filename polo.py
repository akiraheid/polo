#!/usr/bin/env python3

import argparse
import hmac
from http.server import HTTPServer, BaseHTTPRequestHandler
from os.path import exists
import random
import string
from sys import exit

# File of users and their salted/hashed tokens
USER_FILE = "users.txt"

# File of salted/hashed tokens and the last reported IP
IP_FILE = "ips.txt"

SALT = bytes("SnakeCityIjustwannatakeanotherlookatyouwillyouletme", "utf-8")

# Hashed tokens for registered users
users = {}

# Token-IP lookup table
ips = {}

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        body = self.rfile.read(content_length)
        # Use to verify given hash
        #hamc.compare_digest
        self.send_response(200)
        self.end_headers()

        print(f"Got {body}")

def add(args):
    user = args.username
    if user_exists(user):
        print(f"Error: User {user} already exists. Use 'reset' subcommand to change this user's password.")
        exit(1)

    parse_hmac_args(args)
    set_user_token(user)

    with open(USER_FILE, "w") as fp:
        for user in users:
            fp.write(f"{user}:{users[user]}")

def generate_token(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    characters = characters.strip(":") # Remove character used as delimiter in storage
    return "".join(random.choice(characters) for _ in range(length))

def generate_hash(token):
    token = bytes(token, "utf-8")
    obj = hmac.new(token, digestmod="sha3_512")
    obj.update(SALT)
    return obj.hexdigest()

def load_ips(file_path):
    lines = read_lines(file_path)
    for line in lines:
        parts = line.split(":")
        if len(parts) != 2:
            print(f"Expected only two parts for {file_path}")
            exit(1)

        hashed_token = parts[0]
        ip = parts[1]
        ips[hashed_token] = ip

    print(f"Loaded {len(lines)} IPs")

def load_users(file_path):
    lines = read_lines(file_path)
    if len(lines) == 0:
        print(f"No users to track in {file_path}")

    for line in lines:
        parts = line.split(":")
        if len(parts) != 2:
            print(f"Expected only two parts for {file_path}")
            exit(1)

        # Don't care about user name when receiving updates
        #user = parts[0]
        users[parts[0]] = parts[1]

    print(f"Loaded {len(lines)} users")

def parse_hmac_args(args):
    if args.salt:
        SALT = bytes(args.salt, "utf-8")

def read_lines(file_path):
    if exists(file_path):
        with open(file_path, "r") as fp:
            return fp.readlines()

    return []

def set_user_token(user):
    token = generate_token(64)
    print(f"Token for {user} is: {token}")

    hashed_passwd = generate_hash(token)

    users[user] = hashed_passwd
    print("Stored user's hashed token")

def start_server(_):
    port = 8080
    print(f"Starting server on port {port}")
    server = HTTPServer(("localhost", port), HTTPRequestHandler)
    server.serve_forever()

def user_exists(username):
    return username in users

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--ip-file", type=str, help="IP file")
parser.add_argument("-u", "--user-file", type=str, help="User file")
subparsers = parser.add_subparsers()

parser_start = subparsers.add_parser("start", help="Start the server")
parser_start.set_defaults(func=start_server)

parser_add = subparsers.add_parser("add", help="Add a new user")
parser_add.set_defaults(func=add)
parser_add.add_argument("username", type=str, help="User name")
parser_add.add_argument("-s", "--salt", type=str, help="Salt for hash of token")

#parser_reset = subparsers.add_parser("reset", help="Reset an existing user")
#parser_delete = subparsers.add_parser("delete", help="Delete an existing user")

args = parser.parse_args()

if args.ip_file:
    IP_FILE = args.ip_file

if args.user_file:
    USER_FILE = args.user_file

load_users(USER_FILE)
load_ips(IP_FILE)

args.func(args)
