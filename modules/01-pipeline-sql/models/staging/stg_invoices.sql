-- typy, parsowanie mieszanych formatów dat, usunięcie podwójnego loadu
select distinct
    invoice_id,
    coalesce(try_strptime(invoice_date, '%Y-%m-%d'),
             try_strptime(invoice_date, '%d.%m.%Y'),
             try_strptime(invoice_date, '%d/%m/%Y'))::date as invoice_date,
    nullif(trim(customer_id), '')                          as customer_id,
    trim(product_id)                                       as product_id,
    cast(quantity as integer)                              as quantity,
    cast(unit_price as decimal(10, 2))                     as unit_price,
    cast(quantity as integer) * cast(unit_price as decimal(10, 2)) as net_amount,
    currency
from raw_invoices
