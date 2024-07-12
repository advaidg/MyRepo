#!/bin/bash

# Generate the RSA Private Key
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# Convert the Private Key to PKCS8 Format
openssl pkcs8 -topk8 -inform PEM -outform PEM -in private_key.pem -out private_key_pkcs8.pem -nocrypt

# Extract the Public Key in X.509 Format
openssl rsa -pubout -in private_key.pem -out public_key_x509.pem

# Encode the Private Key (PKCS8) in Base64 and ensure it is a single line
base64 -w 0 private_key_pkcs8.pem > private_key_base64.txt

# Encode the Public Key (X.509) in Base64 and ensure it is a single line
base64 -w 0 public_key_x509.pem > public_key_base64.txt

echo "Private Key (PKCS8) Base64 encoded: "
cat private_key_base64.txt

echo "Public Key (X.509) Base64 encoded: "
cat public_key_base64.txt
