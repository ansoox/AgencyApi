"""Tkinter desktop application for controlling the Agency API backend."""

from __future__ import annotations

import os
import tkinter as tk
from datetime import date
from functools import partial
from tkinter import messagebox, ttk
from typing import Any, Iterable

from .api import APIClient, APIError
from .definitions import FieldDefinition, TABLE_DEFINITIONS, TABLE_ORDER, TableDefinition
from .forms import FormDialog, SQLDialog


class AgencyDesktopApp:
    """Main desktop GUI implementation."""

    def __init__(self, root: tk.Tk, base_url: str = "http://localhost:8000") -> None:
        self.root = root
        self.root.title("Agency Desktop")
        self.root.geometry("1024x640")
        self.root.minsize(900, 500)

        self.client = APIClient(base_url=base_url)
        self.active_table = tk.StringVar(value=TABLE_ORDER[0])
        self.current_rows: list[dict[str, Any]] = []
        self.row_cache: dict[str, dict[str, Any]] = {}

        self.status_var = tk.StringVar(value="Ready")

        self._build_menu()
        self._build_main_area()
        self._bind_shortcuts()

        self.load_table_data(self.active_table.get())

    # ------------------------------------------------------------------
    # UI construction helpers
    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        self.menubar = menubar

        # File menu
        file_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="File", menu=file_menu, underline=0)
        file_menu.add_command(
            label="Exit",
            accelerator="Ctrl+E",
            command=self.exit_app,
            underline=1,
        )
        self.file_menu = file_menu

        # Tables menu
        tables_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Tables", menu=tables_menu, underline=0)
        for table_key in TABLE_ORDER:
            definition = TABLE_DEFINITIONS[table_key]
            tables_menu.add_radiobutton(
                label=definition.label,
                variable=self.active_table,
                value=table_key,
                command=partial(self.on_table_selected, table_key),
                underline=0,
            )
        self.tables_menu = tables_menu

        # Operations menu
        operations_menu = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Operations", menu=operations_menu, underline=0)
        operations_menu.add_command(
            label="View Table",
            accelerator="Ctrl+V",
            command=self.view_active_table,
            underline=0,
        )
        operations_menu.add_command(
            label="Add Record",
            accelerator="Ctrl+A",
            command=self.add_record,
            underline=0,
        )
        operations_menu.add_command(
            label="Update Record",
            accelerator="Ctrl+U",
            command=self.update_record,
            underline=0,
        )
        operations_menu.add_command(
            label="Delete Record",
            accelerator="Ctrl+D",
            command=self.delete_record,
            underline=0,
        )
        operations_menu.add_separator()
        operations_menu.add_command(
            label="Filter Table…",
            command=self.filter_table,
            underline=0,
        )
        operations_menu.add_command(
            label="Execute SQL…",
            accelerator="Ctrl+Q",
            command=self.run_special_query,
            underline=8,
        )
        operations_menu.add_command(
            label="Save Last Query…",
            accelerator="Ctrl+S",
            command=self.save_last_query,
            underline=0,
        )
        operations_menu.add_separator()
        operations_menu.add_command(
            label="Create Backup…",
            accelerator="Ctrl+B",
            command=self.create_backup,
            underline=0,
        )
        operations_menu.add_command(
            label="Restore Backup…",
            command=self.restore_backup,
            underline=0,
        )
        operations_menu.add_separator()
        operations_menu.add_command(
            label="Link Artist to Performance…",
            command=self.link_artist_performance,
            underline=0,
        )
        operations_menu.add_command(
            label="Unlink Artist from Performance…",
            command=self.unlink_artist_performance,
            underline=0,
        )
        operations_menu.add_command(
            label="Link Organizer to Program…",
            command=self.link_organizer_program,
            underline=0,
        )
        operations_menu.add_command(
            label="Unlink Organizer from Program…",
            command=self.unlink_organizer_program,
            underline=0,
        )
        operations_menu.add_command(
            label="Link Performance to Program…",
            command=self.link_performance_program,
            underline=0,
        )
        operations_menu.add_command(
            label="Unlink Performance from Program…",
            command=self.unlink_performance_program,
            underline=0,
        )
        self.operations_menu = operations_menu

    def _build_main_area(self) -> None:
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill="both", expand=True)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, show="headings", selectmode="browse")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.bind("<Double-1>", self._on_row_double_click)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=1, column=0, sticky="ew")
        self.tree.configure(xscrollcommand=hsb.set)

        status_bar = ttk.Label(main_frame, textvariable=self.status_var, anchor="w")
        status_bar.pack(fill="x", pady=(10, 0))
        self.status_bar = status_bar

    def _bind_shortcuts(self) -> None:
        bindings = {
            "<Control-a>": self.add_record,
            "<Control-A>": self.add_record,
            "<Control-v>": self.view_active_table,
            "<Control-V>": self.view_active_table,
            "<Control-d>": self.delete_record,
            "<Control-D>": self.delete_record,
            "<Control-u>": self.update_record,
            "<Control-U>": self.update_record,
            "<Control-q>": self.run_special_query,
            "<Control-Q>": self.run_special_query,
            "<Control-s>": self.save_last_query,
            "<Control-S>": self.save_last_query,
            "<Control-b>": self.create_backup,
            "<Control-B>": self.create_backup,
            "<Control-e>": self.exit_app,
            "<Control-E>": self.exit_app,
            "<F10>": self._focus_menubar,
        }
        for sequence, handler in bindings.items():
            self.root.bind_all(sequence, handler)

    # ------------------------------------------------------------------
    # Utility helpers
    def set_status(self, message: str) -> None:
        self.status_var.set(message)

    def on_table_selected(self, table: str) -> None:
        self.active_table.set(table)
        self.load_table_data(table)

    def view_active_table(self, event: tk.Event | None = None) -> None:
        del event
        self.load_table_data(self.active_table.get())

    def load_table_data(self, table: str, rows: list[dict[str, Any]] | None = None) -> None:
        definition = TABLE_DEFINITIONS[table]
        try:
            data = rows if rows is not None else self.client.list_items(table)
        except APIError as exc:
            messagebox.showerror("API Error", str(exc), parent=self.root)
            self.set_status(f"Failed to fetch data for {definition.label}.")
            return

        self.current_rows = data
        self.row_cache = {}

        columns = self._resolve_columns(definition, data)
        self.tree.config(columns=columns)
        for column in columns:
            heading = column.replace("_", " ").title()
            anchor = "center" if column == definition.primary_key else "w"
            self.tree.heading(column, text=heading, anchor=anchor)
            self.tree.column(column, width=140, anchor=anchor, stretch=True)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in data:
            item_id = str(row.get(definition.primary_key, ""))
            values = [self._format_value(row.get(col)) for col in columns]
            self.tree.insert("", "end", iid=item_id, values=values)
            if item_id:
                self.row_cache[item_id] = row

        record_count = len(data)
        self.set_status(f"{definition.label}: {record_count} record(s) loaded.")

    def _resolve_columns(
        self, definition: TableDefinition, rows: Iterable[dict[str, Any]]
    ) -> list[str]:
        base_order = [definition.primary_key] + [field.name for field in definition.fields]
        present_keys = set()
        for row in rows:
            present_keys.update(row.keys())
        ordered = [key for key in base_order if key in present_keys]
        extra = sorted(present_keys.difference(ordered))
        return ordered + extra

    def _format_value(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, (date,)):
            return value.isoformat()
        return str(value)

    def _prepare_payload(
        self, definition: TableDefinition, values: dict[str, str]
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {}
        for field in definition.fields:
            raw_value = values.get(field.name, "")
            try:
                payload[field.name] = self._convert_field_value(field, raw_value)
            except ValueError as exc:
                raise ValueError(f"{field.label}: {exc}") from exc
        return payload

    @staticmethod
    def _convert_field_value(field: FieldDefinition, value: str) -> Any:
        if not value:
            return None
        if field.field_type == "int":
            return int(value)
        if field.field_type == "date":
            parsed = date.fromisoformat(value)
            return parsed.isoformat()
        return value

    def _get_selected_row(self) -> dict[str, Any] | None:
        selection = self.tree.selection()
        if not selection:
            return None
        item_id = selection[0]
        return self.row_cache.get(item_id)

    def _focus_menubar(self, event: tk.Event) -> str:
        del event
        self.root.focus_set()
        self.root.event_generate("<Alt_L>")
        return "break"

    def _on_row_double_click(self, event: tk.Event) -> None:
        del event
        self.update_record()

    # ------------------------------------------------------------------
    # CRUD operations
    def add_record(self, event: tk.Event | None = None) -> None:
        del event
        table = self.active_table.get()
        definition = TABLE_DEFINITIONS[table]
        dialog = FormDialog(
            self.root,
            title=f"Add {definition.label}",
            fields=definition.fields,
        )
        values = dialog.show()
        if values is None:
            return
        try:
            payload = self._prepare_payload(definition, values)
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc), parent=self.root)
            return
        try:
            self.client.create_item(table, payload)
        except APIError as exc:
            messagebox.showerror("API Error", str(exc), parent=self.root)
            return
        self.load_table_data(table)
        self.set_status(f"Record added to {definition.label}.")

    def update_record(self, event: tk.Event | None = None) -> None:
        del event
        table = self.active_table.get()
        definition = TABLE_DEFINITIONS[table]
        selected = self._get_selected_row()
        if not selected:
            messagebox.showwarning(
                "Update Record", "Select a row to update.", parent=self.root
            )
            return
        item_id = selected.get(definition.primary_key)
        if item_id is None:
            messagebox.showerror(
                "Update Record", "Unable to determine selected record id.", parent=self.root
            )
            return
        initial = {
            field.name: self._format_value(selected.get(field.name))
            for field in definition.fields
        }
        dialog = FormDialog(
            self.root,
            title=f"Update {definition.label}",
            fields=definition.fields,
            initial_values=initial,
        )
        values = dialog.show()
        if values is None:
            return
        try:
            payload = self._prepare_payload(definition, values)
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc), parent=self.root)
            return
        try:
            self.client.update_item(table, int(item_id), payload)
        except APIError as exc:
            messagebox.showerror("API Error", str(exc), parent=self.root)
            return
        self.load_table_data(table)
        self.set_status(f"Record {item_id} updated in {definition.label}.")

    def delete_record(self, event: tk.Event | None = None) -> None:
        del event
        table = self.active_table.get()
        definition = TABLE_DEFINITIONS[table]
        selected = self._get_selected_row()
        if not selected:
            messagebox.showwarning(
                "Delete Record", "Select a row to delete.", parent=self.root
            )
            return
        item_id = selected.get(definition.primary_key)
        if item_id is None:
            messagebox.showerror(
                "Delete Record", "Unable to determine selected record id.", parent=self.root
            )
            return
        if not messagebox.askyesno(
            "Confirm Delete",
            f"Delete record {item_id} from {definition.label}?",
            parent=self.root,
        ):
            return
        try:
            self.client.delete_item(table, int(item_id))
        except APIError as exc:
            messagebox.showerror("API Error", str(exc), parent=self.root)
            return
        self.load_table_data(table)
        self.set_status(f"Record {item_id} deleted from {definition.label}.")

    # ------------------------------------------------------------------
    # Additional operations
    def filter_table(self) -> None:
        table = self.active_table.get()
        definition = TABLE_DEFINITIONS[table]
        columns = (definition.primary_key,) + tuple(field.name for field in definition.fields)
        dialog = FormDialog(
            self.root,
            title=f"Filter {definition.label}",
            fields=(
                FieldDefinition("column", "Column", choices=columns),
                FieldDefinition("query", "Contains"),
            ),
        )
        values = dialog.show()
        if values is None:
            return
        column = values["column"]
        query = values["query"]
        try:
            rows = self.client.filter_table(table, column, query)
        except APIError as exc:
            messagebox.showerror("API Error", str(exc), parent=self.root)
            return
        self.load_table_data(table, rows=rows)
        self.set_status(f"Filtered {definition.label} by {column!r}.")

    def run_special_query(self, event: tk.Event | None = None) -> None:
        del event
        dialog = SQLDialog(self.root, title="Execute SQL Query")
        query = dialog.show()
        if query is None:
            return
        try:
            response = self.client.execute_sql(query)
        except APIError as exc:
            messagebox.showerror("API Error", str(exc), parent=self.root)
            return
        if "rows" in response:
            rows = response["rows"]
            self.load_custom_rows(rows)
            self.set_status("SQL query executed successfully.")
        else:
            rowcount = response.get("rowcount", 0)
            messagebox.showinfo(
                "SQL Query",
                f"Query executed. Rows affected: {rowcount}.",
                parent=self.root,
            )
            self.set_status("SQL query executed successfully.")

    def load_custom_rows(self, rows: list[dict[str, Any]]) -> None:
        if not rows:
            self.tree.config(columns=())
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.set_status("Query executed. No rows returned.")
            return
        columns = list(rows[0].keys())
        self.tree.config(columns=columns)
        for column in columns:
            heading = column.replace("_", " ").title()
            self.tree.heading(column, text=heading, anchor="w")
            self.tree.column(column, width=140, anchor="w", stretch=True)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.row_cache = {}
        for index, row in enumerate(rows, start=1):
            item_id = str(index)
            values = [self._format_value(row.get(col)) for col in columns]
            self.tree.insert("", "end", iid=item_id, values=values)
            self.row_cache[item_id] = row

    def save_last_query(self, event: tk.Event | None = None) -> None:
        del event
        dialog = FormDialog(
            self.root,
            title="Save Last Query",
            fields=(FieldDefinition("filename", "Filename", required=False),),
        )
        values = dialog.show()
        if values is None:
            return
        filename = values.get("filename") or None
        try:
            response = self.client.save_last_query(filename)
        except APIError as exc:
            messagebox.showerror("API Error", str(exc), parent=self.root)
            return
        message = response.get("message", "Saved.")
        path = response.get("path")
        if path:
            message += f"\nSaved to: {path}"
        messagebox.showinfo("Save Last Query", message, parent=self.root)
        self.set_status(message)

    def create_backup(self, event: tk.Event | None = None) -> None:
        del event
        dialog = FormDialog(
            self.root,
            title="Create Backup",
            fields=(
                FieldDefinition("path", "Backup Path"),
                FieldDefinition("password", "Superuser Password"),
            ),
        )
        values = dialog.show()
        if values is None:
            return
        try:
            response = self.client.create_backup(values["path"], values["password"])
        except APIError as exc:
            messagebox.showerror("API Error", str(exc), parent=self.root)
            return
        message = response.get("message", "Backup created.")
        path = response.get("path")
        if path:
            message += f"\nLocation: {path}"
        messagebox.showinfo("Create Backup", message, parent=self.root)
        self.set_status(message)

    def restore_backup(self) -> None:
        dialog = FormDialog(
            self.root,
            title="Restore Backup",
            fields=(
                FieldDefinition("path", "Backup Path"),
                FieldDefinition("password", "Superuser Password"),
            ),
        )
        values = dialog.show()
        if values is None:
            return
        try:
            response = self.client.restore_backup(values["path"], values["password"])
        except APIError as exc:
            messagebox.showerror("API Error", str(exc), parent=self.root)
            return
        message = response.get("message", "Backup restored.")
        path = response.get("path")
        if path:
            message += f"\nSource: {path}"
        messagebox.showinfo("Restore Backup", message, parent=self.root)
        self.set_status(message)

    # ------------------------------------------------------------------
    # Relation operations
    def link_artist_performance(self) -> None:
        self._handle_relation_action(
            title="Link Artist to Performance",
            fields=(
                FieldDefinition("artist_id", "Artist ID"),
                FieldDefinition("performance_id", "Performance ID"),
            ),
            action=lambda a_id, p_id: self.client.link_artist_performance(a_id, p_id),
        )

    def unlink_artist_performance(self) -> None:
        self._handle_relation_action(
            title="Unlink Artist from Performance",
            fields=(
                FieldDefinition("artist_id", "Artist ID"),
                FieldDefinition("performance_id", "Performance ID"),
            ),
            action=lambda a_id, p_id: self.client.unlink_artist_performance(a_id, p_id),
        )

    def link_organizer_program(self) -> None:
        self._handle_relation_action(
            title="Link Organizer to Program",
            fields=(
                FieldDefinition("organizer_id", "Organizer ID"),
                FieldDefinition("program_id", "Program ID"),
            ),
            action=lambda o_id, c_id: self.client.link_organizer_program(o_id, c_id),
        )

    def unlink_organizer_program(self) -> None:
        self._handle_relation_action(
            title="Unlink Organizer from Program",
            fields=(
                FieldDefinition("organizer_id", "Organizer ID"),
                FieldDefinition("program_id", "Program ID"),
            ),
            action=lambda o_id, c_id: self.client.unlink_organizer_program(o_id, c_id),
        )

    def link_performance_program(self) -> None:
        self._handle_relation_action(
            title="Link Performance to Program",
            fields=(
                FieldDefinition("performance_id", "Performance ID"),
                FieldDefinition("program_id", "Program ID"),
            ),
            action=lambda p_id, c_id: self.client.link_performance_program(p_id, c_id),
        )

    def unlink_performance_program(self) -> None:
        self._handle_relation_action(
            title="Unlink Performance from Program",
            fields=(
                FieldDefinition("performance_id", "Performance ID"),
                FieldDefinition("program_id", "Program ID"),
            ),
            action=lambda p_id, c_id: self.client.unlink_performance_program(p_id, c_id),
        )

    def _handle_relation_action(
        self,
        title: str,
        fields: tuple[FieldDefinition, FieldDefinition],
        action: Any,
    ) -> None:
        dialog = FormDialog(self.root, title=title, fields=fields)
        values = dialog.show()
        if values is None:
            return
        try:
            first_key, second_key = fields[0].name, fields[1].name
            first_id = int(values[first_key])
            second_id = int(values[second_key])
        except (KeyError, ValueError):
            messagebox.showerror(title, "Enter valid numeric identifiers.", parent=self.root)
            return
        try:
            response = action(first_id, second_id)
        except APIError as exc:
            messagebox.showerror("API Error", str(exc), parent=self.root)
            return
        message = response.get("message", "Operation completed.")
        messagebox.showinfo(title, message, parent=self.root)
        self.set_status(message)

    # ------------------------------------------------------------------
    def exit_app(self, event: tk.Event | None = None) -> None:
        del event
        self.root.quit()


def run_app(base_url: str | None = None) -> None:
    if base_url is None:
        base_url = os.getenv("AGENCY_API_BASE_URL", "http://localhost:8000")
    root = tk.Tk()
    app = AgencyDesktopApp(root, base_url=base_url)
    root.mainloop()


__all__ = ["AgencyDesktopApp", "run_app"]
