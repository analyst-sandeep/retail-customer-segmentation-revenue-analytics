from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"

UCI_XLSX_URL = "https://archive.ics.uci.edu/static/public/352/online+retail.zip"
ZIP_PATH = RAW_DIR / "online_retail.zip"
RAW_XLSX = RAW_DIR / "Online Retail.xlsx"


def download_source_file():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if ZIP_PATH.exists() or RAW_XLSX.exists():
        print("Raw source file already exists. Skipping download.")
        return
    print("Downloading UCI Online Retail dataset...")
    urlretrieve(UCI_XLSX_URL, ZIP_PATH)
    print(f"Downloaded: {ZIP_PATH}")


def extract_zip_if_needed():
    if RAW_XLSX.exists():
        return
    import zipfile

    with zipfile.ZipFile(ZIP_PATH) as zf:
        zf.extractall(RAW_DIR)
    print(f"Extracted source files to: {RAW_DIR}")


def prepare_data():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_excel(RAW_XLSX)

    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    df = df.rename(
        columns={
            "invoiceno": "invoice_no",
            "stockcode": "stock_code",
            "invoicedate": "invoice_date",
            "unitprice": "unit_price",
            "customerid": "customer_id",
        }
    )

    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["customer_id"] = df["customer_id"].astype("Int64")
    df["is_cancellation"] = df["invoice_no"].astype(str).str.startswith("C")
    df["gross_revenue"] = df["quantity"] * df["unit_price"]

    clean = df[
        (df["customer_id"].notna())
        & (df["description"].notna())
        & (df["unit_price"] > 0)
    ].copy()

    clean["order_month"] = clean["invoice_date"].dt.to_period("M").astype(str)
    clean["order_date"] = clean["invoice_date"].dt.date.astype(str)

    positive_sales = clean[(clean["quantity"] > 0) & (~clean["is_cancellation"])].copy()
    snapshot_date = positive_sales["invoice_date"].max() + pd.Timedelta(days=1)

    rfm = (
        positive_sales.groupby("customer_id")
        .agg(
            last_purchase_date=("invoice_date", "max"),
            frequency=("invoice_no", "nunique"),
            monetary_value=("gross_revenue", "sum"),
            total_quantity=("quantity", "sum"),
        )
        .reset_index()
    )
    rfm["recency_days"] = (snapshot_date - rfm["last_purchase_date"]).dt.days
    rfm["r_score"] = pd.qcut(rfm["recency_days"], 5, labels=[5, 4, 3, 2, 1], duplicates="drop")
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["m_score"] = pd.qcut(rfm["monetary_value"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["rfm_score"] = rfm["r_score"].astype(str) + rfm["f_score"].astype(str) + rfm["m_score"].astype(str)

    def segment(row):
        r = int(row["r_score"])
        f = int(row["f_score"])
        m = int(row["m_score"])
        if r >= 4 and f >= 4 and m >= 4:
            return "Champions"
        if r >= 3 and f >= 4:
            return "Loyal Customers"
        if r <= 2 and f >= 3 and m >= 3:
            return "At Risk"
        if r <= 2 and f <= 2:
            return "Hibernating"
        if r >= 4 and f <= 2:
            return "New Customers"
        return "Needs Attention"

    rfm["customer_segment"] = rfm.apply(segment, axis=1)

    monthly = (
        clean.groupby("order_month")
        .agg(
            gross_revenue=("gross_revenue", "sum"),
            invoices=("invoice_no", "nunique"),
            customers=("customer_id", "nunique"),
            units=("quantity", "sum"),
            cancellations=("is_cancellation", "sum"),
        )
        .reset_index()
    )

    clean.to_csv(PROCESSED_DIR / "online_retail_clean.csv", index=False)
    rfm.to_csv(PROCESSED_DIR / "customer_rfm_segments.csv", index=False)
    monthly.to_csv(PROCESSED_DIR / "monthly_revenue_summary.csv", index=False)

    print(f"Rows in cleaned transaction file: {len(clean):,}")
    print(f"Customers in RFM file: {len(rfm):,}")
    print(f"Processed files written to: {PROCESSED_DIR}")


def main():
    download_source_file()
    extract_zip_if_needed()
    prepare_data()


if __name__ == "__main__":
    main()
