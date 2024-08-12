#!/bin/bash
# this script will generate a deterministic random hash to create a mac adress given the seed of the hostname, or any other atomic value
# The name of the VM
vm_name=$1

# Generate a SHA-256 hash of the name
hash_value=$(echo -n "$vm_name" | sha256sum | cut -d' ' -f1)

# Take the first 6 bytes of the hash value and convert them to hexadecimal
hex_part=${hash_value:0:12}

# Create the MAC address from the first 6 hexadecimal digits
mac_address="${hex_part:0:2}:${hex_part:2:2}:${hex_part:4:2}:${hex_part:6:2}:${hex_part:8:2}:${hex_part:10:2}"

# Print the generated MAC address
echo "$mac_address"
