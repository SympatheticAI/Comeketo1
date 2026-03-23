# System Overview — Company Loop

## Purpose

The Company Loop is an autonomous business intelligence system designed to:

1. **Unify fragmented business systems** — Integrate data from sales (Close), operations (Google Calendar/Sheets), task management (ClickUp), and social media into a coherent operational picture
2. **Maintain continuous awareness** — Monitor and synthesize information across all business surfaces in real-time
3. **Reduce dropped tasks and missed follow-ups** — Automatically detect gaps, staleness, and time-sensitive obligations
4. **Generate actionable intelligence** — Produce summaries, task suggestions, and recommendations grounded in actual business state
5. **Enable measured automation** — Promote proven behaviors from observation → suggestion → approved execution

---

## What This System Is

### Business Intelligence Substrate
- Continuous monitoring across sales, operations, finance, partnerships, staffing, and media
- Pattern recognition for stale leads, event complexity, staffing pressure, partner drift, cashflow risk
- Predictive scoring based on historical outcomes and current state

### Shadow-First Validation Platform
- Runs in parallel with existing manual workflows
- Compares system judgments against human decisions
- Builds trust through demonstrated accuracy before automation
- Explicit promotion criteria for each behavior

### Approval-Gated Execution Layer
- Clear distinction between safe autonomous actions and high-stakes decisions
- Human approval required for external communication, financial changes, CRM updates, public posts
- Audit logging of all actions and decisions

### Portable Template Architecture
- Designed for this specific catering/event business first
- Structured for extraction into reusable template for similar businesses
- Parameterized separation of generic vs client-specific logic

---

## What This System Is Not

### Not a Replacement for Human Staff
- Augments human judgment, does not replace it
- Handles routine monitoring, alerting, and low-stakes tasks
- Escalates complex decisions to appropriate human owners
- Preserves final authority with business owners and managers

### Not Uncontrolled Autonomous Execution
- Every autonomous action is explicitly approved in configuration
- High-stakes actions always require human review
- Shadow mode validation required before promotion
- Clear rollback and override mechanisms

### Not an Experimental AI Sandbox
- Production-grade reliability expectations
- Explicit error handling and graceful degradation
- Monitoring and health checks
- Defined rollout phases with validation gates

### Not a One-Off Automation Pile
- Governed architecture with clear separation of concerns
- Modular corridors for each business function
- Reusable prediction primitives
- Version-controlled configuration

---

## Core Architecture Layers

### 1. Runtime Layer
**Location**: `runtime/`

The execution engine that orchestrates all system activity.

**Components**:
- **Scheduler**: Time-based and event-based trigger coordination
- **Dispatcher**: Routes work to appropriate corridor agents
- **State Manager**: Maintains system state and context
- **Trigger Engine**: Evaluates conditions and fires corridor logic
- **Approval Engine**: Manages human approval workflows

### 2. Integration Layer
**Location**: `integrations/`

Tool-specific adapters that abstract away API complexity.

**Integrations**:
- **Google**: Sheets (business data), Calendar (schedule), Drive, Gmail
- **ClickUp**: Task management, workflow coordination
- **Close**: Sales pipeline, leads, opportunities
- **Social Media**: YouTube, TikTok, Instagram, LinkedIn, Twitter
- **VY**: Screenshot-grounded observation and mediated execution
- **Pieces**: Persistent memory and context retention

### 3. Corridor Layer
**Location**: `corridors/`

Business-specific logic organized by functional area.

**Corridors**:
- **Sales**: Lead management, conversion tracking, follow-up generation
- **Operations**: Event scheduling, complexity assessment, logistics
- **Finance**: Cash flow projection, reconciliation, payment tracking
- **Partnerships**: Venue/planner relationships, referral management
- **Workforce**: Labor reports, scheduling, pressure detection
- **Procurement**: Shopping lists, prep requirements
- **Marketing**: Content support, trend capture, audience intelligence
- **Executive**: Owner dashboarding, decision support

### 4. Prediction Layer
**Location**: `prediction/`

The intelligence moat — sophisticated scoring, confidence, and trajectory modeling.

