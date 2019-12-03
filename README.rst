======
Takara
======

Takara is a secure secrets store. Takara differs from other secret stores in
that it supports progressive usage. Secret stores need to be easy to use and
easy to start with, but able to scale from easy local security all the way up
to enterprise and military level security. If someone starts with something
simple, it is optimal if it can scale all the way up.

Simple Usage Tutorial
=====================

Getting started with Takara is easy, it has a lot of options but you don't need
to know them! In fact you only need to know that takara stores encrypted data in
a higherarchy, so data has a location, just like a file on a filesystem.

Install
=======

We will just need to install the basic `takara` for this to work:

.. code-block:: bash

    pip install takara

Create a Crypt Store
====================

Takara stores encrypted data in `units`. This allows you to have seperate units
that store seperate data, these unit can even be used to store data in different
storage systems with different access systems.

But we don't need to worry about that now! We just need to make our first unit!
If you don't tell it what to name the unit, then the unit will default to being
called `main`. Lets make the `main` unit now:

.. code-block:: bash

    takara create

This will create a secure store that is password protected. The command will
prompt you for the password that you wish to use to secure the secrets.

Set a Value
===========

Now that we have a unit set up we can set a value inside it. Just
tell `takara` to chose a path for the unit to be stored and the data to be
stored in said unit.

.. code-block:: bash

    takara set -p my/secret -s 'The speed of an unladen swallow...'

Done! Now the encrypted secret is secure inside of takara.

Get the Value
=============

Getting the value out is just as easy:

.. code-block:: bash

    takara get -p my/secret

Now the plain text of the secret is presented back!