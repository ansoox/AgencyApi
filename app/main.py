from __future__ import annotations

import csv
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import String, cast, select, text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from pydantic import BaseModel

from . import models, schemas
from .config import get_settings
from .database import Base, engine, get_session

settings = get_settings()
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Agency API", version="1.0.0")


@dataclass(frozen=True)
class TableConfig:
    model: type[models.Base]
    create_schema: type[BaseModel]
    update_schema: type[BaseModel]
    read_schema: type[BaseModel]


TABLE_CONFIGS: dict[str, TableConfig] = {
    "artist": TableConfig(
        models.Artist, schemas.ArtistCreate, schemas.ArtistUpdate, schemas.ArtistRead
    ),
    "client": TableConfig(
        models.Client, schemas.ClientCreate, schemas.ClientUpdate, schemas.ClientRead
    ),
    "concert_program": TableConfig(
        models.ConcertProgram,
        schemas.ConcertProgramCreate,
        schemas.ConcertProgramUpdate,
        schemas.ConcertProgramRead,
    ),
    "organizer": TableConfig(
        models.Organizer,
        schemas.OrganizerCreate,
        schemas.OrganizerUpdate,
        schemas.OrganizerRead,
    ),
    "performance": TableConfig(
        models.Performance,
        schemas.PerformanceCreate,
        schemas.PerformanceUpdate,
        schemas.PerformanceRead,
    ),
    "test": TableConfig(
        models.Test, schemas.TestCreate, schemas.TestUpdate, schemas.TestRead
    ),
    "ticket": TableConfig(
        models.Ticket, schemas.TicketCreate, schemas.TicketUpdate, schemas.TicketRead
    ),
    "venue": TableConfig(
        models.Venue, schemas.VenueCreate, schemas.VenueUpdate, schemas.VenueRead
    ),
}

last_query_result: dict[str, list[Any]] = {"columns": [], "rows": []}


def _store_last_query(records: list[Any], to_schema: type[schemas.BaseModel]) -> None:
    """Cache the last query result for CSV export."""
    serialized = [to_schema.model_validate(record).model_dump() for record in records]
    last_query_result["rows"] = serialized
    last_query_result["columns"] = list(serialized[0].keys()) if serialized else []


def _handle_db_error(session: Session, exc: SQLAlchemyError) -> None:
    session.rollback()
    message = str(getattr(exc, "orig", exc))
    raise HTTPException(status_code=400, detail=message)


def _ensure_entity(session: Session, model: type[models.Base], pk: Any) -> models.Base:
    instance = session.get(model, pk)
    if not instance:
        raise HTTPException(
            status_code=404, detail=f"{model.__name__} with id={pk} not found"
        )
    return instance


def register_crud_routes(name: str, config: TableConfig) -> None:
    list_path = f"/api/{name}"
    item_path = f"/api/{name}/{{item_id}}"

    model = config.model
    create_schema = config.create_schema
    update_schema = config.update_schema
    read_schema = config.read_schema

    @app.get(list_path, response_model=list[read_schema])
    def list_items(session: Session = Depends(get_session)):
        records = session.scalars(select(model)).all()
        _store_last_query(records, read_schema)
        return [read_schema.model_validate(record) for record in records]

    @app.get(item_path, response_model=read_schema)
    def get_item(item_id: int, session: Session = Depends(get_session)):
        instance = session.get(model, item_id)
        if not instance:
            raise HTTPException(
                status_code=404, detail=f"{model.__name__} with id={item_id} not found"
            )
        _store_last_query([instance], read_schema)
        return read_schema.model_validate(instance)

    @app.post(list_path, response_model=read_schema, status_code=201)
    def create_item(payload: create_schema, session: Session = Depends(get_session)):
        instance = model(**payload.model_dump())
        session.add(instance)
        try:
            session.commit()
        except SQLAlchemyError as exc:
            _handle_db_error(session, exc)
        session.refresh(instance)
        return read_schema.model_validate(instance)

    @app.put(item_path, response_model=read_schema)
    def update_item(
        item_id: int, payload: update_schema, session: Session = Depends(get_session)
    ):
        instance = session.get(model, item_id)
        if not instance:
            raise HTTPException(
                status_code=404, detail=f"{model.__name__} with id={item_id} not found"
            )
        for field, value in payload.model_dump().items():
            setattr(instance, field, value)
        try:
            session.commit()
        except SQLAlchemyError as exc:
            _handle_db_error(session, exc)
        session.refresh(instance)
        return read_schema.model_validate(instance)

    @app.delete(item_path, status_code=204)
    def delete_item(item_id: int, session: Session = Depends(get_session)):
        instance = session.get(model, item_id)
        if not instance:
            raise HTTPException(
                status_code=404, detail=f"{model.__name__} with id={item_id} not found"
            )
        session.delete(instance)
        session.commit()


