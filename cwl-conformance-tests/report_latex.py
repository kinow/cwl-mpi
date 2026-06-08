#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree

OUTPUT_DIR = Path("output")

RUNNERS = {
    "cwltool": "cwltool",
    "toil": "Toil",
    "streamflow": "StreamFlow",
}

HPCS = ["ft3", "lumi", "mn5"]
# Enforce that all 3 modes must be presented in this exact row order for each HPC
MODES = ["local", "slurm", "batch"]


@dataclass(frozen=True)
class Result:
    passed: int
    failed: int
    skipped: int
    errors: int


AllResultType = dict[str, dict[tuple[str, str, str], Result]]


def parse_junit(xml_path: Path) -> Result:
    tree = ElementTree.parse(xml_path)
    root = tree.getroot()

    testsuite = root.find("testsuite")
    if testsuite is None:
        raise RuntimeError(f"No testsuite in {xml_path}")

    tests = int(testsuite.attrib.get("tests", 0))
    failures = int(testsuite.attrib.get("failures", 0))
    skipped = int(testsuite.attrib.get("skipped", 0))
    errors = int(testsuite.attrib.get("errors", 0))

    passed = tests - failures - skipped - errors

    return Result(passed, failures, skipped, errors)


def collect_results() -> AllResultType:
    results_found: AllResultType = {}

    for runner in RUNNERS:
        results_found[runner] = {}
        runner_dir = OUTPUT_DIR / runner

        if not runner_dir.exists():
            continue

        for hpc_dir in sorted(runner_dir.iterdir()):
            hpc = hpc_dir.name

            for version_dir in sorted(hpc_dir.iterdir()):
                version = version_dir.name

                for mode_dir in sorted(version_dir.iterdir()):
                    mode = mode_dir.name

                    junit = mode_dir / "junit.xml"

                    if junit.exists():
                        result = parse_junit(junit)
                    else:
                        result = Result(0, 0, 0, 0)

                    results_found[runner][(hpc, mode, version)] = result

    return results_found


def print_latex(results_found: AllResultType) -> None:
    print(r"\documentclass{article}")
    print(r"\usepackage{geometry}")
    print(r"\usepackage{array}")
    print(r"\usepackage{multirow}")
    print(r"\usepackage[table]{xcolor}")
    print(r"\usepackage{hhline}")
    print(r"\geometry{margin=1in}")
    print(r"\begin{document}")

    # Map versions
    CWL_VERSIONS = {
        "v1.0": "CWL v1.0.2",
        "v1.1": "CWL v1.1.0",
        "v1.2": "CWL v1.2.1",
    }

    # and HPC names
    HPC_NAMES = {
        "ft3": "FinisTerrae III",
        "lumi": "LUMI",
        "mn5": "MareNostrum 5",
    }

    def cell(r: Result | None) -> tuple[str, str, str]:
        if r is None:
            return ("—", "—", "—")
        return (str(r.passed), str(r.failed), str(r.skipped))

    def success_pct(r: Result | None) -> str:
        if r is None:
            return "—"
        total = r.passed + r.failed + r.skipped
        if total == 0:
            # return "—"
            return "0.0"
        return f"{(r.passed / total) * 100:.1f}"

    for runner_key, runner_name in RUNNERS.items():
        runner_data = results_found.get(runner_key, {})

        print(r"\clearpage")
        print(r"\subsubsection*{" + runner_name + r" Conformance Tests Results}")

        # Build tables per CWL version
        for version_key, version_label in CWL_VERSIONS.items():

            print(r"\begin{table}[ht!]")
            print(r"\centering")
            print(r"\setlength{\tabcolsep}{6pt}")
            print(r"\renewcommand{\arraystretch}{1.2}")

            print(r"\begin{tabular}{|c|c|c|c|c|c|}")
            print(r"\hline")

            # Header
            print(r"\rowcolor{lightgray!50}")
            print(r"\textbf{HPC} & \textbf{Mode} & \textbf{Passed} & \textbf{Failed} & \textbf{Skipped} & \textbf{Success (\%)} \\")
            print(r"\hline")

            for i, hpc in enumerate(HPCS):
                for mode in MODES:

                    rdata = runner_data.get((hpc, mode, version_key))
                    passed, failed, skipped = cell(rdata)
                    pct = success_pct(rdata)
                    if pct == "100.0":
                        pct = r"\textbf{100.0}"
                    hpc_name = HPC_NAMES.get(hpc, hpc.upper())
                    if pct != "—":
                        pct = f"{pct} \%"

                    print(
                        f"{hpc_name} & {mode} & "
                        f"{passed} & {failed} & {skipped} & {pct} \\\\"
                    )

                # visual separator between HPC blocks
                if i < len(HPCS) - 1:
                    print(r"\hline\hline")
                else:
                    print(r"\hline")

            print(r"\end{tabular}")
            print(r"\caption{" + f"{version_label} conformance results on HPC systems." + r"}")
            print(r"\label{tab:" + runner_key + "_" + version_key.replace(".", "") + r"}")
            print(r"\end{table}")

    print(r"\end{document}")


if __name__ == "__main__":
    results = collect_results()
    print_latex(results)
