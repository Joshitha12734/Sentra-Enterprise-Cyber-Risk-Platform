import os

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

NVD_PATH = os.path.join(
    BASE_DIR,
    "Data",
    "nvdcve-2.0-2025.json"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "Outputs"
)

ENGINE_VERSION = "1.0.0"
RULESET_VERSION = "2025.01"