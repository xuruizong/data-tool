from sqlalchemy.sql.sqltypes import BOOLEAN
from sqlalchemy.sql.sqltypes import VARCHAR
from sqlalchemy.sql.sqltypes import CHAR
from sqlalchemy.sql.sqltypes import TEXT
from sqlalchemy.sql.sqltypes import String

from sqlalchemy.sql.sqltypes import DATETIME
from sqlalchemy.sql.sqltypes import DATE

from sqlalchemy.sql.sqltypes import INT
from sqlalchemy.sql.sqltypes import SMALLINT
from sqlalchemy.sql.sqltypes import BIGINT
from pydoris.sqlalchemy.datatype import TINYINT
from pydoris.sqlalchemy.datatype import LARGEINT

from pydoris.sqlalchemy.datatype import DOUBLE
from sqlalchemy.sql.sqltypes  import DECIMAL
from sqlalchemy.sql.sqltypes import FLOAT

from sqlalchemy.sql.sqltypes import JSON

from sqlalchemy import Table


DORIS_TYPE_MAPPING = {
    BOOLEAN: lambda x: "BOOLEAN",
    VARCHAR: lambda x: "STRING",
    CHAR: lambda x: "STRING",
    TEXT: lambda x: "STRING",
    String: lambda x: "STRING",
    
    DATETIME: lambda x: "TIMESTAMP",
    DATE: lambda x: "DATE",

    TINYINT: lambda x: "TINYINT",
    INT: lambda x: "INT",
    SMALLINT: lambda x: "INT",
    BIGINT: lambda x: "BIGINT",
    LARGEINT: lambda x: "STRING",

    DOUBLE: lambda x: "DOUBLE",
    DECIMAL: lambda x: "DECIMAL",
    FLOAT: lambda x: "FLOAT",

    JSON: lambda x: "STRING",
}


WITH_SEGMENT = """'connector' = 'doris',
  'fenodes' = '10.223.225.164:8030,10.223.225.54:8030',
  'username' = '',
  'password' = '',
  'table.identifier' = '{table_full_name}',
  'sink.label-prefix' = '{label}', """

def build_with_segment(table: Table)->str:
    return WITH_SEGMENT.format(table_full_name=table.fullname,
                               label=table.name + "label_1")