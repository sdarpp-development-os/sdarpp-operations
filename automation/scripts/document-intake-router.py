#!/usr/bin/env python3
"""
SDARPP Document Intake Router

Monitors the document intake queue and routes documents to appropriate project folders.
Classifies documents by type and project ID, moves them to correct locations,
and updates the document registry.

Usage:
    python document-intake-router.py [--watch] [--intake-path PATH]

The router watches: 07. AI Agent Workspace/01. Inputs/document-queue/

And routes documents to:
    projects/[PROJECT-ID]/ai-outputs/
    OR
    07. AI Agent Workspace/04. Outputs — Generated/
"""

import os
import shutil
import csv
import sys
import re
from pathlib import Path
from datetime import datetime

# Configuration
DEFAULT_INTAKE_PATH = os.path.expanduser(
    "~/Library/CloudStorage/OneDrive-SDArpp/05. SDARPP Operations/07. AI Agent Workspace/01. Inputs/document-queue"
)
REGISTRY_FILE = "knowledge-base/document-registry.csv"


def extract_project_id(filename: str) -> str:
    """
    Extract project ID from filename.
    Expected format: [PROJECT-ID]_[description].md
    Example: VIC-SDA-WODONGA-2025_compliance-audit.md
    """
    # Match pattern: [STATE]-[TYPE]-[SUBURB]-[YEAR]
    match = re.match(
        r"^([A-Z]{2}-[A-Z]+?-[A-Z\-]+?-\d{4})", filename
    )
    if match:
        return match.group(1)

    return "SYS"  # System/general document if no project ID found


def classify_document(filename: str) -> str:
    """
    Classify document type based on filename.
    """
    filename_lower = filename.lower()

    if any(x in filename_lower for x in ["compliance", "audit"]):
        return "compliance"
    elif any(x in filename_lower for x in ["feasibility", "financial"]):
        return "feasibility"
    elif any(x in filename_lower for x in ["planning", "da"]):
        return "planning"
    elif any(x in filename_lower for x in ["report", "summary"]):
        return "reporting"
    elif any(x in filename_lower for x in ["contract", "agreement"]):
        return "contracts"
    else:
        return "document"


def route_document(source_path: Path, intake_base: Path, onedrive_base: Path) -> bool:
    """
    Route a document to its destination folder and update registry.
    """
    filename = source_path.name
    project_id = extract_project_id(filename)
    doc_type = classify_document(filename)

    print(f"\n📄 Routing: {filename}")
    print(f"   Project: {project_id}")
    print(f"   Type: {doc_type}")

    if project_id != "SYS":
        # Route to project ai-outputs folder
        # Extract state from project ID (e.g., VIC from VIC-SDA-WODONGA-2025)
        state = project_id.split("-")[0]
        projects_base = onedrive_base / f"0X. Projects — {state}"

        # Find matching project folder
        project_folder = None
        if projects_base.exists():
            for folder in projects_base.iterdir():
                if folder.name == project_id:
                    project_folder = folder
                    break

        if project_folder and (project_folder / "ai-outputs").exists():
            destination = project_folder / "ai-outputs" / filename
            print(f"   → Destination: {destination.relative_to(onedrive_base)}")

            # Move file
            try:
                shutil.move(str(source_path), str(destination))
                print(f"   ✅ Routed to project folder")
                return True
            except Exception as e:
                print(f"   ❌ Error moving file: {e}")
                return False
        else:
            print(f"   ⚠️  Project folder or ai-outputs not found, routing to general outputs")
    else:
        print(f"   → General document (no project ID)")

    # Default: route to general outputs
    general_outputs = (
        onedrive_base / "07. AI Agent Workspace/04. Outputs — Generated"
    )

    if doc_type == "compliance":
        destination = general_outputs / "compliance-reports" / filename
    elif doc_type == "feasibility":
        destination = general_outputs / "feasibility-summaries" / filename
    elif doc_type == "planning":
        destination = general_outputs / "da-review-notes" / filename
    elif doc_type == "reporting":
        destination = general_outputs / "governance-summaries" / filename
    else:
        destination = general_outputs / filename

    destination.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.move(str(source_path), str(destination))
        print(f"   ✅ Routed to general outputs")
        return True
    except Exception as e:
        print(f"   ❌ Error moving file: {e}")
        return False


def main():
    intake_path = Path(os.getenv("INTAKE_PATH", DEFAULT_INTAKE_PATH))
    onedrive_base = intake_path.parent.parent.parent  # Navigate back to 05. SDARPP Operations

    print(f"🚀 SDARPP Document Intake Router")
    print(f"════════════════════════════════")
    print(f"Monitoring: {intake_path}")
    print(f"OneDrive base: {onedrive_base}")
    print()

    if not intake_path.exists():
        print(f"❌ Intake path not found: {intake_path}")
        sys.exit(1)

    # Process all files in intake queue
    files_processed = 0
    files_routed = 0

    for file_path in intake_path.glob("*"):
        if file_path.is_file() and not file_path.name.startswith("."):
            files_processed += 1

            if route_document(file_path, intake_path, onedrive_base):
                files_routed += 1

    # Summary
    print()
    print(f"════════════════════════════════")
    print(f"✅ Routing Complete")
    print(f"   Processed: {files_processed}")
    print(f"   Routed: {files_routed}")

    if files_processed > files_routed:
        print(
            f"   ⚠️  {files_processed - files_routed} files failed to route (check errors above)"
        )


if __name__ == "__main__":
    main()
