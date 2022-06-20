![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)
# Python ATM
Python ATM  is a Python terminal system, which runs in the Code Institute mock terminal on Heroku.

Users have the ability to create a bank account in the ATM, update their account details, withdraw and deposit money and the accounts being updated in real time.
## How to use
The ATM has simply controls and interface. The user will be promted to enter a number depending on what they action they would like to carry. They can enter Q at anytime to quit the system.

## Features
### Exisiting Features
- User authentication
- Real time account summary
- Real Time account updates
- Account setup
- Input validation and error checking
- Balance checking. Account is not able to go into negative digits
- Data for user profiles is maintained in an class instance

### Future Features
- Allow users to see past transactions

## Data Model
I used the currentuser class as my model. The class currentuser stores the current user's password, the current balance of their current account and the current balance of their savings account


## Testing
I have manually tested this project by doing the following:
- Passed the code through a PEP8 linter and confirmed there are no problems
- Given invalid inputs: strings when numbers are expected, negative values, non-integers, withdraw more than there is in the account, usernames that are already choosen other users and invalid passwords

### Bugs
## Solved Bugs
- When i entered a string when withdrawing or depositing money, the program would crash. i fixed this by adding data validation function to the input.
- When the program asks to choose one of the options on the screen and the user enters an option not listed, the program would crash. I fixed this by adding a while loop to to only accept the options displayed
- As i got more comfortable with github, I started to use the issues tab to track bugs: https://github.com/jcurran1289/PP3-atm/issues?q=is%3Aissue+is%3Aclosed

### Validator Testing
- PEP8
-- No errors were returned  from PEP8online.com

### Version Control
I used github to track my code. Initially was commiting huge chunks and many changes at once. Then started to do smaller changes one at a time

## Deployment
This project was deployed using Code Institute's mock terminal for Heroku.
The steps for deployment are as follows:
- Fork or clone this repository
- Create a new Heroku app
- Set the buildpacks to Python and NodeJS in that order
- Link the Heroku app to the repository
- Click on Deploy
## Credits
- Code institute for deployment terminal
- Code institute love-sandwichs project for the data validation