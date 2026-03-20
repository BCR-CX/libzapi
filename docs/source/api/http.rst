HTTP & Authentication
=====================

HTTP Client
-----------

.. automodule:: libzapi.infrastructure.http.client
   :members:
   :undoc-members:
   :show-inheritance:

The HTTP client automatically retries on ``429`` (rate limited) and ``5xx`` errors
with exponential backoff (up to 5 retries). The ``Retry-After`` header is respected.

Authentication
--------------

.. automodule:: libzapi.infrastructure.http.auth
   :members:
   :undoc-members:

Two authentication methods are supported:

- **Email + API token**: ``api_token_headers(email, api_token)``
- **OAuth**: ``oauth_headers(token)``

Pagination
----------

.. automodule:: libzapi.infrastructure.http.pagination
   :members:
   :undoc-members:
   :show-inheritance:

Pagination is transparent — methods that return collections yield items lazily.
Both cursor-based and offset pagination are supported depending on the endpoint.
