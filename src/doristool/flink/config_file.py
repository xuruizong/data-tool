import json
from doristool.flink.config_file import DbConfig

# 从配置文件中解析出配置信息
def parse(config_file_path)->tuple:
    json_obj = None
    with open(config_file_path,"r",encoding='utf-8') as file:
        json_obj = json.load(file)
    
    source_config = None
    sink_config = None
    out_config = None

    if "source" in json_obj:
        source_obj = json_obj['source']
        source_config = parse_db_config(source_obj)
    else:
        raise ValueError("source 配置不能为空")
    
    if "sink" in json_obj:
        sink_obj = json_obj['sink']
        sink_config = parse_db_config(sink_obj)
    else:
        raise ValueError("sink 配置不能为空")
    
    if (len(source_config.table_names) 
            != len(sink_config.table_names)):
        raise ValueError("输入和输出的表名个数必须相等")
    
    if "out" in json_obj:
        out_obj = json_obj['out']
        out_config = OutConfig(out_obj['out_path'])
    
    return(source_config,sink_config,out_config)

def parse_db_config(config_json_obj)-> DbConfig:
    if "pool_timeout" in config_json_obj:
        return DbConfig(config_json_obj['url'],
                                config_json_obj['table_names'],
                                config_json_obj["pool_timeout"])
    else:
        return DbConfig(config_json_obj['url'],
                                config_json_obj['table_names'])

class DbConfig:
    def __init__(self,_url,_table_names:list,_pool_timeout=10) -> None:
        self.url=_url,
        self.table_names = _table_names
        self.pool_timeout = _pool_timeout

class OutConfig:
    def __init__(self, _out_path) -> None:
        self.out_path = _out_path

