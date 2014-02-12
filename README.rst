===============================
twitter-bot
===============================

.. image:: https://badge.fury.io/py/twitter-bot.png
    :target: http://badge.fury.io/py/twitter-bot

.. image:: https://travis-ci.org/chrishan/twitter-bot.png?branch=master
        :target: https://travis-ci.org/chrishan/twitter-bot

.. image:: https://pypip.in/d/twitter-bot/badge.png
        :target: https://crate.io/packages/twitter-bot?version=latest


twitter bot

* Free software: BSD license
* Documentation: http://twitter-bot.rtfd.org.


Dumps hot links instead of new links on programming.reddit only after they've got more than 5 comments.

Get started
-----------

* pip install -r requirements.txt

* create a file named local_settings.py in the 'twitter-bot/twitter-bot' dir, and copy and parse the following code with the keys obtained from Twitter and Bitly.


::

    TwitterKey = {
            'consumer_key': "",
            'consumer_secret': "",
            'access_token': "",
            'access_token_secret': ""
            }
    
    BitlyKey = {
            'login': '',
            'apikey': ''
            }

* Create a cron task to run twitter-bot.py, say every five minutes

::

    */5 * * * * python twitter-bot/twitter-bot/twitter-bot.py

Features
--------

* TODO
