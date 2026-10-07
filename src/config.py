from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
SIMULATED = ROOT / "data" / "simulated"
MODELS = ROOT / "models"
LOGS = ROOT / "logs"

SEED = 42
START = "2015-01-01 06:00:00"
END = "2016-01-01 06:00:00"
N_MACHINES = 100