for table_name, configuration in TABLE_CONFIGS.items():
    register_crud_routes(table_name, configuration)


@app.post(
    "/api/artist/{artist_id}/performance/{performance_id}/add",
    response_model=schemas.OperationStatus,
)
def add_artist_performance(
    artist_id: int, performance_id: int, session: Session = Depends(get_session)
):
    _ensure_entity(session, models.Artist, artist_id)
    _ensure_entity(session, models.Performance, performance_id)
    existing = session.get(models.ArtistPerformance, (artist_id, performance_id))
    if existing:
        raise HTTPException(status_code=400, detail="Relation already exists")
    relation = models.ArtistPerformance(
        artist_id=artist_id, performance_id=performance_id
    )
    session.add(relation)
    session.commit()
    return schemas.OperationStatus(message="Artist linked to performance")


@app.post(
    "/api/artist/{artist_id}/performance/{performance_id}/remove",
    response_model=schemas.OperationStatus,
)
def remove_artist_performance(
    artist_id: int, performance_id: int, session: Session = Depends(get_session)
):
    relation = session.get(models.ArtistPerformance, (artist_id, performance_id))
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    session.delete(relation)
    session.commit()
    return schemas.OperationStatus(message="Artist unlinked from performance")


@app.post(
    "/api/organizer/{organizer_id}/concert_program/{program_id}/add",
    response_model=schemas.OperationStatus,
)
def add_organizer_concert_program(
    organizer_id: int, program_id: int, session: Session = Depends(get_session)
):
    _ensure_entity(session, models.Organizer, organizer_id)
    _ensure_entity(session, models.ConcertProgram, program_id)
    existing = session.get(models.OrganizerConcertProgram, (organizer_id, program_id))
    if existing:
        raise HTTPException(status_code=400, detail="Relation already exists")
    relation = models.OrganizerConcertProgram(
        organizer_id=organizer_id, concert_program_id=program_id
    )
    session.add(relation)
    session.commit()
    return schemas.OperationStatus(message="Organizer linked to concert program")


@app.post(
    "/api/organizer/{organizer_id}/concert_program/{program_id}/remove",
    response_model=schemas.OperationStatus,
)
def remove_organizer_concert_program(
    organizer_id: int, program_id: int, session: Session = Depends(get_session)
):
    relation = session.get(models.OrganizerConcertProgram, (organizer_id, program_id))
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    session.delete(relation)
    session.commit()
    return schemas.OperationStatus(message="Organizer unlinked from concert program")


@app.post(
    "/api/performance/{performance_id}/concert_program/{program_id}/add",
    response_model=schemas.OperationStatus,
)
def add_performance_concert_program(
    performance_id: int, program_id: int, session: Session = Depends(get_session)
):
    _ensure_entity(session, models.Performance, performance_id)
    _ensure_entity(session, models.ConcertProgram, program_id)
    existing = session.get(
        models.PerformanceConcertProgram, (performance_id, program_id)
    )
    if existing:
        raise HTTPException(status_code=400, detail="Relation already exists")
    relation = models.PerformanceConcertProgram(
        performance_id=performance_id,
        concert_program_id=program_id,
    )
    session.add(relation)
    session.commit()
    return schemas.OperationStatus(message="Performance linked to concert program")


@app.post(
    "/api/performance/{performance_id}/concert_program/{program_id}/remove",
    response_model=schemas.OperationStatus,
)
def remove_performance_concert_program(
    performance_id: int, program_id: int, session: Session = Depends(get_session)
):
    relation = session.get(
        models.PerformanceConcertProgram, (performance_id, program_id)
    )
    if not relation:
        raise HTTPException(status_code=404, detail="Relation not found")
    session.delete(relation)
    session.commit()
    return schemas.OperationStatus(message="Performance unlinked from concert program")


