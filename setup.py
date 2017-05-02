#setup.py
import sys
from cx_Freeze import setup, Executable
import os

# os.environ['TCL_LIBRARY'] = r'D:\Python35\tcl\tcl8.6'
# os.environ['TK_LIBRARY'] = r'D:\Python35\tcl\tk8.6'
os.environ['TCL_LIBRARY'] = "D:\\Python35\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "D:\\Python35\\tcl\\tk8.6"
build_exe_options = {"packages": ["os","smtplib","struct","Crypto"], "excludes": ["http","html","test"], "include_files" : ['D:/python35/DLLs/tcl86t.dll', 'D:/python35/DLLs/tk86t.dll']}
setup(
    name = "ransom",
    version = "0.1",
    description = "sb",
    options = {"build_exe": build_exe_options},
    executables = [Executable("ransomware.py", base = "Win32GUI")])