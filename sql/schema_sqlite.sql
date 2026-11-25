-- Demonstration schema. The pipeline creates a flexible demographics table.
CREATE TABLE IF NOT EXISTS demographics (
  country TEXT,
  year INTEGER,
  population INTEGER,
  median_age REAL,
  birth_rate REAL,
  death_rate REAL,
  urban_population_pct REAL,
  net_migration INTEGER,
  fertility_rate REAL,
  marriage_rate REAL
);
CREATE INDEX IF NOT EXISTS idx_demographics_year ON demographics(year);
CREATE INDEX IF NOT EXISTS idx_demographics_country_year ON demographics(country, year);
