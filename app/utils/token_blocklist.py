BLOCKLIST = set()

def add_to_blocklist(jti):
    BLOCKLIST.add(jti)

def is_token_revoked(jti):
    return jti in BLOCKLIST