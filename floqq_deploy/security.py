#
# Copyright (c) 2012 Floqq innovation SL. All Right Reserved
#

import os
import tokenize
import base64

from Crypto.Cipher import Blowfish

from floqq_deploy.db import get_config_path, get_current_path, config


class State(object):
    def __init__(self, state=None):
        self.state = state


def parse_settings(token_bucket, whitelist, key, transformer):
    current_token = State()
    def consume(*args):
        args = list(args)
        token_type, token_string = args[0], args[1]
        if token_type == tokenize.NAME:
            if token_string in whitelist:
                current_token.state = token_string
            else:
                current_token.state = None
        elif token_type == tokenize.STRING and current_token.state:
            args[1] = transformer(token_string, key)
        token_bucket.append(args)
    return consume


def transform_settings(app_name, filename, key, transformer):
    """Get the settings specified in the config file under `security` section.

    It looks for the comma separated list of setting names specified in the
    config file under the `security` section and the `secure_settings` option.

    Params
        app_name: Application name. The settings of this app are the ones
                  parsed.
        filename: Name of the file holding the settings.

    Raises
        ValueError if no settings are found for that app name.

    Returns
        A list of tuples where the first element of the tuple is the setting
        name and second element the setting value.
    """
    settings_path = os.path.join(get_current_path(), app_name, filename)
    if not os.path.isfile(settings_path):
        msg = "No settings found for {0!r} app".format(app_name)
        raise ValueError(msg)

    secure_settings_string = config("secure_settings", section="security")
    if secure_settings_string is not None:
        secure_settings = set(s.strip() for s in secure_settings_string.split(","))

        with open(settings_path) as f:
            cipher_tokens = []
            callback = parse_settings(cipher_tokens, secure_settings, key,
                                      transformer)
            tokenize.tokenize(f.readline, callback)
            cipher_settings = tokenize.untokenize(cipher_tokens)

        with open(settings_path, "w") as f:
            f.write(cipher_settings)


def encrypt_settings(app_name, filename, key):
    transform_settings(app_name, filename, key, transformer=encrypt_setting)


def decrypt_settings(app_name, filename, key):
    transform_settings(app_name, filename, key, transformer=decrypt_setting)


def encrypt_setting(value, key):
    return '"{0}"'.format(base64.b64encode(encrypt(value.strip("'\""), key)))


def decrypt_setting(value, key):
    return '"{0}"'.format(decrypt(base64.b64decode(value.strip("'\"")), key))


_PAD_BYTE = "X"


def pad(text):
    """Pad text so its lenth is multiple of 8"""
    padding = (8 - len(text) % 8) * _PAD_BYTE
    return text + padding


def unpad(text):
    """Unpad text padded before with the `pad` function"""
    return text.rstrip(_PAD_BYTE)


def encrypt(text, key):
    """Cipher a text using Blowfish cipher.
    
    Params
        text: text to cipher.
        key: key for encrypt/decrypt.

    Returns
        cipher text.
    """
    cipher = Blowfish.new(key)
    return cipher.encrypt(pad(text))


def decrypt(ciphertext, key):
    """Decipher a text ciphered using Blowfish cipher.
    
    Params
        ciphertext: text to decipher.
        key: key for encrypt/decrypt.

    Returns
        plain text.
    """
    cipher = Blowfish.new(key)
    return unpad(cipher.decrypt(ciphertext))
