from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
INTERIM = ROOT / 'data' / 'interim'
PROCESSED = ROOT / 'data' / 'processed'
DATASETS = [
 '1_датасет_население_возраст_и_пол.csv',
 '2_датасет_рождаемость_смертность_урбанизация.csv',
 '3_датасет_миграция_фертильность_брачность.csv'
]
for p in (RAW, INTERIM, PROCESSED): p.mkdir(parents=True, exist_ok=True)
