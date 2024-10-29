from rich.console import Console
from rich.progress import Progress
from rich.text import Text
from assets.text_file import Text_File
import shutil

console = Console()

class Text_Style:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def common_text(primary_text: str = "", secondary_text: str = "", 
                    primary_text_color="white", primary_text_style="bold", 
                    secondary_text_color="red", secondary_text_style: str = "bold",add_line_break: bool = True,add_text_center:bool=False) -> None:
        """
        Function to display two styled texts in the console.
        """
        # Combine the text color and style into one string
        primary_style = f"{primary_text_style} {primary_text_color}"
        secondary_style = f"{secondary_text_style} {secondary_text_color}"
        
        # Create rich text objects for both texts
        styled_primary = Text(primary_text, style=primary_style)
        styled_secondary = Text(str(secondary_text), style=secondary_style)
        
        # Print both texts if both are provided
        if primary_text and secondary_text:
            console.print(styled_primary, styled_secondary,end="\n" if add_line_break else "".center(shutil.get_terminal_size().columns,"") if add_text_center else "")
        elif primary_text:
            console.print(styled_primary,end="\n" if add_line_break else "".center(shutil.get_terminal_size().columns,"^") if add_text_center else "")
        elif secondary_text:
            console.print(styled_secondary,end="\n" if add_line_break else "".center(shutil.get_terminal_size().columns,"^") if add_text_center else "")
        
        return ""
    
    @staticmethod
    def ExceptionTextFormatter(primary_text: str = "", secondary_text: str = "", 
                    primary_text_color="yellow", primary_text_style="bold", 
                    secondary_text_color="red", secondary_text_style: str = "bold",add_line_break: bool = True) -> None:
        """
        Function to display two styled texts in the console.
        """
        # Combine the text color and style into one string
        primary_style = f"{primary_text_style} {primary_text_color}"
        secondary_style = f"{secondary_text_style} {secondary_text_color}"
        
        # Create rich text objects for both texts
        styled_primary = Text(primary_text, style=primary_style)
        styled_secondary = Text(str(secondary_text), style=secondary_style)
        
        # Print both texts if both are provided
        if primary_text and secondary_text:
            console.print(styled_primary, styled_secondary,end="\n" if add_line_break else "")
        elif primary_text:
            console.print(styled_primary,end="\n" if add_line_break else "")
        elif secondary_text:
            console.print(styled_secondary,end="\n" if add_line_break else "")

        return ""
    
    @staticmethod
    def progress_bar(Progessbar_name:str = Text_File.common_text["loading_data"],Progressbar_time:int=10000,Progressbar_value:int=1):
        for task_seq in range(Progressbar_value):
            task_no = f"Task{task_seq}"
            with Progress() as progress:
                task_no = progress.add_task(f"[red]{Progessbar_name}...[/]", total=Progressbar_time)
                while not progress.finished:
                    progress.update(task_no, advance=0.1)
                return True
    
    def __str__(self) -> str:
        return Text_File.object_text["text_style"]