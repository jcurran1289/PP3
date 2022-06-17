![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)
# Python ATM
Python ATM  is a Python terminal system, which runs in the Code Institute mock terminal on Heroku.

Users have the ability to create a bank account in the ATM,update their, withdraw and deposit money and the accounts being updated in real time.
## How to use
The ATM has simply controls and interface. The user will be promted to enter a number depending on what they would like to do or Q to quit the system.

## Features
### Exisiting Features
- User authentication
- Real time account summary
- Real Time account updates
- Account setup
- Input validation and error checking
- Data for user profiles is maintained in an class instance

### Future Features
- Allow users to see past transactions

## Data Model
I used the currentuser class as my model.   


## Testing
I have manually tested this project by doing the following:
- Passed the code through a PEP8 linter and confirmed there are no problems
- Given invalid inputs: strings when numbers are expected, out of range values and invalid passwords

### Bugs
### Validator Testing
- PEP8
-- No errors were returned  from PEP8online.com

## Deployment
This project was deployed using Code Institute's mock terminal for Heroku.
The steps for deployment are as follows:
- Fork or clone this repository
- Create a new Heroku app
- Set the buildpacks to Python and NodeJS in that order
- Link the Heroku app to the repository
- Click on Deploy
## Credits