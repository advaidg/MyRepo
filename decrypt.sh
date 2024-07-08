#!/bin/bash

# Check for required arguments
if [ $# -ne 5 ]; then
  echo "Usage: $0 <base64_encoded_string> <output_file> <keystore_file> <keystore_password> <alias>"
  exit 1
fi

# Arguments
base64_encoded_string="$1"
output_file="$2"
keystore_file="$3"
keystore_password="$4"
alias="$5"
alias_password="$6"

# Function to decode URL-safe Base64
decode_url_safe_base64() {
  local input="$1"
  local standard_base64_string
  standard_base64_string=$(echo "$input" | tr '_-' '/+')
  local padding=$(( (4 - ${#standard_base64_string} % 4) % 4 ))
  echo "$standard_base64_string$(printf '=%.0s' $(seq 1 $padding))" | base64 --decode
}

# Extract the key from the keystore
key_file=$(mktemp)
keytool -importkeystore -srckeystore "$keystore_file" -srcalias "$alias" -srcstorepass "$keystore_password" -destkeystore "$key_file" -deststoretype PKCS12 -deststorepass "$alias_password"
openssl pkcs12 -in "$key_file" -nocerts -nodes -passin pass:"$alias_password" | openssl rsa -out aes_key.pem

# Read the AES key
aes_key=$(openssl rsa -in aes_key.pem -noout -text | grep -A 1 "private key:" | tail -1 | tr -d ' \n')

# Clean up temporary key file
rm -f "$key_file" aes_key.pem

# Split the input string into IV and encrypted content
IFS='.' read -r iv_base64 encrypted_content_base64 <<< "$base64_encoded_string"

# Decode the IV and encrypted content
iv=$(decode_url_safe_base64 "$iv_base64")
encrypted_content=$(decode_url_safe_base64 "$encrypted_content_base64")

# Save encrypted content to a temporary file
encrypted_file=$(mktemp)
echo -n "$encrypted_content" > "$encrypted_file"

# Decrypt the content using OpenSSL and save to output file
openssl enc -d -aes-256-cbc -in "$encrypted_file" -out "$output_file" -K "$(echo -n "$aes_key" | xxd -p)" -iv "$(echo -n "$iv" | xxd -p)"

# Clean up
rm -f "$encrypted_file"

echo "Decryption complete. Decoded content saved to $output_file"
