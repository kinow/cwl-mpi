# SPDX-License-Identifier: CC-BY-4.0
# Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0)
# https://creativecommons.org/licenses/by/4.0/

from pathlib import Path

import mimetypes
from datetime import UTC, datetime
from rocrate.model.contextentity import ContextEntity
from rocrate.model.person import Person
from ruamel.yaml import YAML

"""Generate an RO-Crate metadata JSON-LD file for the thesis dataset."""

ROOT = Path("..").resolve()

yaml = YAML(typ="safe")

INCLUDED_DIRS = [
    "bibliography",
    "containers",
    "examples",
    "images",
]


def parse_cwl(path: Path) -> tuple[list[str], list[str]]:
    """
    Returns:
        additional_types
        referenced_cwl_files
    """
    try:
        data = yaml.load(path.read_text())
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


def guess_mime(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path)

    if mime:
        return mime

    suffix = path.suffix.lower()

    if suffix == ".cwl":
        return "text/yaml"
    if suffix == ".bib":
        return "text/x-bibtex"

    return "text/plain"


def schema_additional_types(path: Path) -> list[str]:
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

    return []


def iter_files():
    for d in INCLUDED_DIRS:
        base = ROOT / d
        if base.exists():
            for p in base.rglob("*"):
                if p.is_file():
                    yield p


def load_cff(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.load(f)

    return data if isinstance(data, dict) else {}


from rocrate.rocrate import ROCrate


def apply_cff_to_rocrate(crate: ROCrate, cff: dict):
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
    license_id = cff.get("license")
    if license_id:
        license_url = add_license(crate, license_id)
        dataset["license"] = {"@id": license_url}

    # --- authors (support multiple, not just first) ---
    author_nodes = add_authors(crate, cff)
    if author_nodes:
        dataset["author"] = author_nodes


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


def add_authors(crate, cff: dict):
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


def add_workflow_links(crate, file_index, workflow_graph):
    for src, refs in workflow_graph:
        src_entity = file_index.get(src)
        if not src_entity:
            continue

        has_parts = src_entity.get("hasPart", [])
        if not isinstance(has_parts, list):
            has_parts = [has_parts]

        for ref in refs:
            target_path = (ROOT / Path(src).parent / ref).resolve()

            try:
                rel_target = str(target_path.relative_to(ROOT))
            except Exception:
                continue

            if rel_target not in file_index:
                continue

            has_parts.append({"@id": rel_target})

        if has_parts:
            src_entity["hasPart"] = has_parts


def main():
    crate = ROCrate()

    cff = load_cff(Path("../CITATION.cff"))
    apply_cff_to_rocrate(crate, cff)

    file_index = {}
    workflow_graph = []

    for f in iter_files():
        rel = str(f.relative_to(ROOT))
        stat = f.stat()

        additional_types = schema_additional_types(f)
        references = []

        if f.suffix == ".cwl":
            cwl_types, references = parse_cwl(f)
            additional_types.extend(cwl_types)

        entity = crate.add_file(
            source=str(f),
            dest_path=rel,
            properties={
                "encodingFormat": guess_mime(f),
                "contentSize": str(stat.st_size),
                "dateModified": datetime.fromtimestamp(stat.st_mtime, UTC).isoformat(),
                "additionalType": additional_types or None,
            },
            fetch_remote=False,
        )

        file_index[rel] = entity

        if references:
            workflow_graph.append((rel, references))

    add_workflow_links(crate, file_index, workflow_graph)

    out = ROOT / "build/"
    crate.write(out)

    print(f"Wrote RO-Crate -> {out}")


if __name__ == "__main__":
    main()
