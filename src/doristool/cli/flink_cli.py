import click
import os

from doristool.flink.config_file import parse
from doristool.db_client import DbClient
from doristool.flink.flink_sql import generate_sql,generate_table_ddl
from doristool.flink.config_file import DbConfig,OutConfig

@click.command(name="fddl", help="生成单表flink DDL")
@click.option('--dbtype',required=True, help='数据库类型 支持MYSQL DORIS')
@click.option('--host',required=True, help='ip 地址')
@click.option('--port',required=True, help='端口')
@click.option('--username',required=True, help='用户名')
@click.option('--password',required=True, help='密码')
@click.option('--database',required=True, help='数据库')
@click.option('--table',required=True, help='密码')
def fddl(dbtype,host,port,username,password,database,table)->None:
    db_client = DbClient(build_url(dbtype,host,port,username,password,database))
    print(generate_table_ddl(dbtype,db_client.get_table(table)))


@click.command(name="flink", help="flink作业脚本生成")
@click.option('--config',required=True, help='配置文件路径')
def flink(config)->None:
    # 解析出配置
    user_config = parse(config)
    
    source_config: DbConfig = user_config[0]
    sink_config: DbConfig = user_config[1]
    out_config:OutConfig = user_config[2]

    source_db_client = DbClient(source_config.url,source_config.pool_timeout)
    sink_db_client = DbClient(sink_config.url,sink_config.pool_timeout)

    for index,table_name in enumerate(source_config.table_names):
        print("正在处理表"+table_name)
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


def build_url(db_type,host,port,username,password,database) -> str:
    if db_type == "MYSQL":
        return "mysql+pymysql://{username}:{password}@{host}:{port}/{database}"\
                .format(username=username,password=password,host=host,port=port,database=database)
    elif db_type == "DORIS":
        return "doris+pymysql://{username}:{password}@{host}:{port}/{database}"\
                .format(username=username,password=password,host=host,port=port,database=database)
    else:
        raise ValueError("不支持的数据库类型:"+db_type)