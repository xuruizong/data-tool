from sqlalchemy import create_engine, MetaData,Table
from sqlalchemy.sql.sqltypes import BOOLEAN

from sqlalchemy.dialects.mysql.types import INTEGER
from sqlalchemy.dialects.mysql.types import TINYINT
from sqlalchemy.dialects.mysql.types import SMALLINT
from sqlalchemy.dialects.mysql.types import MEDIUMINT
from sqlalchemy.dialects.mysql.types import BIGINT
from sqlalchemy.dialects.mysql.types import FLOAT
from sqlalchemy.dialects.mysql.types import DOUBLE
from sqlalchemy.dialects.mysql.types import DECIMAL
from sqlalchemy.sql.sqltypes import NUMERIC

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
from sqlalchemy.sql.sqltypes import BINARY
from sqlalchemy.sql.sqltypes import BLOB
from sqlalchemy.sql.sqltypes import VARBINARY

from sqlalchemy.dialects.mysql.types import BIT

MYSQL_TYPE_MAPPING = {
    
    TINYINT: lambda x: "SMALLINT" if x.unsigned else "SMALLINT",
    SMALLINT: lambda x: "INT" if x.unsigned else "SMALLINT", 
    MEDIUMINT: lambda x: "INT",
    INTEGER: lambda x: "BIGINT" if x.unsigned else "INT",
    BIGINT: lambda x: "DECIMAL(20, 0)" if x.unsigned else "BIGINT",
    FLOAT: lambda x: "FLOAT",
    DOUBLE: lambda x: "DOUBLE",
    NUMERIC: lambda x: "NUMERIC("+x.precision + "," + x.scale + ")",
    DECIMAL: lambda x: "DECIMAL("+x.precision + "," + x.scale + ")",
    BOOLEAN: lambda x: "BOOLEAN",
    DATE: lambda x: "DATE",
    TIME: lambda x: "TIME",
    DATETIME: lambda x: "TIMESTAMP",
    TIMESTAMP: lambda x: "TIMESTAMP",
    CHAR: lambda x: "STRING",
    NCHAR: lambda x: "STRING",
    VARCHAR: lambda x: "STRING",
    NVARCHAR: lambda x: "STRING",
    TINYTEXT: lambda x: "STRING",
    TEXT: lambda x: "STRING",
    MEDIUMTEXT: lambda x: "STRING",
    LONGTEXT: lambda x: "STRING",
    MEDIUMBLOB: lambda x: "BYTES",
    LONGBLOB: lambda x: "BYTES",
    TINYBLOB: lambda x: "BYTES",
    BINARY: lambda x: "BYTES",
    VARBINARY: lambda x: "BYTES",
    BLOB: lambda x: "BYTES"
}

WITH_SEGMENT = """'connector' = 'jdbc',
  'url' = 'jdbc:mysql://localhost:3306/mydatabase',
  'table-name' = '{table_name}',
  'username' = '',
  'password'=''"""

def build_with_segment(table: Table)->str:
    return WITH_SEGMENT.format(table_name=table.name)