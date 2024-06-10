from sqlalchemy import create_engine, MetaData,Table
from doristool.flink.mappings.factory import get_type_mapping

# flink sql 语句模板

FLINK_SQL_TEMPLATE = """
{source_table_ddl}

{sink_table_ddl}

"""


# ceate table 语句模板
TABLE_CREATE_DDL_TEMPLATE = """
CREATE TABLE IF NOT EXISTS {table_name} 
{{
    {column_segement}
}}
WITH (
    'connector'='doris'
);
"""

COLUMN_DDL_TEMPLATE = " {name} {column_type} "

def generate_sql(source_db_type:str,source_table: Table, 
                 sink_db_type: str,
                 sink_table:Table)->str:
    
    source_column_segement = build_coumn_segement(source_db_type, source_table.columns)
    sink_column_segement =build_coumn_segement(sink_db_type, sink_table.columns)
    
    source_table_ddl = TABLE_CREATE_DDL_TEMPLATE.format(table_name=source_table.name,
                                                        column_segement=source_column_segement)
    sink_table_ddl = TABLE_CREATE_DDL_TEMPLATE.format(table_name=sink_table.name,
                                                       column_segement=sink_column_segement)


    return FLINK_SQL_TEMPLATE.format(source_table_ddl=source_table_ddl,sink_table_ddl=sink_table_ddl)

def build_coumn_segement(db_type,columns)->str:
    
    segement = ""

    for column in columns:
        column_mapping = get_type_mapping(db_type,column.type)
        segement += COLUMN_DDL_TEMPLATE.format(name=column.name,column_type = column_mapping(column.type))
        segement += ",\n"
    return segement