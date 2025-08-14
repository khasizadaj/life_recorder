from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll, VerticalScroll
from textual.widgets import (
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    Markdown,
    Rule,
    Button,
)
from textual import log

from life_recorder.base import LifeRecorder

DB = LifeRecorder()


class ViewingPane(VerticalScroll):
    """A pane to view the details of a selected note."""

    def __init__(self, *args, **kwargs):
        self.record_id = kwargs.pop("record_id", "default")
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        yield Markdown("# Note View", id="note-title")
        yield Rule()
        yield Label("🏷️ new-note", expand=True, id="note-tag")
        yield Label("⏳ soon...", expand=True, id="note-timestamp")
        yield Rule()
        yield Markdown(
            "\n\nNote details will be displayed here.", id="note-content"
        )
        yield Button("Delete", variant="error", id="button-delete")

    def reset(self):
        """Reset the viewing pane to its default state."""
        self.record_id = "default"
        self.query_one("#note-title", Markdown).update("# Note View")
        self.query_one("#note-tag", Label).update("🏷️ new-note")
        self.query_one("#note-timestamp", Label).update("⏳ soon...")
        self.query_one("#note-content", Markdown).update(
            "\n\nNote details will be displayed here."
        )
        for button in self.query(Button):
            button.styles.display = "none"


class Notes(HorizontalScroll):
    BINDINGS = [("escape", "reset_view", "Reset the viewing pane")]

    def compose(self) -> ComposeResult:
        with VerticalScroll(can_focus=False, can_focus_children=True):
            yield Button(
                "New Note",
                id="button-new",
                variant="primary",
            )
            yield ListView(
                *[
                    ListItem(
                        Label(f"[ #{x['id']} ] {x['title']}"), id=x["id"]
                    )
                    for x in DB.records.values()
                ],
                id="list-view",
            )

        yield ViewingPane(
            record_id="default",
            id="note-view",
            can_focus=False,
            can_focus_children=True,
        )

    def action_reset_view(self) -> None:
        self.query_one("#note-view", ViewingPane).reset()
        log.info("Escape key pressed, viewing pane reset to default state.")
        list_view = self.query_one("#list-view", ListView)
        list_view.post_message(message=ListView.Highlighted(list_view, None))

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        list_view = event.control

        if not list_view.highlighted_child:
            return

        details = DB.records[list_view.highlighted_child.id]
        if sorted(details.keys()) != sorted(
            ["id", "timestamp", "tag", "title", "content"]
        ):
            raise ValueError("Record details do not match expected structure.")

        viewing_pane = self.query_one("#note-view", ViewingPane)
        viewing_pane.record_id = details.get("id", "default")

        title = self.query_one("#note-title", Markdown)
        if title.source != details.get("title", ""):
            title.update(
                f"# {details.get('title', '')} [ #{details.get('id', '')} ]"
            )

        tag = self.query_one("#note-tag", Label)
        if tag.renderable != details.get("tag", ""):
            tag.update(f"🏷️ {details.get('tag', '')}")

        timestamp = self.query_one("#note-timestamp", Label)
        if timestamp.renderable != details.get("timestamp", ""):
            timestamp.update(f"⏳ {details.get('timestamp', '')}")

        content = self.query_one("#note-content", Markdown)
        if content.source != details.get("content", ""):
            content.update(details.get("content", ""))

        buttons = viewing_pane.query(Button)
        for button in buttons:
            button.styles.display = "block"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.control.id
        if button_id is None:
            return

        if button_id == "button-delete":
            log.info("Delete button pressed.")
            viewing_pane = self.query_one("#note-view", ViewingPane)

            log.info(f"Deleting note with ID of {viewing_pane.record_id}")
            try:
                DB.delete(viewing_pane.record_id)
            except ValueError as e:
                log.error(f"Invalid record ID: {e}")
                return

            list_item = self.query_one(f"#{viewing_pane.record_id}", ListItem)
            list_item.remove()

            log.info(f"Deleted record with ID: {viewing_pane.record_id}")
            viewing_pane.reset()
            log.info("Viewing pane reset to default state.")

        elif button_id == "button-new":
            log.info("New note button pressed.")


class LifeRecorderApp(App):
    """A Textual app to manage life records"""

    CSS_PATH = "styles/app.tcss"
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True, name="Life Recorder")
        yield VerticalScroll(
            Markdown(
                "## Welcome to Life Recorder. \nReady to jot down your thoughts?",
                id="intro",
            ),
            Notes(can_focus=False, can_focus_children=True, id="notes"),
            can_focus=False,
            can_focus_children=True,
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
