"""Named local identities; no identity provider or notice data leaves the server."""
import base64
import hashlib
import hmac
import json
import os
import secrets
from pathlib import Path
from urllib.parse import urlsplit

ROLES = {'ADMIN', 'TRAINER', 'REVIEWER', 'AUDITOR'}


def password_record(password):
    if len(password) < 14: raise ValueError('Use at least 14 characters')
    salt = secrets.token_hex(16)
    value = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1)
    return {'algorithm': 'scrypt-16384-8-1', 'salt': salt, 'hash': value.hex()}


def verify(password, record):
    if record['algorithm'] != 'scrypt-16384-8-1': return False
    value = hashlib.scrypt(password.encode(), salt=bytes.fromhex(record['salt']), n=16384, r=8, p=1)
    return hmac.compare_digest(value.hex(), record['hash'])


def configuration():
    path = Path(os.environ['VOTING_USERS_FILE'])
    users = json.loads(path.read_text())
    if not users or not isinstance(users, dict): raise ValueError('Named identities are required')
    for name, user in users.items():
        if not name.strip() or ':' in name or not user['roles'] or not set(user['roles']) <= ROLES:
            raise ValueError('Invalid named identity or roles')
        if user['password']['algorithm'] != 'scrypt-16384-8-1' or len(bytes.fromhex(user['password']['salt'])) != 16 or len(bytes.fromhex(user['password']['hash'])) != 64:
            raise ValueError('Invalid password record')
        if user.get('expert_attested') and 'REVIEWER' not in user['roles']:
            raise ValueError('Expert identity must have REVIEWER role')
    if not any('ADMIN' in u['roles'] for u in users.values()): raise ValueError('An administrator is required')
    origin = os.environ['VOTING_PUBLIC_ORIGIN'].rstrip('/')
    parsed = urlsplit(origin)
    local = parsed.hostname in ('localhost', '127.0.0.1', '::1')
    if parsed.path or parsed.query or parsed.fragment or parsed.username or not parsed.hostname:
        raise ValueError('Public origin must contain only scheme and authority')
    if parsed.scheme != 'https' and not (local and os.environ.get('VOTING_ALLOW_LOCAL_HTTP') == 'true'):
        raise ValueError('HTTPS is required outside explicit loopback test mode')
    return users, origin


def authenticate(header, users):
    try:
        scheme, token = header.split(' ', 1)
        if scheme.lower() != 'basic': return None
        name, password = base64.b64decode(token, validate=True).decode().split(':', 1)
        user = users.get(name)
        # Same expensive operation for unknown identities.
        record = user['password'] if user else {'algorithm': 'scrypt-16384-8-1', 'salt': '00' * 16, 'hash': '00' * 64}
        if len(password) > 1024 or not verify(password, record) or not user: return None
        return {'name': name, 'roles': user['roles'], 'expert_attested': bool(user.get('expert_attested'))}
    except (ValueError, KeyError, UnicodeError): return None


def main():
    import argparse
    import getpass
    p = argparse.ArgumentParser(description='Create a named-user secret without storing plaintext passwords')
    p.add_argument('output'); p.add_argument('username'); p.add_argument('--roles', nargs='+', choices=sorted(ROLES), required=True)
    p.add_argument('--expert-attested', action='store_true')
    a = p.parse_args(); path = Path(a.output)
    users = json.loads(path.read_text()) if path.exists() else {}
    if a.username in users: raise ValueError('Identity exists; rotate using a new versioned secret file')
    pw = getpass.getpass('Password: ')
    if pw != getpass.getpass('Repeat password: '): raise ValueError('Passwords differ')
    if a.expert_attested and 'REVIEWER' not in a.roles: raise ValueError('Expert must have REVIEWER role')
    users[a.username] = {'roles': a.roles, 'expert_attested': a.expert_attested, 'password': password_record(pw)}
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp-' + secrets.token_hex(4))
    fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as f: json.dump(users, f, indent=2); f.flush(); os.fsync(f.fileno())
    os.replace(temporary, path)


if __name__ == '__main__': main()
