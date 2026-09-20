import sqlite3
from cryptography.fernet import Fernet
import getpass
import os

# Importing the relevant libraries

connection = sqlite3.connect(':memory:', check_same_thread = False)
# Creating in-memory sqlite db so that on restarts we do not face problem of data already existing

def getConnection():
    return connection

# Run execute script to load whole data into database tables
def init_db():
    cursor =  connection.cursor()
    databaseScriptFile = open('/Users/hannahhemnani/Desktop/WM187/Password Manager/database.sql', "r")
    databaseScript = databaseScriptFile.read()
    databaseScriptFile.close()
    print(f"creating the conditions database")
    cursor.executescript(databaseScript)
    cursor.close()


#  Subroutine for creating an account and adding to the database
def newCredentialsInDB(accountName,user_password):
    cursor = connection.cursor()


    cursor.execute('''
    INSERT into credentials (user_account, user_password)
    VALUES (?,?)
    ''', (accountName,user_password))
    connection.commit()
    cursor.close()

#  This function creates an encryption key and stores it so it can be reused for decryption
def encryptionKey (filePath = 'fernetKey.key'):
    if os.path.exists(filePath):
        with open('fernetKey.key','rb') as fileKey:
            key = fileKey.read()
    else:
        key = Fernet.generate_key()
        with open('fernetKey.key','wb') as fileKey:
            fileKey.write(key)
    return key

# this function checks if the account exists in the table to ensure the account name stays unique
def isAccountExists(accountName,f):
    cursor = connection.cursor()
    isFound = cursor.execute('''
    SELECT * FROM CREDENTIALS WHERE user_account = ?
    ''', (accountName,)).fetchone()
    cursor.close()
    if isFound:
        print("This username is already in use, please enter a different one ")
        return True 
    else:
        return False

#  This function creates and adds a new account in the data base
def createAccount(f):
    while True:
        accountName = input("please input username ")
        if not isAccountExists(accountName,f):
            break
    # this calls isAccountExists to ensure that the new account user name is unique

    new_password = False
 
    while new_password ==False:
        accountPassword = getpass.getpass()
        # getpass.getpass hides the password when being entered for security
        if len(accountPassword) > 8:
            new_password = True
        else:
            print("needs at least 8 characters ")
    print("please enter password again to confirm ")
    confirm_new_password = getpass.getpass()
    # confirming password for security
    if confirm_new_password == accountPassword:
        print("password confirmed ")
        user_password = f.encrypt(confirm_new_password.encode())
        # encrypting the new password to store in the database
        newCredentialsInDB(accountName,user_password)
        # calls function to create and implement account into the database
        return user_password
    else:
        print("password did not match, try again ")
        createAccount(f)

# this function returns the decrypted password of the requested account from the database
def retrievePassword(f,accountRequested):
    cursor = connection.cursor()
    cursor.execute('''
    SELECT user_password
    FROM credentials 
    WHERE user_account = ?''',(accountRequested,))
    encryptedPassword = cursor.fetchone()
    cursor.close()
    if encryptedPassword == None:
        print("account doesn't exist")
        return ""
    else:
        decryptedPassword = f.decrypt(encryptedPassword[0]).decode()
        # decrypts the password stored in the database with the same key that was stored
        return decryptedPassword,encryptedPassword[0]

# This function calls other functions. It creats the database, loads the key and displays the menu of options on loop until exit option is chosen
def main():
    cursor = connection.cursor()
    init_db()
    key = encryptionKey()
    f = Fernet(key)
    action = " "
    while action != 'c':
        action = input("would you like to create account or view account, press 'a' for create account or 'b' for view account or 'c' for exit ")
        if action == 'a':
            createAccount(f)
        elif action == 'b':
            accountRequested = input("which account's password do you want? ")
            userPassword = retrievePassword(f,accountRequested)
            if userPassword != "" :
                print(f"\nusername: {accountRequested} encrypted password is {userPassword[0]} decrypted password: {userPassword[1]}")


if __name__ == "__main__":
    main()









       

     




