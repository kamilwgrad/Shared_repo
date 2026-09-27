"""Generuje surowe CSV z celowymi błędami jakości danych (seed stały = powtarzalne)."""
import csv, random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)
RAW = Path(__file__).parent / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

countries = ["PL", "DE", "CZ", "pl ", "Poland"]  # błąd: niespójne kody krajów
customers = []
for i in range(1, 51):
    customers.append([f"C{i:03d}", f"Klient {i} Sp. z o.o.", random.choice(countries),
                      random.choice(["Retail", "Wholesale", "", "retail"])])  # błąd: puste i różna wielkość liter
customers.append(customers[4])   # błąd: duplikat klienta
customers.append(customers[17])
with open(RAW / "customers.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["customer_id", "customer_name", "country", "segment"]); w.writerows(customers)

products = [["P01", "Karma sucha 10kg", "Pet food", "89.90"], ["P02", "Karma mokra 400g", "Pet food", "7.50"],
            ["P03", "Legowisko L", "Akcesoria", "149,00"],  # błąd: przecinek dziesiętny
            ["P04", "Smycz", "Akcesoria", "39.00"], ["P05", "Witaminy", "Suplementy", ""],  # błąd: brak ceny
            ["P06", "Obroża", "akcesoria", "25.00"]]
with open(RAW / "products.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["product_id", "product_name", "category", "list_price"]); w.writerows(products)

rows, start = [], date(2026, 1, 1)
for i in range(1, 401):
    d = start + timedelta(days=random.randint(0, 240))
    fmt = random.choice(["%Y-%m-%d"] * 8 + ["%d.%m.%Y", "%d/%m/%Y"])  # błąd: mieszane formaty dat
    cust = f"C{random.randint(1, 50):03d}" if random.random() > 0.02 else ""  # błąd: brak klienta
    prod = random.choice(["P01", "P02", "P03", "P04", "P05", "P06", "P99"] if random.random() < 0.02
                         else ["P01", "P02", "P03", "P04", "P05", "P06"])  # błąd: produkt spoza słownika
    qty = random.randint(1, 20) * (-1 if random.random() < 0.03 else 1)  # błąd/korekta: ujemna ilość
    rows.append([f"INV-{i:05d}", d.strftime(fmt), cust, prod, qty, round(random.uniform(5, 150), 2), "PLN"])
rows.append(["INV-00401", "2026-05-14", "C007", "P99", 3, 19.99, "PLN"])  # błąd: produkt spoza słownika (gwarantowany)
rows += random.sample(rows, 8)  # błąd: zduplikowane linie faktur (podwójny load)
with open(RAW / "invoices.csv", "w", newline="") as f:
    w = csv.writer(f); w.writerow(["invoice_id", "invoice_date", "customer_id", "product_id", "quantity", "unit_price", "currency"]); w.writerows(rows)
print("OK:", RAW)
