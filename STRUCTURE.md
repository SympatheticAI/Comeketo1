# Company Loop — Directory Structure Overview

This document provides a complete overview of the directory structure and what each component does.

---

## Quick Reference

```
company-loop/
├── README.md                    # System overview and quick start
├── STRUCTURE.md                 # This file — complete structure guide
├── .env.example                 # Environment configuration template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
│
├── docs/                        # Documentation
│   ├── overview.md              # System purpose and architecture
│   ├── business-map.md          # Corridor definitions
│   ├── system-of-records.md     # Data authority mapping
│   ├── role-map.md              # Human ownership structure (TODO)
│   ├── approvals.md             # Approval rules (TODO)
│   └── rollout-plan.md          # Deployment phases (TODO)
│
├── config/                      # System configuration
│   ├── app.yaml                 # Main configuration
│   ├── environments/            # Environment-specific configs
│   ├── models/                  # Model routing configs (TODO)
│   ├── permissions/             # Approval and access rules (TODO)
│   ├── triggers/                # Trigger definitions (TODO)
│   └── integrations/            # Integration configs (TODO)
│
├── runtime/                     # Core execution engine
│   ├── main.py                  # Entry point
│   └── loop/
│       ├── scheduler.py         # Time-based and event-based triggers
│       ├── dispatcher.py        # Routes work to corridors
│       ├── state_manager.py    # Persistent state management
│       ├── trigger_engine.py   # Trigger evaluation
│       └── approval_engine.py  # Human approval workflows
│
├── integrations/                # Tool-specific adapters
│   ├── google/                  # Sheets, Calendar, Drive, Gmail (TODO)
│   ├── clickup/                 # ClickUp MCP server (TODO)
│   ├── close/                   # Close CRM (TODO)
│   ├── social/                  # YouTube, TikTok, Instagram, etc. (TODO)
│   ├── vy/                      # VY mediation layer (TODO)
│   └── pieces/                  # Pieces memory bridge (TODO)
│
├── corridors/                   # Business-specific logic
│   ├── sales/
│   │   ├── corridor.md          # Complete corridor specification
│   │   ├── rules.yaml           # Business rules (TODO)
│   │   ├── triggers.yaml        # Trigger definitions (TODO)
│   │   ├── tasks.py             # Implementation (TODO)
│   │   ├── summaries.py         # Summary generation (TODO)
│   │   └── templates/           # Email/task templates (TODO)
│   ├── operations/              # (TODO)
│   ├── finance/                 # (TODO)
│   ├── partnerships/            # (TODO)
│   ├── workforce/               # (TODO)
│   ├── procurement/             # (TODO)
│   ├── marketing/               # (TODO)
│   └── executive/               # (TODO)
│
├── prediction/                  # Intelligence layer
│   ├── primitives/
│   │   ├── confidence.py        # Confidence scoring (COMPLETE)
│   │   ├── score.py             # Generic scoring (TODO)
│   │   ├── horizon.py           # Time horizon prediction (TODO)
│   │   └── trajectory.py        # Trend projection (TODO)
│   ├── engines/
│   │   ├── lead_prediction.py   # Lead quality scoring (TODO)
│   │   ├── event_complexity.py  # Event difficulty assessment (TODO)
│   │   ├── staffing_pressure.py # Labor demand forecasting (TODO)
│   │   ├── partner_drift.py     # Relationship health tracking (TODO)
│   │   └── cashflow_risk.py     # Financial risk assessment (TODO)
│   ├── features/                # Feature extraction (TODO)
│   ├── evaluation/              # Metrics and validation (TODO)
│   └── memory/                  # Historical outcomes (TODO)
│
├── memory/                      # Persistent state
│   ├── active/                  # Current obligations
│   ├── corridor/                # Corridor state snapshots
│   ├── relational/              # Venue/partner/client memory
│   ├── summaries/               # Daily and weekly narratives
│   └── archival/                # Resolved records
│
├── workflows/                   # Process definitions
│   ├── shadow-mode/             # Validation processes (TODO)
│   ├── approvals/               # Approval routing (TODO)
│   ├── sweeps/                  # Time-based sweep configs (TODO)
│   └── playbooks/               # Standardized responses (TODO)
│
├── reports/                     # Generated outputs
│   ├── executive/               # Owner dashboards
│   ├── teams/                   # Role-specific summaries
│   └── system/                  # Health and diagnostics
│
├── data/                        # Business data
│   ├── raw/                     # Fetched from integrations
│   ├── normalized/              # Processed business data
│   └── snapshots/               # Point-in-time captures
│
├── scripts/                     # Utilities
│   ├── bootstrap.sh             # Initial setup (COMPLETE)
│   ├── seed_workspace.py        # Data seeding (TODO)
│   ├── sync_close.py            # Manual CRM sync (TODO)
│   ├── sync_clickup.py          # Manual task sync (TODO)
│   └── run_shadow_cycle.py      # Shadow mode testing (TODO)
│
├── tests/                       # Testing
│   ├── unit/                    # Unit tests (TODO)
│   ├── integration/             # Integration tests (TODO)
│   ├── corridor/                # Corridor logic tests (TODO)
│   └── prediction/              # Prediction accuracy tests (TODO)
│
├── deployment/                  # Portability infrastructure
│   ├── local/                   # Local development (TODO)
│   ├── staging/                 # Staging environment (TODO)
│   ├── client-machine/          # Client deployment (TODO)
│   ├── docker/                  # Containerization (TODO)
│   └── checklists/              # Deployment procedures (TODO)
│
├── logs/                        # System logs (auto-created)
└── archive/                     # Deprecated experiments (TODO)
```

