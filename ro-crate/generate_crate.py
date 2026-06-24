# SPDX-License-Identifier: CC-BY-4.0
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0)
# https://creativecommons.org/licenses/by/4.0/

from pathlib import Path

import mimetypes
from contextlib import suppress
from datetime import UTC, datetime
from rocrate.model.contextentity import ContextEntity
from rocrate.model.dataset import Dataset
from rocrate.model.person import Person
from rocrate.rocrate import ROCrate
from ruamel.yaml import YAML
from shutil import move
from tempfile import TemporaryDirectory

"""Generate an RO-Crate metadata JSON-LD file for the thesis dataset.

Part of the data (licence, author, etc.) are retrieved from the CITATION.cff
file to avoid duplicating the information elsewhere. The citation file is
loaded as a YAML by ruamel.yaml.
"""

_ROOT = Path(__file__).resolve().parents[1]
"""Path to store the RO-Crate metadata file, and where to find the dataset files."""

_YAML = YAML(typ="safe")
"""ruamel.yaml object."""

_INCLUDED_DIRS = [
    "bibliography",
    "containers",
    "examples",
    "images",
    "cwl-conformance-tests",
    "workflows"
]
"""What directories are included. These directories have certain expected files/content."""


def _parse_cwl(path: Path) -> tuple[list[str], list[str]]:
    """Parse CWL to find out its RO-Crate entity type.

    A .cwl file may be a CWL Workflow, a CWL tool, or a file used in StreamFlow.

    This function is not perfect, sorry. But I hope it gives future-users
    a way to parse the content more easily and re-use the data in future
    analyses.

    Augments it with:
        additional_types
        referenced_cwl_files
    """
    try:
        data = _YAML.load(path.read_text())
    except Exception:
        return [], []

    if not isinstance(data, dict):
        return [], []

    additional_types = []
    references = []

    cwl_class = data.get("class")

    # --- classify CWL type ---
    if cwl_class == "Workflow":
        additional_types.append("ComputationalWorkflow")

        steps = data.get("steps", {})
        if isinstance(steps, dict):
            for step in steps.values():
                run = step.get("run")
                if isinstance(run, str):
                    references.append(run)

    elif cwl_class == "CommandLineTool":
        additional_types.append("CommandLineTool")

    text = str(data).lower()

    if "streamflow" in text:
        additional_types.append("StreamFlow")

    if any(w in text for w in ("mpi", "slurm", "parallel", "scatter")):
        additional_types.append("HPCWorkflow")

    return list(dict.fromkeys(additional_types)), references


def _guess_mime(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path)

    if mime:
        return mime

    suffix = path.suffix.lower()

    if suffix == ".cwl":
        return "text/yaml"
    if suffix == ".bib":
        return "text/x-bibtex"

    if suffix in {".log", ".out", ".err", ".cmd", ".time", ".exit"}:
        return "text/plain"

    return "text/plain"


def _schema_additional_types(path: Path) -> list[str]:
    suffix = path.suffix.lower()
    name = path.name.lower()

    if suffix in {".png", ".svg", ".jpg", ".jpeg", ".gif"}:
        return ["ImageObject"]

    if suffix == ".bib":
        return ["CreativeWork"]

    if suffix in {".c", ".jinja"}:
        return ["SoftwareSourceCode"]

    if suffix == ".def" or "dockerfile" in name:
        return ["SoftwareSourceCode", "ContainerDefinition"]

    if suffix == ".md":
        return ["CreativeWork"]

    if suffix in {".log", ".out", ".err", ".cmd", ".time", ".exit"}:
        return ["Log", "File"]

    return []


def _iter_files():
    for d in _INCLUDED_DIRS:
        base = _ROOT / d
        if base.exists():
            for p in base.rglob("*"):
                if p.is_file():
                    yield p


def _is_conformance_root(path: Path) -> bool:
    return "cwl-conformance-tests" in path.parts


def load_cff(path: Path) -> dict:
    """Loads a ``CITATION.cff``."""
    with path.open("r", encoding="utf-8") as f:
        data = _YAML.load(f)

    return data if isinstance(data, dict) else {}


def cff2rocrate(crate: ROCrate, cff: dict):
    """Populate an RO-Crate crate with CFF (citation) file information."""

    def add_license(crate, license_id: str) -> str:
        license_url = f"https://spdx.org/licenses/{license_id}.html"

        license_entity = ContextEntity(
            crate,
            license_url,
            {
                "@type": "CreativeWork",
                "name": license_id,
                "url": license_url
            }
        )

        crate.add(license_entity)

        return license_url

    def add_authors(crate, cff: dict) -> list[dict[str, str]]:
        authors = cff.get("authors", [])
        author_nodes = []

        for i, a in enumerate(authors):
            orcid = a.get("orcid")

            author_id = orcid if orcid else f"#author-{i}"

            properties = {
                "givenName": a.get("given-names"),
                "familyName": a.get("family-names"),
            }

            if orcid:
                properties["sameAs"] = {"@id": orcid}
                properties["identifier"] = {"@id": orcid}

            person = Person(crate, author_id, properties)

            crate.add(person)

            author_nodes.append({"@id": author_id})

        return author_nodes

    dataset = crate.root_dataset

    # --- identity ---
    dataset["name"] = cff.get("title")
    dataset["description"] = cff.get("message") or cff.get("abstract") or ""
    dataset["version"] = cff.get("version")

    # --- DOI ---
    doi = cff.get("doi")
    if doi:
        dataset["identifier"] = f"https://doi.org/{doi}"

    # --- keywords ---
    if cff.get("keywords"):
        dataset["keywords"] = cff["keywords"]

    # --- license (FIXED: SPDX → URL) ---
    license_id = str(cff.get("license"))
    if license_id:
        license_url = add_license(crate, license_id)
        dataset["license"] = {"@id": license_url}

    # --- authors (support multiple, not just first) ---
    author_nodes = add_authors(crate, cff)
    if author_nodes:
        dataset["author"] = author_nodes


