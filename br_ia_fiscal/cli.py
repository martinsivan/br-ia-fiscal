import typer
from rich.panel import Panel
from .core.validator import NFeValidator

app = typer.Typer(help="br-ia-fiscal: IA para conformidade fiscal brasileira")

@app.command()
def check(file: str, llm: str = "grok"):
    """Valida NF-e com IA"""
    try:
        with open(file, "r", encoding="utf-8") as f:
            xml_content = f.read()
    except FileNotFoundError:
        typer.echo(f"[red]Arquivo não encontrado: {file}[/]")
        raise typer.Exit(1)

    validator = NFeValidator(llm=llm)
    result = validator.analyze(xml_content)

    console = typer.get_console()
    status = "✓ Válida" if result["valida"] else "✗ Inválida"
    color = "green" if result["valida"] else "red"
    console.print(Panel(f"[{color}][bold]{status}[/]", title="NF-e"))
    console.print(result["summary"])

    if result["erros_estrutura"]:
        console.print("\n[red]Erros de XML:[/]")
        for e in result["erros_estrutura"]:
            console.print(f"  • {e['campo']}: {e['mensagem']}")

    if result["sugestoes_ia"]:
        console.print("\n[yellow]Sugestões de IA:[/]")
        for s in result["sugestoes_ia"]:
            console.print(f"  • {s}")

if __name__ == "main":
    app()
