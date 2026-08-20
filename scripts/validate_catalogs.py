#!/usr/bin/env python3
"""Validate the public Z-Hub catalogs and their cross-references."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
CATALOG_NAMES = ("compositions", "modules", "ecosystem", "datasets")


def load_catalog(name: str, problems: list[str]) -> list[dict]:
    path = PUBLIC / f"{name}.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        problems.append(f"{path.relative_to(ROOT)}: {error}")
        return []

    if not isinstance(data, list):
        problems.append(f"{path.relative_to(ROOT)}: root must be an array")
        return []

    records: list[dict] = []
    seen: set[str | int] = set()
    for index, record in enumerate(data):
        if not isinstance(record, dict):
            problems.append(f"{name}[{index}]: record must be an object")
            continue
        record_id = record.get("id")
        valid_id = (
            isinstance(record_id, str) and bool(record_id.strip())
        ) or (
            name == "datasets" and isinstance(record_id, int) and not isinstance(record_id, bool)
        )
        if not valid_id:
            expected = "an integer or non-empty string" if name == "datasets" else "a non-empty string"
            problems.append(f"{name}[{index}]: id must be {expected}")
        elif record_id in seen:
            problems.append(f"{name}[{index}]: duplicate id '{record_id}'")
        else:
            seen.add(record_id)
        records.append(record)
    return records


def stages(composition: dict):
    pipeline = composition.get("pipeline", [])
    if isinstance(pipeline, list):
        yield from (stage for stage in pipeline if isinstance(stage, dict))
    variants = composition.get("variants", [])
    if isinstance(variants, list):
        for variant in variants:
            if not isinstance(variant, dict):
                continue
            pipeline = variant.get("pipeline", [])
            if isinstance(pipeline, list):
                yield from (stage for stage in pipeline if isinstance(stage, dict))


def check_references(catalogs: dict[str, list[dict]], problems: list[str]) -> None:
    ids = {
        name: {record["id"] for record in records if isinstance(record.get("id"), str)}
        for name, records in catalogs.items()
    }

    for composition in catalogs["compositions"]:
        composition_id = composition.get("id", "?")
        for stage in stages(composition):
            module_id = stage.get("module")
            if module_id and module_id not in ids["modules"]:
                problems.append(
                    f"composition '{composition_id}': unknown module '{module_id}'"
                )
            embedded_id = stage.get("composition")
            if embedded_id and embedded_id not in ids["compositions"]:
                problems.append(
                    f"composition '{composition_id}': unknown composition '{embedded_id}'"
                )
            alternatives = stage.get("alternatives", [])
            if isinstance(alternatives, list):
                for alternative in alternatives:
                    if not isinstance(alternative, dict):
                        continue
                    alternative_id = alternative.get("module")
                    if alternative_id and alternative_id not in ids["modules"]:
                        problems.append(
                            f"composition '{composition_id}': unknown alternative module "
                            f"'{alternative_id}'"
                        )

        for field in ("supersedes", "supersededBy"):
            target = composition.get(field)
            if target and target not in ids["compositions"]:
                problems.append(
                    f"composition '{composition_id}': {field} references unknown '{target}'"
                )
        related = composition.get("relatedTo", [])
        if isinstance(related, list):
            for target in related:
                if target not in ids["compositions"]:
                    problems.append(
                        f"composition '{composition_id}': relatedTo references unknown '{target}'"
                    )

    for entry in catalogs["ecosystem"]:
        entry_id = entry.get("id", "?")
        for field, catalog_name in (
            ("relatedTo", "ecosystem"),
            ("compositions", "compositions"),
        ):
            targets = entry.get(field, [])
            if not isinstance(targets, list):
                continue
            for target in targets:
                if target not in ids[catalog_name]:
                    problems.append(
                        f"ecosystem '{entry_id}': {field} references unknown '{target}'"
                    )


def main() -> int:
    problems: list[str] = []
    catalogs = {name: load_catalog(name, problems) for name in CATALOG_NAMES}
    check_references(catalogs, problems)

    if problems:
        print(f"Catalog validation failed with {len(problems)} problem(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1

    summary = ", ".join(f"{name}={len(catalogs[name])}" for name in CATALOG_NAMES)
    print(f"Catalog validation passed ({summary})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
