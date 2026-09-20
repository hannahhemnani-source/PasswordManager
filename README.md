# PasswordManager
A simple password manager that utilises encryption, enabling users to store and retrieve passwords securely. 

SafePass Password Manager
The SafePass password manager allows user to create accounts and store their passwords in a database securely using encryption. It also allows users to then access passwords from the database for.

Description

This python based password managers allows users to securely create and retrieve account passwords securely. Account details are stored in an SQL database. This is useful as it enhances security, protects sensitiver user information whilst also allowing users to access their passwords without having to remember them.
Features
- Creates new accounts uniquely
- Stores passwords securely using encryption
- Stores credentials in an in memory SQLite database
- Retrieves decrypted password upon user request
- Hides password input when creating account using'getpass'
- Prevents duplicate account creation

Dependencies
- Modules:
  - 'cryptography'
  - 'sqlite3' (this is built in)
  - 'getpass'
  - 'os'



Installing
- Clone the project from Git repository to local computer
'''git clone https://git-lab.cyber.warwick.ac.uk/c5680156/wm187_safepass_5680156/-/tree/ef86e3f5f0f8029b1d1fe5284509d6c089452689/'''
- change current folder into repository folder
'''cd <wm187_safepass_5680156>'''
- Ensure the database.sql file path in init_db() matches where it has been stored. In the code this it stored under '/Users/hannahhemnani/Desktop/WM187/Password Manager/database.sql'
- change this path to your file path


Executing program
- How to run the program
- Run the program on operating system command line (e.g terminal for macOS)
- activate a virtual environment to provide clean slate to run on
'''source venv/bin/activate''' for macOS/Linux
'''venv\Scripts\activate''' for Windows
- Run main Python script from inside the file it is stored in
'''python main.py'''
- Follow the prompts in the terminal:
  - 'a' to create a new account
  - 'b' to retrieve an existing account's password
  - 'c' to exit the program
 
    
Running Unit Tests
- Ensure testmain.py is stored in the same file path as main.py
- Run unittest file using '''python -m unittest testmain.py'''
- Uses unittest module

Help
- Use ctrl c or ctrl z to exit program and restart if any issues encountered
- If following error returned "python command not found" try again using python3 as the command instead
