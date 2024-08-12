#!/bin/bash
# generates a pwassword and hashes it
password=$(openssl rand -base64 32 | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
# Hashes des Passwords
hashed_password=$(echo -n "$password" | openssl passwd -6 -stdin)
#echo "$password"
echo "$hashed_password"