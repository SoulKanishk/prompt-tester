import sqlite3
from contextlib import contextmanager

DB_PATH = "results.db"

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variant_id TEXT,
                input TEXT,
                output TEXT,
                expected TEXT,
                accuracy REAL,
                latency_ms REAL,
                cost_usd REAL,
                input_tokens INTEGER,
                output_tokens INTEGER,
                model TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def log_result(result: dict):
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO results
            (variant_id, input, output, expected, accuracy,
             latency_ms, cost_usd, input_tokens, output_tokens, model)
            VALUES (:variant_id, :input, :output, :expected, :accuracy,
                    :latency_ms, :cost_usd, :input_tokens, :output_tokens, :model)
        """, result)

def get_summary():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT
                variant_id,
                ROUND(AVG(accuracy) * 100, 1)  AS avg_accuracy,
                ROUND(AVG(latency_ms), 0)       AS avg_latency_ms,
                ROUND(SUM(cost_usd), 5)         AS total_cost,
                COUNT(*)                        AS n_runs
            FROM results
            GROUP BY variant_id
        """).fetchall()
    return [dict(r) for r in rows]