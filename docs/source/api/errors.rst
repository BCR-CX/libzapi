Errors
======

All SDK exceptions inherit from :class:`~libzapi.domain.errors.ZapiError`.

.. automodule:: libzapi.domain.errors
   :members:
   :undoc-members:
   :show-inheritance:

Exception Hierarchy
-------------------

.. code-block:: text

   ZapiError
   ├── Unauthorized      — 401 responses
   ├── NotFound          — 404 responses
   ├── UnprocessableEntity — 422 responses
   └── RateLimited       — 429 responses (after retries exhausted)
