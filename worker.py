# worker.py
"""
Start the Prefect worker.
Keep this running to execute scheduled flows.
"""
import subprocess


def main():
    print("🔄 Starting Prefect worker...")
    print("Keep this terminal open")
    print("Press Ctrl+C to stop")
    print("-" * 50)

    try:
        subprocess.run(["python", "-m", "prefect", "worker", "start", "--pool", "pool1"])
    except KeyboardInterrupt:
        print("\n👋 Worker stopped")


if __name__ == "__main__":
    main()
