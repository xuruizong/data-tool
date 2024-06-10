from sqlalchemy import create_engine, MetaData,Table

class DbClient:
    def __init__(self,url,pool_timeout) -> None:
        self.engine=create_engine(url=url,pool_timeout=pool_timeout)
        self.metadata = MetaData()

    # 根据表名称获取表信息
    def get_table(self, table_name) -> Table:
        return Table(table_name, self.metadata, autoload_with=self.engine)
    