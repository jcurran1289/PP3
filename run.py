import gspread
from google.oauth2.service_account import Credentials
import numpy as np


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('pythonATM')

profiles = SHEET.worksheet('profiles')


exist_test = SHEET.worksheet('profiles').get_values('A:b')
exist_username = SHEET.worksheet('profiles').get_values('A:A')
exist_password = SHEET.worksheet('profiles').get_values('B:B')
exist_current_account = SHEET.worksheet('profiles').get_values('C:C')
exist_savings_account = SHEET.worksheet('profiles').get_values('D:D')
numpyUsername = np.array(exist_username)

data = profiles.get_all_values()


def createProfile():
    user_profile = []
    
    print("Enter Username.")
    print("Your username could not contain special characters")
    username = input("Username:")

    if username in Extract(exist_username):
        print('Username exists')
    else:
        print(f"Your username: {username}")
        user_profile.append(username)
        
        password = input("Password:")
        user_profile.append(password)
      
        current_acc = input("Inital log into Current Account:")
        user_profile.append(int(current_acc))
       
        savings_acc = input("Inital log into Savings Account:")
        user_profile.append(int(savings_acc))
       
        worksheet_to_update = SHEET.worksheet('profiles')
        worksheet_to_update.append_row(user_profile)

        print("Your account has been created successfully.")
        print("--Account Summary--")
        print(F"Username: {username}")
        print(F"Current Account: ${current_acc}")
        print(F"Savings Account: ${savings_acc}")
        nextstep = input("\n1.Login or 2.Exit. \nPlease enter 1 or 2\n")
        if int(nextstep) == 1:
            login()
        elif int(nextstep) == 2:
            print("Goodbye")

def accountPassword(username):
    #numpyPassword = np.array(exist_password)
    #arr_index = np.where(numpyUsername == username)
    #password = numpyPassword[arr_index][0]
    password = profiles.cell(profileFind(username).row, profileFind(username).col+1).value
    return password

def accountCurrentAccount(username):
    numpyCurrentAccount = np.array(exist_current_account)
    arr_index = np.where(numpyUsername == username)
    currentAccount = numpyCurrentAccount[arr_index][0]
    return currentAccount

def accountSavingsAccount(username):
    numpySavingsAccount = np.array(exist_savings_account)
    arr_index = np.where(numpyUsername == username)
    savingsAccount = numpySavingsAccount[arr_index][0]
    return savingsAccount

def login():
    inputUsername = input("Enter your username:")
    profileFind(inputUsername)
    inputPassword = input("Enter your password:")
    if accountPassword(inputUsername) == inputPassword:
        print("---Account Summary---")
        print(F"Current Account: ${accountCurrentAccount(inputUsername)}")
        print(F"Savings Account: ${accountSavingsAccount(inputUsername)}")
        nextstep = input("\nWhat would you like to do:1.Withdraw or 2.Deposit or 3.Change Password. \nPlease enter 1, 2 or 3\n")
        if int(nextstep) == 1:
            accountWithdrawn(inputUsername)
        elif int(nextstep) == 2:
            accountDeposit(inputUsername)
        elif int(nextstep) == 3:
            changePassword(inputUsername)
    else:
        print("Incorrect password")
        login()

def accountWithdrawn(username):
    inputWithdrawAccount = input("what account would you like to withdraw from:\n1.Current Account \n2.Savings Account \nPlease enter 1 or 2\n")
    inputWithdrawAmount = input("Amount:$")
    if int(inputWithdrawAccount) == 1:
        #print(F"Current Balance: ${int(accountCurrentAccount(username))-int(inputWithdrawAmount)}")
        profiles.update_cell(profileFind(username).row, profileFind(username).col+2, int(accountCurrentAccount(username))-int(inputWithdrawAmount))
        print(F"Current Balance: ${profiles.cell(profileFind(username).row, profileFind(username).col+2).value}")
        login()
    elif int(inputWithdrawAccount) == 2:
        #print(F"Current Balance: ${int(accountSavingsAccount(username))-int(inputWithdrawAmount)}")
        profiles.update_cell(profileFind(username).row, profileFind(username).col+3, int(accountSavingsAccount(username))-int(inputWithdrawAmount))
        print(F"Current Balance: ${profiles.cell(profileFind(username).row, profileFind(username).col+3).value}")
        login()

def accountDeposit(username):
    inputDepositAccount = input("what account would you like to deposit to:\n1.Current Account \n2.Savings Account \nPlease enter 1 or 2\n")
    inputDepositAmount = input("Amount:$")
    if int(inputDepositAccount) == 1:
        #print(F"Current Balance: ${int(accountCurrentAccount(username))+int(inputDepositAmount)}")
        profiles.update_cell(profileFind(username).row, profileFind(username).col+2, int(accountCurrentAccount(username))+int(inputWithdrawAmount))
        print(F"Current Balance: ${profiles.cell(profileFind(username).row, profileFind(username).col+2).value}")
        login()
    elif int(inputDepositAccount) == 2:
        profiles.update_cell(profileFind(username).row, profileFind(username).col+3, int(accountSavingsAccount(username))+int(inputWithdrawAmount))
        print(F"Current Balance: ${profiles.cell(profileFind(username).row, profileFind(username).col+3).value}")
        login()

def profileFind(username):
    cell = SHEET.worksheet('profiles').find(username)
    return cell

print("Welcome to ATM. please choose an 1 or 2?")
firststep = input("1.Login or 2.Create a profile. \nPlease enter 1 or 2\n")
#print(F"Current Account: {cell}")
if int(firststep) == 1:
    print(F"Current Account: {exist_test}")
    login()
elif int(firststep) == 2:
    createProfile()
