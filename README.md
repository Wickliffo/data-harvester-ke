# 📊 Kenyan Market Data Explorer

An end-to-end data engineering and analytics project that harvests, cleans, and visualizes multi-source market data across Kenya (Real Estate, E-Commerce, and Social Media trends). Built using **Scrapy**, **Pandas**, and **Streamlit**.

![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)
![Scrapy](https://img.shields.io/badge/Scrapy-Web%20Scraper-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 🚀 Features

* **Automated Web Harvesting (Scrapy):** Crawls target sites to extract raw unstructured data on properties, products, and social discussions.
* **Data Transformation & Cleaning (Pandas):** Normalizes messy strings, strips currency symbols (`KSh`), handles missing values, and casts data types for numeric filtering.
* **Interactive Dashboard (Streamlit):** 
  * Multi-category filtering (Property, E-commerce, Social Media).
  * Dynamic price range sliders.
  * Clickable external source links.
* **Data Export:** Instant CSV export options for filtered datasets.

---

## 🛠️ Tech Stack

* **Language:** Python 3.12
* **Scraper Framework:** Scrapy
* **Data Processing:** Pandas, JSON
* **Dashboard / UI:** Streamlit

---

## 📁 Project Structure

```text
data-harvester/
│
├── data_harvester/               # Scrapy project root
│   ├── spiders/                  # Web scrapers (properties, ecommerce, reddit)
│   ├── streamlit_app/            # Streamlit dashboard application
│   │   └── app.py                # Main UI execution script
│   ├── items.py                  # Scrapy data models
│   ├── middlewares.py            # Scrapy middlewares
│   ├── pipelines.py              # Data export/handling pipelines
│   └── settings.py               # Scraper configuration settings
│
├── properties.json               # Harvested real estate data
├── ecommerce.json                # Harvested e-commerce product data
├── reddit_interests.json         # Harvested social media trend data
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
git clone [https://github.com/Wickliffo/kenya-market-data-explorer.git](https://github.com/Wickliffo/kenya-market-data-explorer.git)
cd kenya-market-data-explorer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run data_harvester/data_harvester/streamlit_app/app.py
