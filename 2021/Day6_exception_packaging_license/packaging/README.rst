Hello World
===========

This is a simple example, demonstraiting how you can publish your module/code to PyPI.



Installation
================

Run the following to install

.. code-block:: python
        pip install helloWorld


Usage
=========

.. code-block:: python
        from helloWorld import say_hello

        #Generate "hello, world!"
        say_hello()

        #Generate "Hello, everyone"
        say_hello('everyone')


Developing Hello World
=======================

To install helloWorld, along with the tools you need to develop and run tests, run the following in your virtualenviroment:
.. code-block:: bash
        $ pip installl -e .[dev]



