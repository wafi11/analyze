# 📊 Sales Data Analysis & Visualization Tool

A Python-based data processing tool designed to analyze retail transaction data (Global Superstore dataset) using **DuckDB** for high-performance SQL querying and **Matplotlib** for automated dashboard reporting.

## 🚀 Features

- **SQL on CSV**: Utilizing DuckDB to run complex analytical queries directly on CSV files.
- **Data Normalization**: Logic to handle currency formatting (commas) and correct discount math.
- **Automated Dashboard**: Generates a multi-chart visual report (`dashboard_report.png`).
- **Modular Structure**: Clean separation between database config, queries, and visualization services.

## 📁 Project Structure

```bash
.
├── config/             # Database connection & configurations
├── data/               # Source data (CSV files)
├── migrations/         # SQL migration scripts for DB setup
├── services/
│   ├── query.py        # Core analytical SQL logic
│   └── visualization.py # Matplotlib dashboard generation
├── main.py             # Application entry point
├── requirements.txt    # Project dependencies
└── readme.md           # Project documentation
```

````

## 🛠️ Technical Stack

- **Language**: Python 3.x
- **Query Engine**: DuckDB
- **Data Manipulation**: Pandas
- **Visualization**: Matplotlib
- **Database (Optional)**: PostgreSQL (via psycopg2)

## 📊 Key Metrics Analyzed

1. **User Discounts**: Identifying customers receiving the highest total discounts.
2. **Top Spenders**: Ranking customers by total sales volume.
3. **Logistics Analysis**: Shipping cost distribution by Country and State.
4. **Product Pricing**: Calculating original unit price from discounted sales data.
5. **Nominal Discount**: Calculating the actual currency value saved by customers.

## ⚙️ Setup & Installation

1. **Activate Virtual Environment**:

```bash
source .venv/bin/activate

```

2. **Install Dependencies**:

```bash
pip install -r requirements.txt

```

3. **Run Analysis**:

```bash
python main.py

```

## 📈 Output Example

The tool generates a `dashboard_report.png` containing:

- Horizontal Bar Charts for Customer rankings.
- Vertical Bar Charts for Regional shipping costs.
- Trend Analysis for Product categories.

---

_Developed by Wafi - Software Developer & Data Analyst Enthusiast._

```

```
````
