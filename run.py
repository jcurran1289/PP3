import gspread
from google.oauth2.service_account import Credentials
import pdb


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

data = profiles.get_all_values()


def createProfile():
    """
    creates new profile for user and adds to the google sheet
    """
    values_list = SHEET.worksheet('profiles').col_values(1)
    user_profile = []

    username = input("Enter Username or Q to quit:\n(Username must be at least 2 characters)\n").lower()  # noqa
    if username.lower() == 'q':
        main()

    while len(username) < 2:
        print("Username must be at least 2 characters")
        username = input("Please enter username or Q to quit:\n")
        if username.lower() == 'q':
            main()
            break

    while username in values_list:
        print('Username exists')
        username = input("Please enter username or Q to quit:\n")
        if username.lower() == 'q':
            main()
            break
    print(f"Your username: {username}")
    user_profile.append(username)

    while True:
        password = input("Password or Q to quit:\n(Password must be 6 characters long)\n")  # noqa
        if password.lower() == 'q':
            main()
            break
        if validate_password(password):
            user_profile.append(password)
            break

    while True:
        current_acc = input("Inital log into Current Account or Q to quit:\n").strip()  # noqa
        if current_acc.lower() == 'q':
            main()
            break
        if validate_data(current_acc):
            user_profile.append(int(current_acc))
            break
    while True:
        savings_acc = input("Inital log into Savings Account or Q to quit:\n").strip()  # noqa
        if savings_acc.lower() == 'q':
            main()
            break
        if validate_data(savings_acc):
            user_profile.append(int(savings_acc))
            break

    worksheet_to_update = SHEET.worksheet('profiles')
    worksheet_to_update.append_row(user_profile)

    print("Your account has been created successfully.")
    print("\n --Account Summary--")
    print(F"Username: {username}")
    print(F"Current Account: ${current_acc}")
    print(F"Savings Account: ${savings_acc}")
    nextstep = input("\n1.Login or 2.Exit. \nPlease enter 1 or 2\n").strip()
    if int(nextstep) == 1:
        my_bank = Bank()
        my_bank.login(username, password)
    elif int(nextstep) == 2:
        print("Goodbye")


# Class Name should be UpperCase
class CurrentUser:
    """
    Class that stores that has two methods.
    the first method (__init__) gets the password, current account balance
    and savings account balance of the current user
    the second method (checkPassword) checks to see if the password that
    the current user entered matches the password in the google drive sheet
    """

    def __init__(self, username, password, current_account, savings_account):
        self.username = username
        self.password = password
        self.current_account = current_account
        self.savings_account = savings_account

    def check_password(self):
        input_password = input("Enter your password:\n")
        while input_password != self.password and input_password.strip().lower() != "q":  # noqa
            print("Incorrect password")
            input_password = input("Enter your password or Q to quit:\n")
        if input_password == self.password:
            print("\n You have logged in successfully!")
            print("\n ---Account Summary---")
            print(F"Current Account: ${self.current_account}")
            print(F"Savings Account: ${self.savings_account}")
        elif input_password.strip().lower() == 'q':
            main()


# Move into class

def validate_data(values):
    """
    checks to see if user input is numeric
    """
    try:
        if not values.isnumeric():
            raise ValueError("Invalid entry")
        [int(value) for value in values]
    except ValueError:
        print("Invalid entry: please try again!")
        return False
    return True


def validate_account_balance(values, account_balance):
    """
    checks to see if user input is numeric
    and that the account balance is not negative when the user withdraws
    """
    try:
        if not values.isnumeric():
            raise ValueError(
                "Invalid entry"
            )
        [int(value) for value in values]
        if int(account_balance)-int(values) < 0:
            raise ValueError(
                "Insufficient funds"
            )
    except ValueError as e:
        print(f"{e}: please try again!")
        return False
    return True


def validate_password(pw):
    """
    checks to see if user password is 6 characters long
    """
    try:
        if pw.lower() == 'q':
            main()
        if len(pw) < 6:
            raise ValueError(
                f"Password must be 6 characters long, you provided {len(pw)}"
            )
    except ValueError as e:
        print(f"{e}: please try again!")
        return False
    return True


