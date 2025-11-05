"""Table and field definitions for the desktop GUI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class FieldDefinition:
    """Describe a single field in a table form or dialog."""

    name: str
    label: str
    field_type: str = "str"  # Supported: str, int, date, text
    required: bool = True
    choices: tuple[str, ...] | None = None


@dataclass(frozen=True)
class TableDefinition:
    """Describe a database table exposed by the API."""

    name: str
    label: str
    fields: tuple[FieldDefinition, ...]
    primary_key: str = "id"


TABLE_DEFINITIONS: Mapping[str, TableDefinition] = {
    "artist": TableDefinition(
        name="artist",
        label="Artists",
        fields=(
            FieldDefinition("full_name", "Full Name"),
            FieldDefinition("genre", "Genre"),
            FieldDefinition("organizer_id", "Organizer ID", field_type="int", required=False),
            FieldDefinition("phone_number", "Phone Number", required=False),
            FieldDefinition("work_experience", "Work Experience", field_type="int", required=False),
        ),
    ),
    "client": TableDefinition(
        name="client",
        label="Clients",
        fields=(
            FieldDefinition("full_name", "Full Name"),
            FieldDefinition("phone", "Phone"),
            FieldDefinition("email", "Email"),
            FieldDefinition("age", "Age", field_type="int", required=False),
            FieldDefinition("organizer_id", "Organizer ID", field_type="int", required=False),
        ),
    ),
    "concert_program": TableDefinition(
        name="concert_program",
        label="Concert Programs",
        fields=(
            FieldDefinition("title", "Title"),
            FieldDefinition("date", "Date", field_type="date"),
            FieldDefinition("venue_id", "Venue ID", field_type="int", required=False),
            FieldDefinition("duration", "Duration (minutes)", field_type="int"),
            FieldDefinition("address", "Address", required=False),
            FieldDefinition("number_of_performances", "Number of Performances", field_type="int"),
            FieldDefinition("time", "Time", required=False),
        ),
    ),
    "organizer": TableDefinition(
        name="organizer",
        label="Organizers",
        fields=(
            FieldDefinition("full_name", "Full Name"),
            FieldDefinition("phone", "Phone"),
            FieldDefinition("position", "Position"),
            FieldDefinition("work_experience", "Work Experience", field_type="int", required=False),
        ),
    ),
    "performance": TableDefinition(
        name="performance",
        label="Performances",
        fields=(
            FieldDefinition("title", "Title"),
            FieldDefinition("duration", "Duration (minutes)", field_type="int", required=False),
            FieldDefinition("genre", "Genre"),
            FieldDefinition("number_of_artists", "Number of Artists", field_type="int"),
        ),
    ),
    "test": TableDefinition(
        name="test",
        label="Test Entries",
        fields=(
            FieldDefinition("a", "A", field_type="int", required=False),
            FieldDefinition("b", "B", required=False),
        ),
    ),
    "ticket": TableDefinition(
        name="ticket",
        label="Tickets",
        fields=(
            FieldDefinition("ticket_number", "Ticket Number"),
            FieldDefinition("price", "Price", field_type="int"),
            FieldDefinition("client_id", "Client ID", field_type="int", required=False),
            FieldDefinition("concert_program_id", "Concert Program ID", field_type="int", required=False),
            FieldDefinition("place", "Place", required=False),
            FieldDefinition("address", "Address", required=False),
            FieldDefinition("date", "Date", field_type="date"),
            FieldDefinition("time", "Time", required=False),
        ),
    ),
    "venue": TableDefinition(
        name="venue",
        label="Venues",
        fields=(
            FieldDefinition("name", "Name"),
            FieldDefinition("address", "Address"),
            FieldDefinition("capacity", "Capacity", field_type="int", required=False),
            FieldDefinition("type", "Type"),
        ),
    ),
}


# Mapping to maintain a stable menu order.
TABLE_ORDER: tuple[str, ...] = tuple(TABLE_DEFINITIONS.keys())
