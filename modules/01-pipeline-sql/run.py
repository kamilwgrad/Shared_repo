"""Minimalny pipeline: CSV -> DuckDB (raw) -> staging -> marts -> testy.
To, co robimy tu ręcznie (kolejność, zależności, testy), później zastąpi dbt."""
import sys
from pathlib import Path
import duckdb

ROOT = Path(__file__).parent
DB = ROOT / "warehouse.duckdb"
# Kolejność ma znaczenie: marts zależą od staging. dbt wylicza to sam z ref().
MODELS = ["staging/stg_invoices"]  # TODO (zadanie): dodaj pozostałe modele w dobrej kolejności

TESTS = {
    # TODO (zadanie): brak NULL w kluczach, unikalność klucza wymiaru, reconciliation sum staging vs fact
    "stg_invoices: brak zduplikowanych linii":
        "select count(*) from (select invoice_id from stg_invoices group by 1 having count(*) > 1)",
}

def main() -> int:
    con = duckdb.connect(str(DB))
    for name in ["customers", "products", "invoices"]:
        # all_varchar: raw trzymamy jako tekst, typy nadajemy świadomie w staging
        con.execute(f"create or replace table raw_{name} as "
                    f"select * from read_csv('{ROOT / 'data/raw' / name}.csv', header=true, all_varchar=true)")
    for model in MODELS:
        sql = (ROOT / "models" / f"{model}.sql").read_text()
        con.execute(f"create or replace table {Path(model).name} as {sql}")
        print(f"built {model}: {con.execute(f'select count(*) from {Path(model).name}').fetchone()[0]} rows")
    failed = 0
    for name, sql in TESTS.items():
        bad = con.execute(sql).fetchone()[0]
        print(f"[{'FAIL' if bad else 'PASS'}] {name}")
        failed += bool(bad)
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
