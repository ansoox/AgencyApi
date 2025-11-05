"""Reusable dialogs for the desktop GUI."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Mapping, Sequence

from .definitions import FieldDefinition


class FormDialog(tk.Toplevel):
    """Modal dialog to collect simple field values."""

    def __init__(
        self,
        parent: tk.Tk,
        title: str,
        fields: Sequence[FieldDefinition],
        initial_values: Mapping[str, str] | None = None,
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.resizable(False, False)
        self.initial_values = initial_values or {}
        self.fields = fields
        self.result: dict[str, str] | None = None
        self.widgets: dict[str, tk.Widget] = {}

        self.columnconfigure(1, weight=1)
        self._build_widgets()
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.bind("<Return>", self._on_submit)
        self.bind("<Escape>", self._on_cancel)

        self.transient(parent)
        self.grab_set()
        self._focus_first_widget()

    def _build_widgets(self) -> None:
        padding_opts = {"padx": 10, "pady": 6}
        for row, field in enumerate(self.fields):
            label = ttk.Label(self, text=field.label)
            label.grid(row=row, column=0, sticky="w", **padding_opts)
            widget: tk.Widget
            if field.choices:
                widget = ttk.Combobox(
                    self,
                    values=list(field.choices),
                    state="readonly",
                )
                initial = self.initial_values.get(field.name)
                if initial:
                    widget.set(initial)
                elif field.choices:
                    widget.set(field.choices[0])
            else:
                widget = ttk.Entry(self)
                initial = self.initial_values.get(field.name)
                if initial is not None:
                    widget.insert(0, initial)
            widget.grid(row=row, column=1, sticky="ew", **padding_opts)
            self.widgets[field.name] = widget

        button_frame = ttk.Frame(self)
        button_frame.grid(row=len(self.fields), column=0, columnspan=2, sticky="e", padx=10, pady=(0, 10))

        submit_btn = ttk.Button(button_frame, text="OK", command=self._on_submit)
        submit_btn.grid(row=0, column=0, padx=(0, 6))
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self._on_cancel)
        cancel_btn.grid(row=0, column=1)

    def _focus_first_widget(self) -> None:
        if self.fields:
            first = self.widgets[self.fields[0].name]
            first.focus_set()

    def _collect_values(self) -> dict[str, str]:
        values: dict[str, str] = {}
        for field in self.fields:
            widget = self.widgets[field.name]
            if isinstance(widget, ttk.Combobox):
                value = widget.get().strip()
            elif isinstance(widget, ttk.Entry):
                value = widget.get().strip()
            else:
                value = getattr(widget, "get", lambda: "")().strip()
            if not value and field.required and not field.choices:
                raise ValueError(f"Field '{field.label}' is required.")
            values[field.name] = value
        return values

    def _on_submit(self, event: tk.Event | None = None) -> None:
        del event  # Event is unused; we keep signature for Tk compatibility
        try:
            self.result = self._collect_values()
        except ValueError:
            self.bell()
            return
        self.destroy()

    def _on_cancel(self, event: tk.Event | None = None) -> None:
        del event
        self.result = None
        self.destroy()

    def show(self) -> dict[str, str] | None:
        """Block until the dialog is closed and return the collected values."""
        self.wait_window()
        return self.result


class SQLDialog(tk.Toplevel):
    """Modal dialog for composing SQL queries."""

    def __init__(self, parent: tk.Tk, title: str, initial: str = "") -> None:
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.geometry("600x400")
        self.result: str | None = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        text_label = ttk.Label(self, text="SQL Query:")
        text_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        self.text = tk.Text(self, wrap="word", undo=True)
        self.text.grid(row=1, column=0, sticky="nsew", padx=10, pady=6)
        if initial:
            self.text.insert("1.0", initial)

        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, sticky="e", padx=10, pady=(0, 10))

        submit_btn = ttk.Button(button_frame, text="Execute", command=self._on_submit)
        submit_btn.grid(row=0, column=0, padx=(0, 6))
        cancel_btn = ttk.Button(button_frame, text="Cancel", command=self._on_cancel)
        cancel_btn.grid(row=0, column=1)

        self.protocol("WM_DELETE_WINDOW", self._on_cancel)
        self.bind("<Control-Return>", self._on_submit)
        self.bind("<Escape>", self._on_cancel)

        self.transient(parent)
        self.grab_set()
        self.text.focus_set()

    def _on_submit(self, event: tk.Event | None = None) -> None:
        del event
        query = self.text.get("1.0", "end").strip()
        if not query:
            self.bell()
            return
        self.result = query
        self.destroy()

    def _on_cancel(self, event: tk.Event | None = None) -> None:
        del event
        self.result = None
        self.destroy()

    def show(self) -> str | None:
        self.wait_window()
        return self.result

