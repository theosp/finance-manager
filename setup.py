#!/usr/bin/python
# vim: set fileencoding=utf-8 :

from distutils.core import setup

setup(
    name='finance-manager',
    version='1',
    description='',
    long_description = "",
    author='theosp',
    author_email='333222@gmail.com',
    url='http://www.blogy.me/',
    packages=[
              'finance_manager'
             ],
    provides=[
              'finance_manager'
             ],
    requires=[
              'Crypto'   
              'crack'
    ]
)
