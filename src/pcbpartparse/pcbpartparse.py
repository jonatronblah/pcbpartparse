from textual.app import App, ComposeResult
from textual import on
from textual.widgets import DirectoryTree

from pcbpartparse.config import Settings
from pcbpartparse.loader import Loader

CONFIG = Settings()


class pcbpartparse(App):
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield DirectoryTree(CONFIG.input_path)

    @on(DirectoryTree.FileSelected)
    def handle_file_selected(self, message: DirectoryTree.FileSelected) -> None:
        loader = Loader(
            output_path=CONFIG.output_path,
            input_path=str(message.path),
            group_dict=CONFIG.group_dict,
        )
        loader.load_csv()
        loader.export()
        self.exit()

    async def on_key(self, event):
        if event.key == "escape":
            self.exit()
