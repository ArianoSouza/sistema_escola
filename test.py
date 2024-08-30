from cryptography.fernet import Fernet
import jwt
import base64
import uuid

key_jwt = "omglookatmybutt"
key_string = '65d68596-e0b9-47a8-af9f-ebccc0a5'
key_bytes = key_string.encode(encoding='utf-8')
key_b64 = base64.b64encode(key_bytes)

#senha prof feijaomacassar
#senha aluno beijaflor

fernet = Fernet(key_b64)
senha = 'test483'
senha_teste = senha.encode(encoding='utf-8')
password = fernet.encrypt(senha_teste)

senha_enc='gAAAAABmz58QYF3BGSj4Qp5Ih_tBxe6u1ccfkMLNDOf7jiUAz14EPjcea5pUSXYi6alEPiuDsYI3regQVscgD9D-qnAh47I6ig=='
senha_b = senha_enc.encode('utf-8')
senha_dec = fernet.decrypt(senha_b)
senha_string = senha_dec.decode('utf-8')

print(fernet.decrypt(b'gAAAAABmz6At_5ILG1JyZPaia8Wj2rK-6T6WLGcPl0cAJ9dN13q4HT3x1BOd_vWlP2H4r-iEDZRMqbVzEznrp4adHpIJvB3LSg=='))



