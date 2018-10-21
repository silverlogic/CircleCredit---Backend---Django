# Endpoints

Base URL: http://silverlogic.ngrok.io/api/

Auth Tokens:

Anna: d01f9cf6936f56b6e09bcf6fbd3ee22f926fa59a	
Chris: e07af9db0dd265f1424cf7da6e68d2d03bb8260d	
Kevin: e836b5c3019d6c88148e08504376f136cc7cedb1

## Credit Factors

- Endpoint: `credit-factors/`
- Method: GET
- Authentication: Required. Only returns for current user.
- Properties:
    - `impact`: Currency value, two decimal places, can be negative or positive
    - `source`
        - Values: `loan`, `investment`, `education`, `vouch`, `balance`

Example:
``
{
    'impact': '-100.00', 'source': 'vouch'
}
``

## Credit

- Endpoint: `credit/`
- Method: GET
- Authentication: Required. Only returns for current user.
- Properties:
    - `amount`: Currency value, two decimal places.
   
Example:
``
{
    'amount': '1000.00'
}
``

