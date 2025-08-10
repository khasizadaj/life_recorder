import json
from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widgets import (
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    Markdown,
)

from life_recorder.factory.base import LifeRecorderDB

DB = LifeRecorderDB()
DB.init()


class Notes(HorizontalGroup):
    def compose(self) -> ComposeResult:
        yield ListView(
            *[
                ListItem(Label(f"\n #{x['id']}: {x['title']}\n"))
                for x in DB.records.values()
            ]
        )


class LifeRecorderApp(App):
    """A Textual app to manage stopwatches."""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True, name="Life Recorder")
        yield VerticalGroup(
            Markdown(
                "## Welcome to Life Recorder. \nReady to jot down your thoughts?"
            ),
            Notes(),
        )
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark"
            if self.theme == "textual-light"
            else "textual-light"
        )


def main():
    """Run the app."""
    app = LifeRecorderApp()
    app.run()


if __name__ == "__main__":
    main()
