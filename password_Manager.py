import random
import string
from cryptography.fernet import Fernet


print("What do you want to do?")
print("Type 1 if this is your first time using it.\nType 2 if already used before.\nType 3 for viewing previously saved passowords.")

choice=input()

if choice=='1':
    websitename=input("Enter the site name:")
    username=input("Enter your username/email:")


    s=string.ascii_letters + string.digits + string.punctuation
    n=int(input("Enter length of the password that you need:"))

    while True:
        password="".join(random.sample(s,n))

        print("Here's a password for you:",password)
        print("If you want to use this password,type Yes for another password type No")

        inp=input().lower()
        if inp=="no":
            continue

        elif inp=="yes":
            st1='\n'+"Site:"+websitename+'\n'
            st2="Username/Email:"+username+'\n'
            st3="Password:"+password+'\n'


            #Storing data
            with open("credentials.txt","a") as file:
                file.write(st1+st2+st3)
            #Encryption Process

            def encrypt(filename,master):
                f=Fernet(master)

                with open(filename,"r") as file:
                    file_data=file.read()

                encrypted_data=f.encrypt(bytes(file_data,encoding='utf8'))

                with open(filename,"w") as file:
                    file.write(encrypted_data.decode())


            def write_key():
                key=Fernet.generate_key()
                with open("key.key","wb") as key_file:
                    key_file.write(key)

            def load_key():
                return open("key.key","rb").read()

            write_key()
            filename="credentials.txt"
            key=load_key()
            encrypt(filename,key)

            print("Your credentials have been saved to a file 'credentials.txt' in this directory \nand can be accessed by typing 3 the next time you run this program.")
            break
        else:
            print("Please run this program again and choose yes or no.")
            break

if choice=='2':
    websitename=input("Enter the site name:")
    username=input("Enter your username/email:")


    s=string.ascii_letters + string.digits + string.punctuation
    n=int(input("Enter length of the password that you need:"))

    while True:
        password="".join(random.sample(s,n))

        print("Here's a password for you:",password)
        print("If you want to use this password,type Yes for another password type No")

        inp=input().lower()
        if inp=="no":
            continue

        elif inp=="yes":
            st1='\n'+"Site:"+websitename+'\n'
            st2="Username/Email:"+username+'\n'
            st3="Password:"+password+'\n'

            #Decrypting Previous Data

            def decrypt_again(filename,master):
                f=Fernet(master)
                with open(filename) as file:
                    encrypted_data=file.read()

                decrypted_data=f.decrypt(bytes(encrypted_data,encoding='utf8'))

                with open(filename,"w") as file:
                    file.write(decrypted_data.decode())

            def load_key_again1():
                return open("key.key","rb").read()

            key=load_key_again1()

            filename='credentials.txt'
            decrypt_again(filename,key)

            #Storing data
            with open("credentials.txt","a") as file:
                file.write(st1+st2+st3)

            def encrypt_again1(filename,master):
                f=Fernet(master)

                with open(filename,"r") as file:
                    file_data=file.read()

                encrypted_data=f.encrypt(bytes(file_data,encoding='utf8'))

                with open(filename,"w") as file:
                    file.write(encrypted_data.decode())


            def write_key_again():
                key=Fernet.generate_key()
                with open("key.key","wb") as key_file:
                    key_file.write(key)

            def load_key_again2():
                return open("key.key","rb").read()

            write_key_again()
            filename="credentials.txt"
            key=load_key_again2()
            encrypt_again1(filename,key)
            print("Your credentials have been saved to a file 'credentials.txt' in this directory \nand can be accessed by typing 3 the next time you run this program.")
            break
        else:
            print("Please run this program again and choose yes or no.")
            break


if choice=='3':
    def decrypt(filename,master):
        f=Fernet(master)
        with open(filename) as file:
            encrypted_data=file.read()

        decrypted_data=f.decrypt(bytes(encrypted_data,encoding='utf8'))

        with open(filename,"w") as file:
            file.write(decrypted_data.decode())
    def load_key_again():
        return open("key.key","rb").read()

    key=load_key_again()

    filename='credentials.txt'
    decrypt(filename,key)
    print("You can now go to the file and open it see your credentials.\nWhen done type 'encrypt'")
    while True:
        inp=input()
        if inp=='encrypt':
            def encrypt_again(filename,master):
                f=Fernet(master)

                with open(filename,"r") as file:
                    file_data=file.read()

                encrypted_data=f.encrypt(bytes(file_data,encoding='utf8'))

                with open(filename,"w") as file:
                    file.write(encrypted_data.decode())
            encrypt_again(filename,key)
            print("Encrypted Succesfully.")
            break
