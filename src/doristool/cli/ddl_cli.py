import click
from doristool.doris_ddl_file import generate_ddl_file

@click.command(name="ddl")
@click.option('--config',required=True, help='source config file path')
def ddl(config) -> None:
    print(config)
    generate_ddl_file(config)