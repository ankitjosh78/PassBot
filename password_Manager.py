import random
import string

websitename=input("Enter the site name:")

username=input("Enter your username/email:")


s=string.ascii_letters + string.digits + string.punctuation
n=int(input("Enter length of the password that you need:"))
password="".join(random.sample(s,n))

print("Here's a password for you:",password)

st1="Site:"+websitename+'\n'
st2="Username/Email:"+username+'\n'
st3="Password:"+password+'\n'

with open("credentials.txt","a") as file:
    file.write(st1)
    file.write(st2)
    file.write(st3)
    file.write('\n')

print("Your credentials have been saved to a file 'credentials.txt' in this directory.")
