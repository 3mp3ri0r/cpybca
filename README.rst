======
cpybca
======
:Author: Christoforus Surjoputro <cs_sanmar@yahoo.com>
:Date: $Date: 2017-07-04 $
:Version: $Version: 1.2.0 $
:License: MIT License

.. role:: python(code)
   :language: python

.. image:: https://travis-ci.org/3mp3ri0r/cpybca.svg?branch=master
    :target: https://travis-ci.org/3mp3ri0r/cpybca

.. contents:: Table of content

Introduction
============

`cpybca`_ is python module to access BCA API. In this version, you can check balance, account statement (history), and transfer fund.

Python version
--------------

This module work on python 3.4+. Fully tested on python 3.5.2.

How to install
==============

1. Clone or download this repo https://gitlab.com/3mp3ri0r/cpybca.git.
2. Move this entire project to your project's directory.

How to use
==========

1. Import cpybca to your project by doing this :python:`from cpybca.bca import Bca`.
2. Initiate connection to BCA API server by doing this :python:`bca = BCA('YOUR_API_KEY', 'YOUR_API_SECRET', 'YOUR_BCA_HOST')`.
3. Sign in to BCA API server by doing this :python:`bca.sign_in('YOUR_CLIENT_ID', 'YOUR_CLIENT_SECRET')`.
4. Do action you want by calling :python:`Bca` function.

Get balance
-----------

You can get account balance by doing this:

.. code-block:: python

    bca.get_balance('CORPORATE_ID', 'ACCOUNT_NUMBER')

You can get multiple account balance by doing this:

.. code-block:: python

    bca.get_balance('CORPORATE_ID', ['ACCOUNT_NUMBER1', 'ACCOUNT_NUMBER2'])

Get statement
-------------

You can get account statement or history transaction by doing this:

.. code-block:: python

    bca.get_statement('CORPORATE_ID', 'ACCOUNT_NUMBER', 'START_DATE', 'END_DATE')

Note:

1. :code:`START_DATE` and :code:`END_DATE` use :code:`yyyy-MM-dd` format.
2. Maximum date to get from start to end is 31 day.

Transfer fund
-------------

You can get account statement or history transaction by doing this:

.. code-block:: python

    bca.transfer('CORPORATE_ID', 'SOURCE_ACCOUNT_NUMBER', 'BENEFICIARY_ACCOUNT_NUMBER', 'TRANSACTION_ID', 'TRANSACTION_DATE', 'REFERENCE_ID', 'AMOUNT', 'CURRENCY_CODE', 'REMARK1', 'REMARK2')

Note:

1. :code:`BENEFICIARY_ACCOUNT_NUMBER` is account number you want to receive money.
2. :code:`TRANSACTION_ID` is number of transfer you do on the following day.
3. :code:`TRANSACTION_DATE` is date you do transfer in :code:`yyyy-MM-dd` format.
4. :code:`REFERENCE_ID` is your reference code. It can contain combination of string and numeric. Example: :code:`1234/DP/2017`
5. :code:`AMOUNT` is number of amount you want to send in :code:`string` format. Example: :code:`'1000000.00'`
6. :code:`REMARK1` and :code:`REMARK2` is notes you want to send to receiver. It is not mandatory so you can remove this.

How to contribute
=================

Just create an `issue`_ when you encounter any problem.

.. _`cpybca`: https://gitlab.com/3mp3ri0r/cpybca
.. _`issue`: https://gitlab.com/3mp3ri0r/cpybca/issues