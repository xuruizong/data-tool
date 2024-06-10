from sqlalchemy import create_engine, MetaData,Table
from doristool.flink.mappings.factory import get_type_mapping
from doristool.flink.mappings.factory import build_with_segment

# flink sql 语句模板

FLINK_SQL_TEMPLATE = """
{source_table_ddl}

{sink_table_ddl}

{insert_dml}
"""


# ceate table 语句模板
TABLE_CREATE_DDL_TEMPLATE = """
CREATE TABLE IF NOT EXISTS `{table_name} `
{{
  {column_segement}
}}
WITH (
  {with_segment}
);
"""

COLUMN_DDL_TEMPLATE = " `{name}` {column_type} "

def generate_sql(source_db_type:str,source_table: Table, 
                 sink_db_type: str,
                 sink_table:Table)->str:
    
    source_column_segement = build_coumn_segement(source_db_type, source_table.columns)
    sink_column_segement =build_coumn_segement(sink_db_type, sink_table.columns)

    source_with_segment = build_with_segment(source_db_type,source_table);
    sink_with_segment = build_with_segment(sink_db_type,sink_table);
    
    source_table_ddl = TABLE_CREATE_DDL_TEMPLATE.format(table_name=source_table.name,
                                                        column_segement=source_column_segement,
                                                        with_segment=source_with_segment)
    sink_table_ddl = TABLE_CREATE_DDL_TEMPLATE.format(table_name=sink_table.name,
                                                       column_segement=sink_column_segement,
                                                       with_segment=sink_with_segment)
    
    insert_dml = build_insert_dml(source_table,
                                  sink_table)

    return FLINK_SQL_TEMPLATE.format(source_table_ddl=source_table_ddl
                                     ,sink_table_ddl=sink_table_ddl,
                                     insert_dml=insert_dml)

def build_coumn_segement(db_type,columns)->str:
    
    segement = "" 

    for column in columns:
        column_mapping = get_type_mapping(db_type,column.type)
        segement +="  "
        segement += COLUMN_DDL_TEMPLATE.format(name=column.name,column_type = column_mapping(column.type))
        segement += ",\n"
    return segement

INSERT_DML_TEMPLATE="""insert into `{sink_table_name}` ({column_names})
select {column_names} 
from `{source_table_name}`
"""

def build_insert_dml(source_table: Table,sink_table: Table) -> str:
    source_column_names = list(map(lambda x: str(x.name).casefold(),source_table.columns))
    sink_column_names = list(map(lambda x: str(x.name).casefold(),sink_table.columns))

    common_names=list(set(source_column_names).intersection(sink_column_names))

    colums_segment = ",".join(list(map(lambda x: "`"+x+"`",common_names)))

    return INSERT_DML_TEMPLATE.format(sink_table_name=sink_table.name,
                                      column_names=colums_segment,
                                      source_table_name=source_table.name)