---

## Component Status

### ✅ Complete
- Root README.md
- .env.example with all integration credentials
- .gitignore
- requirements.txt
- docs/overview.md — comprehensive system overview
- docs/business-map.md — all 8 corridors defined
- docs/system-of-records.md — data authority mapping
- config/app.yaml — complete configuration template
- runtime/main.py — entry point with argument parsing
- runtime/loop/scheduler.py — trigger coordination
- runtime/loop/dispatcher.py — corridor routing
- runtime/loop/state_manager.py — persistent state
- runtime/loop/trigger_engine.py — trigger evaluation
- runtime/loop/approval_engine.py — approval workflows
- corridors/sales/corridor.md — complete sales corridor spec
- prediction/primitives/confidence.py — full confidence scoring implementation
- scripts/bootstrap.sh — environment setup script

### ⏳ TODO (High Priority)
- Integration adapters (google/, clickup/, close/, social/, vy/, pieces/)
- Corridor implementations (tasks.py, summaries.py for each)
- Prediction engines (lead quality, event complexity, etc.)
- Shadow mode validation workflows
- Approval routing configuration
- Reporting templates

### ⏳ TODO (Medium Priority)
- Remaining documentation (role-map.md, approvals.md, rollout-plan.md)
- Configuration for triggers, permissions, models
- Test suite
- Health check scripts

### ⏳ TODO (Lower Priority)
- Deployment infrastructure
- Containerization
- Additional prediction primitives
- Advanced corridor logic

---

## How to Use This Structure

### For Development

1. **Start here**: `README.md`
2. **Understand the business**: `docs/business-map.md`
3. **Understand data flow**: `docs/system-of-records.md`
4. **Set up environment**: `scripts/bootstrap.sh`
5. **Configure credentials**: `.env`
6. **Run in shadow mode**: `python runtime/main.py --mode shadow`

### For Extending the System

**Adding a new corridor**:
1. Create `corridors/[name]/corridor.md` (use `sales/corridor.md` as template)
2. Implement `corridors/[name]/tasks.py`
3. Add trigger definitions in `corridors/[name]/triggers.yaml`
4. Enable in `config/app.yaml`

**Adding a new prediction**:
1. Define in `prediction/engines/[name].py`
2. Use `prediction/primitives/confidence.py` for scoring
3. Test in shadow mode before promoting

**Adding a new integration**:
1. Create adapter in `integrations/[tool]/`
2. Add credentials to `.env.example`
3. Configure in `config/integrations/[tool].yaml`
4. Test connectivity in `scripts/test_integrations.py`

---

