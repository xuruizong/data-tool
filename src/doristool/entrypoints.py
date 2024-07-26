import click
import doristool as doristool_package
from doristool.cli.ddl_cli import ddl
from doristool.cli.flink_cli import fddl
from doristool.cli.flink_cli import flink
from doristool.cli.date_cli import generate



@click.group()
@click.version_option(
    version=doristool_package.nice_version_name(),
    prog_name=doristool_package.__package_name__,
    help = "查看版本号"
)
@click.help_option(help="查看帮助信息")
def doristool()-> None:
    pass

# 命令组中添加命令
doristool.add_command(fddl)
doristool.add_command(ddl)
doristool.add_command(flink)
doristool.add_command(generate)


def main(**kwargs):
    doristool()