# placeoftheday

[![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/limiear/placeoftheday?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![License](https://pypip.in/license/placeoftheday/badge.svg)](https://pypi.python.org/pypi/placeoftheday/) [![Downloads](https://pypip.in/download/placeoftheday/badge.svg)](https://pypi.python.org/pypi/placeoftheday/) [![Build Status](https://travis-ci.org/limiear/placeoftheday.svg?branch=master)](https://travis-ci.org/limiear/placeoftheday) [![Coverage Status](https://coveralls.io/repos/limiear/placeoftheday/badge.png)](https://coveralls.io/r/limiear/placeoftheday) [![Code Health](https://landscape.io/github/limiear/placeoftheday/master/landscape.png)](https://landscape.io/github/limiear/placeoftheday/master) [![PyPI version](https://badge.fury.io/py/placeoftheday.svg)](http://badge.fury.io/py/placeoftheday)
[![Supported Python versions](https://pypip.in/py_versions/placeoftheday/badge.svg)](https://pypi.python.org/pypi/placeoftheday/) [![Stories in Ready](https://badge.waffle.io/limiear/placeoftheday.png?label=ready&title=Ready)](https://waffle.io/limiear/placeoftheday)

A python script to This bot present to you the place of the day.

Requirements
============

If you want to use this script on any GNU/Linux or OSX system you just need to execute:

    $ pip install placeoftheday

If you want to improve this script, you should download the [github repository](https://github.com/limiear/placeoftheday) and execute:

    $ make virtualenv deploy

On Ubuntu Desktop there are some other libraries not installed by default (zlibc libssl libbz2-dev libxml2-dev libxslt1-dev python-gevent libpng12-dev) which may need to be installed to use these script. Use the next command to automate the installation of the additional C libraries:

    $ make ubuntu virtualenv deploy


Testing
=======

To test all the project you should use the command:

    $ make test

If you want to help us or report an issue join to us through the [Github issue tracker](https://github.com/limiear/placeoftheday/issues).


Example
=======

To run the bot you should execute:

    $ python -c "import placeoftheday.bot"


About
=====

In this service we used the [MaxMind](https://www.maxmind.com/en/free-world-cities-database) cities database. This software is developed by [LIMIE](http://www.limie.com.ar). You can contact us to [limie.ar@gmail.com](mailto:limie.ar@gmail.com).
