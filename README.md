[![Build](https://github.com/BCR-CX/zapi/actions/workflows/build.yml/badge.svg)](https://github.com/BCR-CX/zapi/actions/workflows/build.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=alert_status&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=bugs&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=code_smells&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=coverage&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=duplicated_lines_density&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=ncloc&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=reliability_rating&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=security_rating&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)
[![Technical Debt](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=sqale_index&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=sqale_rating&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=BCR-CX_zapi&metric=vulnerabilities&token=e968e8f9c809ca74e14256de7dc70d7de9923220)](https://sonarcloud.io/summary/new_code?id=BCR-CX_zapi)

# Libzapi - The Official BCR.CX API Client for Zendesk

![libzapi Logo](images/libzapi_logo.png)

LibZapi is a powerful and easy-to-use API client designed specifically for interacting with the Zendesk. It simplifies the
process of managing customer support tickets, automating workflows, and retrieving data from Zendesk, making it an
essential tool for developers and support teams.

## 📐 Architectural Layers

libapi follows a lightweight Domain-Driven Design (DDD) structure with inspiration from CQRS (Command-Query Responsibility
Segregation).
Even though it’s an SDK, this separation keeps models clear, testable, and easy to extend.

| **Layer**          | **Concern / Responsibility**                                                                                                                                                 | **Example Classes / Modules**                                                |
|--------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------|
| **SDK Interface**  | Public entry point for consumers. Exposes simple, zendesk APIs (e.g., `Ticketing`, `HelpCenter`, `Messaging`). Converts inputs into commands.                                | `libzapi.Ticketing`, `libzapi.HelpCenter`                                       |
| **Application**    | Coordinates use cases. Contains **Commands** and **Services** that implement the SDK’s operations. Responsible for mapping inputs to payloads and orchestrating infra calls. | `CreateUserFieldCmd`, `UpdateGroupCmd`, `UserFieldsService`, `GroupsService` |
| **Domain**         | Defines core business concepts and rules, independent of Zendesk’s API format. Contains entities, value objects, and domain services that enforce invariants.                | `libzapi.domain.models.ticketing.brand.py`, `libzapi.domain.errors.py`             |
| **Infrastructure** | Handles all external integration logic. Encapsulates API clients, request signing, and serialization details.                                                                | `UserFieldsApiClient`, `HttpClient`, `Mappers`                               |

🔄 Example Flow

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

## Getting Started

Clone the repository and install the dependencies:

```bash
git clone https://github.com/BCR-CX/zapi.git
cd libzapi
```

Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

Install Python version 3.12

```bash
uv python install 3.12
```

Check that uv is installed

```bash
uv --version
```

As a smoke test run

```bash
uv run pytest tests/unit
```

If you get the green light, you are ready to go!

## Steps to add a new API endpoint

1. **Identify the Endpoint**: Determine the Zendesk API endpoint you want to add support for. Refer to
   the [Zendesk API documentation](https://developer.zendesk.com/api-reference/) for details.
2. **Start on domain/models**: Create a new model class that represents the data structure returned by the API endpoint.
   Use existing models as references for naming conventions and structure.
3. **Go to infrastructure/mappers**: Implement a mapper class that converts the raw API responses into the model classes
   you created earlier. This class should handle any necessary data transformations.
4. **Go to infrastructure/api_clients**: Create a new API client class that implements the service contract interface.
   This class should handle the actual HTTP requests to the Zendesk API, using the appropriate HTTP methods and
   endpoints. Important. If your request has pagination, make sure to implement the pagination "yield_items" function.
5. **Go to application/services**: Implement a service class that uses the API client to perform operations related to
   the new endpoint. This class should contain easy to read methods that encapsulate the logic for interacting with the
   API.
6. **Write Tests**: Create unit tests for your new models, mappers, API clients, and services. Ensure that all tests
   pass before proceeding.
7. **Update Documentation**: Update the README.md file to include information about the new endpoint, including usage
   examples and any relevant details.
8. **Commit and Push**: Commit your changes to the repository and push them to the appropriate branch. Create a pull
   request for review.
9. **Review and Merge**: Have your code reviewed by a team member. Once approved, merge the changes into the main
   branch.

### Why go through all these steps?

Following these steps ensures that the new API endpoint is integrated into libzapi in a consistent and maintainable manner.
It helps maintain code quality, promotes reusability, and ensures that the new functionality is well-tested and
documented for future reference.

## Testing

Testing uses pytest.
There's also a cool package called hypothesis that does property based testing. As some Zendesk objects has a lot of
fields, this makes testing easier.
