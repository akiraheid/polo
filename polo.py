#!/usr/bin/env python3

import argparse
import hmac
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from os.path import exists
import random
import string
from sys import exit

# File of users and their salted/hashed tokens
USER_FILE = "users.txt"

SALT = bytes("SnakeCityIjustwannatakeanotherlookatyouwillyouletme", "utf-8")

# Hashed tokens for registered users
users = {}

# Token-IP lookup table
ips = {}

def add_user(args):
    user = args.username
    if user_exists(user):
        print(f"Error: User {user} already exists. Use 'reset' subcommand to change this user's password.")
        exit(1)

    parse_hmac_args(args)
    set_user_token(user)
    write_users()

def delete_user(args):
    user = args.username
    if not user_exists(user):
        print(f"Error: User {user} does not exist.")
        exit(1)

    del users[user]
    write_users()
    print(f"Deleted {user}")

def generate_token(length):
    characters = string.ascii_letters + string.digits + "!@#$%^&*(),./<>?;:[]{}-_=+"
    characters = characters.strip(":") # Remove character used as delimiter in storage
    return "".join(random.choice(characters) for _ in range(length))

def generate_hash(token):
    token = bytes(token, "utf-8")
    obj = hmac.new(token, digestmod="sha512")
    obj.update(SALT)
    return obj.hexdigest()

def list_users(args):
    for user in users:
        print(user)

def load_users(file_path):
    lines = read_lines(file_path)
    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(":")
        if len(parts) != 2:
            print(f"Expected only two parts for {file_path}")
            exit(1)

        users[parts[0]] = parts[1]

def parse_hmac_args(args):
    if args.salt:
        SALT = bytes(args.salt, "utf-8")

def read_lines(file_path):
    if exists(file_path):
        with open(file_path, "r") as fp:
            return fp.readlines()

    return []

def reset_user(args):
    user = args.username
    if not user_exists(user):
        print(f"Error: User {user} does not exist.")
        exit(1)

    parse_hmac_args(args)
    print(f"Generating new token for user {user}")
    set_user_token(user)
    write_users()

def set_user_token(user):
    token = generate_token(64)
    print(f"Token for {user} is: {token}")

    hashed_passwd = generate_hash(token)

    users[user] = hashed_passwd
    print("Stored user's hashed token")

def user_exists(username):
    return username in users

def write_users():
    with open(USER_FILE, "w") as fp:
        for user in users:
            fp.write(f"{user}:{users[user]}\n")

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--salt", type=str, help="Salt for hash of token")
parser.add_argument("-u", "--user-file", type=str, help="User file")
subparsers = parser.add_subparsers()

parser_add = subparsers.add_parser("add", help="Add a new user")
parser_add.add_argument("username", type=str, help="User name")
parser_add.set_defaults(func=add_user)

parser_delete = subparsers.add_parser("delete", help="Delete an existing user")
parser_delete.add_argument("username", type=str, help="User name")
parser_delete.set_defaults(func=delete_user)

parser_list = subparsers.add_parser("list", help="List users")
parser_list.set_defaults(func=list_users)

parser_reset = subparsers.add_parser("reset", help="Reset an existing user")
parser_reset.add_argument("username", type=str, help="User name")
parser_reset.set_defaults(func=reset_user)

args = parser.parse_args()

if args.salt:
    SALT = args.salt

if args.user_file:
    USER_FILE = args.user_file

load_users(USER_FILE)

args.func(args)