def add_workflow_links(file_index, workflow_graph):
    """Link CWL Workflows and Tools.

    We have some CWL Workflows with Tools in the project that are related.
    While we are not using CWLProv, we can still link it somehow, to at least
    give future readers a chance to connect/parse/re-use them more easily."""
    for src, refs in workflow_graph:
        src_entity = file_index.get(src)
        if not src_entity:
            continue

        has_parts = src_entity.get("hasPart", [])
        if not isinstance(has_parts, list):
            has_parts = [has_parts]

        for ref in refs:
            target_path = (_ROOT / Path(src).parent / ref).resolve()

            with suppress(FileNotFoundError):
                rel_target = str(target_path.relative_to(_ROOT))

            if rel_target not in file_index:
                continue

            has_parts.append({"@id": rel_target})

        if has_parts:
            src_entity["hasPart"] = has_parts


def _extract_run_group(rel: str) -> str | None:
    parts = Path(rel).parts
    if len(parts) < 5:
        return None

    if parts[0] != "cwl-conformance-tests" or parts[1] != "output":
        return None

    return "/".join(parts[:5]) + "/"


def _workflow_root(rel: str) -> str | None:
    parts = Path(rel).parts
    if len(parts) < 2:
        return None
    if parts[0] != "workflows":
        return None
    return f"workflows/{parts[1]}/"


def main():
    crate = ROCrate()

    cff = load_cff(_ROOT / "CITATION.cff")
    cff2rocrate(crate, cff)

    file_index = {}
    workflow_graph = []

    conformance_dataset = ContextEntity(
        crate,
        "cwl-conformance-tests/",
        {
            "@type": "Dataset",
            "name": "CWL Conformance Tests",
            "description": "Execution results and specifications for CWL conformance testing across runners, HPC systems, and CWL versions."
        }
    )
    crate.add(conformance_dataset)

    workflow_root_dataset = ContextEntity(
        crate,
        "workflows/",
        {
            "@type": "Dataset",
            "name": "MPI + CWL Workflow Experiments",
            "description": "Execution results and specifications for MPI + CWL Workflow Experiments (Simple MPI Workflow, and FALL3D Workflow)."
        }
    )
    crate.add(workflow_root_dataset)

    crate.root_dataset["hasPart"] = crate.root_dataset.get("hasPart", []) + [
        {"@id": "cwl-conformance-tests/"},
        {"@id": "workflows/"},
    ]

    workflow_datasets = {}

    for f in _iter_files():
        rel = str(f.relative_to(_ROOT))
        stat = f.stat()

        additional_types = _schema_additional_types(f)
        references = []

        if f.suffix == ".cwl":
            cwl_types, references = _parse_cwl(f)
            additional_types.extend(cwl_types)

        entity = crate.add_file(
            source=str(f),
            dest_path=rel,
            properties={
                "encodingFormat": _guess_mime(f),
                "contentSize": str(stat.st_size),
                "dateModified": datetime.fromtimestamp(stat.st_mtime, UTC).isoformat(),
                "additionalType": additional_types or None,
            },
            fetch_remote=False,
        )

        file_index[rel] = entity

        if references:
            workflow_graph.append((rel, references))

        is_part_of = []

        # A single dataset with the CWL Conformance Test results
        if "cwl-conformance-tests" in rel:
            is_part_of.append({"@id": "cwl-conformance-tests/"})

        group_id = _extract_run_group(rel)
        if group_id:
            is_part_of.append({"@id": group_id})

        if is_part_of:
            entity["isPartOf"] = is_part_of

        # Two datasets, one for workflows/mpich-sr and one for workflows/fall3d
        if rel.startswith("workflows/"):
            wf_root = _workflow_root(rel)

            if wf_root and wf_root not in workflow_datasets:
                dataset = ContextEntity(
                    crate,
                    wf_root,
                    {
                        "@type": "Dataset",
                        "name": wf_root.strip("/").split("/")[-1],
                        "isPartOf": {"@id": "workflows/"}
                    }
                )

                crate.add(dataset)

                workflow_datasets[wf_root] = dataset

                workflow_root_dataset["hasPart"] = workflow_root_dataset.get("hasPart", []) + [
                    {"@id": wf_root}
                ]

    add_workflow_links(file_index, workflow_graph)

    # TBD: Strange, I seem to recall there was a way to generate just the
    #      JSON-LD file, no?
    rocrate_file = _ROOT / "ro-crate-metadata.json"
    with TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        crate.write(tmp_path)
        tmp_rocrate = Path(tmp_path / "ro-crate-metadata.json")
        move(tmp_rocrate, rocrate_file)
        print(f"Wrote RO-Crate -> {rocrate_file}")


if __name__ == "__main__":
    main()
