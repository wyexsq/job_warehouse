import psycopg2


def transform_ads():
    conn = psycopg2.connect(
        host="localhost",
        database="job_warehouse",
        user="wye",
        password="919630",
    )

    cur = conn.cursor()

    # 先删除旧表，不然嘎嘎报错
    cur.execute("DROP TABLE IF EXISTS ads_top_city , ads_top_education;")

    cur.execute(r"""
        --ADS层
--找到岗位最多的10个城市
create table ads_top_city
as
    SELECT
    city,
    ROUND(avg_mid_salary, 2) AS avg_mid_salary,
    job_stats_count
FROM city_stats
ORDER BY job_stats_count DESC
LIMIT 10;




--按照学历的月薪
create table ads_top_education
as
    SELECT
    education_req,
    ROUND(avg_mid_salary, 2) AS avg_mid_salary,
    job_stats_count
FROM education_stats
ORDER BY job_stats_count DESC
LIMIT 10;""")
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    transform_ads()
