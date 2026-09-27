"""Clipo AI — entry point."""
from __future__ import annotations

import sys
import traceback
from pathlib import Path


def _crash_log_path() -> Path:
    base = Path.home() / "ClipoAI"
    try:
        base.mkdir(exist_ok=True)
        return base / "crash.log"
    except OSError:
        return Path("crash.log")


def main() -> int:
    try:
        from app.ui.main_window import MainApp
        app = MainApp()
        app.mainloop()
        return 0
    except Exception:
        tb = traceback.format_exc()
        try:
            p = _crash_log_path()
            p.write_text(tb, encoding="utf-8")
            # Also surface a message box so the user isn't left with nothing.
            import tkinter as tk
            from tkinter import messagebox
            r = tk.Tk()
            r.withdraw()
            messagebox.showerror(
                "Clipo AI failed to start",
                f"An error occurred while starting the app.\n\n"
                f"Details were saved to:\n{p}\n\n{tb.splitlines()[-1]}",
            )
        except Exception:
            pass
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
