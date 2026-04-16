from dataclasses import dataclass

from libzapi.domain.shared_objects.logical_key import LogicalKey


@dataclass(frozen=True, slots=True)
class Address:
    id: int
    name: str = ""
    city: str = ""
    country_code: str = ""
    province: str = ""
    state: str = ""
    street: str = ""
    zip: str = ""
    provider_reference: str = ""

    @property
    def logical_key(self) -> LogicalKey:
        return LogicalKey("address", str(self.id))
