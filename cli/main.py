import click
from sputnik.engine import Sputnik
from sputnik.parser import Parser


@click.group()
def cli():
    click.echo("======================================")
    click.echo(" Sputnik -- The FHE assembly language ")
    click.echo("======================================\n\n")

@cli.command()
@click.argument('sputnik_filepath')
def run(sputnik_filepath, **kwargs):
    """
    Executes the Sputnik program file at the given path.
    """
    click.echo("Executing Sputnik program...")
    # TODO: Bootstrapping key input

    SputnikParser = Parser(sputnik_filepath)
    program = SputnikParser.get_program()

    sputnik_execution_engine = Sputnik(program, None)
    output = sputnik_execution_engine.execute_program(**kwargs)

    click.echo("Execution complete! Final Status:")
    click.echo("Execution killed?  {}".format(program.is_killed))
    click.echo("Execution halted?  {}\n\n".format(program.is_halted))
    click.echo("Final State or State Machine Output:")
    click.echo(output)


if __name__ == '__main__':
    cli()
