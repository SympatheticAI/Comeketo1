# Sales Corridor

## Purpose
Manage lead lifecycle from initial contact through conversion, with focus on source attribution, ownership, follow-up timing, and tasting-linked conversion.

---

## Data Sources

### Primary: Close CRM
- **Leads**: Contact information, source, status
- **Opportunities**: Qualified leads with event details
- **Activities**: Calls, emails, meetings, notes
- **Custom fields**: Source attribution, tasting scheduled, rep assignment

### Secondary: Google Sheets
- Lead source tracking
- Attribution data
- Sales performance metrics

### Tertiary: Google Calendar
- Tasting appointments
- Consultation meetings
- Follow-up reminders

---

## Business Objects

### Lead
```yaml
id: string (Close lead ID)
name: string
email: string
phone: string
source: string (referral, web, event, partner)
status: string (new, contacted, qualified, lost, won)
assigned_rep: string
created_at: datetime
last_activity_at: datetime
tasting_scheduled: boolean
tasting_date: datetime (optional)
```

### Opportunity
```yaml
id: string (Close opportunity ID)
lead_id: string
event_date: datetime
event_type: string (wedding, corporate, private, etc.)
guest_count: int
value: float
stage: string (quote, proposal, negotiation, won, lost)
probability: float (0-100)
```

### Source
```yaml
name: string (partner name, campaign, channel)
type: string (venue, planner, web, referral, event)
leads_generated: int
conversion_rate: float
avg_deal_value: float
quality_score: float (0-10)
```

---

## Trigger Definitions

### Time-Based Triggers

#### Stale Lead Detection (Realtime — Every 5 min)
```yaml
trigger_id: stale_lead_detection
cadence: realtime (5 min)
condition: |
  lead.status IN ['new', 'contacted', 'qualified']
  AND (NOW() - lead.last_activity_at) > 7 days
  AND NOT EXISTS (
    SELECT 1 FROM tasks
    WHERE lead_id = lead.id
    AND status = 'open'
  )
actions:
  - Generate follow-up reminder
  - Create ClickUp task for assigned rep
  - Flag in daily brief
approval_required: false (low-stakes task creation)
```

#### Tasting Conversion Tracking (Daily)
```yaml
trigger_id: tasting_conversion_tracking
cadence: daily
condition: |
  lead.tasting_scheduled = true
  AND lead.tasting_date < NOW() - 2 days
  AND NOT EXISTS (
    SELECT 1 FROM opportunities
    WHERE lead_id = lead.id
  )
actions:
  - Generate conversion check reminder
  - Create follow-up task for rep
  - Update source quality score if lost
approval_required: false
```

### Event-Based Triggers

#### New Lead Created
```yaml
trigger_id: new_lead_created
event_type: webhook (Close CRM)
condition: |
  event.type = 'lead.created'
actions:
  - Extract source attribution
  - Assign to rep based on rules
  - Create initial follow-up task
  - Add to daily brief
approval_required: false
```

#### Opportunity Stage Change
```yaml
trigger_id: opportunity_stage_change
event_type: webhook (Close CRM)
condition: |
  event.type = 'opportunity.updated'
  AND event.changes.stage IS NOT NULL
actions:
  - Update revenue projection
  - Notify relevant corridor (operations if won, finance for projections)
  - Update source performance if won/lost
  - Generate summary for executive brief
approval_required: false
```

---

## Corridor Logic

### 1. Stale Lead Detection

**Purpose**: Identify leads falling through cracks

**Logic**:
```python
async def detect_stale_leads():
    """
    Find leads with no activity in threshold window.

    Steps:
    1. Query Close for leads with status in [new, contacted, qualified]
    2. Filter where last_activity_at > 7 days ago
    3. Check for existing open tasks (avoid duplicate reminders)
    4. Generate follow-up recommendations
    5. Create ClickUp tasks for assigned reps
    6. Log for daily brief
    """
    # Implementation in corridors/sales/tasks.py
    pass
```

**Outputs**:
- ClickUp task: "Follow up with [Lead Name]"
- Daily brief item: "X stale leads requiring attention"
- Prediction: Lead quality score adjustment

### 2. Source Attribution

**Purpose**: Track where leads originate, measure source quality

**Logic**:
```python
async def attribute_source(lead):
    """
    Determine lead source and update tracking.

    Steps:
    1. Extract source from lead custom field or UTM parameters
    2. Classify source type (venue, planner, web, referral, event)
    3. Update source tracking sheet
    4. Calculate source quality score
    5. Link to partner record if applicable
    """
    # Implementation in corridors/sales/tasks.py
    pass
```

