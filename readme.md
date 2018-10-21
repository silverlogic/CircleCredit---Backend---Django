# Endpoints

BASE URL: http://silverlogic.ngrok.io/api/

## Credit Factors

- Endpoint: `credit-factors/`
- Method: GET
- Authentication: Required. Only returns for current user.
- Properties:
    - `impact`: Currency value, two decimal places, can be negative or positive
    - `source`
        - Values: `vouches`, `investments`, `loans`, `quiz`, `credit-score`, `balance`

Example:
``
{
    'impact': '-100.00', 'source': 'vouches'
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