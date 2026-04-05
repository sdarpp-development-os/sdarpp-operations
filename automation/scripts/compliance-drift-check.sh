#!/bin/bash

# SDARPP Compliance Drift Detection
#
# Checks all projects' SDA compliance checklists for stale items
# (not updated in 90+ days) and missing checklist items.
#
# Outputs: Issues raised in GitHub for items needing attention
#
# Runs weekly via GitHub Actions

set -e

# Configuration
ONEDRIVE_BASE="$HOME/Library/CloudStorage/OneDrive-SDArpp/05. SDARPP Operations"
STALE_THRESHOLD_DAYS=90
GITHUB_REPO="sdarpp-development-os/sdarpp-operations"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get cutoff date
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CUTOFF_DATE=$(date -u -v-90d +%Y-%m-%d)
else
    # Linux
    CUTOFF_DATE=$(date -u -d "90 days ago" +%Y-%m-%d)
fi
TODAY=$(date +%Y-%m-%d)

echo "🔍 SDARPP Compliance Drift Detection"
echo "════════════════════════════════════"
echo "Stale threshold: $STALE_THRESHOLD_DAYS days (before $CUTOFF_DATE)"
echo "Scan date: $TODAY"
echo ""

STALE_ITEMS_FOUND=0
MISSING_ITEMS_FOUND=0
PROJECTS_WITH_DRIFT=0

# Function to check project compliance
check_project_compliance() {
    local project_path="$1"
    local project_id=$(basename "$project_path")
    local checklist_file="$project_path/sda/sda-compliance-checklist.md"

    if [ ! -f "$checklist_file" ]; then
        echo -e "${YELLOW}⚠️  $project_id: No SDA compliance checklist found${NC}"
        return
    fi

    # Get file modification date
    if [[ "$OSTYPE" == "darwin"* ]]; then
        FILE_DATE=$(stat -f %Sm -t "%Y-%m-%d" "$checklist_file")
    else
        FILE_DATE=$(date -d @$(stat -c %Y "$checklist_file") +%Y-%m-%d)
    fi

    # Check if stale
    if [[ "$FILE_DATE" < "$CUTOFF_DATE" ]]; then
        ((STALE_ITEMS_FOUND++))
        ((PROJECTS_WITH_DRIFT++))
        echo -e "${YELLOW}⚠️  DRIFT: $project_id${NC}"
        echo "      Last updated: $FILE_DATE (stale as of $CUTOFF_DATE)"
        echo "      Action: Checklist needs review and update"
    else
        echo -e "${GREEN}✅ $project_id: Current${NC}"
    fi

    # Check for missing checklist items
    # (Placeholder: in production, would parse checklist against master matrix)
    local item_count=$(grep -c "^| " "$checklist_file" 2>/dev/null || echo 0)
    if [ $item_count -lt 20 ]; then
        ((MISSING_ITEMS_FOUND++))
        echo "      ⚠️  Possible missing items (found: $item_count, expected: ~30)"
    fi
}

# Scan all projects
echo "Scanning projects..."
echo ""

for state_folder in "$ONEDRIVE_BASE/0"*"Projects"*"/"; do
    if [ ! -d "$state_folder" ]; then
        continue
    fi

    STATE=$(basename "$state_folder")
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📍 $STATE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    for project_path in "$state_folder"/*/; do
        project_name=$(basename "$project_path")

        # Skip state admin folder
        if [[ "$project_name" == _STATE-ADMIN* ]]; then
            continue
        fi

        check_project_compliance "$project_path"
    done

    echo ""
done

# Summary and GitHub Issue creation
echo "════════════════════════════════════"
echo "📊 Compliance Drift Summary"
echo "════════════════════════════════════"
echo -e "${YELLOW}Projects with drift detected: $PROJECTS_WITH_DRIFT${NC}"
echo -e "${YELLOW}Stale checklist items: $STALE_ITEMS_FOUND${NC}"
echo -e "${YELLOW}Possible missing items: $MISSING_ITEMS_FOUND${NC}"

if [ $PROJECTS_WITH_DRIFT -gt 0 ] || [ $MISSING_ITEMS_FOUND -gt 0 ]; then
    echo ""
    echo "⚠️  DRIFT DETECTED — Issues should be raised for remediation"
    echo ""
    echo "GitHub Issue would be created with:"
    echo "  Title: [COMPLIANCE DRIFT] SDA Design Standard Compliance — $TODAY"
    echo "  Body: Stale items: $STALE_ITEMS_FOUND | Missing items: $MISSING_ITEMS_FOUND"
    echo "  Labels: compliance, automated, sda-design-standard"
    echo ""
    echo "In production environment (GitHub Actions), gh CLI would execute:"
    echo "  gh issue create --repo $GITHUB_REPO --title '...' --body '...' --label 'compliance,automated'"
else
    echo ""
    echo -e "${GREEN}✅ No compliance drift detected${NC}"
    echo "All projects have current checklists"
fi
