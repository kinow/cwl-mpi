#!/usr/bin/env python3

import sys
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import defaultdict
from ruamel.yaml import YAML

PLATFORMS = ("ft3", "mn5", "lumi")
MODES = ("local", "slurm", "batch")

"""Script used to generate a PDF with several tables.

These tables are used to evaluate the execution of the CWL Conformance Tests
over several HPC platforms."""


def latex_escape(s):
    if s is None:
        return ""

    s = str(s)

    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }

    for k, v in replacements.items():
        s = s.replace(k, v)

    return s


def latex_wrap_identifier(s):
    s = latex_escape(s)
    return r"\seqsplit{" + s + r"}"


def parse(root, specs):
    data = defaultdict(
        lambda: defaultdict(
            lambda: defaultdict(dict)
        )
    )

    for xml_file in root.rglob("junit.xml"):
        parts = xml_file.relative_to(root).parts

        runner = parts[0]

        platform = "unknown"
        mode = "unknown"

        for p in parts:
            p_lower = p.lower()

            if p_lower in PLATFORMS:
                platform = p_lower

            if p_lower in MODES:
                mode = p_lower

        group = mode

        try:
            tree = ET.parse(xml_file)
        except Exception as e:
            print(f"Failed to parse {xml_file}: {e}", file=sys.stderr)
            continue

        for tc in tree.findall(".//testcase"):
            failure = tc.find("failure")
            if failure is None:
                continue

            if runner in ["cwltool", "toil"]:
                name = tc.attrib.get("file", "FAIL_NAME")
            else:
                name = tc.attrib.get("name", "unknown")
            tc_name = tc.attrib.get("name", "unknown")
            desc = get_doc(runner, group, name, tc_name, specs)

            existing = data[runner][platform][mode].get(name)

            if existing is None:
                data[runner][platform][mode][name] = desc
            else:
                if existing == tc_name and desc != tc_name:
                    data[runner][platform][mode][name] = desc

    return data


def print_table(failure_map, caption, label):
    count = len(failure_map)
    full_caption = f"{caption} ({count} unique failure{'s' if count != 1 else ''})"

    print(r"\section*{" + latex_escape(full_caption) + "}")
    print(r"\label{" + label + "}")

    print(r"\begin{longtable}{p{0.35\textwidth} >{\raggedright\arraybackslash}p{0.6\textwidth}}")
    print(r"\toprule")
    print(r"\textbf{ID} & \textbf{Description} \\")
    print(r"\midrule")
    print(r"\endfirsthead")

    print(r"\toprule")
    print(r"\textbf{ID} & \textbf{Description} \\")
    print(r"\midrule")
    print(r"\endhead")

    for test_id in sorted(failure_map.keys()):
        tid = latex_wrap_identifier(test_id)
        desc = latex_escape(failure_map[test_id])
        print(f"{tid} & {desc} \\\\")

    print(r"\bottomrule")
    print(r"\end{longtable}")
    print()


def merge_modes(failure_map, modes):
    merged = {}

    for m in modes:
        if m not in failure_map:
            continue

        for k, v in failure_map[m].items():
            if k not in merged:
                merged[k] = v

    return merged


def mode_sort_key(runner, mode):
    # special rule: toil batch always last
    if runner == "toil" and mode == "batch":
        return (2, mode)

    # everything else normal
    return (0, mode)


def load_specs(spec_path, version):
    if not spec_path:
        return {}

    path = Path(spec_path) / f"v{version}.yaml"
    if not path.exists():
        return {}
    yaml = YAML(typ="safe")
    with open(path, "r") as f:
        data = yaml.load(f)

    lookup = {}
    if not data:
        return lookup
    for entry in data:
        if not isinstance(entry, dict):
            continue

        if version == "1.2":
            key = entry.get("id")
        else:
            key = entry.get("label")

        if key is None:
            continue

        lookup[str(key)] = entry.get("doc")

    return lookup


def get_doc(runner, mode, test_id, tc_name, specs):
    # correct priority:
    # v1.2 → id
    # v1.1 → label
    # v1.0 → label

    key = str(test_id)

    # v1.2 (id-based)
    if key in specs["1.2"]:
        return specs["1.2"][key]

    # v1.1 / v1.0 (label-based)
    if key in specs["1.1"]:
        return specs["1.1"][key]

    if key in specs["1.0"]:
        return specs["1.0"][key]

    return tc_name


