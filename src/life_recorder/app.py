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
)
from textual import log

from life_recorder.factory.read import ReadLifeRecorder

DB = ReadLifeRecorder()


class Notes(HorizontalScroll):
    def compose(self) -> ComposeResult:
        yield ListView(
            *[
                ListItem(Label(f"\n #{x['id']}: {x['title']}\n"), id=x["id"])
                for x in DB.records.values()
            ],
            id="list-view",
        )
        yield VerticalScroll(
            MarkdownViewer(
                "# Note View \nNote will be displayed here.",
                show_table_of_contents=False,
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

    def on_list_view_selected(self):
        list_view = self.query_one(selector="#list-view", expect_type=ListView)

        if not list_view.highlighted_child:
            return

        note_view = self.query_one(
            selector="#note-view", expect_type=VerticalScroll
        )
        # remove all markdown viewers (we should only have one)
        self.query(MarkdownViewer).remove()

        log.info(DB.records[list_view.highlighted_child.id])
        content = DB.records[list_view.highlighted_child.id]["content"]

        selected_item_in_markdown = MarkdownViewer(
            content, show_table_of_contents=False
        )
        note_view.mount(selected_item_in_markdown)


def main():
    """Run the app."""
    app = LifeRecorderApp()
    app.run()


if __name__ == "__main__":
    main()
