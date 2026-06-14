#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path

"""Script to generate the Simple MPI Workflow Results.

Note that this is not a copy and paste output. The results were analyzed
individually, because some runners produced a successful run but in reality
were doing `singularity mpirun` instead of `mpirun singularity`.

After this analysis, the table was manually edited to include the IN
(Invalid) results.
"""

LOG_DIR = Path("output")

RUNNERS = ["cwltool", "streamflow", "toil"]
PLATFORMS = ["ft3", "lumi", "mn5", "laptop", "aws"]
CONTAINERS = ["none", "docker", "singularity"]
TESTS = [
    ("workflow-base",
     "Simple MPI workflow execution results across runners, platforms, and container backends with baseCommand: mpirun (TO: time-out, IN: invalid)"),
    ("workflow-req",
     "Simple MPI workflow execution results across runners, platforms, and container backends with MPIRequirement (TO: time-out, IN: invalid)"),
]
PLATFORM_NAMES = {
    "ft3": "FinisTerrae III",
    "lumi": "LUMI",
    "mn5": "MareNostrum 5",
    "laptop": "Laptop",
    "aws": "AWS",
}


@dataclass
class Result:
    status: str
    time: float | None


def read_result(base: Path, test: str) -> Result | None:
    exit_file = base / f"{test}.exit"
    time_file = base / f"{test}.time"

    if not exit_file.exists():
        return None

    status = exit_file.read_text().strip()

    if time_file.exists():
        try:
            t = float(time_file.read_text().strip())
        except Exception:
            t = None
    else:
        t = None

    return Result(status=status, time=t)


def collect():
    data = {}

    for runner in RUNNERS:
        runner_dir = LOG_DIR / runner
        if not runner_dir.exists():
            continue

        data[runner] = {}

        for platform in runner_dir.iterdir():
            if platform.name not in PLATFORMS:
                continue

            for container in platform.iterdir():
                if container.name not in CONTAINERS:
                    continue

                key = (platform.name, container.name)
                data[runner][key] = {}

                for f in container.glob("*.exit"):
                    test = f.stem
                    data[runner][key][test] = read_result(container, test)

    return data


# -----------------------------
# LaTeX printing
# -----------------------------

def fmt_time(t):
    if t is None:
        return "—"
    return f"{t:.1f}"


def fmt_status(status):
    if status == "0":
        return r"\textbf{OK}"
    if status in ("124", "timeout"):
        return "TO"
    if status in ("137", "killed"):
        return "KILLED"
    return status


def print_table(data, test, caption):
    print(r"\begin{table}[ht!]")
    print(r"\centering")
    print(r"\setlength{\tabcolsep}{6pt}")
    print(r"\renewcommand{\arraystretch}{1.2}")
    print(r"\begin{tabular}{|c|c|c|c|c|}")
    print(r"\hline")
    print(r"\rowcolor{lightgray!50}")
    print(
        r"\textbf{Runner} & "
        r"\textbf{HPC} & "
        r"\textbf{Container} & "
        r"\textbf{Status} & "
        r"\textbf{Time (s)} \\"
    )
    print(r"\hline")

    first_runner = True

    for runner in RUNNERS:

        if runner not in data:
            continue

        if not first_runner:
            print(r"\hline\hline")

        first_runner = False

        runner_data = data[runner]

        for platform in PLATFORMS:
            for container in CONTAINERS:

                result = (
                    runner_data
                    .get((platform, container), {})
                    .get(test)
                )

                if result is None:
                    continue

                status = fmt_status(result.status)
                time = fmt_time(result.time)

                print(
                    f"{runner} & "
                    f"{PLATFORM_NAMES.get(platform, platform)} & "
                    f"{container} & "
                    f"{status} & "
                    f"{time} \\\\"
                )

    print(r"\hline")
    print(r"\end{tabular}")
    print(f"\\caption{{{caption}}}")
    print(r"\end{table}")
    print()


def print_latex_tables(data):
    print(r"\documentclass{article}")
    print(r"\usepackage{geometry}")
    print(r"\usepackage[table]{xcolor}")
    print(r"\geometry{margin=1in}")
    print(r"\begin{document}")

    for test, caption in TESTS:
        print_table(data, test, caption)

    print(r"\end{document}")


if __name__ == "__main__":
    data = collect()
    print_latex_tables(data)