class Bank:
    """
    the main menu of the atm when the user login successfuly
    the user can change their password, withdraw or deposit to/from their account
    """
    def __init__(self):
        self.username = None
        self.password = None
        self.savings_account = None

    def login(self, username, password):
        print("Logging in")
        self.username = username
        self.password = password

        print("\n You have logged in successfully!")
        self.account_balance()
        self.main_menu()

    def account_balance(self):
        print("Getting Account Blance")
        print("\n --- Account Summary ---")
        print(f"Current Account: ${self.get_current_balance(account_type='1')}")
        print(f"Savings Account: ${self.get_current_balance(account_type='2')}")

    def main_menu(self):
        print("Welcome to the Main Menu")
        print(f"\nWelcome Back {self.username}")
        nextstep = input("\nWhat would you like to do:\n1.Withdraw \n2.Deposit \n3.Change Password \nQ.Quit \nPlease enter 1, 2, 3 or Q\n").strip()  # noqa
        while nextstep.lower() not in ("1", "2", "3", "q"):
            print("Invalid entry.\nPlease select 1, 2, 3 or Q to quit")
            nextstep = str(input("Enter your answer here \n").strip())
        if nextstep == '1':
            self.withdraw()
        elif nextstep == '2':
            self.deposit()
        elif nextstep == '3':
            self.change_password()
        elif nextstep.lower() == 'q':
            print("Goodbye")
            # main()

    def deposit(self):
        selected_account = str(input("what account would you like to deposit to:\n1.Current Account \n2.Savings Account \nPlease enter 1, 2, or Q\n")).strip()  # noqa
        while selected_account.lower() not in ("1", "2", "q"):
            print("Invalid entry.\nPlease select 1, 2 or Q to quit")
            selected_account = str(input("Enter your answer here \n").strip())

        if selected_account == '1' or selected_account == '2':
            while True:
                # Print the current Balance
                current_balance = self.get_current_balance(account_type=selected_account)
                print(f"Current Balance: ${int(current_balance)}")

                deposit_amount = input("How much would you like to deposit or type Q to quit:$\n").strip()  # noqa
                if deposit_amount.strip().lower() == 'q':
                    self.main_menu()
                    break

                if validate_data(deposit_amount):
                    cell = profiles.find(self.username)
                    
                    row = cell.row
                    col = cell.col+2 if selected_account == '1' else cell.col+3
                    current_amount = profiles.cell(row, col).value

                    new_amount = int(current_amount)+int(deposit_amount)

                    profiles.update_cell(row, col, new_amount)  # noqa

                    print(f"Current Balance: ${profiles.cell(row, col).value}")  # noqa
                    self.main_menu()
                    break
        elif selected_account.lower() == 'q':
            self.main_menu()

    def withdraw(self):
        selected_account = str(input("what account would you like to withdraw to:\n1.Current Account \n2.Savings Account \nPlease enter 1, 2, or Q\n")).strip()  # noqa
        while selected_account.lower() not in ("1", "2", "q"):
            print("Invalid entry.\nPlease select 1, 2 or Q to quit")
            selected_account = str(input("Enter your answer here \n").strip())

        if selected_account == '1' or selected_account == '2':
            while True:
                # Print the current Balance
                current_balance = self.get_current_balance(account_type=selected_account)
                print(f"Current Balance: ${int(current_balance)}")

                withdraw_amount = input("How much would you like to withdraw or type Q to quit:$\n").strip()  # noqa
                if withdraw_amount.strip().lower() == 'q':
                    self.main_menu()
                    break

                if validate_account_balance(withdraw_amount, current_balance):
                    cell = profiles.find(self.username)
                    row = cell.row
                    col = cell.col+2 if selected_account == '1' else cell.col+3
                    current_amount = profiles.cell(row, col).value

                    new_amount = int(current_amount)-int(withdraw_amount)

                    profiles.update_cell(row, col, new_amount)  # noqa

                    print(f"Current Balance: ${profiles.cell(row, col).value}")  # noqa
                    self.main_menu()
                    break
        elif selected_account.lower() == 'q':
            self.main_menu()

    def change_password(self):
        """
        if the user wishes to change their password
        """
        while True:
            new_password = input("Please enter new password or Q to quit:\n").strip()  # noqa
            if new_password.strip().lower() == 'q':
                    self.main_menu()
                    break
            if validate_password(new_password):
                cell = profiles.find(self.username)
                profiles.update_cell(cell.row, cell.col+1, new_password)  # noqa
                break
        print("Password Updated")
        self.main_menu()

    def get_current_balance(self, account_type=None):
        """
        gets current account balance for username that was entered
        """

        cell = profiles.find(self.username)
        row = cell.row
        col = cell.col+2 if account_type == '1' else cell.col+3
        current_amount = profiles.cell(row, col).value

        return current_amount


def main():
    """
    initial screen
    """
    my_bank = Bank()

    answer = str(input("1.Login or 2.Create a profile. \nPlease enter 1, 2 or Q to quit\n").strip())  # noqa
    while answer.lower() not in ("1", "2", "q"):
        print("Invalid entry.\nPlease select 1, 2 or Q to quit")
        answer = str(input("enter your answer here \n").strip())

    if answer == '1':
        input_username = input("Enter your username:\n").lower()
        result = check_user(input_username)

        if 'data' in result:
            data = result['data']
            username = data['username']
            password = data['password']

            input_password = input("Enter your password:\n")

            while input_password != password and input_password.strip().lower() != "q":  # noqa
                print("Incorrect password")
                input_password = input("Enter your password or Q to quit:\n")
            
            if input_password == password:
                my_bank.login(username, password)
        else:
            print("Username not found")
            main()
            
    elif answer == '2':
        createProfile()
    elif answer.lower() == 'q':
        print("---Goodbye---")


def check_user(input_username):
    """
    checks if the username exists
    """
    cell = profiles.find(input_username)
    if cell:
        username = profiles.cell(cell.row, cell.col).value
        password = profiles.cell(cell.row, cell.col+1).value
        current_account = profiles.cell(cell.row, cell.col+2).value
        savings_account = profiles.cell(cell.row, cell.col+3).value  # noqa

        return {"data": {"username": username, "password": password, "current_account": current_account, "savings_account": savings_account}}
    else:
        return {"success": False}


def get_current_balance(self, account_type=None):
    """
    gets current account balance for username that was entered
    """

    cell = profiles.find(self.username)
    row = cell.row
    col = cell.col+2 if account_type == '1' else cell.col+3
    current_amount = profiles.cell(row, col).value

    return current_amount


print("Welcome to ATM")
main()
