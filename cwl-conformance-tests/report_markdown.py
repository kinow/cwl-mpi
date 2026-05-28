#!/usr/bin/env python3

from pathlib import Path
from xml.etree import ElementTree

OUTPUT_DIR = Path("output")

RUNNERS = {
    "cwltool": "cwltool",
    "toil": "Toil",
    "streamflow": "StreamFlow",
}

HPCS = ["ft3", "lumi", "mn5"]

# Enforce all 3 modes are present and in this exact order
MODES = ["local", "slurm", "batch"]

VERSIONS = ["v1.0", "v1.1", "v1.2"]

ResultKey = tuple[str, str, str]
RunnerResults = dict[ResultKey, str]
AllResults = dict[str, RunnerResults]


def status_icon(summary: str) -> str:
    # Handle the new N/A state gracefully with a neutral icon or leave it out if preferred
    if summary == "N/A":
        return "⚪"

    if summary in {"missing", "0P"}:
        return "🔴"

    parts = summary.split(" / ")

    passed = 0
    failures = 0
    errors = 0

    for part in parts:
        if part.endswith("P"):
            passed = int(part[:-1])
        elif part.endswith("F"):
            failures = int(part[:-1])
        elif part.endswith("E"):
            errors = int(part[:-1])

    if passed == 0:
        return "🔴"

    if failures == 0 and errors == 0:
        return "🟢"

    if failures > passed:
        return "🔴"

    return "🟡"


def decorate(summary: str) -> str:
    return f"{status_icon(summary)} {summary}"


def parse_junit(xml_path: Path) -> str:
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

    parts = [f"{passed}P"]

    if failures:
        parts.append(f"{failures}F")

    if skipped:
        parts.append(f"{skipped}S")

    if errors:
        parts.append(f"{errors}E")

    return " / ".join(parts)


def collect_results() -> AllResults:
    results_found: AllResults = {}

    for runner in RUNNERS:
        runner_dir = OUTPUT_DIR / runner

        results_found[runner] = {}

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
                        summary = parse_junit(junit)
                    else:
                        summary = "missing"

                    results_found[runner][(hpc, mode, version)] = summary

    return results_found


def print_markdown_tables(results_found: AllResults) -> None:
    for runner_key, runner_name in RUNNERS.items():
        print(f"# {runner_name}\n")

        print("| HPC | Mode | CWL v1.0 | CWL v1.1 | CWL v1.2 |")
        print("|---|---|---|---|---|")

        runner_data = results_found.get(runner_key, {})

        # Generate structural matrix combinations of all HPCS and MODES deterministic order
        flat_rows = []
        for hpc in HPCS:
            for mode in MODES:
                flat_rows.append((hpc, mode))

        previous_hpc = None

        for hpc, mode in flat_rows:
            # Separation blank row when the cluster context shifts
            if previous_hpc is not None and previous_hpc != hpc:
                print("|  |  |  |  |  |")

            # Look up individual summaries, fallback to "N/A" if key doesn't exist
            v10 = decorate(runner_data.get((hpc, mode, "v1.0"), "N/A"))
            v11 = decorate(runner_data.get((hpc, mode, "v1.1"), "N/A"))
            v12 = decorate(runner_data.get((hpc, mode, "v1.2"), "N/A"))

            # Bolding identifiers to match the structural depth separation style
            print(
                f"| **{hpc.upper()}** | **{mode}** | "
                f"{v10} | {v11} | {v12} |"
            )

            previous_hpc = hpc

        print()
        print("---")
        print()


if __name__ == "__main__":
    results = collect_results()
    print_markdown_tables(results)