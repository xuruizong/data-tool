from sqlalchemy import create_engine, MetaData,Table
from doristool.flink.mappings.mysql import MYSQL_TYPE_MAPPING,build_with_segment as mysql_build_with_segment
from doristool.flink.mappings.doris import DORIS_TYPE_MAPPING,build_with_segment as doris_build_with_segment

def build_with_segment(db_type,table: Table)->str:
    if (db_type == "MYSQL"):
        return mysql_build_with_segment(table)
    elif db_type == "DORIS":
        return doris_build_with_segment(table)
    else:
        raise ValueError("不支持的数据库类型" + str(db_type))


def get_type_mapping(db_type,column_type):
    type_mapping = None
    if (db_type == "MYSQL"):
        type_mapping = MYSQL_TYPE_MAPPING
    elif db_type == "DORIS":
        type_mapping = DORIS_TYPE_MAPPING
    else:
        raise ValueError("不支持的数据库类型" + str(db_type))

    if (type(column_type) in type_mapping):
        return type_mapping[type(column_type)]
    else:
        raise ValueError("未知的数据类型" + str(type(column_type)))