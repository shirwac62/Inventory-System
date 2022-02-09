import base64
import six

key = '1234567890'


def url_encode(val):
    val = str(val)
    encoded_chars = []
    for i in range(len(val)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(val[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    encoded_string = encoded_string.encode('latin') if six.PY3 else encoded_string
    return base64.urlsafe_b64encode(encoded_string).rstrip(b'=').decode("utf-8")


def url_decode(val):
    string = base64.urlsafe_b64decode(str.encode(val) + b'===')
    string = string.decode('latin') if six.PY3 else string
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string
