windowbox-barker
================

Windowbox Barker is a small script that queries a Windowbox site for new posts,
and tweets links to any that it finds.

Requirements
------------

Windowbox Barker is developed and tested on Python 2.7. It may or may not
require some amount of effort to get it to work under Python 3.

You'll need the usual stuff: `python`, `python-pip`.

Installation and Operation
--------------------------

1. Clone the repo somewhere and `cd` into that directory.

2. Make a virtualenv, unless you enjoy living on the edge. These instructions
   assume your virtualenv is all set up and activated.

3. `pip install -r reqs.txt`

4. `cp config-example.ini config.ini`

5. Edit the new `config.ini` file and fill in all the fields. Change the default
   settings if you think you can do better.

6. `python windowbox-barker.py` - Put it in a cron job for maximum fun.

Configuration Parameters
------------------------

**[windowbox] Section**



**[twitter] Section**
