import time
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMPOSE_FILE = ROOT / "code" / "deployment" / "docker-compose.yml"


def run_stage(name, command):
    print(f"\n--- Running: {name} ---")

    try:
        subprocess.run(command, check=True)
        print(f"[{name}] Completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"[{name}] ERROR: {e}")
        raise


def automate_pipeline():
    run_stage(
        "Stage 1 & 2: DVC Data & Model Pipeline",
        ["dvc", "repro"],
    )

    run_stage(
        "Stage 3: Deployment",
        [
            "docker",
            "compose",
            "-f",
            str(COMPOSE_FILE),
            "up",
            "--build",
            "-d",
        ],
    )

    run_stage(
        "Reload trained model",
        [
            "docker",
            "compose",
            "-f",
            str(COMPOSE_FILE),
            "restart",
            "fastapi",
        ],
    )


if __name__ == "__main__":
    while True:
        print(
            f"\n[{time.strftime('%H:%M:%S')}] "
            "Starting new pipeline cycle"
        )

        try:
            automate_pipeline()
            print("\nPipeline cycle completed successfully!")
        except Exception as e:
            print(f"\nPipeline stopped due to an error: {e}")

        print("Waiting 5 minutes before the next run\n")
        time.sleep(300)