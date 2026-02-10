#!/bin/bash
# Initialize a new Webflow Designer Extension project using create-webflow-extension.
#
# Usage:
#   ./init-extension.sh <project-name> [options]
#
# Options:
#   --pm <manager>       Package manager to use (pnpm|npm|yarn|bun). Default: pnpm
#   --linter <linter>    Linter to configure (oxlint|biome|eslint)
#   --skip-git           Skip git initialization
#   --skip-install       Skip automatic dependency installation
#   --quiet              Suppress non-essential output

set -e

# ---------------------------------------------------------------------------
# Parse arguments
# ---------------------------------------------------------------------------

PROJECT_NAME=""
PASS_THROUGH_ARGS=()
SELECTED_PM="pnpm"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --pm)
            SELECTED_PM="$2"
            PASS_THROUGH_ARGS+=("--pm" "$2")
            shift 2
            ;;
        --linter)
            PASS_THROUGH_ARGS+=("--linter" "$2")
            shift 2
            ;;
        --skip-git)
            PASS_THROUGH_ARGS+=("--skip-git")
            shift
            ;;
        --skip-install)
            PASS_THROUGH_ARGS+=("--skip-install")
            shift
            ;;
        --quiet)
            PASS_THROUGH_ARGS+=("--quiet")
            shift
            ;;
        -*)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
        *)
            # First positional argument is the project name
            if [[ -z "$PROJECT_NAME" ]]; then
                PROJECT_NAME="$1"
            else
                echo "Unexpected argument: $1" >&2
                exit 1
            fi
            shift
            ;;
    esac
done

if [[ -z "$PROJECT_NAME" ]]; then
    echo "Usage: ./init-extension.sh <project-name> [options]"
    echo ""
    echo "Options:"
    echo "  --pm <manager>     Package manager (pnpm|npm|yarn|bun). Default: pnpm"
    echo "  --linter <linter>  Linter to configure (oxlint|biome|eslint)"
    echo "  --skip-git         Skip git initialization"
    echo "  --skip-install     Skip dependency installation"
    echo "  --quiet            Suppress non-essential output"
    exit 1
fi

# ---------------------------------------------------------------------------
# Preflight checks
# ---------------------------------------------------------------------------

if ! command -v node &> /dev/null; then
    echo "Error: Node.js is required but not installed." >&2
    echo "Install it from https://nodejs.org or via a version manager like fnm/nvm." >&2
    exit 1
fi

if ! command -v npx &> /dev/null; then
    echo "Error: npx is required but not found on PATH." >&2
    echo "It ships with npm >= 5.2. Make sure Node.js is installed correctly." >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Scaffold the project
# ---------------------------------------------------------------------------

echo "Creating Webflow Designer Extension: $PROJECT_NAME"
if [[ ${#PASS_THROUGH_ARGS[@]} -gt 0 ]]; then
    echo "  Options: ${PASS_THROUGH_ARGS[*]}"
fi
echo ""

npx create-webflow-extension@latest "$PROJECT_NAME" "${PASS_THROUGH_ARGS[@]}"

# ---------------------------------------------------------------------------
# Success message and next steps
# ---------------------------------------------------------------------------

echo ""
echo "Project '$PROJECT_NAME' created successfully!"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  $SELECTED_PM dev"
echo ""
echo "Then in Webflow:"
echo "  1. Go to Workspace Settings > Apps & Integrations > Develop"
echo "  2. Create or configure your app (set the development URL to http://localhost:1337)"
echo "  3. Install the app on a test site"
echo "  4. Open the Designer and press 'E' to open the apps panel"
echo "  5. Launch your development app"
echo ""
