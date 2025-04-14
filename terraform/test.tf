resource "snowflake_database" "test_db" {
  name    = "TF_TEST_DB"
  comment = "Temp test db"
}
