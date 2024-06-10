import click

from doristool.flink.config_file import parse
from doristool.db_client import DbClient

@click.command(name="flink")
@click.option('--config',required=True, help='source config file path')
def flink(config)->None:
    # 解析出配置
    user_config = parse(config)
    
    source_config = user_config[0]
    sink_config = user_config[1]
    out_config = user_config[2]

    source_db_client = DbClient(source_config.url,source_config.pool_timeout)
    sink_db_client = DbClient(sink_config.url,sink_config.pool_timeout)

    for table_name in source_config.table_names:
        source_table = source_db_client.get_table(table_name)
        sink_table = sink_db_client.get_table(table_name)
