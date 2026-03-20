"""
Ticketing basics: list, create, update tickets, and query organizations.

Usage:
    uv run python examples/ticketing_basics.py
"""

from libzapi import Ticketing
from libzapi.domain.errors import NotFound, RateLimited, ZapiError

tk = Ticketing(
    base_url="https://acme.zendesk.com",
    email="you@example.com",
    api_token="your_api_token",
)

# --- List tickets (pagination is automatic) ---
print("=== Recent tickets ===")
for ticket in tk.tickets.list_recent():
    print(f"  #{ticket.id} [{ticket.status}] {ticket.subject}")

# --- Get a single ticket ---
try:
    ticket = tk.tickets.get(ticket_id=1)
    print(f"\nTicket #{ticket.id}: {ticket.subject}")
except NotFound:
    print("\nTicket #1 not found")

# --- Create a ticket ---
new_ticket = tk.tickets.create(
    subject="Printer on fire",
    description="The printer on floor 3 is literally on fire.",
    priority="urgent",
    tags=["hardware", "fire"],
)
print(f"\nCreated ticket #{new_ticket.id}")

# --- Update a ticket ---
updated = tk.tickets.update(
    ticket_id=new_ticket.id,
    priority="high",
    tags=["hardware", "resolved"],
)
print(f"Updated ticket #{updated.id}, priority={updated.priority}")

# --- Create with custom fields ---
tk.tickets.create(
    subject="Custom field demo",
    description="This ticket has custom field values.",
    custom_fields=[
        {"id": 123, "value": "option_a"},
        {"id": 456, "value": "some text"},
    ],
)

# --- List groups ---
print("\n=== Groups ===")
for group in tk.groups.list_all():
    print(f"  {group.id}: {group.name}")

# --- Search organizations ---
print("\n=== Organizations matching 'Acme' ===")
for org in tk.organizations.search(name="Acme"):
    print(f"  {org.id}: {org.name}")

# --- Error handling ---
try:
    tk.tickets.get(ticket_id=99999999)
except NotFound:
    print("\nTicket not found (expected)")
except RateLimited:
    print("\nRate limited — the SDK retries automatically, but the limit was exceeded")
except ZapiError as e:
    print(f"\nUnexpected error: {e}")
