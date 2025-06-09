Repo for SCC V2

## Security

### JWT Secret Key

For production environments, it is crucial to set the `JWT_SECRET_KEY` environment variable to a strong, random string. This key is used to sign and verify JSON Web Tokens (JWTs), and a weak or compromised key could lead to severe security vulnerabilities.

**Do not use the default key (`default-secret-key`) in a production environment.**

#### Generating a Strong Secret Key

You can generate a cryptographically strong secret key using OpenSSL with the following command:

```bash
openssl rand -hex 32
```

This command will output a 32-byte (256-bit) hexadecimal string, which is suitable for use as a `JWT_SECRET_KEY`.

Set this generated key as an environment variable in your production deployment environment. For example:

```bash
export JWT_SECRET_KEY="your_generated_strong_secret_key"
```

### Redis Connection (for Token Blocklist)

If you are using the token blocklist feature (which is enabled by default), the application will require a Redis instance for storing revoked tokens.

Set the `REDIS_URL` environment variable to point to your Redis instance. The default development value is `redis://localhost:6379/0`. For production, ensure this points to your production Redis server or service.

Example:
```bash
export REDIS_URL="redis://your-production-redis-host:6379/0"
```

### Security Headers

The application automatically adds several HTTP security headers to all responses to help protect against common web vulnerabilities. These include:

-   **`X-Content-Type-Options: nosniff`**
    -   Prevents browsers from MIME-sniffing a response away from the declared content type. This reduces the risk of drive-by downloads and attacks where assets are served with incorrect MIME types.

-   **`X-Frame-Options: DENY`**
    -   Prevents the site from being rendered within an `<iframe>`, `<frame>`, `<embed>`, or `<object>`. This helps to protect against clickjacking attacks.

-   **`Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';`**
    -   A Content Security Policy (CSP) helps to prevent Cross-Site Scripting (XSS), clickjacking, and other code injection attacks by restricting the sources from which content (like scripts, styles, images) can be loaded.
    -   The current policy is restrictive:
        -   `default-src 'self'`: Allows loading resources only from the application's own origin.
        -   `script-src 'self'`: Allows executing scripts only from the application's own origin.
        -   `object-src 'none'`: Disallows loading plugins (e.g., Flash, Java).
    -   This policy may need to be adjusted based on specific application needs (e.g., if using CDNs for scripts/styles, or embedding content from external sites).

#### Strict-Transport-Security (HSTS)

It is highly recommended to implement HTTP Strict Transport Security (HSTS) if your application is served exclusively over HTTPS. HSTS tells browsers to only communicate with your site using HTTPS, preventing downgrade attacks.

HSTS is typically best configured at the web server (e.g., Nginx, Apache) or load balancer level. An example HSTS header:

`Strict-Transport-Security: max-age=31536000; includeSubDomains`

Ensure you understand the implications of HSTS, especially `includeSubDomains` and preloading, before enabling it.
