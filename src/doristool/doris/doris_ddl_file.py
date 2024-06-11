from doristool.doris.config_file import parse_json
from doristool.doris.config_file import parse_sink_config
from doristool.doris.config_file import parse_source_config
from doristool.common.db_client import DbClient
from doristool.doris.unique_ddl import UniqueDDL
from doristool.doris.duplicate_dll import Duplicate
from doristool.doris.sink_config import SinkConfig

def generate_ddl_file(config_file) -> None:
    json_obj = parse_json(config_file)
    source_conifg = parse_source_config(json_obj['source'])
    sink_config = parse_sink_config(json_obj['sink'])

    db_client = DbClient(source_conifg._url,
                         source_conifg._pool_timeout)

    # 生成ddl
    ddl = genrate_ddl(source_conifg._table_names,
                      db_client,sink_config)
    # ddl输出到文件
    out_to_file(ddl,sink_config._out_path)

# 生成ddl
def genrate_ddl(table_names, db_client:DbClient, sink_config:SinkConfig) -> str:
    ddl=""

    for table_name in table_names:
        print("正在处理表" + table_name)   
        table_ddl = genrate_ddl_table(table_name, db_client,sink_config)
        ddl += table_ddl
        ddl += ";"
        ddl += "\n\n"
    return ddl
        

def genrate_ddl_table(table_name, db_client:DbClient,sink_config:SinkConfig) -> str:
    # 获取表对象
    table = db_client.get_table(table_name)
    # 获取主键字段
    primary_keys = [column.name for column in table.primary_key.columns]
    # 获取表注释
    table_comment = table.comment

    sink_table_name = sink_config._prefix + table_name


    doris_ddl = None
    if len(primary_keys) > 0 :
        doris_ddl = UniqueDDL(sink_table_name,primary_keys,table_comment)
    else:
        doris_ddl = Duplicate(sink_table_name,table_comment)

    
    # 获取字段信息
    for column in table.columns:
        doris_ddl.add_cloumn(column)

    if sink_config.has_add_columns():
        ddl_segment=add_columns_ddl_segment(sink_config._add_columns)
        return doris_ddl.to_ddl(column_blcok_deal=lambda x: x+ddl_segment)
    else:
        return doris_ddl.to_ddl()


def add_columns_ddl_segment(add_columns)->str:
    ddl_segment=""
    for column in add_columns:
        ddl_segment += "    "
        ddl_segment += column
        ddl_segment += ","
        ddl_segment += "\n"
    return ddl_segment

def out_to_file(ddl, file_path)-> None:
    with open(file_path, "w") as f:
        f.write(ddl)
