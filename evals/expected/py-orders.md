# Answer key – py-orders (Python, tests present)

Test command: `python -m unittest discover -s tests -t .` (6 tests, all green).

## Patterns – expected verdict
| Element | Where | Expected verdict |
|---|---|---|
| `PaymentFactory` | shop/payments.py | **Name only** (static simple factory, one product); **Over-engineered** is also accepted. Remedy: Inline Method / call the constructor, or inject the payment. Must not propose Abstract Factory. |
| `ConfigManager.get_instance()` | shop/config.py | **Misapplied Singleton**: mutable global state (`orders_count` incremented by `process`), tests interfere with each other. Severity High or Medium. Remedy: pass config/counter explicitly. |

## Expected smells (pass: at least 6 of 8)
| Smell | Where | Severity | Expected technique |
|---|---|---|---|
| Long Method | `OrderProcessor.process` (~80 lines, section comments) | High | Extract Method per section (validate, subtotal, discount, shipping, tax, invoice) |
| Switch Statements repeated on `customer_type` | `process` (discount, shipping) + `estimated_days` | High | Replace Type Code with State/Strategy or Subclasses → Replace Conditional with Polymorphism (or a map of functions/classes per type, idiomatic in Python) |
| Primitive Obsession | `customer_type` string; money as float; `item` as dict | Medium | Replace Type Code with Class (Enum), Replace Array/dict with Object (`LineItem` dataclass) |
| Data Clumps | `street, city, zip_code, country` | Medium | Extract Class `Address` (+ Move Method of `shipping_label`) |
| Magic numbers | `0.22`, `0.05`, `0.10`, `500`, `20`, `7.5`, `12`, `2.5` | Low/Medium | Replace Magic Number with Symbolic Constant |
| Feature Envy | `shipping_label`, invoice address line | Low/Medium | Move Method to `Address`/`Customer` |
| Long Parameter List / boolean flags | `process(customer, items, coupon, express, gift_wrap)` | Low | Introduce Parameter Object, or leave it (acceptable) |
| Temporary Field | `last_invoice` used as an output channel | Low | Separate Query from Modifier / return the invoice |

Bonus (not in the original key, found by agents and confirmed): a small order with coupon
`WELCOME10` gets a negative taxable amount and negative tax (a €5 item costs €1.40). It must be
reported as a bug / behavior change, not fixed inside a refactoring step.

## Expected pattern opportunities
- **Strategy** (or polymorphism on customer type) for discount/shipping/delivery days: justified
  because the same switch is duplicated in 3 places. "Enum + table of functions/dataclasses" is
  also accepted.
- Coupon: small switch, must **not** get a pattern (Extract Method at most).

## Expected behavior in Fix mode
1. Finds the test command and runs it before starting (green baseline).
2. Shows an ordered plan (Extract Method/constants first, then Address, then polymorphism on the
   type) and **stops to wait for approval**.
3. Re-runs the tests after every step; the totals (312.5, 259.5, 622.2, 315.00) do not change.
4. Does not touch files outside the perimeter when the perimeter is `shop/orders.py`; flags
   `config.py` as "outside scope".

## Penalize
- Proposing Abstract Factory/Builder/Observer without a concrete problem.
- Changing totals, invoice text or exception types.
- Doing everything in one step, or editing code before approval.
