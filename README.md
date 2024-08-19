# BankAPI Documentation

This project is designed to create an API that simulates basic banking operations. Developed using Django Rest Framework, this API includes features such as user registrations, account management, deposit/withdrawal, and transfer operations.

## Purpose of the API

This API is designed to simulate the backend side of online banking operations. Created to test and enhance my skills with Django Rest Framework, this API facilitates basic banking operations such as account management, deposits/withdrawals, and transfers. By using this API, you can build a structure that simulates the core of a banking system.

## Base URL

The base URL of the API is as follows. To run the API in your own environment, you need to host it on AWS or similar cloud services and use your own domain.

  ```bash
    http://your_domain/accounts
  ```

## Authentication

The API uses Django's token-based authentication mechanism. To use the API, users need to obtain a token and include this token in each of their requests. The token is provided to the user during the login process and must be specified in the `Authorization` header for each API request.

### Authentication Requirements

1. **Token Acquisition**: After logging in, the user receives a token. This token is provided during the login process and is used for authentication purposes.

2. **Token Usage**: For every request that requires authentication, the token must be specified in the `Authorization` header. The token ensures the validity and authorization of users accessing the API.


## Headers

The following headers are used in all requests:

```bash
  Content-Type: application/json
  Authorization: Token user_token (for requests requiring authentication only)
```

## API Operations

### 1. Register (POST)

1. Endpoint: /register/
2. Description: Used to register a new user.
3. Example JSON Payload:
   ```bash
          {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "test@example.com",
            "password": "6_digit_number",
            "identity_no": "turkish_national_id",
            "phone_number": "turkish_phone_number"
          }
   ```

### 2. Login (POST)

1. Endpoint: /login/
2. Description: Logs in a user and provides a token.
3. Example JSON Payload:
  ```bash
          {
            "identity_no": "turkish_national_id",
            "password": "123456"
          }
   ```
4. Response:

  ```bash
          {
            "token": "user_token"
          }
  ```

### 3. Logout (GET)

1. Endpoint: /logout/
2. Description: Logs out the user from the system. Requires authentication.
3. Header:
  ```bash
          Authorization: Token user_token
  ```

### 4. Profile (GET, PUT, PATCH, DELETE)

1. Endpoint: /profile/
2. Description: Retrieves, updates, or deletes the user's profile information. Requires authentication.
3. Example GET Response:
  ```bash
         {
          "id": 3,
          "first_name": "",
          "last_name": "",
          "email": "",
          "identity_no": "",
          "phone_number": "",
          "customer_no": "",
          "created_at": "",
          "updated_at": ""
        }
  ```

4. PATCH/PUT: Only the `email` and `phone_number` fields can be updated.

### 5. Bank Accounts (GET, POST)

1. Endpoint: /profile/my_accounts/
2. Description: Retrieves the user's bank accounts or creates a new account. Requires authentication.
3. Example POST Payload:
   ```bash
         {
            "account_type": "non_term" or "term"
         }
    ```
   
4. Example GET Payload:
   
  ```bash
         [
          {
            "id": 4,
            "account_type": "non_term",
            "account_number": "",
            "iban": "tr_iban",
            "balance": "0.00",
            "created_at": "",
            "updated_at": ""
          }
        ]
  ```

### 6. Account Details (GET, PUT, PATCH, DELETE)

1. Endpoint: /profile/my_accounts/{account_id}/
2. Description: Retrieves, updates, or deletes the details of a specific bank account. Requires authentication.
3. Example GET Response:
  ```bash
         {
          "id": 4,
          "account_type": "non_term",
          "account_number": "",
          "iban": "tr_iban",
          "balance": "0.00",
          "created_at": "",
          "updated_at": ""
        }
  ```
4. PATCH/PUT: Only the `account_type` field can be updated.

### 7. Deposit and Withdrawal (GET, POST)

1. Endpoint: /profile/my_accounts/{account_id}/dw/
2. Description: Performs deposit or withdrawal transactions for a specific account. Requires authentication.
3. Example POST Payload:
  ```bash
         {
          "types": "deposit" or "withdraw",
          "amount": 500
          }
  ```

4. Example GET Payload:
   
 ```bash
      [
        {
          "id": 9,
          "account": 4,
          "types": "deposit",
          "amount": "500.00",
          "extract_number": "15895300378065333938",
          "date": ""
        }
      ]
```

### 8. Transfer (GET, POST)

1. Endpoint: /profile/my_accounts/{account_id}/transfer/
2. Description: Transfers money from one account to another. Requires authentication.
3. Example POST Payload:
```bash
      {
        "amount": 200,
        "iban": "target_iban",
        "description": "optional"
      }
```
4. Example Get Payload:

```bash
      [
        {
          "id": 3,
          "account": 4,
          "iban": "target_account",
          "amount": "200.00",
          "description": null,
          "date": "",
          "extract_number": "17308543263531962939"
        }
      ]
```

# Installation

1. Clone the Project:
   
  ```bash
     git clone https://github.com/mtsftware/BankAPI
  ```

2. Create and Activate the Virtual Environment:

   ```bash
      python -m venv .venv
      source .venv/bin/activate  # Linux/macOS
      .venv\Scripts\activate      # Windows
   ```

3. Install Dependencies:

     ```bash
    pip install -r requirements.txt
     ```

4. Create the .env file and configure it (Use MySQL):

     ```bash
     cp .env.example .env
     ```

5. Create the database and apply migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Start the development server:

   ```bash
    python manage.py runserver
   ```
    

