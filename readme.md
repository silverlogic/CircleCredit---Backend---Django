# Endpoints

Base URL: http://silverlogic.ngrok.io/api/

Auth Tokens:

Anna: d01f9cf6936f56b6e09bcf6fbd3ee22f926fa59a	
Chris: e07af9db0dd265f1424cf7da6e68d2d03bb8260d	
Kevin: e836b5c3019d6c88148e08504376f136cc7cedb1

## Credit Factors

#### List

- Endpoint: `credit-factors/`
- Method: GET
- Authentication: Required. Only returns for current user.
- Properties:
    - `impact`: Currency value, two decimal places, can be negative or positive
    - `source`
        - Values: `LOAN`, `INVESTMENT`, `EDUCATION`, `VOUCH`, `BALANCE`

Example:
````json
[
    {
        "impact": "-100.00", 
        "source": "VOUCH"
    }
]
````

## Credit

#### Retrieve

- Endpoint: `credit/`
- Method: GET
- Authentication: Required. Only returns for current user.
- Properties:
    - `amount`: Currency value, two decimal places.
   
Example:
````json
{
    "amount": "1000.00"
}
````

## Loan

#### List

- Endpoint: `loans/`
- Method: GET
- Authentication: Required. Only returns for current user.
- Properties:
    - `original_amount`: Currency value, two decimal places.
    - `paid_amount`: Currency value, two decimal places.
    - `interest`: Currency value, two decimal places.
    - `description`: Description, up to 256 characters
    - `id`: ID
   
Example:
````json
[
    {
        "original_amount": "300.00",
        "paid_amount": "0.00",
        "interest": "20.00",
        "description": "Loan for a palette of Coca Cola.",
        "id": 2
    }
]
````

#### Retrieve (Borrower)

- Endpoint: `loans/{id}`
- Method: GET
- Authentication: Logged in as borrower
- Properties:
    - `original_amount`: Currency value, two decimal places.
    - `paid_amount`: Currency value, two decimal places.
    - `interest`: Currency value, two decimal places.
    - `description`: Description, up to 256 characters
    - `id`: ID
   
Example:
````json
{
    "original_amount": "300.00",
    "paid_amount": "0.00",
    "interest": "20.00",
    "description": "Loan for a palette of Coca Cola.",
    "id": 2
}
````

#### Retrieve (Investor/Cosigner)

- Endpoint: `loans/{id}`
- Method: GET
- Authentication: Logged in as a user who is not the borrower
- Properties:
    - `amount`: Currency value, two decimal places.
    - `borrower`
        - `firstname`
        - `lastname`
    - `description`: Description, up to 256 characters
    - `id`: ID
   
Example:
````json
{
    "amount": "100.00",
    "borrower": {
        "firstname": "Chris",
        "lastname": "Johnston"
    },
    "description": "Loan for plastic cups.",
    "id": 3
}
````

#### Create Loan

- Endpoint: `loans/`
- Method: POST
- Authentication: Logged in as the user you want to create a loan for
- Properties:
    - `original_amount`
    - `description`

Example Request:
````json
{
	"description": "A loan for soda pop.",
	"original_amount": "1000.00"
}
````

#### Calculate Interest

- Endpoint: `loans/calculate_interest`

Example Request:
````json
{
	"original_amount": "1000.00"
}
````

Example Response:
````json
{
    "interest": 200
}
````