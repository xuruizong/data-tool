from sqlalchemy import create_engine, MetaData,Table


def generate_sql(source_table: Table, 
                 sink_table:Table)->str:
    pass