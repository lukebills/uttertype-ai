from rich import box
from rich.align import Align
from rich.console import Console
from rich.table import Table
from rich.text import Text
from datetime import datetime


class ConsoleTable:
    def __init__(self, total_cost_decimals: int = 6):
        self.console = Console()
        self.table = Table(show_footer=False)
        self.total_cost = 0
        self.total_cost_decimals = total_cost_decimals
        self._setup_table()

    def _update_cost(self, cost: float):
        self.total_cost += cost
        self.table.columns[2].footer = (
            f"${round(self.total_cost, self.total_cost_decimals)}"
        )

    def _setup_table(self):
        self.centered_table = Align.center(self.table)
        self.table.add_column("Date", no_wrap=True)
        self.table.add_column(
            "Transcription", Text.from_markup("[b]Total:", justify="right")
        )
        self.table.add_column(
            "Cost", Text.from_markup("[b]$0", justify="right"), no_wrap=True
        )
        self.table.show_footer = True

        self.table.columns[0].header_style = "bold green"
        self.table.columns[0].style = "green"
        self.table.columns[1].header_style = "bold blue"
        self.table.columns[1].style = "blue"
        self.table.columns[1].footer = "Total"
        self.table.columns[2].header_style = "bold cyan"
        self.table.columns[2].style = "cyan"
        self.table.row_styles = ["none", "dim"]
        self.table.box = box.SIMPLE_HEAD

    def __enter__(self):
        self.console.clear()
        self.console.print(self.centered_table)

    def __exit__(self, *args, **kwargs):
        pass

    def insert(self, transcription: str, cost: float):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%dth %B, %I:%M%p")
        self.table.add_row(formatted_datetime, transcription, f"${cost}")
        self._update_cost(cost)
        # Clear the console and reprint the table
        self.console.clear()
        self.console.print(self.centered_table)
        # Text("API Error", style="bold red")
