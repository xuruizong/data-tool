import click
from doristool.doris_ddl_file import generate_ddl_file

@click.command(name="ddl",help="批量mysql转doris建表脚本")
@click.option('--config',required=True, help='配置文件路径')
def ddl(config) -> None:
    print(config)
    generate_ddl_file(config)