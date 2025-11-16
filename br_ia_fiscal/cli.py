import typer
from rich.console import Console
from .core.validator import NFeValidator

app = typer.Typer()
console = Console()

@app.command()
def validar(arq: str):
    validator = NFeValidator()
    result = validator.validate(arq)
    console.print(f"[green]Válida![/]" if result["valida"] else "[red]Inválida[/]")
    for s in result["sugestoes_ia"]:
        console.print(f"[yellow]• {s}[/]")