**Components**:
- **Primitives**: Core prediction building blocks (score, confidence, horizon, trajectory)
- **Engines**: Domain-specific prediction models (lead quality, event complexity, partner drift, etc.)
- **Features**: Business signal extraction from integrated data
- **Evaluation**: Metrics, false positive review, promotion rules
- **Memory**: Historical outcomes, learned weights

### 5. Memory Layer
**Location**: `memory/`

Persistent state beyond session boundaries.

**Memory Classes**:
- **Active**: Current obligations, unresolved tasks, approval queue
- **Corridor**: State snapshots for each business function
- **Relational**: Venue/partner/client relationship history
- **Summaries**: Daily and weekly narrative continuity
- **Archival**: Resolved and historical records

### 6. Workflow Layer
**Location**: `workflows/`

Process definitions and operational patterns.

**Workflows**:
- **Shadow Mode**: Validation and comparison logic
- **Approvals**: Approval routing and requirements
- **Sweeps**: Time-based monitoring cadences
- **Playbooks**: Standardized responses to common patterns

### 7. Reporting Layer
**Location**: `reports/`

Generated outputs for humans.

**Report Types**:
- **Executive**: Daily briefs, weekly summaries, urgent exceptions
- **Team**: Role-specific task lists and summaries
- **System**: Health monitoring, mismatch logging, promotion reviews

---

## Operating Principles

### 1. Shadow Mode First
Every new behavior starts in observation-only mode. The system mirrors manual workflows, compares its judgments, and builds a track record before promotion to autonomous execution.

### 2. Explicit Approval Gates
High-stakes actions always require human approval:
- External client communication
- Financial record modifications
- Public social media posts
- Staff assignment changes
- Critical CRM updates

### 3. Confidence-Based Execution
Every prediction and recommendation includes explicit confidence scoring. Low-confidence outputs are flagged for human review. High-confidence outputs may be automated if validated.

### 4. Graceful Degradation
Integration failures, API errors, and unexpected states are handled gracefully. The system continues operating with reduced functionality rather than failing catastrophically.

### 5. Audit Everything
All actions, decisions, and state changes are logged with timestamps, context, and reasoning. This enables debugging, compliance, and continuous improvement.

### 6. Business-First Organization
The system is organized around business functions (sales, operations, finance) rather than tools (ClickUp, Close, Google). This makes it portable and understandable to non-technical stakeholders.

---

## Deployment Philosophy

### Phase 1: Environment Setup
- Establish connectivity to all integration points
- Validate read access to business data
- Test approval and notification pathways

### Phase 2: Observation Only
- Monitor business surfaces without taking action
- Generate summaries and insights
- Build baseline for comparison

### Phase 3: Draft Generation
- Create suggested tasks, follow-ups, and updates
- Submit for human approval
- Track approval/rejection patterns

### Phase 4: Validated Automation
- Promote proven behaviors to autonomous execution
- Maintain human oversight for edge cases
- Continuous evaluation of accuracy

### Phase 5: Template Extraction
- Document generic vs client-specific patterns
- Package reusable components
- Create deployment guide for similar businesses

---

## Success Metrics

### Operational Metrics
- **Task completion rate**: Percentage of generated tasks marked complete
- **Follow-up effectiveness**: Conversion improvement from automated reminders
- **Stale lead reduction**: Decrease in leads going cold
- **Event readiness**: Reduction in last-minute preparation issues
- **Partner engagement**: Improvement in relationship check-in cadence

### System Metrics
- **Prediction accuracy**: Percentage of correct judgments vs human baseline
- **False positive rate**: Incorrect alerts or recommendations
- **Coverage**: Percentage of business activity monitored
- **Latency**: Time from event to system awareness
- **Uptime**: System availability and reliability

### Business Metrics
- **Lead conversion**: Improvement in close rates
- **Operational efficiency**: Reduction in dropped tasks
- **Revenue visibility**: Accuracy of cash flow projections
- **Staff utilization**: Reduction in scheduling conflicts
- **Client satisfaction**: Feedback on communication quality

---

## Next Steps

1. Read [Business Map](business-map.md) for detailed corridor definitions
2. Review [System of Records](system-of-records.md) for data authority mapping
3. Check [Role Map](role-map.md) for human ownership structure
4. Examine [Approval Rules](approvals.md) for execution gates
5. Follow [Rollout Plan](rollout-plan.md) for deployment sequence
