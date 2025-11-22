# Security features Implemented 

## 1. Secure Settings 
- DEBUG = False
- SECURE_BROWSER_XSS_FILTER = True
- SECURE_CONTENT_TYPE_NOSNIFF = True
- X_FRAME_OPTIONS = 'DENY'
- CSRF_COOKIE_SECURE = True
- SESSION_COOKIE_SECURE = True

## 2. CSRF Protection 
All html forms include `{% csrf_token %}`.

## 3. Safe Views 
- No Raw SQL used.
- User input is sanitized using `strip()`.
- Django ORM used for all DB queries.

## 4. CSP
A basic cintent Security Policy was added throughmiddleware:
`default-src 'self'`
