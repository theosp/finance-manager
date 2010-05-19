#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""This module is used to set and get the user's login details to leumi check:
login_details() docstring.

"""

from Crypto.Cipher import Blowfish
import crack
import pickle
import os
import re

# Settings:
default_login_details_path = os.path.expanduser('~/.open-leumi')

def _right_pad_to_product(string, product):
    """Returns a string that consists of the supplied string right padded with
    \0 to make its length a multiple of product.

    """

    return string + (product - (len(string) % product)) * "\0"

def _unpad(string):
    """removes all the \0 at the end of the string.

    """

    return re.sub("\0*$", '', string)

def _encrypt(encryption_key, string):
    cipher_obj = Blowfish.new(encryption_key)
    return cipher_obj.encrypt(string)

def _decrypt(encryption_key, string):
    cipher_obj = Blowfish.new(encryption_key)
    return cipher_obj.decrypt(string)

def _load_login_details(encryption_key,\
                        login_details_path=default_login_details_path):
    return pickle.loads(_unpad(_decrypt(encryption_key, open(login_details_path).read())))

def _save_login_details(encryption_key,\
                        login_details,
                        login_details_path=default_login_details_path):
    open(login_details_path, 'w').write(_encrypt(encryption_key, _right_pad_to_product(pickle.dumps(login_details), 8)))

def login_details(encryption_key,\
                  user_id=None, password=None, authentication=None,\
                  login_details_path=default_login_details_path):
    """This function is used to get, set and update the user's login details to
    his account managment in Leumi.

    To avoid the need to request the login details every time the user wants to
    use the open-leumi package we encrypt the login details using the supplied
    encryption_key and saves them to the disk.

    The Login Details File:
    The encrypted login details file saved to the path specified at
    default_login_details_path or login_details_path , it contains
    pickled dictionary that holds the login details as they named above.

    Set:
    login_details(encryption_key, user_id, password, authentication) is used to
    set the user's login details file.

    Update:
    If only part of the optional params supplied then login_details updates the
    login details file with them.
    Actually, that works even if there is no login details file, in which case
    we create it, so technically it possible (though not recommanded) to set
    the user login details as follow:
        login_details(encryption_key, user_id="user_id"):
        login_details(encryption_key, password="password"):
        login_details(encryption_key, authentication="authentication"):

    Get:
    login_details(encryption_key) returns the login details as a dictionary.

    Exceptions:
    

    """

    login_details = {}

    login_details_path = os.path.expanduser(login_details_path)

    if user_id is not None:
        login_details['user_id'] = user_id

    if password is not None:
        login_details['password'] = password

    if authentication is not None:
        login_details['authentication'] = authentication

    # If Get mode
    if not login_details:
        return _load_login_details(encryption_key, login_details_path)

    # If Set mode
    if len(login_details) == 3:
        # check password strengh, if the password isn't powerful enouth it raises
        # ValueError exception with the specified password weaknes
        crack.VeryFascistCheck(encryption_key)
        return _save_login_details(encryption_key, login_details, login_details_path)

    # Update mode
    # There is no login details file yet
    if not os.path.exists(login_details_path):
        # Initiate a new login details file
        # check password strengh, if the password isn't powerful enouth it raises
        # ValueError exception with the specified password weaknes
        crack.VeryFascistCheck(encryption_key)
        return _save_login_details(encryption_key, login_details, login_details_path)

    current_login_details = _load_login_details(encryption_key, login_details_path)
    current_login_details.update(login_details)

    login_details = current_login_details

    return _save_login_details(encryption_key, login_details, login_details_path)

