#!/bin/bash

# Check for required arguments
if [ $# -ne 3 ]; then
  echo "Usage: $0 <base64_encoded_string> <aes_key_file> <output_file>"
  exit 1
fi

# Arguments
base64_encoded_string="$1"
aes_key_file="$2"
output_file="$3"

# Function to decode URL-safe Base64
decode_url_safe_base64() {
  local input="$1"
  local standard_base64_string
  standard_base64_string=$(echo "$input" | tr '_-' '/+')
  local padding=$(( (4 - ${#standard_base64_string} % 4) % 4 ))
  echo "$standard_base64_string$(printf '=%.0s' $(seq 1 $padding))" | base64 --decode
}

# Split the input string into IV and encrypted content
IFS='.' read -r iv_base64 encrypted_content_base64 <<< "$base64_encoded_string"

# Decode the IV and encrypted content
iv=$(decode_url_safe_base64 "$iv_base64" | xxd -p | tr -d '\n')
encrypted_content=$(decode_url_safe_base64 "$encrypted_content_base64")

# Decode the AES key from the file
aes_key_base64=$(cat "$aes_key_file")
aes_key=$(echo "$aes_key_base64" | base64 --decode | xxd -p | tr -d '\n')

# Save the encrypted content to a temporary file
encrypted_file=$(mktemp)
echo -n "$encrypted_content" > "$encrypted_file"

# Decrypt the content using OpenSSL and save to output file
openssl enc -d -aes-256-cbc -in "$encrypted_file" -out "$output_file" -K "$aes_key" -iv "$iv" -p -nopad

# Clean up
rm -f "$encrypted_file"

echo "Decryption complete. Decoded content saved to $output_file"
