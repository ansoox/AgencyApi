from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class ArtistBase(BaseModel):
    full_name: str
    genre: str
    organizer_id: int | None = None
    phone_number: str | None = None
    work_experience: int | None = Field(default=None, ge=0)


class ArtistCreate(ArtistBase):
    pass


class ArtistUpdate(ArtistBase):
    pass


class ArtistRead(ArtistBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ClientBase(BaseModel):
    full_name: str
    phone: str
    email: str
    age: int | None = Field(default=None, ge=0)
    organizer_id: int | None = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(ClientBase):
    pass


class ClientRead(ClientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ConcertProgramBase(BaseModel):
    title: str
    date: date
    venue_id: int | None = None
    duration: int = Field(gt=0)
    address: str | None = None
    number_of_performances: int = Field(gt=0)
    time: str | None = None


class ConcertProgramCreate(ConcertProgramBase):
    pass


class ConcertProgramUpdate(ConcertProgramBase):
    pass


class ConcertProgramRead(ConcertProgramBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrganizerBase(BaseModel):
    full_name: str
    phone: str
    position: str
    work_experience: int | None = Field(default=None, ge=0)


class OrganizerCreate(OrganizerBase):
    pass


class OrganizerUpdate(OrganizerBase):
    pass


class OrganizerRead(OrganizerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PerformanceBase(BaseModel):
    title: str
    duration: int | None = Field(default=None, gt=0)
    genre: str
    number_of_artists: int = Field(gt=0)


class PerformanceCreate(PerformanceBase):
    pass


class PerformanceUpdate(PerformanceBase):
    pass


class PerformanceRead(PerformanceBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TestBase(BaseModel):
    a: int | None = None
    b: str | None = None


class TestCreate(TestBase):
    pass


class TestUpdate(TestBase):
    pass


class TestRead(TestBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TicketBase(BaseModel):
    ticket_number: str
    price: int = Field(ge=0)
    client_id: int | None = None
    concert_program_id: int | None = None
    place: str | None = None
    address: str | None = None
    date: date
    time: str | None = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(TicketBase):
    pass


class TicketRead(TicketBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class VenueBase(BaseModel):
    name: str
    address: str
    capacity: int | None = Field(default=None, gt=0)
    type: str


class VenueCreate(VenueBase):
    pass


class VenueUpdate(VenueBase):
    pass


class VenueRead(VenueBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SQLQuery(BaseModel):
    query: str


class CSVRequest(BaseModel):
    filename: str | None = None


class BackupRequest(BaseModel):
    path: str
    superuser_password: str


class RestoreRequest(BackupRequest):
    pass


class OperationStatus(BaseModel):
    message: str
    path: str | None = None
