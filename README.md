# 🚀 Real-Time Fraud Analytics Cloud Pipeline

A cloud-native data pipeline that ingests transaction data from Kaggle, transforms it using Apache Spark, stores it in Snowflake, and analyzes it to detect fraudulent activity — all orchestrated with Apache Airflow.

---

## 📌 Project Objective

To automate fraud detection using real-time analytics with a cloud-based ETL pipeline:

- Ingestion of Kaggle fraud transaction data to AWS S3  
- Cleans and transforms data using PySpark  
- Batch ingestion of transformed data into Snowflake 
- Executes analytical SQL queries to extract fraud insights
- Infrastructure provisioned using Terraform   
- Fully automated via Apache Airflow

---

## ⚙️ Tech Stack

- **Orchestration**: Apache Airflow  
- **Storage**: AWS S3  
- **Processing**: PySpark  
- **Data Warehouse**: Snowflake  
- **Ingestion**: Python (Boto3, Pandas, Kaggle API)  
- **Infrastructure-as-Code**: Terraform  
- **Other**: SQL, Git

---

## 📂 Project Structure

```
fraud-analytics-pipeline/
├── spark_jobs/
│   └── transform_fraud_data.py        # PySpark transformation script
├── ingestion/
│   └── batch_ingestion.py             # Load transformed data to Snowflake
├── terraform/
│   └── snowflake_resources.tf         # Snowflake DB/table setup
├── sql/
│   └── fraud_insights.sql             # SQL analytics queries
├── requirements.txt
└── README.md
```

---

## 🧱 Architecture

```
Kaggle ➝ S3 ➝ PySpark ➝ Cleaned Data ➝ Snowflake ➝ SQL Queries ➝ Fraud Insights
            ↑                                           ↓
         Orchestrated end-to-end using Apache Airflow
```

---

## ✅ Completed Steps

1. **Data Ingestion to S3:**  
   - Downloaded fraud transactions dataset from Kaggle using the Kaggle API  
   - Uploaded raw CSV data to AWS S3

2. **Transformation with PySpark:**  
   - Loaded raw CSV data from S3  
   - Casted numeric fields (`amount`, `distance_from_home`, `velocity_last_hour`)  
   - Parsed timestamps into proper datetime format  
   - Casted `is_fraud` and `transaction_hour` as integer types  
   - Saved the cleaned data back to S3


3. **Infrastructure Provisioning with Terraform:**  
   - Created Snowflake database, schema, and `FRAUD_TRANSACTIONS` table  
   - Configured access roles and warehouse

4. **Batch Ingestion to Snowflake:**  
   - Loaded transformed CSV data from S3 to Snowflake using Python + Snowflake connector  
   - Verified data types and row integrity  

5. **SQL Analytics in Snowflake:**  
   - Ran fraud detection queries to derive insights  

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/fraud-analytics-pipeline.git
cd fraud-analytics-pipeline
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Add the following to your `.env` or export directly in your shell:

```bash
# Snowflake
export SNOWFLAKE_ACCOUNT=your_account
export SNOWFLAKE_USER=your_user
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_WAREHOUSE=your_warehouse

# AWS
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### 4. Start Airflow (via Docker)

```bash
docker-compose up -d
```

Then open [http://localhost:8080](http://localhost:8080) to access the Airflow UI.

---

## 🔁 DAG Workflow

1. **Download Kaggle Data** → Upload to S3  
2. **PySpark Transformation**  
3. **Batch Ingestion to Snowflake**  
4. **Run SQL Transformations and Insights**

---

### 📊 Example Fraud Insights

- 💯 Total number of transactions processed  
- ⚠️ Fraud rate as a percentage of overall transactions  
- 🏪 Top 10 merchant categories most associated with fraud  
- 🌍 Countries with the highest volume of fraudulent activity  
- 🚩 High-risk merchants with elevated fraud counts  
- 🕒 Hours of the day with the most fraud occurrences  

---

## 📈 Improvements Coming

- Kafka for real-time streaming  
- ML models for fraud prediction  
- Streamlit dashboard integration  
- Unit tests and CI/CD with GitHub Actions  

---

## 👤 Author

**Mairo Gospel**  
Data Engineer | DevOps | Cloud-Native Analytics

---

## 📝 License

This project is licensed under the MIT License.

graph LR
    A[Kaggle API] --> B(AWS S3 Bucket);
    B --> C{PySpark Transformation};
    C --> D(Transformed Data in S3);
    E[Terraform Configuration] --> F(Snowflake Database/Schema/Table);
    D --> G(Python Batch Ingestion Script);
    G --> F;
    F --> H{SQL Analytics in Snowflake};
    I[Airflow DAG] --> A;
    I --> C;
    I --> E;
    I --> G;
    I --> H;
    H --> J{Fraud Pattern Insights};
    J --> K[Reporting/Visualization];
    L[Real-time Data Stream (Future)] --> M(Kafka/Simulated Events);
    M --> N{Streaming Data Processing (Future)};
    N --> F;
    I --> L;

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#ccf,stroke:#333,stroke-width:2px
    style C fill:#9cf,stroke:#333,stroke-width:2px
    style D fill:#ccf,stroke:#333,stroke-width:2px
    style E fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#bbf,stroke:#333,stroke-width:2px
    style G fill:#f9f,stroke:#333,stroke-width:2px
    style H fill:#bbf,stroke:#333,stroke-width:2px
    style I fill:#ff9,stroke:#333,stroke-width:2px
    style J fill:#bbf,stroke:#333,stroke-width:2px
    style K fill:#ccf,stroke:#333,stroke-width:2px
    style L fill:#ddd,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    style M fill:#ddd,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5
    style N fill:#ddd,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5

    subgraph Data Ingestion
        direction LR
        A -- Download --> B
    end

    subgraph Data Processing
        direction LR
        B -- Raw Data --> C
        C -- Transformed Data --> D
    end

    subgraph Infrastructure
        direction TB
        E -- Provisions --> F
    end

    subgraph Batch Ingestion
        direction TB
        D -- Reads --> G
        G -- Loads --> F
    end

    subgraph Analytics
        direction LR
        F -- Queries --> H
        H -- Insights --> J
    end

    subgraph Orchestration
        direction TB
        I -- Orchestrates --> Data Ingestion
        I -- Orchestrates --> Data Processing
        I -- Orchestrates --> Infrastructure
        I -- Orchestrates --> Batch Ingestion
        I -- Orchestrates --> Analytics
    end

    subgraph Future Real-time Streaming
        direction LR
        L -- Receives --> M
        M -- Processes --> N
        N -- Ingests --> F
    end
