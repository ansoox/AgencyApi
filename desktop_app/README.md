# Agency Desktop Application

This Tkinter application provides a classic desktop interface for every operation exposed by the Agency API backend.

## Launch

```bash
python -m desktop_app.app
```

The app assumes the backend API is available at `http://localhost:8000`. Set the `AGENCY_API_BASE_URL` environment variable before launching to point to a different server.

## Navigation

- Menus: `File`, `Tables`, `Operations` (open with `F10`, or `Alt` + underlined letter).
- Active table data are displayed immediately after launch. Rotate tables through `Tables` menu.
- All actions are available both through menu selections (mouse) and keyboard shortcuts.

## Keyboard Shortcuts

- `Ctrl+A` — add record to the active table.
- `Ctrl+V` — refresh data for the active table.
- `Ctrl+D` — delete the selected record in the active table.
- `Ctrl+U` — update the selected record in the active table.
- `Ctrl+Q` — execute a custom SQL query.
- `Ctrl+S` — save the most recent query result to CSV.
- `Ctrl+B` — create a database backup.
- `Ctrl+E` — exit the application.

All dialog windows are modal, navigable with `Tab` / `Shift+Tab`, and support cursor movement for field editing.