**Outputs**:
- Google Sheets: Source tracking updated
- Close custom field: Source attribution recorded
- Partner relationship: Referral logged

### 3. Tasting Conversion Tracking

**Purpose**: Monitor conversion from tasting to booking

**Logic**:
```python
async def track_tasting_conversion():
    """
    Monitor tastings and conversion outcomes.

    Steps:
    1. Query leads with tasting_scheduled = true
    2. Check if opportunity created after tasting
    3. Calculate time from tasting to close
    4. Update source quality if conversion happens
    5. Flag lost tastings for review
    """
    # Implementation in corridors/sales/tasks.py
    pass
```

**Outputs**:
- Source quality score update
- Conversion pattern analysis
- Rep performance metrics

### 4. Rep Load Balancing

**Purpose**: Distribute leads fairly across sales reps

**Logic**:
```python
async def balance_rep_load():
    """
    Monitor lead distribution and workload.

    Steps:
    1. Count active leads per rep
    2. Calculate workload score (lead count + opportunity count)
    3. Identify uneven distribution
    4. Suggest reassignment if threshold exceeded
    """
    # Implementation in corridors/sales/tasks.py
    pass
```

**Outputs**:
- Weekly summary: Rep workload report
- Suggestion: Reassignment recommendations (approval required)

---

## Prediction Integration

### Lead Quality Score
**Predictor**: `prediction/engines/lead_prediction.py`

**Inputs**:
- Source type and history
- Lead responsiveness (time to first response)
- Engagement level (email opens, call answers)
- Event type and timing
- Guest count (if provided)

**Output**:
- Quality score (0-10)
- Conversion probability (0-100%)
- Recommended follow-up timing

**Usage**: Prioritize rep time on high-quality leads

---

## Allowed Outputs

### Observation Mode
- Lead summaries and lists
- Stale lead reports
- Source performance analysis
- Conversion metrics

### Draft Mode
- Follow-up email drafts
- Task suggestions (not created)
- Lead prioritization recommendations

### Approved Automation
- ClickUp task creation for follow-ups
- Internal notes in Close CRM
- Lead tagging and categorization
- Source tracking updates
- Daily/weekly summary generation

---

## Approval Required For

- Sending outbound client communication (emails, texts)
- Changing lead ownership/assignment
- Modifying opportunity value or stage
- Archiving or deleting leads
- Updating contact information

---

## Integration Points

### Inputs from Other Corridors
- **Partnerships**: Referral events create leads
- **Marketing**: Campaign performance informs source quality

### Outputs to Other Corridors
- **Operations**: Booked events (won opportunities) flow to calendar
- **Finance**: Deal values and expected close dates for revenue projection
- **Executive**: Summary statistics and urgent exceptions

---

## Metrics & KPIs

### Corridor Performance
- Lead response time (time from creation to first contact)
- Stale lead rate (% of leads inactive > 7 days)
- Conversion rate (leads to opportunities, opportunities to bookings)
- Average deal value
- Sales cycle length (lead creation to booking)

### Source Performance
- Lead volume by source
- Conversion rate by source
- Average deal value by source
- Source quality score trends

### Rep Performance
- Lead load per rep
- Conversion rate per rep
- Average deal value per rep
- Response time per rep

---

## Shadow Mode Validation

### Comparison Targets
- **Stale lead detection**: Compare system-identified stale leads vs rep-identified
- **Follow-up timing**: Compare system recommendations vs actual rep behavior
- **Source quality scores**: Compare predicted quality vs actual conversion

### Promotion Criteria
- **Stale lead detection**: 90%+ accuracy (system identifies same leads as reps)
- **Task creation**: 80%+ task completion rate (reps complete generated tasks)
- **Source scoring**: 85%+ correlation with actual conversion rates

---

## Configuration Files

- `rules.yaml`: Corridor-specific rules and thresholds
- `triggers.yaml`: Trigger definitions and schedules
- `tasks.py`: Python implementation of corridor logic
- `summaries.py`: Summary generation logic
- `templates/`: Email/task templates

---

## Next Steps

1. Implement corridor logic in `corridors/sales/tasks.py`
2. Define trigger schedules in `corridors/sales/triggers.yaml`
3. Create templates in `corridors/sales/templates/`
4. Develop lead quality predictor in `prediction/engines/lead_prediction.py`
