openssl genrsa -out private_key_file.pem 1024
openssl rsa -in private_key_file.pem -pubout -out public_key_file.pem