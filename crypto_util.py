from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# 固定のキーとIV（本番では環境変数などで管理するべき）
KEY = b'REDACTED_KEY'
IV = b'REDACTED_IV'

def encrypt_password(plain_text):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    ct_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
    return base64.b64encode(ct_bytes).decode('utf-8')

def decrypt_password(encrypted_text):
    cipher = AES.new(KEY, AES.MODE_CBC, IV)
    pt = unpad(cipher.decrypt(base64.b64decode(encrypted_text)), AES.block_size)
    return pt.decode('utf-8')