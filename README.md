# BankAPI Dökümantasyon

Bu proje, temel bankacılık işlemlerini simüle eden bir API oluşturmak amacıyla geliştirilmiştir. Django Rest Framework kullanılarak hazırlanan bu API, kullanıcı kayıtları, hesap yönetimi, para yatırma/çekme ve transfer işlemleri gibi özellikleri içerir.

## API'nin Amacı

Bu API, internet bankacılığı işlemlerinin backend tarafını simüle etmek amacıyla geliştirilmiştir. Django Rest Framework yeteneklerimi test etmek ve geliştirmek için oluşturduğum bu API, temel bankacılık işlemlerinin (hesap yönetimi, para yatırma/çekme, transferler vb.) gerçekleştirilmesini sağlar. API'yi kullanarak, bankacılık sisteminin çekirdeğini simüle eden bir yapı oluşturabilirsiniz.

## Base URL

API'nin temel URL'si aşağıdaki gibidir. API'yi kendi ortamınızda çalıştırmak için AWS veya benzeri bulut hizmetlerinde barındırmanız ve kendi domaininizi kullanmanız gerekmektedir.

  ```bash
    http://your_domain/accounts
  ```

## Authentication

API, Django'nun token-based authentication (token tabanlı kimlik doğrulama) mekanizmasını kullanır. Kullanıcıların API'yi kullanabilmesi için, bir token elde etmeleri ve bu token'ı her isteklerinde göndermeleri gerekmektedir. Bu token, kullanıcıya login işlemi sırasında sağlanır ve Authorization başlığı altında her API isteğinde belirtilmelidir.

### Authentication Gereksinimleri

1. **Token Alma**: Kullanıcı giriş yaptıktan sonra bir token alır. Bu token, giriş işlemi sırasında sağlanır ve kimlik doğrulama amacıyla kullanılır.

2. **Token Kullanımı**: Kimlik doğrulaması gerektiren her istekte, `Authorization` başlığı altında bu token belirtilmelidir. Token, API'ye erişim izni verilen kullanıcıların doğruluğunu ve yetkilendirilmesini sağlar.


## Headers

Tüm isteklerde aşağıdaki başlıklar kullanılır:

```bash
  Content-Type: application/json
  Authorization: Token user_token (sadece kimlik doğrulaması gerektiren işlemler için)
```

## API İşlemleri

### 1. Register (POST)

1. Endpoint: /register/
2. Açıklama: Kullanıcı kaydı yapmak için kullanılır.
3. Örnek JSON Gönderim:
   ```bash
          {
            "first_name": "first_name",
            "last_name": "last_name",
            "email": "test@example.com",
            "password": "6_haneli_rakam",
            "identity_no": "türkiye_cumhuriyeti_kimlik_no",
            "phone_number": "Türkiye_kodlu_telefon_numarası"
          }
   ```

### 2. Login (POST)

1. Endpoint: /login/
2. Açıklama: Kullanıcı girişi yapar ve bir token alır.
3. Örnek JSON Gönderim:

  ```bash
          {
            "identity_no": "türkiye_cumhuriyeti_kimlik_no",
            "password": "123456"
          }
   ```
4. Yanıt:

  ```bash
          {
            "token": "user_token"
          }
  ```

### 3. Logout (GET)

1. Endpoint: /logout/
2. Açıklama: Kullanıcının sistemden çıkış yapmasını sağlar. Authentication gerektirir.
3. Başlık:
  ```bash
          Authorization: Token user_token
  ```

### 4. Profile (GET, PUT, PATCH, DELETE)

1. Endpoint: /profile/
2. Açıklama: Kullanıcı profil bilgilerini görüntüler, günceller veya siler. Authentication gerektirir.
3. GET Örneği:
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

4. PATCH/PUT: Yalnızca email ve phone_number alanları güncellenebilir.

### 5. Banka Hesapları (GET, POST)

1. Endpoint: /profile/my_accounts/
2. Açıklama: Kullanıcının banka hesaplarını görüntüler veya yeni bir hesap oluşturur. Authentication gerektirir.
3. POST Örneği:
   ```bash
         {
            "account_type": "non_term" or "term"
         }
  ```

GET Örneği:
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

### 6. Hesap Detayı (GET, PUT, PATCH, DELETE)

1. Endpoint: /profile/my_accounts/{account_id}/
2. Açıklama: Belirli bir banka hesabının detaylarını görüntüler, günceller veya siler. Authentication gerektirir.
3. GET Örneği:
  ```bash
         {
          "id": 4,
          "account_type": "non_term",
          "account_number": "",
          "iban": "iban_tr",
          "balance": "0.00",
          "created_at": "",
          "updated_at": ""
        }
  ```
4. PATCH/PUT: Sadece account_type alanı güncellenebilir.

### 7. Para Yatırma ve Para Çekme (GET, POST)

1. Endpoint: /profile/my_accounts/{account_id}/dw/
2. Açıklama: Belirli bir hesaba para yatırma veya hesaptan para çekme işlemi gerçekleştirir. Authentication gerektirir.
3. POST Örneği:
  ```bash
         {
          "types": "deposit" or "withdraw",
          "amount": 500
          }
  ```
4. GET Örneği:
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
2. Açıklama: Belirli bir hesaptan başka bir hesaba para transferi yapar. Authentication gerektirir.
3. POST Örneği:
```bash
      {
        "amount": 200,
        "iban": "target_iban",
        "description": "opsiyonel"
      }
```
4. GET Örneği:

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

    

