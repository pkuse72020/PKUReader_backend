
import rsa,base64

def encrypt_data(data):
    ret_data = {}
    with open('public_key_file.pem', mode='rb') as privfile:
        keydata = privfile.read()
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(keydata)
    for key in data:
        value=data[key]
        ret_data[key]=base64.b64encode(rsa.encrypt(value.encode('utf-8'),pubkey)).decode('utf-8')
    return ret_data

if __name__ == "__main__":
    print(encrypt_data({"username": "gyq", "password": "123456"}))

