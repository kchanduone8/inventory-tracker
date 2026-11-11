# Relational Inventory Management & Tracking System

A relational data tracking CLI built with Python and SQLite. Implements a 3NF normalized schema to track stock quantities, categories, and inventory alert thresholds.

## Key Features
- **Relational Integrity:** Implements normalized tables with foreign keys to prevent data duplication.
- **SQL Injection Defense:** All queries utilize strict parameterization.
- **Alert Aggregation:** Uses SQL `INNER JOIN` and conditional filtering to isolate supplies below critical reorder limits.

## Usage
```bash
python inventory_app.py
