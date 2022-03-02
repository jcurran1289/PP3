import gspread
from google.oauth2.service_account import Credentials

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

exist_username = SHEET.worksheet('profiles').get_values('A:A')
data = profiles.get_all_values()


def createProfile():
    user_profile = []
    
    print("Enter Username.")
    print("Your username could not contain special characters")
    print(exist_username)
    username = input("Username:")

    if username in Extract(exist_username):
        print('Username exists')
    else:
        print(f"Your username: {username}")
        user_profile.append(username)
        print(user_profile)
        password = input("Password:")
        user_profile.append(password)
        print(user_profile)
        current_acc = input("Inital log into Current Account:")
        user_profile.append(int(current_acc))
        print(user_profile)
        savings_acc = input("Inital log into Savings Account:")
        user_profile.append(int(savings_acc))
        print(user_profile)
        worksheet_to_update = SHEET.worksheet('profiles')
        worksheet_to_update.append_row(user_profile)


def Extract(lst):
    return [item[0] for item in lst]

      
print("Welcome to ATM. please choose an 1 or 2?")

firststep = input("1.Login or 2.Create a profile. please enter 1 or 2\n")

if int(firststep) == 1:
    print("wwee")
elif int(firststep) == 2:
    createProfile()
