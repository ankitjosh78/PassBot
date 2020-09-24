from cryptography.fernet import Fernet
import  base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import string
import random

sampleSpace=string.ascii_letters+string.digits+string.punctuation

#Greeting!
print("Hello, welcome to PassBot. This is a simple,easy to use password manager,to store all your important credentials.")

while True:
    print("To know more, type 'help'")
    print("If you are ready to use and this is your first time,Type 'New'\nIf already used before type 'Old")

    userChoice=input("Enter your choice:").lower()

    if userChoice=='new':
        
        while True:
            readyOrNot=input("Now we shall ask you for your credentials.When ready type 'ready' else type 'quit':")
            
            #Credentials Input
            if readyOrNot.lower()=="ready":
                websiteName=input("Enter the website name whose details you want to save:")
                username=input("Enter the username/email for the site:")
                passChoice=input("If you want to use a strong generated password type 1 or If you want to use your own password type 2:")
                
                if passChoice=='1':
                    passLen=int(input("Enter the length of the password that you want to use(e,g:8/10):"))
                    password="".join(random.sample(sampleSpace,passLen))
                
                elif passChoice=='2':
                    password=input("Enter the password that you want to use:")
                
                else:
                    print("Wrong Choice")
                    continue

                #Input for master password
                masterPassword=input("Enter a master password to store all your credentials(make sure you remember it):").encode()
                salt=b'salt_'
                #Making a salt file
                with open("salt.txt","w") as slt:
                    slt.write(salt.decode())
                
                #One time process
                kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
                #Deriving the key from the masterPassword and salt.
                key=base64.urlsafe_b64encode(kdf.derive(masterPassword))

                s1='\n'+'Site:'+websiteName+'\n'
                s2='User id:'+username+'\n'
                s3='Password:'+password+'\n'
                #Writing the credentials to a text file.
                with open("credentials.txt","w") as file:
                    file.write(s1+s2+s3)

                #Initializing the Fernet
                f=Fernet(key)
                #Encryption process
                with open("credentials.txt") as file:
                    data=file.read()
                encryptedData=f.encrypt(bytes(data,encoding='utf8'))

                with open("credentials.txt","w") as file:
                    file.write(encryptedData.decode())

                print("Your credentials have been safely stored and are encrypted.")
                break
            elif readyOrNot.lower()=='quit':
                quit()        
            else:
                print("Wrong Choice")
        break
    if userChoice=='old':
        print("To enter new credentials type 1\nTo view saved passwords type 2:")
        manageOrStore=input("Enter your choice:")
        #If user wants to enter new data
        if manageOrStore=='1':
            masterPassword=input("Enter your master password:").encode()
            
            with open("salt.txt") as slt:
                salt=slt.read().encode()

            kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
            new_key=base64.urlsafe_b64encode(kdf.derive(masterPassword))

            f=Fernet(new_key)
            with open("credentials.txt") as file:
                encryptedData=file.read()
            
            decryptedData=f.decrypt(bytes(encryptedData,encoding='utf8'))

            with open("credentials.txt","w") as file:
                file.write(decryptedData.decode())
            
            while True:
                readyOrNot=input("Now we shall ask you for your credentials.When ready type 'ready' else type 'quit': ")
                if readyOrNot.lower()=="ready":
                    
                    websiteName=input("Enter the website name whose details you want to save:")
                    username=input("Enter the username/email for the site:")
                    passChoice=input("If you want to use a strong generated password type 1 or If you want to use your own password type 2:")
                    
                    if passChoice=='1':
                        passLen=int(input("Enter the length of the password that you want to use(e,g:8/10):"))
                        password="".join(random.sample(sampleSpace,passLen))
                    
                    elif passChoice=='2':
                        password=input("Enter the password that you want to use:")
                    
                    else:
                        print("Wrong Choice")
                        continue
                    s1='\n'+'Site:'+websiteName+'\n'
                    s2='User id:'+username+'\n'
                    s3='Password:'+password+'\n'
                    with open("credentials.txt","a") as file:
                        file.write(s1+s2+s3)
                    with open("credentials.txt") as file:
                        data=file.read()
                    encryptedData=f.encrypt(bytes(data,encoding='utf8'))
                    with open("credentials.txt","w") as file:
                        file.write(encryptedData.decode())
                        print("Your credentials have been safely stored and are encrypted.")
                    
                    break

                #If user wants to quit        
                elif readyOrNot.lower()=='quit':
                    with open("credentials.txt") as file:
                        data=file.read()
                    encryptedData=f.encrypt(bytes(data,encoding='utf8'))
                    with open("credentials.txt","w") as file:
                        file.write(encryptedData.decode())
                    quit()

        #If user wants to view stored data
        if manageOrStore=='2':
            
            masterPassword=input("Enter your master password to continue:").encode()
            with open("salt.txt") as slt:
                salt=slt.read().encode()
            #Key deriving process
            kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
            new_key=base64.urlsafe_b64encode(kdf.derive(masterPassword))
            f=Fernet(new_key)
            with open("credentials.txt") as file:
                encryptedData=file.read()
            
            decryptedData=f.decrypt(bytes(encryptedData,encoding='utf8'))

            with open("credentials.txt","w") as file:
                file.write(decryptedData.decode())
            print("The file is now decrypted and you can go to it to see your credentials.")
            
            while True:
                inp=input("When done type 'encrypt': ")
                if inp.lower()=='encrypt':
                    with open("credentials.txt") as file:
                        data=file.read()
                    encryptedData=f.encrypt(bytes(data,encoding='utf8'))
                    with open("credentials.txt","w") as file:
                        file.write(encryptedData.decode())
                    print("Encrypted")
                    break
        break    
            
    if userChoice=='help':
        print()
        print("Right now,you are viewing the help section of PassBot(A simple yet quite effective password manager)")
        print("If you are using this for the 1st time then type 'new' \n")
        print("If you have already used this to save some passwords and want to view them ,then type 'old' and choose option 2\n")
        print("If you have already used this and want to save another password,then type 'old' and choose 1")
        print("You will now go back to the menu.")
        print()
