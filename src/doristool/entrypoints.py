import click
import doristool as doristool_package
from doristool.cli.ddl_cli import ddl
from doristool.cli.flink_cli import flink



@click.group()
@click.version_option(
    version=doristool_package.nice_version_name(),
    prog_name=doristool_package.__package_name__,
)
def doristool()-> None:
    pass

# 命令组中添加命令
doristool.add_command(ddl)
doristool.add_command(flink)


def main(**kwargs):
    doristool()