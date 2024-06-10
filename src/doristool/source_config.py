class SourceConfig:
    def __init__(self,url, table_names, pool_timeout: float) -> None:
        self._url=url
        self._table_names=table_names
        self._pool_timeout = pool_timeout