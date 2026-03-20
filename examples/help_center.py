"""
Help Center: list articles, manage categories and sections.

Usage:
    uv run python examples/help_center.py
"""

from libzapi import HelpCenter
from libzapi.domain.errors import ZapiError

hc = HelpCenter(
    base_url="https://acme.zendesk.com",
    email="you@example.com",
    api_token="your_api_token",
)

try:
    # --- List all articles ---
    print("=== All articles ===")
    for article in hc.articles.list_all():
        print(f"  [{article.id}] {article.title}")

    # --- Articles by locale ---
    print("\n=== English articles ===")
    for article in hc.articles.list_all_by_locale("en-us"):
        print(f"  [{article.id}] {article.title}")

    # --- Incremental article export ---
    print("\n=== Articles updated since timestamp ===")
    for article in hc.articles.list_incremental(start_time=1700000000):
        print(f"  [{article.id}] {article.title}")

    # --- Categories CRUD ---
    print("\n=== Creating category ===")
    category = hc.categories.create(
        name="Billing",
        locale="en-us",
        description="All billing-related articles",
        position=1,
    )
    print(f"  Created category: {category.id} — {category.name}")

    hc.categories.update(
        category_id=category.id,
        name="Billing & Payments",
        description="Updated billing category",
        position=1,
    )
    print(f"  Updated category: {category.id}")

    # --- Sections CRUD ---
    print("\n=== Creating section ===")
    section = hc.sections.create(
        category_id=category.id,
        name="Invoices",
        locale="en-us",
        description="Invoice-related help articles",
        position=1,
    )
    print(f"  Created section: {section.id} — {section.name}")

    # Clean up
    hc.sections.delete(section.id)
    hc.categories.delete(category.id)
    print("\nCleaned up test data.")

except ZapiError as e:
    print(f"Zendesk API error: {e}")
