#!/bin/bash

# SDARPP Project Structure Validator
#
# Validates that all projects follow the universal project folder template.
# Checks for required folders at each lifecycle stage.
#
# Usage: ./validate-project-structure.sh [--fix] [--project-path PATH]

set -e

# Configuration
ONEDRIVE_BASE="$HOME/Library/CloudStorage/OneDrive-SDArpp/05. SDARPP Operations"
PROJECT_STAGES=(
    "00. Project Administration"
    "01. Acquisition"
    "02. Due Diligence"
    "03. Planning — DA & Approvals"
    "04. Design"
    "05. Procurement & Contracts"
    "06. Construction"
    "07. Operations & SDA Management"
    "08. Financials — Development"
)

ADMIN_SUBFOLDERS=(
    "Project Brief"
    "Contacts Register"
    "Decision Log"
    "Risk Register"
    "Meeting Notes"
)

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
VALID_PROJECTS=0
INVALID_PROJECTS=0
FIXED_PROJECTS=0

# Functions
log_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  WARNING: $1${NC}"
}

validate_project() {
    local project_path="$1"
    local project_name=$(basename "$project_path")

    echo ""
    echo "Validating: $project_name"

    local all_stages_exist=true

    # Check each required stage
    for stage in "${PROJECT_STAGES[@]}"; do
        if [ -d "$project_path/$stage" ]; then
            echo "  ✅ $stage"
        else
            echo "  ❌ MISSING: $stage"
            all_stages_exist=false

            if [ "$FIX_MODE" = true ]; then
                mkdir -p "$project_path/$stage"
                echo "     → Created"
            fi
        fi
    done

    # Check Project Administration subfolders
    echo ""
    for subfolder in "${ADMIN_SUBFOLDERS[@]}"; do
        if [ -d "$project_path/00. Project Administration/$subfolder" ]; then
            echo "  ✅ 00. Project Administration/$subfolder"
        else
            echo "  ❌ MISSING: 00. Project Administration/$subfolder"
            all_stages_exist=false

            if [ "$FIX_MODE" = true ]; then
                mkdir -p "$project_path/00. Project Administration/$subfolder"
                echo "     → Created"
            fi
        fi
    done

    if [ "$all_stages_exist" = true ]; then
        ((VALID_PROJECTS++))
        log_success "Project $project_name is VALID"
    else
        ((INVALID_PROJECTS++))
        if [ "$FIX_MODE" = true ]; then
            ((FIXED_PROJECTS++))
            log_success "Project $project_name FIXED (missing folders created)"
        else
            log_warning "Project $project_name has MISSING folders (run with --fix to create)"
        fi
    fi
}

# Main
main() {
    FIX_MODE=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
        --fix)
            FIX_MODE=true
            shift
            ;;
        --project-path)
            PROJECT_PATH="$2"
            shift 2
            ;;
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
        esac
    done

    echo "🔍 SDARPP Project Structure Validator"
    echo "════════════════════════════════════"
    echo "Base path: $ONEDRIVE_BASE"
    echo "Fix mode: $FIX_MODE"
    echo ""

    # Scan all state project folders
    for state_folder in "$ONEDRIVE_BASE/0"*"Projects"*"/"; do
        if [ -d "$state_folder" ]; then
            STATE=$(basename "$state_folder")

            echo ""
            echo "━━ $STATE ━━"

            # Scan projects in this state
            for project_path in "$state_folder"/*/; do
                project_name=$(basename "$project_path")

                # Skip state admin folder
                if [[ "$project_name" == _STATE-ADMIN* ]]; then
                    continue
                fi

                validate_project "$project_path"
            done
        fi
    done

    # Summary
    echo ""
    echo "════════════════════════════════════"
    echo "📊 Validation Summary"
    echo "════════════════════════════════════"
    log_success "Valid projects: $VALID_PROJECTS"
    log_warning "Invalid projects: $INVALID_PROJECTS"

    if [ $INVALID_PROJECTS -gt 0 ]; then
        if [ "$FIX_MODE" = true ]; then
            log_success "Fixed projects: $FIXED_PROJECTS"
            echo ""
            echo "✅ All missing folders have been created."
        else
            echo ""
            echo "Run with --fix flag to automatically create missing folders:"
            echo "  ./validate-project-structure.sh --fix"
        fi
    else
        log_success "All projects have valid structure!"
    fi
}

main "$@"
