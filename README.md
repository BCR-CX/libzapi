[![Build](https://github.com/BCR-CX/libzapi/actions/workflows/build.yml/badge.svg)](https://github.com/BCR-CX/libzapi/actions/workflows/build.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzapi&metric=coverage&token=5382993ce4e5b6d8b65848ab77a971e2b51077ae)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzapi)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_libzapi&metric=alert_status&token=5382993ce4e5b6d8b65848ab77a971e2b51077ae)](https://sonarcloud.io/summary/new_code?id=BCR-CX_libzapi)

# libzapi — Python SDK for the Zendesk API

A typed, batteries-included Python client for Zendesk. Handles authentication, pagination, retries, and error mapping so you can focus on your integration.

## Installation

```bash
pip install libzapi
```

Requires Python 3.12+.

## Quick Start

**Email + API token:**

```python
from libzapi import Ticketing

ticketing = Ticketing(
    base_url="https://yourcompany.zendesk.com",
    email="you@company.com",
    api_token="your_api_token",
)
```

**OAuth:**

```python
ticketing = Ticketing(
    base_url="https://yourcompany.zendesk.com",
    oauth_token="your_oauth_token",
)
```

All three entry points (`Ticketing`, `HelpCenter`, `CustomData`) accept the same auth arguments.

## Ticketing

```python
from libzapi import Ticketing

tk = Ticketing("https://acme.zendesk.com", email="a@b.com", api_token="tok")

# List tickets — pagination is automatic
for ticket in tk.tickets.list():
    print(ticket.id, ticket.subject)

# Get a single ticket
ticket = tk.tickets.get(ticket_id=12345)

# Create a ticket
new_ticket = tk.tickets.create(
    subject="Printer on fire",
    description="The printer on floor 3 is literally on fire.",
    priority="urgent",
    tags=["hardware", "fire"],
)

# Update a ticket
tk.tickets.update(ticket_id=new_ticket.id, priority="high", tags=["resolved"])

# Create with custom fields
tk.tickets.create(
    subject="Custom field example",
    description="Body text",
    custom_fields=[{"id": 123, "value": "abc"}],
)

# Search organizations
for org in tk.organizations.search(name="Acme"):
    print(org.id, org.name)

# List groups
for group in tk.groups.list_all():
    print(group.id, group.name)
```

## Help Center

```python
from libzapi import HelpCenter

hc = HelpCenter("https://acme.zendesk.com", email="a@b.com", api_token="tok")

# List all articles
for article in hc.articles.list_all():
    print(article.id, article.title)

# Articles by locale
for article in hc.articles.list_all_by_locale("en-us"):
    print(article.title)

# Incremental export (unix timestamp)
for article in hc.articles.list_incremental(start_time=1700000000):
    print(article.title)

# Categories CRUD
category = hc.categories.create(
    name="Billing", locale="en-us", description="Billing articles", position=1
)
hc.categories.update(category.id, name="Billing & Payments", description="Updated", position=1)
hc.categories.delete(category.id)

# Sections
section = hc.sections.create(
    category_id=category.id, name="Invoices", locale="en-us", description="Invoice help", position=1
)
hc.sections.delete(section.id)
```

## Custom Objects

```python
from libzapi import CustomData

cd = CustomData("https://acme.zendesk.com", email="a@b.com", api_token="tok")

# List custom objects
for obj in cd.custom_objects.list_all():
    print(obj.key, obj.title)

# Get a specific object
obj = cd.custom_objects.get("my_object")

# List fields for an object
for field in cd.custom_object_fields.list_all("my_object"):
    print(field.key, field.type)

# Query records with sort and filter
for record in cd.custom_object_records.list_all(
    custom_object_key="my_object",
    sort_type="updated_at",
    sort_order="desc",
    page_size=50,
):
    print(record.id, record.name)
```

## Error Handling

libzapi raises typed exceptions for Zendesk API errors:

```python
from libzapi.domain.errors import ZapiError, NotFound, Unauthorized, RateLimited, UnprocessableEntity

try:
    ticket = tk.tickets.get(ticket_id=99999999)
except NotFound:
    print("Ticket does not exist")
except Unauthorized:
    print("Check your credentials")
except RateLimited:
    print("Too many requests — SDK retries automatically, but limit was exceeded")
except UnprocessableEntity as e:
    print("Validation error:", e)
except ZapiError as e:
    print("Unexpected API error:", e)
```

## Pagination

Pagination is transparent. Methods that return collections yield items lazily — the SDK fetches the next page automatically when needed. Both cursor-based and offset pagination are supported depending on the Zendesk endpoint.

```python
# Just iterate — no page management needed
for ticket in tk.tickets.list():
    process(ticket)
```

## Retries

The HTTP client automatically retries on `429` (rate limited) and `5xx` errors with exponential backoff (up to 5 retries). The `Retry-After` header is respected.

## Available Services

### Ticketing

| Service | Attribute | Description |
|---------|-----------|-------------|
| Account Settings | `account_settings` | Account configuration |
| Attachments | `attachments` | File attachments |
| Automations | `automations` | Automation rules |
| Brands | `brands` | Brand management |
| Brand Agents | `brand_agents` | Brand-agent assignments |
| Email Notifications | `email_notifications` | Email notification settings |
| Groups | `groups` | Agent groups |
| Macros | `macros` | Macro management |
| Organizations | `organizations` | Organization management |
| Requests | `requests` | End-user requests |
| Schedules | `schedules` | Business schedules |
| Sessions | `sessions` | User sessions |
| SLA Policies | `sla_policies` | SLA policy management |
| Support Addresses | `support_addresses` | Support email addresses |
| Suspended Tickets | `suspended_tickets` | Suspended ticket management |
| Tickets | `tickets` | Ticket CRUD and queries |
| Ticket Audits | `ticket_audits` | Ticket audit logs |
| Ticket Fields | `ticket_fields` | Ticket field definitions |
| Ticket Forms | `ticket_forms` | Ticket form management |
| Ticket Metrics | `ticket_metrics` | Ticket metrics |
| Ticket Triggers | `ticket_triggers` | Trigger rules |
| Ticket Trigger Categories | `ticket_trigger_categories` | Trigger categorization |
| Users | `users` | User management |
| User Fields | `user_fields` | User field definitions |
| Views | `views` | View management |
| Workspaces | `workspaces` | Agent workspaces |

### Help Center

| Service | Attribute | Description |
|---------|-----------|-------------|
| Account Custom Claims | `account_custom_claims` | Custom JWT claims |
| Articles | `articles` | Article listing and export |
| Article Attachments | `articles_attachments` | Article file attachments |
| Categories | `categories` | Category CRUD |
| Sections | `sections` | Section CRUD |
| User Segments | `user_segments` | User segment management |

### Custom Data

| Service | Attribute | Description |
|---------|-----------|-------------|
| Custom Objects | `custom_objects` | Custom object definitions |
| Custom Object Fields | `custom_object_fields` | Field definitions per object |
| Custom Object Records | `custom_object_records` | Record CRUD and queries |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for architecture details, development setup, and how to add new endpoints.
