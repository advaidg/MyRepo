#!/bin/bash

# Generate an RSA key pair
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private_key.pem -out public_key.pem

# Encode the keys in Base64
base64EncodedPrivateKey=$(openssl base64 -in private_key.pem | tr -d '\n')
base64EncodedPublicKey=$(openssl base64 -in public_key.pem | tr -d '\n')

# Print the Base64 encoded keys
echo "Base64 Encoded Public Key:"
echo $base64EncodedPublicKey
echo
echo "Base64 Encoded Private Key:"
echo $base64EncodedPrivateKey

# Clean up
rm private_key.pem public_key.pem
