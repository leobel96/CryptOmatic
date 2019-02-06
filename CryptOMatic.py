# default modules
from getpass import getpass
from os import path, remove, walk, system
from platform import system as operative_system
import sys

# decoration modules
from colorama import init as colorama_init
from colorama import Fore, Style
from pyfiglet import Figlet

# encryption modules
from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from Crypto.Random import get_random_bytes

# parameters for scrypt KDF
N = 1048576
r = 8
p = 1

allFiles = []
extension = '.crypt'

def encrypt(filename, password):
    chunksize = 64 * 1024
    nonce = 1
    salt = get_random_bytes(16)
    key = KDF.scrypt(password, salt, 32, N, r, p)
    outFile = filename + extension
    with open(filename, "rb") as infile:
        with open(outFile, "wb") as outfile:
            outfile.write(salt)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    # print('{} chunks used'.format(nonce))
                    break
                cipher = AES.new(key, AES.MODE_GCM, bytes(nonce))
                outChunk, tag = cipher.encrypt_and_digest(chunk)
                outfile.write(tag)
                outfile.write(outChunk)
                nonce += 1


def decrypt(filename, password):
    chunksize = 64 * 1024
    nonceSize = 8
    nonce = 1
    outFile, outFile_extension = path.splitext(filename)
    with open(filename, "rb") as infile:
        with open(outFile, "wb") as outfile:
            salt = infile.read(16)
            key = KDF.scrypt(password, salt, 32, N, r, p)
            while True:
                tag = infile.read(16)
                rchunk = infile.read(chunksize)
                if len(rchunk) == 0:
                    # print('{} chunks used'.format(nonce))
                    break
                try:
                    cipher = AES.new(key, AES.MODE_GCM, bytes(nonce))
                    outChunk = cipher.decrypt_and_verify(rchunk, tag)
                    outfile.write(outChunk)
                    nonce += 1
                except ValueError:
                    print(Fore.RED + "Integrity verification failed. " +
                          "The password is wrong or the file " +
                          "has been modified without authorization. "
                          )
                    input("Press ENTER and try again.")
                    outfile.close()
                    remove(outFile)
                    sys.exit()


def allfiles(directory):
    for root, dirs, files in walk(directory):
        for names in files:
            if option1 == 'e':
                allFiles.append(path.join(root, names))
            else:
                no_extension, file_extension = path.splitext(names)
                if file_extension == extension:
                    allFiles.append(path.join(root, names))


def main():
    colorama_init(autoreset=True)
    f = Figlet(font='big')
    print(Fore.GREEN + f.renderText('CryptOmatic'))
    option1 = input("Type E to Encrypt or D to Decrypt: ")
    if option1.upper() == 'E':
        print("You have chosen to encrypt!")
        option2 = input("Type S to encrypt a Single file "
                        "or F to encrypt a Folder: ")
        if option2.upper() == 'S':
            print("You have chosen a single file!")
            option3 = input("Write the file path and name with extension or "
                            "simply drag \'n\' drop it: ")
            option3 = option3.replace('"', '').replace("'", '')
            if not path.isfile(option3):
                input(Fore.RED + "Invalid file. Press ENTER to exit")
                sys.exit()
            option4 = getpass("Insert password for encryption, harder "
                              "it is and stronger will be encryption: ")
            encrypt(option3, option4)
            print(Fore.GREEN + "Encryption finished")
            input("If everything is ok, press ENTER "
                  "to remove the old file and exit")
            if operative_system() == "Windows":
                system("sdelete64 " + '"' + option3.replace('\\', '/') + '"')
            elif operative_system() == "Linux":
                system("shred -zu " + '"' + option3.replace('\\', '/') + '"')
        elif option2.upper() == 'F':
            print('You have chosen an entire folder!')
            option3 = input("Type the folder path or simply "
                            "drag \'n\' drop it: ")
            option3 = option3.replace('"', '').replace("'", '')
            if not path.isdir(option3):
                input(Fore.RED + "Invalid folder. Press ENTER to exit")
                sys.exit()
            option4 = getpass("Insert password for encryption, harder "
                              "it is and stronger will be encryption: ")
            allfiles(option3)
            for File in allFiles:
                encrypt(File, option4)
            print(Fore.GREEN + "Encryption finished")
            input("If everything is ok, press ENTER to "
                  "remove the old files and exit")
            if operative_system() == "Windows":
                for File in allFiles:
                    system("sdelete64 " + '"' + File.replace('\\', '/') + '"')
            elif operative_system() == "Linux":
                for File in allFiles:
                    system("shred -zu " + '"' + File.replace('\\', '/') + '"')
        else:
            print('Wrong option selected. Retry')
    elif option1.upper() == 'D':
        print('You have chosen to decrypt!')
        option2 = input("Type S to decrypt a Single file or F "
                        "to decrypt a Folder: ")
        if option2.upper() == 'S':
            print('You have chosen a single file!')
            option3 = input("Write the file path and name with extension or "
                            "simply drag \'n\' drop it: ")
            option3 = option3.replace('"', '').replace("'", '')
            if not path.isfile(option3):
                input(Fore.RED + "Invalid file. Press ENTER to exit")
                sys.exit()
            option4 = getpass("Insert password for decryption: ")
            decrypt(option3, option4)
            print(Fore.GREEN + "Decryption finished")
            input("If everything is ok, "
                  "press ENTER to remove the old file and exit")
            if operative_system() == "Windows":
                system("sdelete64 " + '"' + option3.replace('\\', '/') + '"')
            elif operative_system() == "Linux":
                system("shred -zu " + '"' + option3.replace('\\', '/') + '"')
        elif option2.upper() == 'F':
            print("You have chosen an entire folder")
            option3 = input("Type the folder path or "
                            "simply drag \'n\' drop it: ")
            option3 = option3.replace('"', '').replace("'", '')
            if not path.isdir(option3):
                input(Fore.RED + "Invalid folder. Press ENTER to exit")
                sys.exit()
            option4 = getpass("Insert password for decryption: ")
            allfiles(option3)
            for File in allFiles:
                decrypt(File, option4)
            print(Fore.GREEN + "Decryption finished")
            input("If everything is ok, press ENTER to remove " +
                  "the old files and exit")
            if operative_system() == "Windows":
                for File in allFiles:
                    system("sdelete64 " + '"' + File.replace('\\', '/') + '"')
            elif operative_system() == "Linux":
                for File in allFiles:
                    system("shred -zu " + '"' + File.replace('\\', '/') + '"')
        else:
            input(Fore.RED + "Wrong option selected. Press ENTER to exit")
            sys.exit()
    else:
        input(Fore.RED + "Wrong option selected. Press ENTER to exit")
        sys.exit()

main()
