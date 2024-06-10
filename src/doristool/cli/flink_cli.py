import click
import os

from doristool.flink.config_file import parse
from doristool.db_client import DbClient
from doristool.flink.flink_sql import generate_sql
from doristool.flink.config_file import DbConfig,OutConfig

@click.command(name="flink")
@click.option('--config',required=True, help='source config file path')
def flink(config)->None:
    # 解析出配置
    user_config = parse(config)
    
    source_config: DbConfig = user_config[0]
    sink_config: DbConfig = user_config[1]
    out_config:OutConfig = user_config[2]

    source_db_client = DbClient(source_config.url,source_config.pool_timeout)
    sink_db_client = DbClient(sink_config.url,sink_config.pool_timeout)

    for index,table_name in enumerate(source_config.table_names):
        source_table = source_db_client.get_table(table_name)
        sink_table_name = sink_config.table_names[index]
        sink_table = sink_db_client.get_table(sink_table_name)
        flink_sql =generate_sql(source_config.db_type,source_table,
                            sink_config.db_type,sink_table)
        out_to_file(flink_sql,table_name,out_config.out_path)

def out_to_file(flink_sql,table_name,path):
    file_path=os.path.join(path,table_name+".sql")
    with open(file_path, "w") as f:
        f.write(flink_sql)
