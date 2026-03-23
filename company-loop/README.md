# Company Loop — Autonomous Business Intelligence System

**Status**: Initial deployment for catering/event business
**Runtime**: Claude Code + MCP servers + VY mediation layer
**Purpose**: Unified awareness across sales, operations, finance, partnerships, staffing, and media

---

## System Architecture

### Core Stack
- **Orchestration**: Claude Code (primary runtime brain)
- **Model Access**: GPT Plus OAuth → Codex (via configured routing)
- **Execution Layer**: VY (screenshot-grounded observation + mediated action)
- **Memory/Context**: Pieces server (persistent memory substrate)

### Integration Surface
- **ClickUp**: Task management and workflow coordination
- **Close**: Sales pipeline, lead management, opportunity tracking
- **Google Suite**: Sheets (business data), Calendar (operational schedule), Drive, Gmail
- **Social Media**: YouTube, TikTok, Instagram, LinkedIn, Twitter (both publishing AND intelligence gathering)

### Business Corridors
- **Sales**: Lead intake, attribution, ownership, conversion, follow-up
- **Operations**: Event/job scheduling, complexity assessment, staffing, logistics
- **Finance**: Cash flow projection, reconciliation, payment tracking
- **Partnerships**: Venue/planner relationships, referral management
- **Workforce**: Labor reports, scheduling, seasonal pressure detection
- **Procurement**: Shopping lists, prep requirements, quantity extraction
- **Marketing/Media**: Content support, trend capture, audience intelligence
- **Executive**: Owner dashboarding, high-level summaries, decision support

---

## Operating Principles

### Shadow Mode First
- Manual workflows remain intact during validation phase
- Loop observes and mirrors existing processes
- Outputs compared against human judgment
- Trust earned through demonstrated reliability
- Promotion to autonomous execution only after validation

### Approval Gates
High-stakes actions require human approval:
- External client communication
- Financial record changes
- Public social media posts
- Staff assignment modifications
- CRM data updates

### Safe Autonomous Actions
- Internal summaries and observations
- Low-risk task generation
- Metadata tagging
- Passive monitoring
- Draft creation
- Proposed updates (not yet committed)

---

## Directory Structure

```
company-loop/
├── docs/              Documentation and business maps
├── config/            System configuration and permissions
├── runtime/           Core execution engine
├── integrations/      Tool-specific adapters (MCP servers, APIs)
├── corridors/         Business-specific logic by functional area
├── prediction/        Intelligence layer (scoring, confidence, trajectory)
├── memory/            Active obligations, corridor state, relationships
├── workflows/         Process definitions, shadow mode, approvals
├── reports/           Generated outputs for teams and executives
├── data/              Raw and normalized business data
├── scripts/           Bootstrap, sync, and utility scripts
├── tests/             Unit, integration, and corridor tests
├── deployment/        Portability and rollout infrastructure
└── logs/              System activity and debugging
```

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ (for MCP servers)
- Google Cloud API credentials
- ClickUp API token
- Close API key
- VY configured
- Pieces server running

### Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Bootstrap workspace
./scripts/bootstrap.sh

# Run validation
python scripts/run_shadow_cycle.py
```

### First Run
```bash
# Start the loop in observation-only mode
python runtime/main.py --mode shadow
```

---

## Deployment Phases

### Phase 1: Environment and Connectivity
- Set up integrations
- Establish read-only monitoring
- Validate data access

### Phase 2: Observation-Only Loop
- Corridor definitions active
- Summary generation
- Trigger capture
- No autonomous execution

### Phase 3: Task and Draft Generation
- ClickUp task creation (approval-gated)
- Close recommendations
- Calendar-derived summaries
- Partner follow-up suggestions

### Phase 4: Validated Partial Automation
- Approved task updates
- Approved CRM actions
- Low-risk execution
- Measured promotion of proven behaviors

### Phase 5: Portable Template Layer
- Extract reusable patterns
- Parameterize client-specific elements
- Package for similar businesses

---

## Productization Path

This deployment is designed to become a **reusable template** for similar service businesses:

- Referral-driven growth patterns
- Sales + operations + staffing coupling
- Spreadsheet-native reality common in industry
- Repeatable corridor structures

Generic components will be extracted into a base template while client-specific configurations remain modular.

---

## Documentation

- [System Overview](docs/overview.md)
- [Business Map](docs/business-map.md)
- [System of Records](docs/system-of-records.md)
- [Role Map](docs/role-map.md)
- [Approval Rules](docs/approvals.md)
- [Rollout Plan](docs/rollout-plan.md)

---

## Support

For questions about this deployment, see `docs/` or contact the deployment team.
