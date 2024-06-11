# data-tool

#### 介绍
data-tool是一个数据开发中常用的一些工具集，主要功能如下：
1. 生成mysql到doris表结构迁移脚本
2. flinksql 作业脚本生成

#### 安装教程

``` bash
    pip install data-tool
```

#### 使用说明
1. 生成mysql到doris表结构迁移脚本批量生成
生成命令

```bash
    doristool ddl --config=配置文件完整路径
```
配置文件样例
```json
{
    "source": {
        "url": "mysql+pymysql://root:***@127.0.0.1:3306/test",
        "table_names":["user_info","mssq_item_version"],
        "pool_timeout": 1000
    },
    "sink": {
        "out_file":"/home/wangzhen/workspace/doris-tools/out/ddl.sql",
        "prefix":"ods_tymh_sys_",
        "add_columns":[
            " `_delete_flag` INT NULL DEFAULT \"0\"",
            "`_update_time` DATETIME NULL DEFAULT CURRENT_TIMESTAMP"
        ]
    }
}
```

``` bash
    doristool fddl --dbtype=MYSQL --host=*** --port=3306 --username=root --password=*** --database=test --table=mssq_item_version
```
