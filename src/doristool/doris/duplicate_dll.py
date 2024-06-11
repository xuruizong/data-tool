from doristool.doris.doris_ddl import DorisDDL
from sqlalchemy.sql.schema import Column
from doristool.doris.doris_ddl import comment_escape

class Duplicate(DorisDDL):
    def __init__(self,table_name,table_comment) -> None:
        self._table_name = table_name
        self.columns=[]

        if table_comment != None:
            self._table_comment = comment_escape(table_comment)
        else:
            self._table_comment = None
    
    # 添加字段
    def add_cloumn(self,column: Column) -> None:
        self.columns.append(column)
    
    # 生成DDL
    def to_ddl(self, column_blcok_deal=None)->str:
        # 列模块
        column_block = super().build_column_block(self.columns)
        if column_blcok_deal is not None:
            column_block = column_blcok_deal(column_block)

        ddl = "";
        ddl += "CREATE TABLE IF NOT EXISTS ";
        ddl += self._table_name;
        ddl += "\n"
        ddl += "(\n"
        ddl += column_block
        ddl += "\n"
        ddl += ")\n"

        # 表注释
        if self._table_comment != None:
            ddl += "COMMENT " 
            ddl += "'"
            ddl += self._table_comment
            ddl += "'"
            ddl += "\n"

        ddl += "DISTRIBUTED BY HASH(`"
        ddl += self.columns[0].name
        ddl += "`) BUCKETS 1"
        ddl += "\n"

        ddl += "PROPERTIES ( \n"
        ddl += "\"replication_allocation\" = \"tag.location.default: 1\""
        ddl += ")"
        return ddl;