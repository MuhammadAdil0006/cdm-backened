- Create virtual environment
``` python -m venv .venv```
- activate it.
``` . .venv/bin/activate```
- install dependancies
``` pip install -r requirements.txt```


- Setup database
- Run migration command
``` python manage.py migrate```
- Up the server 
```python manage.py runserver```

In order to start celery worker in a separate container
```celery -A AiMapper worker --loglevel=info```
# Keycloak OAuth2 Authentication Backend

This backend has been tested with a standard Keycloak installation, but you might need to specialize it and tune the parameters according to your configuration.

This setup specializes the OAuth2 backend, which primarily offers authorization rather than authentication capabilities. Although Keycloak provides a full OpenID Connect implementation, its configuration can be labor-intensive.

This backend is designed to retrieve an access token, assuming that the token contains the necessary user details for authentication. The integrity of the authentication process is ensured through public key verification for the `access_token`, along with OpenID Connect `aud` (audience) field checking.

## Setup Instructions

### 1. Create a New Keycloak Client
1. Navigate to the **Clients** section in the Keycloak Admin Console.
2. Choose a `Client ID` under the **General Settings** pane.
3. In the **Capability config** pane, select:
   - `Client authentication`
   - `Authorization`
4. Add a valid redirect url
    http://localhost:8000/accounts/complete/keycloak/
### 2. Configure Client Parameters
- **Settings:** Copy the `Client ID` and use it as the `KEY` value in your settings.
- **Credentials:**
  - Under **Client Authenticator**, select `Client Id and Secret`.
  - Copy the `Client secret` value and use it as the `SECRET` in your settings.

### 3. Configure Token Signing
To ensure tokens work with JWT, configure the following settings:

- **Advanced > Fine-Grain OpenID Connect Configuration:**
  - **User Info Signed Response Algorithm:** `RS256`
  - **Request Object Signature Algorithm:** `RS256`

### 4. Re-enable Audience (Fix for KEYCLOAK-6638)
To include the `aud` (audience) field in tokens:
1. Navigate to **Client Scopes**.
2. Select your **Client ID-dedicated** scope.
3. Click **Add Mapper** > **Audience**.
4. Name the mapper and select your Client ID under `Included Client Audience`.

### 5. Obtain the Public Key
- Go to **Realm Settings > Keys**.
- Copy the `Public key` and use it as `PUBLIC_KEY` in your settings.

### 6. Configure Access Token Fields
To ensure correct token fields are included:
1. Navigate to **Clients > Client ID > Mappers**.
2. Include at least the `ID_KEY` value and any dictionary keys required in the `get_user_details` method.


### 7. Configure Django Settings
Example configuration for Django:

```python
SOCIAL_AUTH_KEYCLOAK_KEY = 'example'
SOCIAL_AUTH_KEYCLOAK_SECRET = '1234abcd-1234-abcd-1234-abcd1234adcd'
SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY = \
  'pempublickeythatis2048bitsinbase64andhaseg392characters'
SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL = \
  'https://sso.com/auth/realms/example/protocol/openid-connect/auth'
SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL = \
  'https://sso.com/auth/realms/example/protocol/openid-connect/token'
```

### 8. Configure User Association
By default, users are associated via the `username` field. To change the key:

```python
SOCIAL_AUTH_KEYCLOAK_ID_KEY = 'email'
```

**Important:** Ensure that your Keycloak and Django user databases do not conflict, preventing user account hijacking due to incorrect associations.

### 9. Keycloak Login URL
Users can log in via the following endpoint:

```
http://localhost:8000/accounts/login/keycloak
```

### 10. Running Celery Worker
To start the Celery worker for async tasks, run:

```bash
celery -A AiMapper worker --loglevel=info
```

---
This completes the setup for integrating Keycloak authentication with Django.



<!-- localhost:8000/accounts/login/keycloak -->