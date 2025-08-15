from textual.app import App, ComposeResult
from textual.containers import HorizontalScroll, VerticalScroll, VerticalGroup
from textual.widgets import (
    Footer,
    Header,
    Label,
    ListItem,
    ListView,
    Markdown,
    Rule,
    Button,
    Input,
    Static,
)
from textual.validation import Length
from textual import log, on

from life_recorder.base import LifeRecorder

DB = LifeRecorder()


class NewNoteForm(Static):

    BINDINGS = [
        ("ctrl+enter", "action_submit", "Submit the form"),
        ("enter", "action_submit", "Submit the form"),
    ]

    def compose(self) -> ComposeResult:
        with VerticalGroup(id="new-note-container", classes="new-note", disabled=True):
            yield Markdown("### Add new note")
            yield Static("")

            yield Label("Title")
            yield Input(
                placeholder="Title",
                id="new-note-title",
                validate_on=["submitted"],
                validators=[Length(minimum=1, maximum=50)],
            )
            yield Label("", variant="error", classes="error", id="new-note-error-title")
            yield Static("")

            yield Label("Content")
            yield Input(
                placeholder="Content",
                validate_on=["submitted"],
                validators=[Length(minimum=1, maximum=50)],
                id="new-note-content",
            )
            yield Label("", variant="error", classes="error", id="new-note-error-content")
            yield Static("")

            yield Label("Tag (Optional)")
            yield Input(
                placeholder="Tag",
                valid_empty=True,
                id="new-note-tag",
                validate_on=["submitted"],
                validators=[Length(minimum=2, maximum=25)],
            )
            yield Label("", variant="error", classes="error", id="new-note-error-tag")
            yield Static("")

            yield Button("Save", variant="primary", id="button-save")

    # async def on_button_pressed(self, event: Input.Submitted) -> None:
    #     """Handle input submission."""
    #     await self.validate_form()
    #     await self.create_note()

    @on(Input.Submitted)
    @on(Button.Pressed, selector="#button-save")
    async def submit(self, _: Button.Pressed | Input.Submitted) -> None:
        await self.validate_form()
        await self.create_note()

    async def validate_form(self):
        tag_input = self.tag_input
        res = tag_input.validate(tag_input.value)
        log.info(f"Tag input validation result: {res}")
        tag_error_label = self.query_one("#new-note-error-tag", Label)
        if res is not None and not res.is_valid:
            description = res.failures[0].description
            if description is not None:
                tag_error_label.update(description)
                log.error(f"Tag input validation failed: {description}")
            tag_error_label.styles.display = "block"
            return
        else:
            tag_error_label.styles.display = "none"

        title_input = self.title_input
        res = title_input.validate(title_input.value)
        log.info(f"Title input validation result: {res}")
        title_error_label = self.query_one("#new-note-error-title", Label)
        if res is not None and not res.is_valid:
            description = res.failures[0].description
            if description is not None:
                title_error_label.update(description)
                log.error(f"Title input validation failed: {description}")
            title_error_label.styles.display = "block"
            return
        else:
            title_error_label.styles.display = "none"

        content_input = self.content_input
        res = content_input.validate(content_input.value)
        log.info(f"Content input validation result: {res}")
        content_error_label = self.query_one("#new-note-error-content", Label)
        if res is not None and not res.is_valid:
            description = res.failures[0].description
            if description is not None:
                content_error_label.update(description)
                log.error(f"Content input validation failed: {description}")
            content_error_label.styles.display = "block"
            return
        else:
            content_error_label.styles.display = "none"

    async def create_note(self) -> None:

        log.info("Creating new note with provided details.")
        log.info(f"Tag: {self.tag_input.value}")
        log.info(f"Title: {self.title_input.value}")
        log.info(f"Content: {self.content_input.value}")

    @property
    def tag_input(self):
        return self.query_one("#new-note-tag", Input)

    @property
    def title_input(self):
        return self.query_one("#new-note-title", Input)

    @property
    def content_input(self):
        return self.query_one("#new-note-content", Input)


class ViewingPane(VerticalScroll):
    """A pane to view the details of a selected note."""

    def __init__(self, *args, **kwargs):
        self.record_id = kwargs.pop("record_id", "default")
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        # TODO Activate form
        # yield NewNoteForm()
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
        self.query_one("#button-delete", Button).styles.display = "none"


class Notes(HorizontalScroll):
    BINDINGS = [("escape", "reset_view", "Reset the viewing pane")]

    def compose(self) -> ComposeResult:
        with VerticalScroll(can_focus=False, can_focus_children=True):
            yield Button(
                "New Note",
                id="button-new",
                variant="primary",
                disabled=True,
            )
            yield ListView(
                *[
                    ListItem(Label(f"[ #{x['id']} ] {x['title']}"), id=x["id"])
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
