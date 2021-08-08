import base64
import os
import random
import string

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Sample Space
sampleSpace = string.ascii_letters + string.digits + string.punctuation

# Functions
# For getting the credentials


def getCredentials():
    # Credentials Input
    websiteName = input(
        "Enter the website name whose details you want to save:")
    username = input("Enter the username/email for the site:")
    passChoice = input(
        "If you want to use a strong generated password type 1 or If you want to use your own password type 2:"
    )

    if passChoice == '1':
        passLen=16
        passLenChoice=input("Default password length is 16, To use a longer/shorter password type 'n' else press any other key:")
        if passLenChoice.lower()=="n":
            passLen = int(
                input(
                    "Enter the length of the password that you want to use(e,g:8/10/69) [MAX:128]:"
                ))
            if(passLen > 128):
                passLen=16
                print("Password length too big , reverting back to default size of 16.")        
        password=""
        while passLen!=0:
            password+=random.choice(sampleSpace)
            passLen-=1

    elif passChoice == '2':
        password = input("Enter the password that you want to use:")

    return [websiteName, username, password]


# For getting the master password


def getMasterPassword(case):
    if case==1:
        masterPassword = input(
            "Enter a master password to store all your credentials(make sure you remember it):"
        ).encode()
    if case==2:
        masterPassword = input(
                "Enter your master password to continue:").encode()

    return masterPassword


# For deriving the key


def keyDeriving(masterPassword, salt=None):
    # Making a salt file
    if salt != None:
        with open("salt.txt", "wb") as slt:
            slt.write(salt)

    #When the salt file is already present
    elif salt == None:
        try:
            with open("salt.txt","rb") as slt:
                salt = slt.read()
        # If salt file is not found then it has not been created or is removed.
        except FileNotFoundError:
            print()
            print(
                "Error! No entries found! They have been either deleted or not created at the first place."
            )
            quit()
    # One time process of deriving key from master password and salt.

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    new_key = base64.urlsafe_b64encode(kdf.derive(masterPassword))

    return new_key


# For writing the data


def writeData(websiteName, username, password, mode):
    s1 = '\n' + 'Site:' + websiteName + '\n'
    s2 = 'User id:' + username + '\n'
    s3 = 'Password:' + password + '\n'
    # Writing the credentials to a text file.
    with open("credentials.txt", mode) as file:
        file.write(s1 + s2 + s3)


# For encryting the data


def encryptData(key, case):
    f = Fernet(key)

    # Encryption process
    with open("credentials.txt") as file:
        data = file.read()
    encryptedData = f.encrypt(bytes(data, encoding='utf8'))

    with open("credentials.txt", "w") as file:
        file.write(encryptedData.decode())
    if case == 1:
        print("Your credentials have been safely stored and are encrypted.")
        return
    if case == 2:
        quit()
    if case == 3:
        print("Encrypted")


# For decrypting the data


def decryptData(new_key):
    f = Fernet(new_key)
    with open("credentials.txt") as file:
        encryptedData = file.read()

    try:
        decryptedData = f.decrypt(bytes(encryptedData, encoding='utf8'))

        with open("credentials.txt", "w") as file:
            file.write(decryptedData.decode())

        return
    except InvalidToken:
        print()
        print("Wrong password, please try again!")

        quit()


# Help section


def helpSection():
    print()
    print(
        "Right now,you are viewing the help section of PassBot(A simple yet quite effective password manager)"
    )
    print("If you are using this for the 1st time then type 'new' \n")
    print(
        "If you have already used this to save some passwords and want to view them ,then type 'old' and choose option 2"
    )
    print(
        "If you have already used this and want to save another password,then type 'old' and choose 1"
    )
    print("You will now go back to the menu.")
    print()
    return

# Main program starts from here.
# Greetings!
print(
    "Hello, welcome to PassBot. This is a simple,easy to use password manager,to store all your important credentials."
)

while True:
    print("To know more, type 'help'")
    print(
        "If you are ready to use and this is your first time,Type 'New'\nIf already used before type 'Old'"
    )

    userChoice = input("Enter your choice:").lower()

    if userChoice == 'new':

        while True:
            # prompt for ready

            readyOrNot = input(
                "Now we shall ask you for your credentials.When ready type 'ready' else type 'quit':"
            )
            # if ready

            if readyOrNot.lower() == "ready":
                # input of credentials
                websiteName, username, password = [
                    str(x) for x in getCredentials()
                ]

                # Input for master password
                masterPassword = getMasterPassword(1)

                # One time process
                salt = os.urandom(16)
                key = keyDeriving(masterPassword, salt)

                # writing the data
                writeData(websiteName, username, password, 'w')

                # Encryption process
                encryptData(key, 1)

                break
            elif readyOrNot.lower() == 'quit':
                quit()
            else:
                print("Wrong Choice")
        break
    if userChoice == 'old':
        print(
            "To enter new credentials type 1\nTo view saved passwords type 2:")
        manageOrStore = input("Enter your choice:")

        # If user wants to enter new data
        if manageOrStore == '1':

            masterPassword=getMasterPassword(2)

            new_key = keyDeriving(masterPassword)

            decryptData(new_key)

            while True:
                readyOrNot = input(
                    "Now we shall ask you for your credentials.When ready type 'ready' else type 'quit': "
                )
                if readyOrNot.lower() == "ready":

                    websiteName, username, password = [
                        str(x) for x in getCredentials()
                    ]

                    writeData(websiteName, username, password, 'a')

                    encryptData(new_key, 1)

                    break

                # If user wants to quit
                elif readyOrNot.lower() == 'quit':
                    encryptData(new_key, 2)

        # If user wants to view stored data
        if manageOrStore == '2':

            masterPassword=getMasterPassword(2)

            new_key = keyDeriving(masterPassword)
            decryptData(new_key)

            print(
                "The file is now decrypted and you can go to it to see your credentials."
            )

            while True:
                inp = input("When done type 'encrypt': ")
                if inp.lower() == 'encrypt':
                    encryptData(new_key, 3)
                    break
        break

    if userChoice == 'help':
        helpSection()
    else:
        print("Wrong Choice, you will be sent to the help section now")
        print()
