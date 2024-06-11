# data-tool

#### 介绍
data-tool是一个数据开发中常用的一些工具集，主要功能如下：
1.生成mysql到doris表迁移脚本
2.flinksql 作业脚本生成

#### 安装教程

``` bash
    pip install data-tool
```

#### 使用说明

``` bash
    doristool fddl --dbtype=MYSQL --host=*** --port=3306 --username=root --password=*** --database=test --table=mssq_item_version
```
