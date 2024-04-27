if __name__ != "__main__":
    exit(0)

import subprocess
experiments = ["custom_providers", "depth_opt_custom_providers", 
                "fake_providers", "draw_all_5_topologies", 
                "single_custom_provider", "specific_fake_providers"]
running = []
for experiment in experiments:
    print(f"Started {experiment}")
    process = subprocess.Popen(["./venv/Scripts/python", "-m", f"source.experiments.{experiment}"], stdout=subprocess.DEVNULL)
    running.append((experiment, process))

for experiment, process in running:
    exit_code = process.wait()
    print(f"{experiment} done with code: {exit_code}")