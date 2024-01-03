from os import getlogin, urandom, unlink
from os.path import exists
from base64 import b64encode, b64decode
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from json import loads, dumps


savePath = f'C:/Users/{getlogin()}/AppData/LocalLow/Horny Doge/Peeping Dorm Manager'
fileName = 'GameSave_0.dat'
password = 'PeepingHG20221124'

if exists(f'{savePath}/decrypted.json'):
    with open(f'{savePath}/decrypted.json', 'r', encoding='utf-8') as f:
        data = loads(f.read())
    data['datas'] = [each | {'data': dumps(each['data'], separators=(',', ':'), ensure_ascii=False)} for each in data['datas']]
    iv = urandom(8)
    key = PBKDF2(password, iv, 8)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    data = cipher.encrypt(pad(dumps(data, separators=(',', ':'), ensure_ascii=False).encode(), 8))
    with open(f'{savePath}/{fileName}', 'wb') as f:
        f.write(b64encode(iv + data))
    unlink(f'{savePath}/decrypted.json')
else:
    with open(f'{savePath}/{fileName}', 'r') as f:
        data = b64decode(f.read())
    iv, data = data[:8], data[8:]
    key = PBKDF2(password, iv, 8)
    cipher = DES.new(key, DES.MODE_CBC, iv)
    data = loads(unpad(cipher.decrypt(data), 8))
    data['datas'] = [each | {'data': loads(each['data'])} for each in data['datas']]
    with open(f'{savePath}/decrypted.json', 'w', encoding='utf-8') as f:
        f.write(dumps(data, ensure_ascii=False, indent=4))
