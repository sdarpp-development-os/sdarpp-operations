#!/usr/bin/env python3
"""
SDARPP OneDrive Index Builder

Scans the local OneDrive mount (05. SDARPP Operations) and generates/updates
the master document-registry.csv with file paths, types, and metadata.

Usage:
    python build-onedrive-index.py [--onedrive-path PATH] [--output FILE]

Environment:
    ONEDRIVE_PATH: Override default OneDrive mount path

Example:
    python build-onedrive-index.py --onedrive-path ~/Library/CloudStorage/OneDrive-SDArpp
"""

import os
import csv
import sys
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
DEFAULT_ONEDRIVE_PATH = os.path.expanduser("~/Library/CloudStorage/OneDrive-SDArpp/05. SDARPP Operations")
OUTPUT_FILE = "knowledge-base/document-registry.csv"
SDARPP_OPERATIONS_ROOT = "05. SDARPP Operations"

# Document type classification
DOC_TYPE_PATTERNS = {
    "compliance": ["compliance", "checklist", "audit"],
    "regulatory": ["Design Standard", "Act", "Regulation", "Framework"],
    "template": ["template", "prompt", "guide"],
    "governance": ["risk-register", "decision-log", "summary"],
    "contract": ["agreement", "contract", "appointment"],
    "financial": ["feasibility", "model", "cost", "budget"],
    "planning": ["DA", "planning", "zoning", "controls"],
    "project": ["project", "brief", "report"],
}


def classify_document_type(filename: str, folder_path: str) -> str:
    """
    Classify document type based on filename and folder structure.
    """
    combined = f"{filename} {folder_path}".lower()

    for doc_type, keywords in DOC_TYPE_PATTERNS.items():
        if any(keyword.lower() in combined for keyword in keywords):
            return doc_type

    return "document"


def scan_onedrive(root_path: str) -> list:
    """
    Recursively scan OneDrive folder and extract document metadata.
    """
    documents = []
    root_path = Path(root_path)

    if not root_path.exists():
        print(f"❌ Error: OneDrive path not found: {root_path}")
        return documents

    for file_path in root_path.rglob("*"):
        if file_path.is_file():
            # Skip hidden and system files
            if file_path.name.startswith(".") or file_path.name.startswith("~"):
                continue

            # Get relative path from root
            relative_path = str(file_path.relative_to(root_path))
            folder_path = str(file_path.parent.relative_to(root_path))

            # Get file modification time
            mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            date_modified = mod_time.strftime("%Y-%m-%d")

            # Determine project ID (extract from path if applicable)
            if "Projects" in relative_path:
                parts = relative_path.split(os.sep)
                # Format: 0X. Projects — STATE/PROJECT-ID/...
                project_id = parts[1] if len(parts) > 1 else "SYS"
            else:
                project_id = "SYS"  # System/general document

            # Classify document type
            doc_type = classify_document_type(file_path.name, folder_path)

            # Extract version if present (e.g., _V1.0)
            version = "1.0"
            if "_V" in file_path.name:
                try:
                    version_str = file_path.name.split("_V")[1].split(".")[0]
                    version = f"{version_str}.{file_path.name.split('_V')[1].split('.')[1]}"
                except IndexError:
                    pass

            # Determine status
            status = "current"
            if "[DRAFT]" in file_path.name:
                status = "draft"
            elif "[SUPERSEDED]" in file_path.name:
                status = "superseded"
            elif file_path.name.startswith("~"):
                status = "temporary"

            documents.append({
                "project_id": project_id,
                "folder_path": folder_path,
                "filename": file_path.name,
                "document_type": doc_type,
                "version": version,
                "date_modified": date_modified,
                "status": status,
            })

    return documents


def write_registry(documents: list, output_file: str) -> None:
    """
    Write document registry to CSV file.
    """
    fieldnames = [
        "project_id",
        "folder_path",
        "filename",
        "document_type",
        "version",
        "date_modified",
        "status",
    ]

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(documents)

    print(f"✅ Registry written: {output_file}")
    print(f"   Total documents indexed: {len(documents)}")


def main():
    parser = argparse.ArgumentParser(
        description="Build SDARPP OneDrive document registry"
    )
    parser.add_argument(
        "--onedrive-path",
        default=os.getenv("ONEDRIVE_PATH", DEFAULT_ONEDRIVE_PATH),
        help="Path to OneDrive SDARPP Operations folder",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_FILE,
        help="Output CSV file path",
    )

    args = parser.parse_args()

    print(f"🔍 Scanning OneDrive: {args.onedrive_path}")
    documents = scan_onedrive(args.onedrive_path)

    if documents:
        print(f"📄 Found {len(documents)} documents")
        write_registry(documents, args.output)
    else:
        print("❌ No documents found or path not accessible")
        sys.exit(1)


if __name__ == "__main__":
    main()
