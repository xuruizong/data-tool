from sqlalchemy.sql.schema import Column

from sqlalchemy.sql.schema import Column

from sqlalchemy.dialects.mysql.types import INTEGER
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.dialects.mysql.types import SMALLINT
from sqlalchemy.dialects.mysql.types import MEDIUMINT
from sqlalchemy.dialects.mysql.types import BIGINT
from sqlalchemy.dialects.mysql.types import FLOAT
from sqlalchemy.dialects.mysql.types import DOUBLE
from sqlalchemy.dialects.mysql.types import DECIMAL

from sqlalchemy.sql.sqltypes import DATE
from sqlalchemy.dialects.mysql.types import DATETIME
from sqlalchemy.dialects.mysql.types import TIMESTAMP
from sqlalchemy.dialects.mysql.types import YEAR
from sqlalchemy.dialects.mysql.types import TIME

from sqlalchemy.dialects.mysql.types import CHAR
from sqlalchemy.dialects.mysql.types import NCHAR
from sqlalchemy.dialects.mysql.types import VARCHAR
from sqlalchemy.dialects.mysql.types import NVARCHAR

from sqlalchemy.dialects.mysql.types import TINYTEXT
from sqlalchemy.dialects.mysql.types import TEXT
from sqlalchemy.dialects.mysql.types import MEDIUMTEXT
from sqlalchemy.dialects.mysql.types import LONGTEXT

from sqlalchemy.dialects.mysql.types import MEDIUMBLOB
from sqlalchemy.dialects.mysql.types import LONGBLOB
from sqlalchemy.dialects.mysql.types import TINYBLOB

from sqlalchemy.dialects.mysql.types import BIT

# 注释转义处理
def comment_escape(comment:str) -> None:
    # 单引号转义
    return comment.replace("'","''")

# 构建行表达式  `ID` VARCHAR(65533) NOT NULL COMMENT '主键'
def build_cloumn_segment(column: Column)->str:
    column_segment = "    "

    # 构建列名
    column_segment += "`" 
    column_segment += column.name 
    column_segment +=  "` " 
    # 构建类型
    column_segment += trans_column_type(column.type)
    # 是否非空
    if column.nullable != None and not column.nullable:
            column_segment += " NOT NULL "

    # 列注释
    if (column.comment != None):
        column_segment += " COMMENT "
        column_segment += "'"
        column_segment += comment_escape(column.comment)
        column_segment += "'"
    column_segment += ",\n"
    return column_segment

# 列类型转化
def trans_column_type(column_type) -> str:
    if (isinstance(column_type, INTEGER)):
        if column_type.unsigned:
            return "BIGINT"
        else:
            return "INT"
    if (isinstance(column_type, TINYINT)):
        if column_type.unsigned:
            return "SMALLINT"
        else:
            return "TINYINT"
    if (isinstance(column_type, SMALLINT)):
        if column_type.unsigned:
            return "MEDIUMINT"
        else:
            return "SMALLINT"
    if (isinstance(column_type, MEDIUMINT)):
        if column_type.unsigned:
            return "INT"
        else:
            return "MEDIUMINT"
    if (isinstance(column_type, BIGINT)):
        if column_type.unsigned:
            return "LARGEINT"
        else:
            return "BIGINT"
    
    if (isinstance(column_type, FLOAT)):
        return "FLOAT"
    if (isinstance(column_type, DOUBLE)):
        return "DOUBLE"
    if (isinstance(column_type, DECIMAL)):
        if column_type.unsigned:
            return "DECIMAL(" + str(column_type.precision + 1) + "," + str(column_type.scale) + ")"
        else:
            return "DECIMAL(" + str(column_type.precision) + "," + str(column_type.scale) + ")"
    
    if (isinstance(column_type, DATE)):
        return "DATE"
    if (isinstance(column_type, DATETIME)):
        return "DATETIME"
    if (isinstance(column_type, TIMESTAMP)):
        return "DATETIME"
    if (isinstance(column_type, TIME)):
        return "STRING"
    if (isinstance(column_type, YEAR)):
        return "SMALLINT"
    
    if (isinstance(column_type, CHAR)):
        return "CHAR(" + str(column_type.length) + ")";
    if (isinstance(column_type, VARCHAR)):
        return "VARCHAR(" + str(column_type.length * 3) + ")";
    if (isinstance(column_type, NCHAR) or
        isinstance(column_type, NVARCHAR)):
        return "STRING"

    if (isinstance(column_type, TINYTEXT) or 
        isinstance(column_type, TEXT) or 
        isinstance(column_type, MEDIUMTEXT) or
        isinstance(column_type, LONGTEXT) or
        isinstance(column_type, MEDIUMBLOB) or
        isinstance(column_type, LONGBLOB) or
        isinstance(column_type, TINYBLOB)):
        return "STRING"
    
    if (isinstance(column_type, BIT)):
        if column_type.length == 1:
            return "BOOLEAN"
        else:
            return "STRING"

    raise ValueError("未知的数据类型:"+ str(column_type) + str(type(column_type)))

class DorisDDL:
    # 生成ddl语句
    # @param column_blcok_deal 字段块处理函数
    def to_ddl(self,column_blcok_deal)->str:
        pass

    def add_cloumn(self,column: Column) -> None:
        pass

    def build_column_block(self,columns)-> str:
        column_block = ""
        for column in columns:
            column_block += build_cloumn_segment(column)
        return column_block