from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll, VerticalScroll
from textual.widgets import (
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    Markdown,
    MarkdownViewer,
    Rule,
)
from textual import log

from life_recorder.factory.read import ReadLifeRecorder

DB = ReadLifeRecorder()


class Notes(HorizontalScroll):
    def compose(self) -> ComposeResult:
        yield ListView(
            *[
                ListItem(
                    Label(f"\n [ #{x['id']} ] {x['title']}\n"), id=x["id"]
                )
                for x in DB.records.values()
            ],
            id="list-view",
        )
        yield VerticalScroll(
            Markdown("# Note View", id="note-title"),
            Rule(),
            Label(" 🏷️ new-note", expand=True, id="note-tag"),
            Label(" ⏳ soon...", expand=True, id="note-timestamp"),
            Rule(),
            Markdown(
                "\n\nNote details will be displayed here.", id="note-content"
            ),
            id="note-view",
        )


class LifeRecorderApp(App):
    """A Textual app to manage life records"""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header(show_clock=True, name="Life Recorder")
        yield VerticalScroll(
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

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        list_view = event.control

        if not list_view.highlighted_child:
            return

        details = DB.records[list_view.highlighted_child.id]
        if sorted(details.keys()) != sorted(
            ["id", "timestamp", "tag", "title", "content"]
        ):
            raise ValueError("Record details do not match expected structure.")

        title = self.query_one("#note-title", Markdown)
        if title.source != details.get("title", ""):
            title.update(
                f"# {details.get('title', '')} [ #{details.get('id', '')} ]"
            )

        tag = self.query_one("#note-tag", Label)
        if tag.renderable != details.get("tag", ""):
            tag.update(f" 🏷️ {details.get('tag', '')}")

        timestamp = self.query_one("#note-timestamp", Label)
        if timestamp.renderable != details.get("timestamp", ""):
            timestamp.update(f" ⏳ {details.get('timestamp', '')}")

        content = self.query_one("#note-content", Markdown)
        if content.source != details.get("content", ""):
            content.update(details.get("content", ""))


def main():
    """Run the app."""
    app = LifeRecorderApp()
    app.run()


if __name__ == "__main__":
    main()
