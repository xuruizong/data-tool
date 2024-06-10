from doristool.doris_ddl import DorisDDL
from sqlalchemy.sql.schema import Column
from doristool.doris_ddl import comment_escape

class UniqueDDL(DorisDDL):
    def __init__(self,table_name,primary_keys: list,table_comment) -> None:
        self._primary_keys = primary_keys
        self._table_name = table_name
        self.columns=[]

        if table_comment != None:
            self._table_comment = comment_escape(table_comment)
        else:
            self._table_comment = None
    
    # 添加字段
    def add_cloumn(self,column: Column) -> None:
        try:
            # 插入的同时进行排序 保证主键字段在最前面
            index = self._primary_keys.index(column.name)
            self.columns.insert(index,column)
        except ValueError:
            # 不是主键字段直接追加到最后面
            self.columns.append(column)
        
    # 生成DDL
    def to_ddl(self,column_blcok_deal=None)->str:
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
        # 键
        ddl += "UNIQUE KEY"
        ddl += self.unique_key()
        ddl += "\n";
        # 表注释
        if self._table_comment != None:
            ddl += "COMMENT " 
            ddl += "'"
            ddl += self._table_comment
            ddl += "'"
            ddl += "\n"

        ddl += "DISTRIBUTED BY HASH(`"
        ddl += self._primary_keys[0]
        ddl += "`) BUCKETS 1"
        ddl += "\n"

        ddl += "PROPERTIES ( \n"
        ddl += "\"replication_allocation\" = \"tag.location.default: 1\",\n"
        ddl += "\"enable_unique_key_merge_on_write\" = \"true\"\n"
        ddl += ")"
        return ddl;
    
    def unique_key(self)->str:
        sql_segment = "("
        for index,key in enumerate(self._primary_keys):
            sql_segment = sql_segment + "`" + key + "`"
            if index != len(self._primary_keys) -1:
                sql_segment += ","
        sql_segment += ")"
        return sql_segment

    