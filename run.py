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


class currentuser:
    def __init__(self, username, password, current_account, savings_account):
        self.username = username
        self.password = password
        self.current_account = current_account
        self.savings_account = savings_account


def profileFind(username):
    cell = SHEET.worksheet('profiles').find(username)
    return cell


def createProfile():
    values_list = SHEET.worksheet('profiles').col_values(1)
    user_profile = []

    print("Enter Username.")
    print("Your username could not contain special characters")
    username = input("Username:\n")

    while username in values_list:
        print('Username exists')
        print("Enter Username.")
        print("Your username could not contain special characters")
        username = input("Username:\n")
    print(f"Your username: {username}")
    user_profile.append(username)

    password = input("Password:\n")
    user_profile.append(password)

    while True:
        current_acc = input("Inital log into Current Account:\n")
        if validate_data(current_acc):
            user_profile.append(int(current_acc))
            break
    while True:
        savings_acc = input("Inital log into Savings Account:\n")
        if validate_data(savings_acc):
            user_profile.append(int(savings_acc))
            break

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

    password = profiles.cell(profileFind(username).row,
                             profileFind(username).col+1).value
    return password


def accountCurrentAccount(username):

    currentAccount = profiles.cell(profileFind(username).row,
                                   profileFind(username).col+2).value
    return currentAccount


def accountSavingsAccount(username):

    savingsAccount = profiles.cell(profileFind(username).row, profileFind(username).col+3).value  # noqa
    return savingsAccount


def login():
    inputUsername = input("Enter your username:\n")
    profileFind(inputUsername)
    Current_user = currentuser(SHEET.worksheet('profiles').find(inputUsername),
                            accountPassword(inputUsername),
                            accountCurrentAccount(inputUsername),
                            accountSavingsAccount(inputUsername))   # noqa
    print(Current_user.current_account)

    inputPassword = input("Enter your password:\n")
    # if accountPassword(inputUsername) == inputPassword:
    while inputPassword not in (Current_user.password, "q"):
        print("Incorrect password")
        inputPassword = input("Enter your password:\n")
    if inputPassword == Current_user.password:
        print("---Account Summary---")
        print(F"Current Account: ${Current_user.current_account}")
        print(F"Savings Account: ${Current_user.savings_account}")
        mainMenu(inputUsername)


def mainMenu(username):

    nextstep = input("\nWhat would you like to do:\n1.Withdraw \n2.Deposit \n3.Change Password \nQ.Quit \nPlease enter 1, 2, 3 or Q\n")  # noqa
    if int(nextstep) == 1:
        accountWithdrawn(username)
    elif int(nextstep) == 2:
        accountDeposit(username)
    elif int(nextstep) == 3:
        changePassword(username)
    elif nextstep.lower() == 'q':
        print("Goodbye")


def accountWithdrawn(username):

    inputWithdrawAccount = str(input("what account would you like to withdraw from:\n1.Current Account \n2.Savings Account \nQ.Quit  \nPlease enter 1, 2, or Q\n").strip())  # noqa
    while inputWithdrawAccount.lower() not in ("1", "2", "q"):
        print("Please select 1, 2 or Q to quit")
        inputWithdrawAccount = str(input("Enter your answer here \n").strip())
    if inputWithdrawAccount == '1':
        while True:
            print(F"Current Balance: ${int(accountCurrentAccount(username))}")
            inputWithdrawAmountCurrent = input("How much would you like to withdraw:$\n")  # noqa
            if validate_data(inputWithdrawAmountCurrent):
                profiles.update_cell(profileFind(username).row, profileFind(username).col+2, int(accountCurrentAccount(username))-int(inputWithdrawAmountCurrent))  # noqa
                print(F"New Balance: ${profiles.cell(profileFind(username).row, profileFind(username).col+2).value}")  # noqa
                mainMenu(username)
                break
    elif inputWithdrawAccount == '2':
        while True:
            print(F"Current Balance: ${int(accountSavingsAccount(username))}")
            inputWithdrawAmountSavings = input("How much would you like to withdraw:$\n")  # noqa
            if validate_data(inputWithdrawAmountSavings):
                profiles.update_cell(profileFind(username).row, profileFind(username).col+3, int(accountSavingsAccount(username))-int(inputWithdrawAmountSavings))  # noqa
                print(F"Current Balance: ${profiles.cell(profileFind(username).row, profileFind(username).col+3).value}")  # noqa
                mainMenu(username)
                break
    elif inputWithdrawAccount.lower() == 'q':
        print("Goodbye")


def accountDeposit(username):

    inputDepositAccount = str(input("what account would you like to deposit to:\n1.Current Account \n2.Savings Account \nPlease enter 1, 2, or Q\n"))  # noqa
    while inputDepositAccount.lower() not in ("1", "2", "q"):
        print("Please select 1, 2 or Q to quit")
        inputDepositAccount = str(input("Enter your answer here \n").strip())
    if inputDepositAccount == '1':
        while True:
            print(F"Current Balance: ${int(accountCurrentAccount(username))}")
            inputDepositAmountCurrent = input("How much would you like to deposit:$\n")  # noqa
            if validate_data(inputDepositAmountCurrent):
                profiles.update_cell(profileFind(username).row, profileFind(
                    username).col+2, int(accountCurrentAccount(username))+int(inputDepositAmountCurrent))  # noqa
                print(
                    F"Current Balance: ${profiles.cell(profileFind(username).row, profileFind(username).col+2).value}")  # noqa
                mainMenu(username)
                break
    elif inputDepositAccount == '2':
        while True:
            print(F"Current Balance: ${int(accountCurrentAccount(username))}")
            inputDepositAmountSaving = input("How much would you like to deposit:$\n")  # noqa
            if validate_data(inputDepositAmountSaving):
                profiles.update_cell(profileFind(username).row, profileFind(username).col+3, int(accountSavingsAccount(username))+int(inputDepositAmountSaving))  # noqa
                print(F"Current Balance: ${profiles.cell(profileFind(username).row, profileFind(username).col+3).value}")  # noqa
                mainMenu(username)
                break
    elif inputDepositAccount.lower() == 'q':
        print("Goodbye")


def changePassword(username):
    updatedPassword = input("Please enter new password:\n")
    profiles.update_cell(profileFind(username).row,
                         profileFind(username).col+1, updatedPassword)
    login()


def validate_data(values):

    try:
        [int(value) for value in values]
    except ValueError as e:
        print(f"Invalid amount: please try again!")
        return False
    return True


def main():
    answer = str(input("1.Login or 2.Create a profile. \nPlease enter 1 or 2\n").strip())  # noqa
    while answer.lower() not in ("1", "2", "q"):
        print("Please select 1, 2 or Q to quit")
        answer = str(input("enter your answer here \n").strip())
    if answer == '1':
        login()
    elif answer == '2':
        createProfile()
    elif answer.lower() == 'q':
        print("Goodbye")


print("Welcome to ATM")
main()