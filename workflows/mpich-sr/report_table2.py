#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path

LOG_DIR = Path("output")

RUNNERS = ["cwltool", "streamflow", "toil"]
PLATFORMS = ["ft3", "lumi", "mn5", "laptop", "aws"]
CONTAINERS = ["none", "docker", "singularity"]


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


def fmt_status(s):
    if s == "0":
        return "OK"
    if s == "timeout":
        return "TO"
    if s == "killed":
        return "KILLED"
    return s


def print_latex_single_table(data):
    print(r"\documentclass{article}")
    print(r"\usepackage{booktabs}")
    print(r"\usepackage{geometry}")
    print(r"\geometry{margin=1in}")
    print(r"\begin{document}")

    print(r"\begin{table}[ht!]")
    print(r"\centering")
    print(r"\begin{tabular}{llllcc}")
    print(r"\toprule")
    print(r"Runner & HPC & Container & Test & Status & Time (s) \\")
    print(r"\midrule")

    for runner, runner_data in sorted(data.items()):

        for (platform, container), tests in sorted(runner_data.items()):

            for test, result in sorted(tests.items()):

                if result is None:
                    continue

                status = result.status
                if status == "0":
                    status = "OK"
                elif status == "124":
                    status = "TO"
                elif status == "137":
                    status = "KILLED"

                time = "—" if result.time is None else f"{result.time:.1f}"

                print(
                    f"{runner} & "
                    f"{platform} & "
                    f"{container} & "
                    f"{test} & "
                    f"{status} & "
                    f"{time} \\\\"
                )

    print(r"\bottomrule")
    print(r"\end{tabular}")
    print(r"\caption{HPC workflow execution results across runners, platforms, and container backends.}")
    print(r"\end{table}")

    print(r"\end{document}")


if __name__ == "__main__":
    data = collect()
    print_latex_single_table(data)
