"""
Custom Objects: list objects, fields, and query records.

Usage:
    uv run python examples/custom_objects.py
"""

from libzapi import CustomData
from libzapi.domain.errors import ZapiError

cd = CustomData(
    base_url="https://acme.zendesk.com",
    email="you@example.com",
    api_token="your_api_token",
)

try:
    # --- List all custom objects ---
    print("=== Custom objects ===")
    for obj in cd.custom_objects.list_all():
        print(f"  {obj.key}: {obj.title}")

    # --- Get a specific object ---
    obj = cd.custom_objects.get("my_object")
    print(f"\nObject: {obj.key} — {obj.title}")

    # --- List fields for an object ---
    print(f"\n=== Fields for '{obj.key}' ===")
    for field in cd.custom_object_fields.list_all(obj.key):
        print(f"  {field.key} ({field.type})")

    # --- Query records with sorting ---
    print(f"\n=== Records for '{obj.key}' (newest first) ===")
    for record in cd.custom_object_records.list_all(
        custom_object_key=obj.key,
        sort_type="updated_at",
        sort_order="desc",
        page_size=10,
    ):
        print(f"  {record.id}: {record.name}")

    # --- Check object limits ---
    limit = cd.custom_object_records.limit()
    print(f"\nRecord limit: {limit}")

except ZapiError as e:
    print(f"Zendesk API error: {e}")
