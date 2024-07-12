#!/bin/bash

# Generate an RSA key pair
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private_key.pem -out public_key.pem

# Remove the PEM headers/footers and encode the keys in Base64
base64EncodedPrivateKey=$(openssl pkcs8 -topk8 -nocrypt -in private_key.pem | openssl base64 -A | tr -d '\n')
base64EncodedPublicKey=$(openssl rsa -in private_key.pem -pubout | openssl base64 -A | tr -d '\n')

# Print the Base64 encoded keys
echo "Base64 Encoded Public Key:"
echo $base64EncodedPublicKey
echo
echo "Base64 Encoded Private Key:"
echo $base64EncodedPrivateKey

# Clean up
rm private_key.pem public_key.pem