## Key Design Principles

### 1. Business-First Organization
- Organized around business functions (sales, operations, finance)
- Not organized around tools (ClickUp, Close, Google)
- Makes system understandable to non-technical stakeholders

### 2. Prediction-Centered Intelligence
- Prediction layer is separate from business logic
- Confidence scoring is explicit and structured
- Historical accuracy tracking enables continuous improvement

### 3. Integration Modularity
- Each integration is self-contained
- Failures in one integration don't cascade
- Easy to add/remove/replace integrations

### 4. Runtime Separation
- Runtime engine is independent of corridors
- Corridors are independent of each other
- Clear separation of concerns

### 5. Deployment Portability
- Configuration is external to code
- Environment-specific settings isolated
- Easy to move from development to production

---

## Execution Modes

### Shadow Mode (Observation Only)
```bash
python runtime/main.py --mode shadow
```
- System observes and generates recommendations
- Nothing executes automatically
- All outputs require human approval
- Used for validation before promotion

### Draft Mode (Suggestion Generation)
```bash
python runtime/main.py --mode draft
```
- System generates tasks, drafts, and suggestions
- Submits for human approval
- Approved items execute
- Used for semi-autonomous operation

### Autonomous Mode (Approved Actions Execute)
```bash
python runtime/main.py --mode autonomous
```
- Approved action types execute automatically
- High-stakes actions still require approval
- Used after validation in shadow/draft modes

---

## Integration Points

### Google Suite
- **Sheets**: Business data (leads, events, finance, staff, partners)
- **Calendar**: Event schedule, operational timeline
- **Drive**: Document storage (if needed)
- **Gmail**: Communication monitoring (if enabled)

### ClickUp
- **Tasks**: Work item management
- **Lists**: Organized by corridor (sales, operations, admin)
- **Webhooks**: Real-time task updates

### Close CRM
- **Leads**: Contact and pipeline management
- **Opportunities**: Deal tracking
- **Activities**: Interaction history
- **Webhooks**: Real-time lead/opportunity updates

### Social Media
- **YouTube**: Content and engagement
- **TikTok**: Content and engagement
- **Instagram**: Content and engagement
- **LinkedIn**: Professional content
- **Twitter/X**: Real-time engagement

### VY (Mediation Layer)
- **Screenshot observation**: Visual monitoring
- **UI execution**: Browser-based actions
- **Shell bridging**: Terminal operations

### Pieces (Memory/Context)
- **Persistent memory**: Long-term context
- **Code snippets**: Implementation patterns
- **Context recall**: Historical reference

---

## Next Steps

### Immediate (This Week)
1. Review this structure with client and tech person
2. Finalize integration credentials in `.env`
3. Implement Google Sheets integration (highest priority data source)
4. Implement Close CRM integration (lead management)
5. Test one corridor end-to-end (recommend Sales)

### Short-Term (Next 2 Weeks)
1. Implement remaining integrations (ClickUp, Calendar, Social)
2. Complete all 8 corridor implementations
3. Build out prediction engines (lead quality, event complexity)
4. Deploy in shadow mode for validation

### Medium-Term (Next Month)
1. Validate shadow mode predictions vs manual workflows
2. Promote high-accuracy behaviors to draft mode
3. Build reporting infrastructure
4. Prepare for autonomous mode (validated actions only)

---

## Support Resources

- **Documentation**: All `.md` files in `docs/`
- **Configuration**: `config/app.yaml` with inline comments
- **Examples**: `corridors/sales/` and `prediction/primitives/confidence.py`
- **Bootstrap**: `scripts/bootstrap.sh` for environment setup

---

## Questions?

Common questions and where to find answers:

**Q: Which system is authoritative for X data?**
A: See `docs/system-of-records.md`

**Q: What does corridor Y do?**
A: See `docs/business-map.md` and `corridors/Y/corridor.md`

**Q: How do I add a new integration?**
A: See "Adding a new integration" section above

**Q: What's the difference between shadow/draft/autonomous modes?**
A: See "Execution Modes" section above

**Q: How does confidence scoring work?**
A: See `prediction/primitives/confidence.py` for complete implementation
