# Dataset passport

The supplied archive `csv.rar` contains three large files named for population/age/sex, births/deaths/urbanization, and migration/fertility/marriage. The archive could not be extracted in this runtime because a RAR5 extraction utility is not available. The project therefore includes **small illustrative synthetic data** in `data/raw/` for test-running the pipeline. Replace these sample CSVs with the original files extracted from your archive before reporting final empirical values.

Illustrative columns (joined by country and year):
- country: country name (text)
- year: year of observation
- population: population count (integer)
- median_age: median age (decimal)
- birth_rate, death_rate: rates (decimal)
- urban_population_pct: urban share, percent
- net_migration: net migration estimate (integer)
- fertility_rate: fertility rate (decimal)
- marriage_rate: marriage rate (decimal)

Sample contains intentionally introduced duplicate, whitespace, and missing-value text to demonstrate cleaning. It is synthetic, not a claim about real demographic statistics.
