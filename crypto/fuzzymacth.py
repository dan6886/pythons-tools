import base64
from Crypto.Cipher import AES


##############################################


######################################################

class HashManager():

    def __init__(self) -> None:
        super().__init__()
        self.key = "469282670"

    # #######MD5加密#######
    # def get_md5(self, the_string):
    #     the_string_with_salt = the_string + the_salt
    #     the_md5 = hashlib.md5()
    #     the_md5.update(the_string_with_salt.encode('utf-8'))
    #     the_string_md5 = the_md5.hexdigest()
    #     return the_string_md5
    #
    # #######SHA1加密#######
    # def get_sha1(self, the_string):
    #     the_string_with_salt = the_string + the_salt
    #     the_sha1 = hashlib.sha1()
    #     the_sha1.update(the_string_with_salt.encode('utf-8'))
    #     the_string_sha1 = the_sha1.hexdigest()
    #     return the_string_sha1
    #
    # #######SHA256加密#######
    # def get_sha256(self, the_string):
    #     the_string_with_salt = the_string + the_salt
    #     the_sha256 = hashlib.sha256()
    #     the_sha256.update(the_string_with_salt.encode('utf-8'))
    #     the_string_sha1 = the_sha256.hexdigest()
    #     return the_string_sha1
    #
    # #######SHA512加密#######
    # def get_sha512(self, the_string):
    #     the_string_with_salt = the_string + the_salt
    #     the_sha512 = hashlib.sha512()
    #     the_sha512.update(the_string_with_salt.encode('utf-8'))
    #     the_string_sha1 = the_sha512.hexdigest()
    #     return the_string_sha1

    #######AES加密，ECB模式#######
    def get_aes_ecb(self, the_string):
        aes = AES.new(self.pkcs7padding_tobytes(self.key), AES.MODE_ECB)  # 初始化加密器
        encrypt_aes = aes.encrypt(self.pkcs7padding_tobytes(the_string))  # 进行aes加密
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 用base64转成字符串形式
        return encrypted_text

    #######AES解密，ECB模式#######
    def back_aes_ecb(self, the_string):
        aes = AES.new(self.pkcs7padding_tobytes(the_key), AES.MODE_ECB)  # 初始化加密器
        decrypted_base64 = base64.decodebytes(
            the_string.encode(encoding='utf-8'))  # 逆向解密base64成bytes
        decrypted_text = str(aes.decrypt(decrypted_base64), encoding='utf-8')  # 执行解密密并转码返回str
        decrypted_text_last = self.pkcs7unpadding(decrypted_text)  # 去除填充处理
        return decrypted_text_last

    #######AES加密，CFB模式#######
    def get_aes_cfb(self, the_string):
        key_bytes = self.pkcs7padding_tobytes(self.key)
        iv = key_bytes
        aes = AES.new(key_bytes, AES.MODE_CFB, iv)  # 初始化加密器，key,iv使用同一个
        encrypt_aes = iv + aes.encrypt(the_string.encode())  # 进行aes加密
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 用base64转成字符串形式
        return encrypted_text

    #######AES解密，CFB模式#######
    def back_aes_cfb(self, the_string):
        key_bytes = self.pkcs7padding_tobytes(self.key)
        iv = key_bytes
        aes = AES.new(key_bytes, AES.MODE_CFB, iv)  # 初始化加密器，key,iv使用同一个
        decrypted_base64 = base64.decodebytes(
            the_string.encode(encoding='utf-8'))  # 逆向解密base64成bytes
        decrypted_text = str(aes.decrypt(decrypted_base64[16:]), encoding='utf-8')  # 执行解密密并转码返回str
        return decrypted_text

    #######AES加密，CBC模式#######
    def get_aes_cbc(self, the_string):
        key_bytes = self.pkcs7padding_tobytes(self.key)
        iv = key_bytes
        aes = AES.new(key_bytes, AES.MODE_CBC, iv)  # 初始化加密器，key,iv使用同一个
        encrypt_bytes = aes.encrypt(self.pkcs7padding_tobytes(the_string))  # 进行aes加密
        encrypted_text = str(base64.b64encode(encrypt_bytes), encoding='utf-8')  # 用base64转成字符串形式
        return encrypted_text

    #######AES解密，CBC模式#######
    def back_aes_cbc(self, the_string):
        key_bytes = self.pkcs7padding_tobytes(self.key)
        iv = key_bytes
        aes = AES.new(key_bytes, AES.MODE_CBC, iv)  # 初始化加密器，key,iv使用同一个
        decrypted_base64 = base64.b64decode(the_string)  # 逆向解密base64成bytes
        decrypted_text = str(aes.decrypt(decrypted_base64), encoding='utf-8')  # 执行解密密并转码返回str
        decrypted_text_last = self.pkcs7unpadding(decrypted_text)  # 去除填充处理
        return decrypted_text_last

    #######填充相关函数#######
    def pkcs7padding_tobytes(self, text):
        return bytes(self.pkcs7padding(text), encoding='utf-8')

    def pkcs7padding(self, text):
        bs = AES.block_size
        ####tips：utf-8编码时，英文占1个byte，而中文占3个byte####
        length = len(text)
        bytes_length = len(bytes(text, encoding='utf-8'))
        padding_size = length if (bytes_length == length) else bytes_length
        ####################################################
        padding = bs - padding_size % bs
        padding_text = chr(padding) * padding  # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
        return text + padding_text

    def pkcs7unpadding(self, text):
        length = len(text)
        unpadding = ord(text[length - 1])
        return text[0:length - unpadding]

    def set_key(self, key):
        self.key = key


if __name__ == "__main__":
    manager = HashManager()
    print(manager.get_aes_cfb("直接在你的源码中导入PyQt5.sip"))
    # print(manager.back_aes_cfb("YWFhYWFhYWFhYWFhYWFhAUOWwpaaKlc29ZgLhP2NmQ=="))
