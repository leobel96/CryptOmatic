![Logo](https://github.com/leobel96/CryptOmatic/blob/master/icon.png)

# 🔒CryptOmatic🔒
A simple command line file encrypter/decrypter

## Dependencies
- Colorama (`pip install colorama`)
- Pyfiglet (`pip install pyfiglet`)
- PyCryptodome (`pip install pycryptodome`)
- SDelete64 (https://docs.microsoft.com/en-us/sysinternals/downloads/sdelete). Download the folder and extract the file "sdelete64.exe" placing it in the same folder where you will launch the script

## How it works
Using a simple terminal interface, this python script lets you encrypt and, then, decrypt, one or more files. After the user has inserted encryption key, a key derivation function (scrypt) derives a key from it using a random salt to make it unique. The key is, then, used to encrypt the file using AES256 and GMAC authentication. Before encryption the file is authenticated with GMAC and, then, encrypted if authentication is successfull.

An important feature present in this script is secure deletion: using SDelete (or shred in linux), the unencrypted file is removed from disk without leaving traces in a way much different from the usual "move to bin". Yes, the script can run on both Linux and Windows.

I suggest you to add your folder to a zip archive and, then, encrypt it as file if it contains a great number of files: the script iteratively encrypts each file and takes much time.

## Disclaimer
I assume no responsibility for file damages/bugs/security exploits.
