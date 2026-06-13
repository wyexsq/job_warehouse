import psycopg2


def transform_dws():
    conn = psycopg2.connect(
        host="localhost",
        database="job_warehouse",
        user="wye",
        password="919630",
    )

    cur = conn.cursor()

    # 先删除旧表，不然嘎嘎报错
    cur.execute("DROP TABLE IF EXISTS city_stats ,education_stats ,industry_stats;")

    cur.execute(r"""
        --按照城市分组，求城市的平均月薪和岗位，北京遥遥领先
create table city_stats as
    select
        city,
        avg(cast(salary_mid as numeric)) as avg_mid_salary,
        count(*) as job_stats_count
from dwd_job_clean
where
    city is not null
group by city
order by job_stats_count;

--接下来是按照不同学历要求分组，要求每一个学历只有一行，统计岗位数量和月薪均值
create table education_stats as
       select
           education_req,
           round(avg(cast(salary_mid as numeric)),2 )as avg_mid_salary,
           count(*) as job_stats_count
from dwd_job_clean
group by education_req
order by job_stats_count;


--最后一个是按照行业划分，这个数据特别乱，先看看具体情况
SELECT DISTINCT industry
FROM dwd_job_clean
WHERE industry IS NOT NULL
ORDER BY industry;""")
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    transform_dws()
