import logging

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_ods():
    df = pd.read_excel(
        "/mnt/c/Users/27533/Desktop/job_warehouse/f56253b9bbcb1edffb1b2d233d35e24f.xlsx"
    )
    df.columns = df.columns.str.strip()

    df = df.rename(
        columns={
            "数据来源": "source_cat",
            "数据源": "source_cat",
            "公司位置": "city",
            "公司分级": "company_grade",
            "公司名称": "company_name",
            "公司规模": "company_size",
            "公司部门": "department",
            "公司阶段": "company_stage",
            "学历要求": "education_req",
            "岗位分类": "job_category",
            "岗位名称": "job_title",
            "岗位类型": "job_type",
            "岗位要求": "job_req",
            "岗位诱惑": "job_perks",
            "平均年薪": "avg_annual_sal",
            "所处行业": "industry",
            "最低月薪": "salary_min",
            "最高月薪": "salary_max",
        }
    )

    cols = [
        "source_cat",
        "city",
        "company_grade",
        "company_name",
        "company_size",
        "department",
        "company_stage",
        "education_req",
        "job_category",
        "job_title",
        "job_type",
        "job_req",
        "job_perks",
        "avg_annual_sal",
        "industry",
        "salary_min",
        "salary_max",
    ]

    records = [
        tuple(None if pd.isna(v) else str(v) for v in row)
        for row in df[cols].itertuples(index=False)
    ]

    conn = psycopg2.connect(
        host="localhost", database="job_warehouse", user="wye", password="919630"
    )
    cur = conn.cursor()
    execute_batch(
        cur,
        """
        INSERT INTO ods_job_raw
        (source_cat,city,company_grade,company_name,company_size,
         department,company_stage,education_req,job_category,job_title,
         job_type,job_req,job_perks,avg_annual_sal,industry,salary_min,salary_max)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """,
        records,
    )
    conn.commit()
    logging.info(f"成功导入 {len(records)} 条数据")
    cur.close()
    conn.close()


if __name__ == "__main__":
    load_ods()
