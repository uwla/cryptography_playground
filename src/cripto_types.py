from cripto_utils import randint
from abc import abstractmethod

class KeyGenerationScheme():
    def __init__(self, sec_level):
        self.sec_level = sec_level
        self.generate_public_parameters(sec_level)

    def generate_public_parameters(self, sec_level):
        pass

    def get_public_params(self):
        return self.public_params
    
    @abstractmethod
    def generate_secrete_key(self):
        pass

    @abstractmethod
    def derive_public_key(self, sec_key):
        pass

    def generate_key(self):
        sec_key = self.generate_secrete_key()
        pub_key = self.derive_public_key(sec_key)
        return (pub_key, sec_key)

    # may be overwritten
    def generate_sample_msg(self):
        return randint(2, self.sec_level)

class SignatureScheme(KeyGenerationScheme):
    @abstractmethod
    def sign(self, msg, sec_key):
        pass

    @abstractmethod
    def verify(self, msg, pub_key, signature):
        pass

    def test_signature(self):
        msg = self.generate_sample_msg()
        pub_key, sec_key = self.generate_key()
        signature = self.sign(msg, sec_key)
        valid = self.verify(msg, pub_key, signature)
        print((pub_key, sec_key), msg, signature, valid)
        assert valid == True

class EncryptionScheme(KeyGenerationScheme):
    @abstractmethod
    def encrypt(self, msg, pub_key):
        pass

    @abstractmethod
    def decrypt(self, msg, sec_key):
        pass

    def test_encryption(self):
        pub_key, sec_key = self.generate_key()
        msg = self.generate_sample_msg()
        encrypted = self.encrypt(msg, pub_key)
        decrypted = self.decrypt(encrypted, sec_key)
        print((pub_key, sec_key), msg, encrypted, decrypted)
        assert decrypted == msg