#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
import re

"""Script to generate the Simple MPI Workflow Results.

Note that this is not a copy and paste output. The results were analyzed
individually, because some runners produced a successful run but in reality
were doing `singularity mpirun` instead of `mpirun singularity`.

After this analysis, the table was manually edited to include the IN
(Invalid) results.
"""

LOG_DIR = Path("output")

ANSI_ESCAPE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")

TABLE_CONTAINERS = ["none", "singularity"]
DOCKER_CONTAINER = "docker"

RUNNERS = ["cwltool", "toil"]  # "streamflow" == Does not support the MPIRequirement
PLATFORMS = ["lumi", "mn5", "laptop", "cloud"]  # "ft3" == VPN is offline due to security issues
CONTAINERS = ["none", "docker", "singularity"]
TESTS = [
    ("workflow-base",
     "Simple MPI workflow using \\protect\\textbf{baseCommand: mpirun}. Execution time is shown in seconds. “INVALID” indicates runs where the MPI job was launched via Singularity instead of the host MPI launcher."),
    ("workflow-req",
     "Simple MPI workflow using \\protect\\textbf{code:MPIRequirement}. Execution time is shown in seconds."),
]
PLATFORM_NAMES = {
    "ft3": "FinisTerrae III",
    "lumi": "LUMI",
    "mn5": "MareNostrum 5",
    "laptop": "Laptop",
    "cloud": "Cloud",
}


@dataclass
class Result:
    status: str
    time: float | None
    mode: str | None = None


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

    mode = None

    log_file = base / f"{test}.log"

    if base.name == "singularity":
        mode = detect_singularity_mode(log_file)

    return Result(
        status=status,
        time=t,
        mode=mode,
    )


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
    if status == "1":
        return r"ERROR"
    if status in ("124", "timeout"):
        return "TO"
    if status in ("137", "killed"):
        return "KILLED"
    return status


def cell_value(result):
    if result is None:
        return "--"

    status = fmt_status(result.status)

    # successful but invalid Singularity launch
    if result.status == "0" and result.mode == "invalid":
        status = "INVALID"

    if result.time is None:
        return status

    return f"{status} ({int(round(result.time))})"


def print_runner_table(data, runner, test):
    runner_data = data.get(runner, {})

    print(rf"\textbf{{{runner}}}\\[0.2cm]")

    print(r"\begin{tabular}{|l|c|c|}")
    print(r"\hline")
    print(r"\rowcolor{lightgray!50}")
    print(r"\textbf{System} & \textbf{No Container} & \textbf{Singularity} \\")
    print(r"\hline")

    for platform in PLATFORMS:
        none_result = (
            runner_data
            .get((platform, "none"), {})
            .get(test)
        )

        sing_result = (
            runner_data
            .get((platform, "singularity"), {})
            .get(test)
        )

        print(
            f"{PLATFORM_NAMES.get(platform, platform)} & "
            f"{cell_value(none_result)} & "
            f"{cell_value(sing_result)} \\\\"
        )

    print(r"\hline")
    print(r"\end{tabular}")
    print(r"\\[0.6cm]")


def print_table(data, test, caption):
    print(r"\begin{table}[ht!]")
    print(r"\centering")
    print(r"\renewcommand{\arraystretch}{1.2}")

    for runner in RUNNERS:
        if runner not in data:
            continue

        print_runner_table(data, runner, test)

    print(f"\\caption{{{caption}}}")
    print(r"\label{table:" + test + "}")
    print(r"\end{table}")
    print()


def print_docker_summary(data):
    """The Docker tests always pass, on laptop and cloud. So no point in adding
    these to the table. This function prints the summary to the stdout in the
    command line so that it can be used for reporting."""
    print("\n" + "=" * 80)
    print("DOCKER RESULTS SUMMARY")
    print("=" * 80)

    for test, _ in TESTS:
        print(f"\n[{test}]")

        for runner in RUNNERS:

            runner_data = data.get(runner, {})

            for platform in PLATFORMS:

                result = (
                    runner_data
                    .get((platform, DOCKER_CONTAINER), {})
                    .get(test)
                )

                if result is None:
                    continue

                print(
                    f"{runner:10s} "
                    f"{PLATFORM_NAMES.get(platform, platform):15s} "
                    f"{fmt_status(result.status)}"
                )


def print_latex_tables(data):
    print(r"\documentclass{article}")
    print(r"\usepackage{geometry}")
    print(r"\usepackage[table]{xcolor}")
    print(r"\geometry{margin=1in}")
    print(r"\begin{document}")

    for test, caption in TESTS:
        print_table(data, test, caption)

    print(r"\end{document}")


def detect_singularity_mode(log_file: Path) -> str | None:
    if not log_file.exists():
        return None

    text = log_file.read_text(errors="ignore")
    text = ANSI_ESCAPE.sub("", text)
    lines = text.splitlines()

    commands = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # cwltool and Toil both write logs with [job abc..., then write the command line (multiline)
        if ("[job mpirun" in line or "[job sr-workflow.mpirun" in line) and "$" in line:
            # extract everything after '$'
            cmd = line.split("$", 1)[1].strip()

            i += 1
            while i < len(lines):

                next_line = lines[i]

                # stop if next log event starts, joining all the shell multiline \'s lines
                if next_line.startswith("[") and "]" in next_line and "$" in next_line:
                    break

                # stop if new job starts
                if "[job" in next_line and "$" in next_line:
                    break

                # append continuation lines
                cmd += " " + next_line.strip()

                i += 1

            commands.append(cmd)
            continue

        i += 1

    # Classify only MPI-related commands, looking whether they are using the
    # hybrid/bind mode of Singularity + MPI, or running MPI inside the container
    # (which is not optimised and must be discarded).
    for cmd in commands:
        if "mpirun" not in cmd and "srun" not in cmd:
            continue

        cmd = " ".join(cmd.split())

        has_singularity = "singularity" in cmd
        has_mpi = ("mpirun" in cmd or "srun" in cmd)

        if not has_singularity or not has_mpi:
            continue

        mpi_pos = min(cmd.find("mpirun") if "mpirun" in cmd else float("inf"),
                      cmd.find("srun") if "srun" in cmd else float("inf"))

        sing_pos = cmd.find("singularity")

        if sing_pos < mpi_pos:
            return "invalid"

        if mpi_pos < sing_pos:
            return "hybrid"

    return None


if __name__ == "__main__":
    data = collect()
    print_latex_tables(data)
    print_docker_summary(data)
