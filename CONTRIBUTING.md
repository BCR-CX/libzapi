# Contributing to libzapi

## Getting Started

Clone the repository and install dependencies:

```bash
git clone https://github.com/BCR-CX/zapi.git
cd libzapi
```

Install [uv](https://docs.astral.sh/uv/):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

Install Python 3.12 and project dependencies:

```bash
uv python install 3.12
uv sync
```

Run the unit tests as a smoke test:

```bash
uv run pytest tests/unit
```

## Architecture

libzapi follows a lightweight Domain-Driven Design (DDD) structure with inspiration from CQRS.

| Layer | Responsibility | Examples |
|-------|---------------|----------|
| **SDK Interface** | Public entry point for consumers. Exposes `Ticketing`, `HelpCenter`, `CustomData`. | `libzapi.Ticketing`, `libzapi.HelpCenter` |
| **Application** | Coordinates use cases. Contains Commands and Services that implement operations. | `CreateUserFieldCmd`, `GroupsService` |
| **Domain** | Core business concepts and rules, independent of Zendesk's API format. | `libzapi.domain.models.ticketing.brand`, `libzapi.domain.errors` |
| **Infrastructure** | External integration: API clients, HTTP, serialization. | `TicketFieldApiClient`, `HttpClient`, mappers |

### Data Flow

```text
User calls libzapi.Ticketing(...).groups.list_all()
        ↓
SDK Interface: forwards call to GroupsService
        ↓
Application: GroupsService invokes GroupsApiClient to fetch data
        ↓
Infrastructure: GroupsApiClient executes HTTP GET to Zendesk API
        ↓
Domain: maps JSON into Group domain entities
        ↓
Returns List[Group] to the SDK user
```

## Steps to Add a New API Endpoint

1. **Identify the endpoint** — Find it in the [Zendesk API docs](https://developer.zendesk.com/api-reference/).

2. **Create the domain model** (`domain/models/`) — Frozen dataclass with `slots=True`. Use existing models as reference.

3. **Create the mapper** (`infrastructure/mappers/`) — Converts raw API JSON into domain models. Handle any data transformations here.

4. **Create the API client** (`infrastructure/api_clients/`) — Implements HTTP requests to the Zendesk API. If the endpoint supports pagination, use the `yield_items` function.

5. **Create the service** (`application/services/`) — High-level methods that wrap the API client. Keep methods readable and self-explanatory.

6. **Write tests** — Unit tests for models, mappers, API clients, and services. All tests must pass before proceeding.

7. **Update documentation** — Add usage examples to the README if the endpoint is user-facing.

8. **Commit and push** — Create a pull request for review.

9. **Review and merge** — Get approval from a team member before merging.

### Why these steps?

Following this process keeps the codebase consistent and maintainable. Each layer has a clear responsibility, making it easy to test in isolation and extend later.

## Testing

Testing uses **pytest**. We also use **hypothesis** for property-based testing, which is useful for Zendesk objects with many fields.

```bash
# Unit tests
uv run pytest tests/unit

# Full suite with coverage (requires Zendesk credentials)
tox -vv

# Linting
tox -e lint

# Single test file
uv run pytest tests/unit/path/to/test_file.py

# Single test
uv run pytest tests/unit/path/to/test_file.py::test_name -v
```

Integration tests require these environment variables:
- `ZENDESK_URL`
- `ZENDESK_EMAIL`
- `ZENDESK_TOKEN`

## Code Style

- Python 3.12+ with full type annotations
- Line length limit: 120 characters (enforced by Ruff)
- Format: `uv run ruff format .`
- Lint and auto-fix: `uv run ruff check . --fix`