def collect_runner_mode(runner_data, mode):
    merged = {}

    for platform in PLATFORMS:
        platform_data = runner_data.get(platform, {})

        if mode not in platform_data:
            continue

        for test_id, desc in platform_data[mode].items():
            merged.setdefault(test_id, desc)

    return merged


def collect_platform_union(runner_data, platform):
    merged = {}

    platform_data = runner_data.get(platform, {})

    for mode in MODES:
        if mode not in platform_data:
            continue

        for test_id, desc in platform_data[mode].items():
            merged.setdefault(test_id, desc)

    return merged


def collect_runner_union(runner_data):
    merged = {}

    for platform in PLATFORMS:
        platform_data = runner_data.get(platform, {})

        for mode in MODES:
            if mode not in platform_data:
                continue

            for test_id, desc in platform_data[mode].items():
                merged.setdefault(test_id, desc)

    return merged


def main():
    if len(sys.argv) not in (2, 3):
        sys.exit(f"usage: {sys.argv[0]} PATH [SPEC_DIR]")

    spec_dir = Path(sys.argv[2]) if len(sys.argv) == 3 else None

    specs = {
        "1.0": load_specs(spec_dir, "v1.0") if spec_dir else {},
        "1.1": load_specs(spec_dir, "v1.1") if spec_dir else {},
        "1.2": load_specs(spec_dir, "v1.2") if spec_dir else {},
    }

    data = parse(Path(sys.argv[1]), specs)

    print(r"\documentclass{article}")
    print(r"\usepackage{longtable}")
    print(r"\usepackage{booktabs}")
    print(r"\usepackage{array}")
    print(r"\usepackage{seqsplit}")
    print(r"\begin{document}")

    # Iterate through runners (cwltool, streamflow, toil)
    first = True

    for runner in sorted(data.keys()):
        if not first:
            print(r"\clearpage")
        first = False

        print(rf"\section*{{{latex_escape(runner)}}}")
        print(r"\addcontentsline{toc}{section}{" + latex_escape(runner) + "}")

        # --------------------------------------------------
        # mode summaries (across all platforms)
        # --------------------------------------------------

        print(r"\subsection*{Mode summaries}")

        for mode in MODES:
            failures = collect_runner_mode(data[runner], mode)

            if failures:
                print_table(
                    failures,
                    f"Failed {runner} tests ({mode} mode)",
                    f"tab:failed_{runner}_{mode}"
                )

        runner_union = collect_runner_union(data[runner])

        if runner_union:
            print_table(
                runner_union,
                f"Failed {runner} tests (all platforms/modes union)",
                f"tab:failed_{runner}_union"
            )

        # --------------------------------------------------
        # platform summaries
        # --------------------------------------------------

        for platform in PLATFORMS:
            platform_data = data[runner].get(platform)

            if not platform_data:
                continue

            print(rf"\subsection*{{{platform.upper()}}}")

            for mode in MODES:
                failures = platform_data.get(mode)

                if failures:
                    print_table(
                        failures,
                        f"Failed {runner} tests on {platform} ({mode} mode)",
                        f"tab:{runner}_{platform}_{mode}"
                    )

            platform_union = collect_platform_union(
                data[runner],
                platform
            )

            if platform_union:
                print_table(
                    platform_union,
                    f"Failed {runner} tests on {platform} (all modes union)",
                    f"tab:{runner}_{platform}_union"
                )

        runner_union = collect_runner_union(data[runner])

        if runner_union:
            print_table(
                runner_union,
                f"Failed {runner} tests (all platforms/modes union)",
                f"tab:failed_{runner}_union"
            )

        # summarize platforms too

        for platform in PLATFORMS:
            platform_data = data[runner].get(platform)

            if not platform_data:
                continue

            print(rf"\subsection*{{{platform.upper()}}}")

            for mode in MODES:
                failures = platform_data.get(mode)

                if failures:
                    print_table(
                        failures,
                        f"Failed {runner} tests on {platform} ({mode} mode)",
                        f"tab:{runner}_{platform}_{mode}"
                    )

            platform_union = collect_platform_union(
                data[runner],
                platform
            )

            if platform_union:
                print_table(
                    platform_union,
                    f"Failed {runner} tests on {platform} (all modes union)",
                    f"tab:{runner}_{platform}_union"
                )

    print(r"\end{document}")


if __name__ == "__main__":
    main()
