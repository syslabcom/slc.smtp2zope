Introduction
============

slc.mailrouter bridges the gap between zope and email. It is based on the same
idea as products such as mailboxer: a script is invoked by your mail transfer
agent (postfix, exim) and the body of the email is passed to this script on
stdin. This is then communicate to zope using an http post, where it is parsed
and handled.

This package implements the smtp2zope script.
