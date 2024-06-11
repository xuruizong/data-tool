class SinkConfig:
    def __init__(self,out_path,prefix,add_columns=None) -> None:
        self._out_path=out_path
        self._prefix=prefix
        self._add_columns=add_columns
    
    def has_add_columns(self)->bool:
        if self._add_columns is not None and len(self._add_columns) > 0:
            return True;
        else:
            return False