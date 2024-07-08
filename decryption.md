List Entries in the Keystore

sh
Copy code
keytool -list -v -keystore your_keystore_file.jks -storepass your_keystore_password
Convert JKS to PKCS12

This step converts the JKS keystore to a PKCS12 keystore, specifying the alias and passwords.

sh
Copy code
keytool -importkeystore -srckeystore your_keystore_file.jks -srcstorepass your_keystore_password -srcalias your_alias -destkeystore key.p12 -deststoretype PKCS12 -deststorepass your_alias_password
Extract the AES Key from the PKCS12 Keystore

Use openssl to extract the key.

sh
Copy code
openssl pkcs12 -in key.p12 -nocerts -nodes -passin pass:your_alias_password -out key.pem
Inspect the PEM File

Inspect the extracted key to ensure it's in the correct format.

sh
Copy code
cat key.pem
