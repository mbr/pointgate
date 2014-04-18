DynDNS-like URL updates for PointDNS
====================================

As of May 2014, `DynDNS <https://dyndns.org>`_ does no longer support free
DNS entries, so a replacement is required. This small app allows the usage
of `PointDNS <https://pointhq.com>`_ as a drop-in replacement because it
mimicks the venerable DynDNS API, which is supported by many consumer
routers worldwide.

It's meant to be hosted on `heroku <https://heroku.com>`_ and comes with all
the security flaws of the original DynDNS, so do not use this for serious
business.


Installation
------------

Simple::

  git clone https://github.com/mbr/pointgate
  heroku create --region eu <heroku app name>
  heroku config:set POINTGATE_UPDATE_USER=<a username to login for the router>
  heroku config:set POINTGATE_UPDATE_PASSWORD=<a password to login>
  heroku config:set POINTGATE_POINTDNS_USER=<your pointhq account's email>
  heroku config:set POINTGATE_POINTDNS_API_KEY=<your pointdns api key>
