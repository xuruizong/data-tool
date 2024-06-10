from doristool.flink.mappings.mysql import MYSQL_TYPE_MAPPING
from doristool.flink.mappings.doris import DORIS_TYPE_MAPPING

def get_type_mapping(db_type,column_type):
    type_mapping = None
    if (db_type == "MYSQL"):
        type_mapping = MYSQL_TYPE_MAPPING
    elif db_type == "DORIS":
        type_mapping = DORIS_TYPE_MAPPING
    else:
        raise ValueError("不支持的数据库类型" + str(column_type))

    if (type(column_type) in type_mapping):
        return type_mapping[type(column_type)]
    else:
        raise ValueError("未知的数据类型" + str(type(column_type)))