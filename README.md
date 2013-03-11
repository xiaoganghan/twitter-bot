Dumps hot links instead of new links on programming.reddit only after they've got more than 5 comments.

Get started
===========

create a file named local_settings.py in the 'source' dir, and copy and parse the following code with the keys obtained from Twitter and Bitly.

```python
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

```

change appname in app.yaml to the name of your app on appengine.

License
=======
Apache 2.0
