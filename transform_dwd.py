import psycopg2

def transform_dwd():
    conn = psycopg2.connect(
        host="localhost",
        database="job_warehouse",
        user="wye",
        password="919630",
    )

    cur = conn.cursor()

    # 先删除旧表，不然嘎嘎报错
    cur.execute("DROP TABLE IF EXISTS dwd_job_clean;")


    cur.execute(r"""
        --因为文本有问题，首位有空格，所以先清洗干净，然后不同平台的薪资范围设置有问题，单位有问题，想办法统一，而且有的最小值比最大值还大，数据有问题影响后续DWS层
CREATE TABLE dwd_job_clean AS
SELECT
    id,
    TRIM(source_cat)     AS source_cat,
    TRIM(city)           AS city,
    TRIM(company_grade)  AS company_grade,
    TRIM(company_name)   AS company_name,
    TRIM(company_size)   AS company_size,
    TRIM(company_stage)  AS company_stage,
    TRIM(education_req)  AS education_req,
    TRIM(job_category)   AS job_category,
    TRIM(job_title)      AS job_title,
    TRIM(industry)       AS industry,
    COALESCE(CAST(NULLIF(TRIM(salary_min), '') AS NUMERIC), 0) AS salary_min,
    COALESCE(CAST(NULLIF(TRIM(salary_max), '') AS NUMERIC), 0) AS salary_max,
    ROUND(
        (COALESCE(CAST(NULLIF(TRIM(salary_min), '') AS NUMERIC), 0) +
         COALESCE(CAST(NULLIF(TRIM(salary_max), '') AS NUMERIC), 0)) / 2, 1
    ) AS salary_mid,
    CAST(avg_annual_sal AS NUMERIC) AS avg_annual_sal,
    load_time
FROM ods_job_raw
WHERE
    -- 至少有一个薪资字段有有效数字（或者 avg_annual_sal 有效，可根据需要调整）
    (salary_min ~ '^\d+(\.\d+)?$' OR salary_max ~ '^\d+(\.\d+)?$')
    AND avg_annual_sal ~ '^\d+(\.\d+)?$'
    -- 对非 NULL 的原始值进行范围检查（NULL 不参与，因为已转为 0 但原始是 NULL 视为通过）
    AND (salary_min IS NULL OR CAST(salary_min AS NUMERIC) BETWEEN 1 AND 200)
    AND (salary_max IS NULL OR CAST(salary_max AS NUMERIC) BETWEEN 1 AND 300)
    -- 如果两个原始值都存在，则必须满足 min < max；否则（有任一为 NULL）跳过该条件
    AND (salary_min IS NULL OR salary_max IS NULL
         OR CAST(salary_min AS NUMERIC) < CAST(salary_max AS NUMERIC));"""
    )
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    transform_dwd()
