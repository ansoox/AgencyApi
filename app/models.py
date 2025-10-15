from sqlalchemy import CheckConstraint, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Organizer(Base):
    __tablename__ = "organizer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    position: Mapped[str] = mapped_column("position", String(100), nullable=False)
    work_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (CheckConstraint("work_experience >= 0", name="organizer_work_experience_check"),)


class Venue(Base):
    __tablename__ = "venue"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)

    __table_args__ = (CheckConstraint("capacity > 0", name="venue_capacity_check"),)


class Artist(Base):
    __tablename__ = "artist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    genre: Mapped[str] = mapped_column(String(100), nullable=False)
    organizer_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("agency.organizer.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
    )
    phone_number: Mapped[str | None] = mapped_column(String(20), nullable=True)
    work_experience: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (CheckConstraint("work_experience >= 0", name="artist_work_experience_check"),)


class Client(Base):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)
    organizer_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("agency.organizer.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
    )

    __table_args__ = (CheckConstraint("age >= 0", name="client_age_check"),)


class Performance(Base):
    __tablename__ = "performance"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    duration: Mapped[int | None] = mapped_column(Integer, nullable=True)
    genre: Mapped[str] = mapped_column(String(100), nullable=False)
    number_of_artists: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (CheckConstraint("duration > 0", name="performance_duration_check"),)


class ConcertProgram(Base):
    __tablename__ = "concert_program"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    venue_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("agency.venue.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
    )
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    number_of_performances: Mapped[int] = mapped_column(Integer, nullable=False)
    time: Mapped[str | None] = mapped_column("time", String(20), nullable=True)


class Ticket(Base):
    __tablename__ = "ticket"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticket_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    client_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("agency.client.id", onupdate="CASCADE", ondelete="SET NULL"),
        nullable=True,
    )
    concert_program_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("agency.concert_program.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
    )
    place: Mapped[str | None] = mapped_column(String(50), nullable=True)
    address: Mapped[str | None] = mapped_column(String(100), nullable=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    time: Mapped[str | None] = mapped_column("time", String(20), nullable=True)

    __table_args__ = (CheckConstraint("price >= 0", name="ticket_price_check"),)


class Test(Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    a: Mapped[int | None] = mapped_column(Integer, nullable=True)
    b: Mapped[str | None] = mapped_column(Text, nullable=True)


class ArtistPerformance(Base):
    __tablename__ = "artist_performance"

    artist_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agency.artist.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    performance_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agency.performance.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )


class OrganizerConcertProgram(Base):
    __tablename__ = "organizer_concert_program"

    organizer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agency.organizer.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    concert_program_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agency.concert_program.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )


class PerformanceConcertProgram(Base):
    __tablename__ = "performance_concert_program"

    performance_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agency.performance.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
    concert_program_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("agency.concert_program.id", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
    )
