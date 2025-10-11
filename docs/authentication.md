# Custom Authentication System

DidactAI uses a custom authentication backend that allows users to log in using either their username or email address, providing flexibility and improved user experience.

## Features

### Email or Username Login
Users can authenticate using either:
- Their username (e.g., `john_doe`)
- Their email address (e.g., `john@example.com`)

### Case Insensitive Authentication
The authentication system is case insensitive, meaning:
- `JOHN@EXAMPLE.COM` and `john@example.com` are treated as the same
- `JOHN_DOE` and `john_doe` are treated as the same

### Security Features
- Password verification using Django's built-in password hashing
- User status verification (active users only)
- Timing attack protection for non-existent users
- Proper handling of edge cases (multiple users, inactive users)

## Technical Implementation

### Backend Class
The custom authentication is implemented in `accounts/backends.py`:

```python
class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to login with either
    their email address or username.
    """
```

### Configuration
The backend is configured in `settings.py`:

```python
AUTHENTICATION_BACKENDS = [
    'accounts.backends.EmailOrUsernameModelBackend',  # Custom backend
    'django.contrib.auth.backends.ModelBackend',     # Default Django backend
]
```

### Form Integration
The login form (`CustomAuthenticationForm`) has been updated to reflect this capability:
- Placeholder text: "Username or Email"
- Single input field handles both authentication methods

## Testing

### Automated Tests
Run the authentication backend tests:
```bash
python manage.py test accounts.test_auth_backend
```

### Manual Testing
Use the custom management command to test authentication:
```bash
# Test with username
python manage.py test_auth your_username your_password

# Test with email
python manage.py test_auth your_email@example.com your_password
```

## Usage Examples

### In Forms
Users can enter either format in the login form:
- `admin` or `admin@didactia.com`
- `john_doe` or `john@example.com`

### In Code
The Django authentication system works seamlessly:
```python
from django.contrib.auth import authenticate

# Both work with the same user
user1 = authenticate(username='john_doe', password='password123')
user2 = authenticate(username='john@example.com', password='password123')
# user1 and user2 refer to the same user object
```

### Case Sensitivity
All these authenticate the same user:
```python
authenticate(username='John@Example.com', password='password123')
authenticate(username='JOHN@EXAMPLE.COM', password='password123')  
authenticate(username='john@example.com', password='password123')
authenticate(username='JOHN_DOE', password='password123')
authenticate(username='john_doe', password='password123')
```

## Error Handling

### Non-existent Users
- Returns `None` for authentication attempts with non-existent users
- Provides helpful error messages in the test command

### Multiple Users (Edge Case)
- Handles scenarios where multiple users might have the same email
- Prioritizes username matches over email matches
- Returns `None` for security if ambiguous matches occur

### Inactive Users
- Inactive users cannot authenticate even with correct credentials
- Follows Django's standard user authentication flow

## Migration from Standard Authentication

This system is backward compatible with Django's default authentication:
1. Existing users can continue using their username
2. They can now also use their email address
3. No changes required to existing user accounts
4. Standard Django admin authentication continues to work

## Security Considerations

1. **Timing Attacks**: The backend includes protection against timing attacks by running password hashing even for non-existent users
2. **Case Sensitivity**: While authentication is case insensitive, the actual stored usernames and emails retain their original case
3. **Email Uniqueness**: Ensure email fields are unique in your user model to prevent authentication ambiguity
4. **Password Security**: Uses Django's standard password validation and hashing

## Troubleshooting

### Authentication Fails
1. Verify the user exists: Check both username and email
2. Confirm the user is active: `user.is_active` should be `True`
3. Test password separately: Ensure the password is correct
4. Check case sensitivity: Try different case combinations

### Multiple Authentication Backends
The system uses multiple backends in order:
1. Custom Email/Username backend (primary)
2. Django default backend (fallback)

If authentication fails with the custom backend, Django will try the default backend.

## API Integration

For REST API authentication, the system works with:
- Django REST Framework's built-in authentication
- Token authentication
- Session authentication

Example API usage:
```python
# POST to /api/auth/login/
{
    "username": "user@example.com",  # or username
    "password": "password123"
}
```