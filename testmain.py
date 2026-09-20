import unittest
import sqlite3
from cryptography.fernet import Fernet
import os
from main import init_db,encryptionKey,newCredentialsInDB,isAccountExists,retrievePassword, getConnection

class TestPasswordManager(unittest.TestCase):

    def setUp(self):
        self.conn = getConnection()
        self.testFile = 'testFernetKey.key'
        print("setup")
        init_db()
        self.cursor = self.conn.cursor()
# set up and tear down methods ensure the test environment is prepared beforehand and cleaned up after the tests occur
    def tearDown(self):
        print("tear down")
        if os.path.exists(self.testFile):
            os.remove(self.testFile)
        self.cursor.close()

# this test checks if the encryption key works
    def test_encryptionKey_works(self):
        key = encryptionKey()
        self.assertTrue(os.path.exists('fernetKey.key'))
        self.assertIsInstance(key,bytes)
        Fernet(key)
        secondKey = encryptionKey()
        # checking if the same key is returned when function is returned
        self.assertEqual(key,secondKey)

# this test tests if the credentials in the database are inserted correctly
    def test_newCredentialsInDB(self):
        key = encryptionKey()
        f = Fernet(key)
        cursor = self.conn.cursor()
        testPassword = f.encrypt(b'password123')
        newCredentialsInDB("user123",testPassword)
        # this creates a new user in the database
        checkExists = cursor.execute('''
        SELECT * FROM credentials WHERE user_password = ? ''' ,(testPassword,)).fetchone()
        self.assertEqual("user123",checkExists[1])
        # this checks if the user exists by searching by the password in the database
        cursor.close()

# this checks if a user name is unique when creating the account
    def test_isAccountExists(self):
        cursor = self.conn.cursor()
        key = encryptionKey()
        f = Fernet(key)
        cursor.execute('''
        INSERT INTO credentials (user_account, user_password)
        VALUES (?,?)''', ("existingUser",f.encrypt(b'password1'))
        )
        self.conn.commit()
        # creating a test account
        doesExist = isAccountExists("existingUser",f)
        # calling isAccountExists with an existing user to check if it exists
        self.assertTrue(doesExist)
        cursor.close()
    
# tests if the decrypted password is returned if requested
    def test_retrievePassword(self):
        cursor = self.conn.cursor()
        key = encryptionKey()
        f = Fernet(key)

        cursor.execute('''
        INSERT INTO credentials (user_account, user_password)
        VALUES (?,?)''', ("user1",f.encrypt(b'findThisPassword'))
        )
        self.conn.commit()
        # creating a test account 

        retrieveUserPassword = retrievePassword(f,"user1")
        self.assertEqual(retrieveUserPassword[0],"findThisPassword")
        # finds the password in database and checks if it is decrypted correctly

        noResult = retrievePassword(f,"accountDoesntExist")
        self.assertEqual(noResult, "")
        # error handling, checks if empty string is returned if the account does not exist in database








if __name__ == '__main__':
    init_db()
    unittest.main()

