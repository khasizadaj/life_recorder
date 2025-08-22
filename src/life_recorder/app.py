from textual.app import App, ComposeResult
from textual.message import Message
from textual.containers import (
    HorizontalScroll,
    VerticalScroll,
    VerticalGroup,
    HorizontalGroup,
)
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


class NoteForm(Static):
    BINDINGS = [
        ("ctrl+enter", "action_submit", "Submit the form"),
        ("enter", "action_submit", "Submit the form"),
    ]

    def __init__(
        self,
        variant: str | None = None,
        record_id: str | None = None,
        *args,
        **kwargs,
    ):
        if variant is not None and variant not in ["new", "update"]:
            raise ValueError(f"Invalid variant: {variant}")

        self.variant = variant if variant else "new"

        if self.variant == "update":
            if record_id is None:
                raise ValueError(
                    "record_id must be provided for update variant"
                )
        self.record_id = record_id
        super().__init__(*args, **kwargs)

    def compose(self) -> ComposeResult:
        with VerticalGroup(id="new-note-container", classes="new-note"):
            yield Label("Add new note", id="new-note-form-title")
            yield Static("")

            yield Label("Title")
            yield Input(
                placeholder="Title",
                id="new-note-title",
                validate_on=["submitted"],
                validators=[Length(minimum=1, maximum=50)],
            )
            yield Label(
                "", variant="error", classes="error", id="new-note-error-title"
            )
            yield Static("")

            yield Label("Content")
            yield Input(
                placeholder="Content",
                validate_on=["submitted"],
                validators=[Length(minimum=1, maximum=50)],
                id="new-note-content",
            )
            yield Label(
                "",
                variant="error",
                classes="error",
                id="new-note-error-content",
            )
            yield Static("")

            yield Label("Tag (Optional)")
            yield Input(
                placeholder="Tag",
                valid_empty=True,
                id="new-note-tag",
                validate_on=["submitted"],
                validators=[Length(minimum=2, maximum=25)],
            )
            yield Label(
                "", variant="error", classes="error", id="new-note-error-tag"
            )
            yield Static("")

            with HorizontalGroup(id="new-note-actions"):
                yield Button("Save", variant="primary", id="button-save")
                yield Button("Cancel", id="button-cancel")

    class Created(Message):
        """Note created message."""

        def __init__(self, record: dict[str, str]) -> None:
            self.record = record
            super().__init__()

    class Updated(Message):
        """Note updated message."""

        def __init__(self, record: dict[str, str]) -> None:
            self.record = record
            super().__init__()

    @on(Input.Submitted)
    @on(Button.Pressed, selector="#button-save")
    async def submit(self, _: Button.Pressed | Input.Submitted) -> None:
        validation_result = await self.validate_form()
        if not validation_result:
            return
        if self.variant == "update":
            note = await self.update_note()
            self.post_message(self.Updated(note))
        else:
            note = await self.create_note()
            self.post_message(self.Created(note))
        await self.reset()

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
            return False
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
            return False
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
            return False
        else:
            content_error_label.styles.display = "none"

        return True

    async def create_note(self) -> dict[str, str]:
        log.info("Creating new note with provided details.")
        log.info(f"Tag: {self.tag_input.value}")
        log.info(f"Title: {self.title_input.value}")
        log.info(f"Content: {self.content_input.value}")
        note = DB.create(
            {
                "tag": self.tag_input.value,
                "title": self.title_input.value,
                "content": self.content_input.value,
            }
        )
        return note

    async def update_note(self) -> dict[str, str]:
        if self.record_id is None:
            raise ValueError("record_id must be set for update operation")

        log.info(f"Updating note with provided details for {self.record_id}")
        log.info(f"Tag: {self.tag_input.value}")
        log.info(f"Title: {self.title_input.value}")
        log.info(f"Content: {self.content_input.value}")

        note = DB.update(
            identifier=self.record_id,
            record={
                "tag": self.tag_input.value,
                "title": self.title_input.value,
                "content": self.content_input.value,
            },
        )
        return note

    @property
    def tag_input(self):
        return self.query_one("#new-note-tag", Input)

    @property
    def title_input(self):
        return self.query_one("#new-note-title", Input)

    @property
    def content_input(self):
        return self.query_one("#new-note-content", Input)

    async def reset(self, record: dict[str, str] | None = None) -> None:
        """Reset the form inputs to their default state."""
        if record is not None and not isinstance(record, dict):
            raise ValueError("Invalid record format.")

        if record is None:
            self.tag_input.value = ""
            self.title_input.value = ""
            self.content_input.value = ""
        else:
            self.tag_input.value = record.get("tag", "")
            self.title_input.value = record.get("title", "")
            self.content_input.value = record.get("content", "")

        # Clear error labels and hide them
        tag_error_label = self.query_one("#new-note-error-tag", Label)
        tag_error_label.update("")
        tag_error_label.styles.display = "none"

        title_error_label = self.query_one("#new-note-error-title", Label)
        title_error_label.update("")
        title_error_label.styles.display = "none"

        content_error_label = self.query_one("#new-note-error-content", Label)
        content_error_label.update("")
        content_error_label.styles.display = "none"


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
        with HorizontalGroup(id="note-view-actions"):
            yield Button(
                "Update",
                variant="default",
                id="button-update",
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
        buttons = self.query(Button)
        for button in buttons:
            button.styles.display = "none"


class Notes(HorizontalScroll):
    BINDINGS = [("escape", "reset_view", "Reset the viewing pane")]

    def compose(self) -> ComposeResult:
        with VerticalScroll(can_focus=False, can_focus_children=True):
            yield Button("New Note", id="button-new", variant="primary")
            yield NoteForm()
            yield ListView(
                *[self.create_list_item(x) for x in DB.records.values()],
                id="list-view",
            )

        yield ViewingPane(
            record_id="default",
            id="note-view",
            can_focus=False,
            can_focus_children=True,
        )

    def toggle_button_new(self):
        new_note_button = self.query_one("#button-new", Button)
        if new_note_button.disabled:
            new_note_button.label = "New note"
            new_note_button.disabled = False
        else:
            new_note_button.label = "Adding new note ..."
            new_note_button.disabled = True

    @on(Button.Pressed, "#button-new")
    @on(Button.Pressed, "#button-cancel")
    async def toggle_form(self) -> None:
        log.info("New note button pressed.")

        new_note_form = self.query_one(NoteForm)
        if new_note_form.styles.display == "block":
            self.toggle_button_new()
            new_note_form.styles.display = "none"
            await new_note_form.reset()
        else:
            self.toggle_button_new()
            new_note_form.styles.display = "block"
            new_note_form.variant = "new"
            new_note_form.query_one("#new-note-title", Input).focus()

    @on(NoteForm.Created)
    async def update_list_view(self, event: NoteForm.Created) -> None:
        log.debug(
            f"New note created, updating list view for {event.record['id']}"
        )

        list_item = self.create_list_item(event.record)
        self.list_view.mount(list_item)
        log.debug("List view updated with new note")

        new_note_form = self.query_one(NoteForm)
        new_note_form.styles.display = "none"
        log.debug("New note form hidden after submission.")

        self.toggle_button_new()

    @on(NoteForm.Updated)
    def update_note_content(self, event: NoteForm.Updated) -> None:
        log.debug(f"Updating note content for {event.record['id']}")
        viewing_pane = self.query_one("#note-view", ViewingPane)
        viewing_pane.query_one("#note-tag", Label).update(
            f"🏷️ {event.record['tag']}"
        )
        viewing_pane.query_one("#note-title", Markdown).update(
            f"# {event.record['title']} [ #{event.record['id']} ]"
        )
        viewing_pane.query_one("#note-content", Markdown).update(
            event.record["content"]
        )

        self.update_list_view_item(event.record)

        log.debug("Note content updated successfully.")

        new_note_form = self.query_one(NoteForm)
        new_note_form.styles.display = "none"
        log.debug("New note form hidden after submission.")

        self.toggle_button_new()

    def action_reset_view(self) -> None:
        self.query_one("#note-view", ViewingPane).reset()
        log.info("Escape key pressed, viewing pane reset to default state.")
        list_view = self.query_one("#list-view", ListView)
        list_view.post_message(message=ListView.Highlighted(list_view, None))

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        list_view = event.control

        if not list_view.highlighted_child:
            raise ValueError("No highlighted child in ListView.")

        if not list_view.highlighted_child.id:
            raise ValueError("No ID found for highlighted child in ListView.")

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

    @on(Button.Pressed, "#button-delete")
    def delete_note(self) -> None:
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

    @on(Button.Pressed, "#button-update")
    async def update_note(self) -> None:
        log.info("Update note button pressed.")
        new_note_form = self.query_one(NoteForm)
        new_note_form.styles.display = "block"
        new_note_form.variant = "update"
        new_note_form.record_id = self.viewing_pane.record_id
        log.info(f"Preparing to update note with ID: {new_note_form.__dict__}")

        list_view = self.list_view
        if not list_view.highlighted_child:
            raise ValueError("No highlighted child in ListView.")

        if not list_view.highlighted_child.id:
            raise ValueError("No ID found for highlighted child in ListView.")

        record = DB.records[list_view.highlighted_child.id]
        await new_note_form.reset(record=record)

        new_note_form.query_one("#new-note-title", Input).focus()

    def create_list_item(self, record: dict[str, str]) -> ListItem:
        """Create new list item for note to live in."""
        text = f"[ #{record['id']} ] {record['title']}"
        label_id = f"note-label-{record['id']}"
        label = Label(text, id=label_id)
        list_item = ListItem(label, id=record["id"])
        return list_item

    def update_list_view_item(self, record: dict[str, str]) -> None:
        list_item = self.query_one(f"#{record['id']}", ListItem)
        label = list_item.query_one(Label)
        label.update(f"[ #{record['id']} ] {record['title']}")

    @property
    def list_view(self) -> ListView:
        return self.query_one("#list-view", ListView)

    @property
    def viewing_pane(self):
        return self.query_one("#note-view", ViewingPane)


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
