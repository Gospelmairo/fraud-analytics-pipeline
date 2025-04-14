resource "snowflake_database" "fraud_db" {
  name    = "FRAUD_ANALYTICS"
  comment = "Database for Real-Time Fraud Insights"



}

resource "snowflake_schema" "raw_schema" {
  name     = "RAW"
  database = snowflake_database.fraud_db.name
  comment  = "Raw data schema for fraud transactions"
  depends_on = [snowflake_database.fraud_db]  # ✅ ensures DB is created first

}

resource "snowflake_table" "fraud_table" {
  name     = "FRAUD_TRANSACTIONS"
  database = snowflake_database.fraud_db.name
  schema   = snowflake_schema.raw_schema.name
  comment  = "Table to store raw fraud transaction data"

  column {
    name = "transaction_id"
    type = "STRING"
  }
  column {
    name = "customer_id"
    type = "STRING"
  }
  column {
    name = "card_number"
    type = "STRING"
  }
  column {
    name = "timestamp"
    type = "TIMESTAMP_NTZ"
  }
  column {
    name = "merchant_category"
    type = "STRING"
  }
  column {
    name = "merchant_type"
    type = "STRING"
  }
  column {
    name = "merchant"
    type = "STRING"
  }
  column {
    name = "amount"
    type = "FLOAT"
  }
  column {
    name = "currency"
    type = "STRING"
  }
  column {
    name = "country"
    type = "STRING"
  }
  column {
    name = "city"
    type = "STRING"
  }
  column {
    name = "city_size"
    type = "STRING"
  }
  column {
    name = "card_type"
    type = "STRING"
  }
  column {
    name = "card_present"
    type = "BOOLEAN"
  }
  column {
    name = "device"
    type = "STRING"
  }
  column {
    name = "channel"
    type = "STRING"
  }
  column {
    name = "device_fingerprint"
    type = "STRING"
  }
  column {
    name = "ip_address"
    type = "STRING"
  }
  column {
    name = "distance_from_home"
    type = "FLOAT"
  }
  column {
    name = "high_risk_merchant"
    type = "BOOLEAN"
  }
  column {
    name = "transaction_hour"
    type = "INTEGER"
  }
  column {
    name = "weekend_transaction"
    type = "BOOLEAN"
  }
  column {
    name = "velocity_last_hour"
    type = "INTEGER"
  }
  column {
    name = "is_fraud"
    type = "BOOLEAN"
  }
}
