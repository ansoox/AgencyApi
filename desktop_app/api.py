"""HTTP client helper for interacting with the Agency API backend."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


class APIError(RuntimeError):
    """Raised when the backend API returns an error."""


@dataclass(frozen=True)
class APIClient:
    """Thin wrapper around requests.Session for the Agency API."""

    base_url: str = "http://localhost:8000"
    timeout: float = 15.0

    def __post_init__(self) -> None:
        object.__setattr__(self, "_session", requests.Session())
        object.__setattr__(self, "_base", self.base_url.rstrip("/"))

    def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        url = f"{self._base}{path}"
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.timeout
        try:
            response = self._session.request(method, url, **kwargs)
        except requests.RequestException as exc:
            raise APIError(f"Network error: {exc}") from exc

        if response.status_code >= 400:
            detail: str
            try:
                payload = response.json()
                if isinstance(payload, dict):
                    if "detail" in payload:
                        detail = str(payload["detail"])
                    else:
                        detail = str(payload)
                else:
                    detail = str(payload)
            except ValueError:
                detail = response.text.strip() or response.reason
            raise APIError(f"{response.status_code}: {detail}")

        if response.headers.get("content-type", "").startswith("application/json"):
            try:
                return response.json()
            except ValueError as exc:
                raise APIError("Invalid JSON response") from exc
        return response.text

    # CRUD operations -----------------------------------------------------
    def list_items(self, table: str) -> list[dict[str, Any]]:
        data = self._request("GET", f"/api/{table}")
        return list(data) if isinstance(data, list) else []

    def fetch_item(self, table: str, item_id: int) -> dict[str, Any]:
        data = self._request("GET", f"/api/{table}/{item_id}")
        return dict(data) if isinstance(data, dict) else {}

    def create_item(self, table: str, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("POST", f"/api/{table}", json=payload)

    def update_item(self, table: str, item_id: int, payload: dict[str, Any]) -> dict[str, Any]:
        return self._request("PUT", f"/api/{table}/{item_id}", json=payload)

    def delete_item(self, table: str, item_id: int) -> None:
        self._request("DELETE", f"/api/{table}/{item_id}")

    def filter_table(self, table: str, column: str, query: str) -> list[dict[str, Any]]:
        params = {"column": column, "query": query}
        data = self._request("GET", f"/api/db/filter/{table}", params=params)
        return list(data) if isinstance(data, list) else []

    # Database utilities --------------------------------------------------
    def execute_sql(self, query: str) -> dict[str, Any]:
        payload = {"query": query}
        return self._request("POST", "/api/db/query", json=payload)

    def save_last_query(self, filename: str | None = None) -> dict[str, Any]:
        payload = {"filename": filename} if filename else {}
        return self._request("POST", "/api/db/csv", json=payload or None)

    def create_backup(self, path: str, password: str) -> dict[str, Any]:
        payload = {"path": path, "superuser_password": password}
        return self._request("POST", "/api/db/backup", json=payload)

    def restore_backup(self, path: str, password: str) -> dict[str, Any]:
        payload = {"path": path, "superuser_password": password}
        return self._request("POST", "/api/db/restore", json=payload)

    # Relation helpers ----------------------------------------------------
    def link_artist_performance(self, artist_id: int, performance_id: int) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/api/artist/{artist_id}/performance/{performance_id}/add",
        )

    def unlink_artist_performance(self, artist_id: int, performance_id: int) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/api/artist/{artist_id}/performance/{performance_id}/remove",
        )

    def link_organizer_program(self, organizer_id: int, program_id: int) -> dict[str, Any]:
        return self._request(
            "POST", f"/api/organizer/{organizer_id}/concert_program/{program_id}/add"
        )

    def unlink_organizer_program(self, organizer_id: int, program_id: int) -> dict[str, Any]:
        return self._request(
            "POST", f"/api/organizer/{organizer_id}/concert_program/{program_id}/remove"
        )

    def link_performance_program(self, performance_id: int, program_id: int) -> dict[str, Any]:
        return self._request(
            "POST", f"/api/performance/{performance_id}/concert_program/{program_id}/add"
        )

    def unlink_performance_program(self, performance_id: int, program_id: int) -> dict[str, Any]:
        return self._request(
            "POST", f"/api/performance/{performance_id}/concert_program/{program_id}/remove"
        )

