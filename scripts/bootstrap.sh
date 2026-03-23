#!/bin/bash
#
# Bootstrap Script — Company Loop Initial Setup
#
# This script prepares the environment for first run.
#
# Steps:
# 1. Create Python virtual environment
# 2. Install dependencies
# 3. Verify integrations can be reached
# 4. Create initial config from .env
# 5. Initialize memory directories
# 6. Run health checks
#

set -e  # Exit on error

echo "======================================"
echo "Company Loop — Bootstrap"
echo "======================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Found: Python $python_version"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "  ERROR: Python 3.11+ required"
    exit 1
fi
echo "  ✓ Python version OK"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "  ✓ Virtual environment created"
else
    echo "  ✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "  ✓ Activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "  ✓ Dependencies installed"
echo ""

# Check for .env file
echo "Checking environment configuration..."
if [ ! -f ".env" ]; then
    echo "  WARNING: .env file not found"
    echo "  Creating from .env.example..."
    cp .env.example .env
    echo "  ✓ Created .env from template"
    echo ""
    echo "  IMPORTANT: Edit .env and add your API credentials before running!"
    echo ""
else
    echo "  ✓ .env file exists"
fi
echo ""

# Create memory directories if they don't exist
echo "Initializing memory directories..."
mkdir -p memory/active
mkdir -p memory/corridor
mkdir -p memory/relational
mkdir -p memory/summaries/daily
mkdir -p memory/summaries/weekly
mkdir -p memory/archival
echo "  ✓ Memory directories created"
echo ""

# Create logs directory
echo "Initializing logs directory..."
mkdir -p logs
echo "  ✓ Logs directory created"
echo ""

# Create data directories
echo "Initializing data directories..."
mkdir -p data/raw/{close,clickup,google,social}
mkdir -p data/normalized/{leads,events,staffing,finance,partners}
mkdir -p data/snapshots
echo "  ✓ Data directories created"
echo ""

# Create reports directories
echo "Initializing reports directories..."
mkdir -p reports/executive/{daily-briefs,weekly-summaries,urgent-exceptions}
mkdir -p reports/teams/{sales,operations,admin,media}
mkdir -p reports/system/{health,mismatches,promotion-reviews}
echo "  ✓ Reports directories created"
echo ""

# Run health checks
echo "Running health checks..."
echo "  (This will verify connectivity to integrations)"
echo ""

# TODO: Actually run health checks
# python scripts/health_check.py

echo "  ⚠ Health checks not yet implemented"
echo "  Manual verification required for:"
echo "    - Google Cloud API access"
echo "    - ClickUp API access"
echo "    - Close API access"
echo "    - Social media API access"
echo ""

# Summary
echo "======================================"
echo "Bootstrap Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API credentials"
echo "  2. Test integrations: python scripts/test_integrations.py"
echo "  3. Run in shadow mode: python runtime/main.py --mode shadow"
echo ""
echo "For detailed instructions, see docs/rollout-plan.md"
echo ""
