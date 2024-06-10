from doristool.source_config import SourceConfig
from doristool.sink_config import SinkConfig
import json

def parse_json(file_path) -> json:
    with open(file_path,'r', encoding='utf-8') as file:
       return json.load(file)
    
def parse_source_config(json_obj) -> SourceConfig:
    pool_timeout = 10
    if "pool_timeout" in json_obj:
        pool_timeout = json_obj['pool_timeout']
    print("超时时间:" + str(pool_timeout))
    source_config = SourceConfig(json_obj['url']
                                 ,json_obj['table_names']
                                 ,pool_timeout)
    return source_config

def parse_sink_config(json_obj) -> SinkConfig:
    sink_config=SinkConfig(json_obj['out_file']
                           ,json_obj['prefix']
                           ,json_obj['add_columns'])
    return sink_config