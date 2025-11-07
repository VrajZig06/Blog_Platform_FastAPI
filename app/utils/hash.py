from pwdlib import PasswordHash

def hash_user_password(password:str):
    hash_password = PasswordHash.recommended()
    return hash_password.hash(password)

def verify_user_password(plain_password:str,hash_user_password:str):
    hash_password = PasswordHash.recommended()

    return hash_password.verify(plain_password,hash_user_password)