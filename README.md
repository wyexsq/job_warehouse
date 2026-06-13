# job_warehouse

基于招聘数据的四层数据仓库项目

## 项目架构

ODS → DWD → DWS → ADS

- ODS：原始招聘数据，从天池Excel数据集批量导入，保留原始字段不做转换
- DWD：数据清洗层，去除首尾空格，过滤异常薪资，计算月薪中位数
- DWS：按城市、学历聚合统计岗位数量和平均月薪
- ADS：Top10城市岗位排名、各学历薪资对比

## 技术栈

PostgreSQL / Python / pandas / Apache Airflow / WSL/docker

## 调度

Airflow DAG每日定时执行完整流水线，ODS→DWD→DWS→ADS依次重建

## 运行

1. 安装依赖：`pip install pandas psycopg2-binary openpyxl apache-airflow`
2. 初始化数据库：执行 `sql/init_db.sql`
3. 启动Airflow：`airflow standalone`
4. 在Web UI触发DAG：`job_warehouse_pipeline`