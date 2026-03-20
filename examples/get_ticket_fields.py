"""
List all ticket fields from your Zendesk instance.

Usage:
    uv run python examples/get_ticket_fields.py
"""

from libzapi import Ticketing
from libzapi.domain.errors import ZapiError

sdk = Ticketing(
    base_url="https://acme.zendesk.com",
    email="you@example.com",
    api_token="your_api_token",
)

try:
    print("=== Listing ticket fields ===")
    for field in sdk.ticket_fields.list_all():
        print(f"[{field.id}] {field.title} (type={field.type}, required={field.required})")

except ZapiError as e:
    print("Zendesk API error:", e)
