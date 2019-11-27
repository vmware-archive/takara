More seals
==========

For now the local file store and fernet cipher are good to move things forward. But we do need to add the shamir seal


How App-mergable is this?
=========================

Can this be merged into Idem and Heist without issue?

Docs
====

Once it is fleshed out a little more this needs docs

Transport
=========

We need to make the transport system functional so that this can present an api over http and unix sockets

Transparent config/sls loading
==============================

It would be optimal if this could store an entire sls tree and be directly usable via conf

Fuse filesystem?
================

Would is be possible to make a mountable read only fuse fs?

Then we could just mount secrets on systems and store large parts of config files?