@app.post("/api/db/query")
def execute_sql_query(
    payload: schemas.SQLQuery, session: Session = Depends(get_session)
):
    result = session.execute(text(payload.query))
    if result.returns_rows:
        rows = result.mappings().all()
        data = [dict(row) for row in rows]
        last_query_result["rows"] = data
        last_query_result["columns"] = list(rows[0].keys()) if rows else []
        return {"rows": data}
    session.commit()
    last_query_result["rows"] = []
    last_query_result["columns"] = []
    return {"rowcount": result.rowcount}


@app.get("/api/db/filter/{table_name}")
def filter_table(
    table_name: str,
    column: str = Query(..., description="Column name to filter by"),
    query: str = Query(..., description="Substring to search for"),
    session: Session = Depends(get_session),
):
    config = TABLE_CONFIGS.get(table_name)
    if not config:
        raise HTTPException(status_code=404, detail="Table not found")
    column_attr = getattr(config.model, column, None)
    if column_attr is None:
        raise HTTPException(status_code=400, detail="Unknown column for selected table")
    stmt = select(config.model).where(cast(column_attr, String).ilike(f"%{query}%"))
    records = session.scalars(stmt).all()
    _store_last_query(records, config.read_schema)
    return [config.read_schema.model_validate(record) for record in records]


@app.post("/api/db/csv", response_model=schemas.OperationStatus)
def save_last_query_to_csv(payload: schemas.CSVRequest | None = None):
    if not last_query_result["rows"]:
        raise HTTPException(
            status_code=400, detail="No query executed or result is empty"
        )
    filename = (
        payload.filename if payload and payload.filename else "last_query.csv"
    ).strip()
    if not filename:
        raise HTTPException(status_code=400, detail="Filename cannot be empty")
    if not filename.endswith(".csv"):
        filename += ".csv"
    target_dir = settings.csv_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / filename
    with target_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=last_query_result["columns"])
        writer.writeheader()
        writer.writerows(last_query_result["rows"])
    return schemas.OperationStatus(message="CSV saved", path=str(target_path))


def _confirm_superuser(password: str) -> None:
    if password != settings.superuser_password:
        raise HTTPException(status_code=403, detail="Invalid superuser password")


def _build_pg_command(
    url: URL, binary: str, extra_args: list[str]
) -> tuple[list[str], dict[str, str]]:
    env = {}
    if url.password:
        env["PGPASSWORD"] = url.password
    host = url.host or "localhost"
    port = str(url.port or 5432)
    user = url.username or "postgres"
    base_args = [binary, "-h", host, "-p", port, "-U", user]
    return base_args + extra_args, env


@app.post("/api/db/backup", response_model=schemas.OperationStatus)
def create_backup(
    payload: schemas.BackupRequest, session: Session = Depends(get_session)
):
    del session  # session is unused but keeps dependency consistent
    _confirm_superuser(payload.superuser_password)
    url = make_url(settings.database_url)
    backup_path = Path(payload.path)
    if not backup_path.is_absolute():
        backup_path = settings.backup_dir / backup_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    cmd, env = _build_pg_command(
        url, "pg_dump", ["-F", "c", "-d", url.database, "-f", str(backup_path)]
    )
    complete_env = os.environ.copy()
    complete_env.update(env)
    try:
        subprocess.run(
            cmd, check=True, capture_output=True, text=True, env=complete_env
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500, detail=f"{cmd[0]} not found: {exc}"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise HTTPException(
            status_code=500, detail=exc.stderr.strip() or "Backup failed"
        ) from exc
    return schemas.OperationStatus(message="Backup completed", path=str(backup_path))


@app.post("/api/db/restore", response_model=schemas.OperationStatus)
def restore_backup(
    payload: schemas.RestoreRequest, session: Session = Depends(get_session)
):
    del session  # session is unused but keeps dependency consistent
    _confirm_superuser(payload.superuser_password)
    url = make_url(settings.database_url)
    backup_path = Path(payload.path)
    if not backup_path.exists():
        raise HTTPException(status_code=404, detail="Backup file not found")
    cmd, env = _build_pg_command(
        url,
        "pg_restore",
        ["-d", url.database, "-c", str(backup_path)],
    )
    complete_env = os.environ.copy()
    complete_env.update(env)
    try:
        subprocess.run(
            cmd, check=True, capture_output=True, text=True, env=complete_env
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500, detail=f"{cmd[0]} not found: {exc}"
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise HTTPException(
            status_code=500, detail=exc.stderr.strip() or "Restore failed"
        ) from exc
    return schemas.OperationStatus(message="Restore completed", path=str(backup_path))
