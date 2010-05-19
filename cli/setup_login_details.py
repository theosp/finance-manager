#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""interactively get the user login details.

"""

import getpass
import login_details

bank = "leumi_co_il"

cur_bank = __import__('finance_manager.' + bank)

if __name__ == "__main__":
    print "Choose password for open-leumi"

    encryption_key = getpass.getpass('Password: ')

    print 'Your leumi login details:'
    user_id = raw_input('User Id: ')
    password = getpass.getpass('Password: ')
    authentication = raw_input('Authentication: ')

    passed_crack_check = False
    while not passed_crack_check:
        try:
            login_details.login_details(encryption_key, user_id, password, authentication)
        except ValueError, e:
            print "The open-leumi password is not strong enough:", e
            encryption_key = getpass.getpass('Password: ')
        else:
            passed_crack_check = True
