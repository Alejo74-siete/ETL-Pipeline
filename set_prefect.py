# setup.py
"""
One-time setup for Prefect.
Run this once to configure everything.
"""
import subprocess


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    try:
        subprocess.run(cmd, check=True, shell=True)
        print(f"✅ {description} complete")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {description} failed")
        return False


def main():
    print("🚀 Setting up Prefect for Production ETL")
    print("=" * 50)

    # Ask user preference
    print("\nChoose Prefect backend:")
    print("1. Local server (simpler, for development)")
    print("2. Prefect Cloud (better for production)")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "2":
        print("\n📱 Setting up Prefect Cloud...")
        print("You'll need to:")
        print("1. Sign up at https://app.prefect.cloud")
        print("2. Get your API key")
        run_command("prefect cloud login", "Prefect Cloud login")
    else:
        print("\n🖥️  Using local Prefect server")
        print("Starting server in background...")
        print("UI will be at: http://localhost:4200")
        subprocess.Popen(["prefect", "server", "start"])
        import time

        time.sleep(5)

    # Create work pool
    run_command(
        "prefect work-pool create default --type process",
        "Creating work pool",
    )

    # Deploy
    run_command("prefect deploy --all", "Deploying flows")

    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\nNext steps:")
    print("1. Start worker: python worker.py")
    print("2. View UI: http://localhost:4200 (or Prefect Cloud)")
    print("3. Test run: python run.py")


if __name__ == "__main__":
    main()
