# Endpoints

Base URL: http://silverlogic.ngrok.io/api/

Auth Tokens:

Anna: `4b69237fc1d872a28a3afa1ec700ca7f2bdce017`

Chris: `6719624e606c83676c00e71a8f0010a4b3c9350f`	

Kevin: `0e49529c28fa56ed3a26d82a571c3bb06ea9b797`

Rob: `5b14a5a9d3f23f71b5a3d7b80d3b9c4484fb3fee`

- [Credit Factors](#credit-factors)
- [Credit](#credit)
- [Loans](#loan)
- [Device](#devices)
- [Users](#users)
- [Investments](#investments)

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

#### Synchrony Credit Score

- Endpoint: `synchrony-credit-score/`
- Method: GET
- Authentication: None

Example:
````json
{
    "syfCreditScore": "600",
    "ficoScore": "600",
    "delinquentAccounts": "1",
    "bankruptAccounts": "0",
    "averageAccountAge": "3",
    "paymentHistory": "0.75"
}
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

#### Update (Submit/Accept) Loan

- Endpoint: `loans/{id}`
- Method: PATCH
- Authentication: Logged in as the user you want to submit
- Properties:
    - `status`

Example Request:
````json
{
	"status": "ACTIVE"
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
	"loan": 3
}
````

Example response:
```json
{
    "amount": "0.00",
    "loan": {
        "amount": "2000.00",
        "borrower": {
            "firstname": "Anna",
            "lastname": "Elde"
        },
        "description": "",
        "id": 1
    },
    "vouching_user": 3,
    "status": "INVITED",
    "id": 95
}
```

### Accept or Decline to Vouch
- Endpoint: `vouches/{id}/`
- Method: PATCH
- Authentication: Logged in as vouching user

To accept:
````json
{
  "status": "ACCEPTED",
  "amount": 100,
  "investment": 200
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

### Investments

Endpoint: `investments/`
Accepts: GET, RETRIEVE (at `investments/{id}`), and POST (won't need to use--investment is created through vouch right now)