# Endpoints

Base URL: http://silverlogic.ngrok.io/api/

Auth Tokens:

Anna: `d01f9cf6936f56b6e09bcf6fbd3ee22f926fa59a`

Chris: `e07af9db0dd265f1424cf7da6e68d2d03bb8260d`	

Kevin: `e836b5c3019d6c88148e08504376f136cc7cedb1`

- [Credit Factors](#credit-factors)
- [Credit](#credit)
- [Loans](#loan)
- [Device](#devices)
- [Users](#users)

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
    - `description`: **Optional**

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

## Devices

#### Create Device

- Endpoint: `devices/`
- Method: POST
- Authentication: Logged in

Request:
````json
{
    "registration_id": [
        "This field is required."
    ],
    "type": [
        "This field is required."
    ]
}
````

## Users

#### List Friends

- Endpoint: `users/`
- Method: GET
- Authentication: Logged in as user you want friends

Example response:
````json
[
    {
        "name": "Chris Johnston",
        "stars": 3,
        "job": "Soda Vendor",
        "id": 2
    },
    {
        "name": "Kevin Lavi",
        "stars": 4,
        "job": "Hat Vendor",
        "id": 3
    },
    {
        "name": "Rob Doischen",
        "stars": 2,
        "job": "Carpet Vendor",
        "id": 4
    }
]
````

## Vouches

#### List Vouches for a Loan

- Endpoint: `loans/{id}/vouches`
- Method: GET
- Authentication: Logged in as loan borrower

Example response:
````json
[
    {
        "amount": "100.00",
        "loan": 2,
        "vouching_user": {
            "name": "Chris Johnston",
            "stars": 3,
            "job": "Soda Vendor",
            "id": 2
        },
        "status": "INVITED"
    }
]
````

#### List User's Current Vouches

- Endpoint: `vouches/`
- Method: GET
- Authentication: Logged in as vouching user

Example response:
```json
[
    {
        "amount": "100.00",
        "loan": {
            "amount": "100.00",
            "borrower": {
                "firstname": "Chris",
                "lastname": "Johnston"
            },
            "description": "Loan for plastic cups.",
            "id": 3
        },
        "vouching_user": 1,
        "status": "INVITED",
        "id": 5
    }
]
```

#### Invite to Vouch for a Loan

- Endpoint: `vouches/`
- Method: POST
- Authentication: Logged in as loan borrower

Example request:
````json
{
	"vouching_user": 2,
	"amount": 100,
	"loan": 3
}
````

Example response:
```json
{
    "amount": "100.00",
    "loan": 3,
    "vouching_user": 2,
    "status": "INVITED"
}
```

### Accept or Decline to Vouch
- Endpoint: `vouches/{id}/`
- Method: PATCH
- Authentication: Logged in as vouching user

To accept:
````json
{
  "status": "ACCEPTED"
}
````

To decline:
````json
{
  "status": "DECLINED"
}
````

Response:
```json
{
    "amount": "100.00",
    "loan": {
        "amount": "100.00",
        "borrower": {
            "firstname": "Chris",
            "lastname": "Johnston"
        },
        "description": "Loan for plastic cups.",
        "id": 3
    },
    "vouching_user": 1,
    "status": "ACCEPTED",
    "id": 5
}
```