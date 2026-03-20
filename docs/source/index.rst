libzapi — Python SDK for the Zendesk API
========================================

A typed, batteries-included Python client for Zendesk. Handles authentication,
pagination, retries, and error mapping so you can focus on your integration.

Installation
------------

.. code-block:: bash

   pip install libzapi

Requires Python 3.12+.

Quick Start
-----------

.. code-block:: python

   from libzapi import Ticketing

   tk = Ticketing(
       base_url="https://yourcompany.zendesk.com",
       email="you@company.com",
       api_token="your_api_token",
   )

   for ticket in tk.tickets.list():
       print(ticket.id, ticket.subject)

All three entry points (:class:`~libzapi.application.services.ticketing.Ticketing`,
:class:`~libzapi.application.services.help_center.HelpCenter`,
:class:`~libzapi.application.services.custom_data.CustomData`) accept the same
authentication arguments (``email`` + ``api_token``, or ``oauth_token``).

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/services
   api/models
   api/errors
   api/http
