from flask import Response

def add_security_headers(response: Response) -> Response:
    """
    Adds common security headers to HTTP responses.
    """
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; object-src 'none';"
    # Note: Strict-Transport-Security (HSTS) is typically best configured at the web server/proxy level (e.g., Nginx, Apache)
    # if the application is served over HTTPS. It's not usually set in the application itself
    # unless the app has direct knowledge of whether it's being served via HTTPS.
    # Example if you were to set it (conditionally):
    # if request.is_secure:
    #     response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response
