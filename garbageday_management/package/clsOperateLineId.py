"""package clsOperateLineId.py
    * A function that encrypts or decrypts line_id
"""
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import base64

PASSWORD = "gVLhpdDiPLU7GfkedQ6bX0Ghi1yGphj9"

class OperateLineId(object):
    """OperateLineId""" 
    def create_aes(self, iv):
        """create_aes()

        Function to create aes

        Args:
            self: instance
            iv str: random string 
           
            
        Returns:
            the create aes
        """
        sha = SHA256.new()
        sha.update(PASSWORD.encode())
        key = sha.digest()
        return AES.new(key, AES.MODE_CFB, iv)

    def encrypt(self, data):
        """encrypt()

        Function to encrypt

        Args:
            self: instance
            data str: data to encrypt
           
            
        Returns:
            the encrypt string
        """
        system_name = 'garbageday'.encode()
        iv = base64.b64encode(system_name)

        return iv + self.create_aes(iv).encrypt(data)

    def decrypt(self, data):
        """decrypt()

        Function to decrypt

        Args:
            self: instance
            data str: data to decrypt
           
            
        Returns:
            the decrypt string
        """
        
        iv, cipher = data[:AES.block_size], data[AES.block_size:]
        return self.create_aes(iv).decrypt(cipher)
