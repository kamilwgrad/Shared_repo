# Moduł 01 — Pipeline SQL: raw → staging → marts

## Sytuacja biznesowa

Dział controllingu firmy sprzedającej produkty dla zwierząt dostaje co miesiąc eksport z trzech systemów: faktury, klienci, produkty. Dziś ktoś ręcznie czyści to w Excelu, a dashboard sprzedaży **nie zgadza się z raportem finansowym**. Masz zbudować powtarzalny pipeline i model, któremu finanse uwierzą.

Nikt nie powiedział ci, co w danych jest nie tak. To część zadania.

## Uruchomienie

Środowisko zarządzamy przez [uv](https://docs.astral.sh/uv/) (instalacja: `curl -LsSf https://astral.sh/uv/install.sh | sh`). Zależności są w `pyproject.toml` w głównym katalogu repo.

```bash
uv sync                          # raz, w głównym katalogu repo
cd modules/01-pipeline-sql
uv run python generate_data.py   # tworzy data/raw/*.csv
uv run python run.py
```

Nowa biblioteka: `uv add <nazwa>` (nie `pip install`), żeby trafiła do `pyproject.toml` i `uv.lock`.

## Zadanie

W swoim repo portfolio, na branchu `modul-01`:

1. **Zanim otworzysz AI:** przejrzyj CSV i wypisz w `DECISIONS.md` wszystkie problemy jakości danych, które widzisz. Potem zapytaj AI i porównaj — co ono znalazło, a ty nie, i odwrotnie.
2. Dokończ modele: `stg_customers`, `stg_products`, `dim_customer`, `dim_product`, `fct_sales`. Dopisz je do `MODELS` w `run.py`.
3. Dodaj testy w `run.py`: brak NULL w kluczach faktu, unikalność klucza wymiaru, **zgodność sumy kwot między staging a fact** (reconciliation — robiłeś to przy migracji Oracle → BigQuery).
4. `DECISIONS.md`: minimum 4 decyzje wg [szablonu](../../docs/jak-pracujemy.md#szablon-decisionsmd). Musi być w nich co najmniej jedna decyzja, która **nie jest techniczna, tylko biznesowa**.
5. Minimum 3 commity, potem Pull Request do `main` w swoim portfolio. Review: Monika (`pinsleepe`).

## Pytania na obronę (przygotuj się, bez AI)

- Jaki jest grain `fct_sales`? Skąd wiesz?
- Co się stanie z fakturą, której klienta nie ma w słowniku? Dlaczego tak?
- Finanse mówią, że sprzedaż za maj jest o 2% za wysoka. Gdzie szukasz najpierw?
- Czemu raw trzymamy jako tekst?
