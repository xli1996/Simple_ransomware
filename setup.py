#setup.py
import sys
from cx_Freeze import setup, Executable
build_exe_options = {"packages": ["os","random","struct","Crypto.Cipher","Crypto"], "excludes": []}
setup(
    name = "ransom",
    version = "0.1",
    description = "sb",
    options = {"build_exe": build_exe_options},
    executables = [Executable("python.py", base = "Win32GUI")])