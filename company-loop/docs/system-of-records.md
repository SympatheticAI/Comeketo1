# System of Records — Data Authority Mapping

This document defines **which system is authoritative** for each class of business data. When conflicts arise between systems, the system of record is considered correct.

This is critical for preventing data inconsistencies, especially in spreadsheet-native businesses where information often lives in multiple places.

---

## Core Principle

**System of Record = Source of Truth**

- The system designated as "system of record" is the **authoritative source**
- Other systems may cache or reference this data, but **cannot override it**
- Updates to authoritative data should ideally happen **only in the system of record**
- The loop **reads** from system of record and **writes** to secondary/advisory systems (unless explicitly approved otherwise)

---

## Sales & Lead Management

### Leads and Opportunities
**System of Record**: **Close CRM**

- Lead contact information
- Opportunity stage and value
- Activity history
- Deal ownership

**Secondary Sources**:
- Google Sheets may duplicate lead data for reporting
- ClickUp may reference lead IDs for task context

**Read/Write Rules**:
- Loop reads leads from Close
- Loop may create ClickUp tasks linked to leads
- Loop may create Google Sheet summaries
- Loop **does not modify Close lead data without approval**

### Lead Source Attribution
**System of Record**: **Google Sheets** (Source Tracking sheet)

- Where lead originated (referral, web, event, partner)
- Source quality scores
- Attribution details

**Secondary Sources**:
- Close CRM custom fields may store source data
- ClickUp may reference source for context

**Read/Write Rules**:
- Loop reads source data from Google Sheets
- Loop may update source scores based on conversion outcomes
- Loop writes source reference to Close custom field

---

## Events & Operations

### Event Schedule
**System of Record**: **Google Calendar**

- Event date and time
- Location
- Client name
- Event type

**Secondary Sources**:
- Google Sheets may include event details
- ClickUp may reference events for task context
- Close opportunities may link to events

**Read/Write Rules**:
- Loop reads event schedule from Calendar
- Loop **does not create or modify calendar events without approval**
- Loop may create ClickUp prep tasks linked to events
- Loop may update Google Sheets event tracking

### Event Details (menu, guest count, requirements)
**System of Record**: **Google Sheets** (Event Details sheet)

- Menu selections
- Guest count
- Special requirements
- Equipment needs
- Client preferences

**Secondary Sources**:
- Calendar event descriptions may summarize details
- ClickUp tasks may reference requirements

**Read/Write Rules**:
- Loop reads event details from Google Sheets
- Loop may flag missing or inconsistent information
- Loop **does not modify event details without approval**

---

## Finance

### Revenue Projections
**System of Record**: **Google Sheets** (Finance Tracking sheet)

- Projected income by week/month
- Expected expenses
- Cash flow forecasts

**Secondary Sources**:
- Close deal values inform projections
- Calendar events provide timing

**Read/Write Rules**:
- Loop reads deal values from Close
- Loop reads event dates from Calendar
- Loop **writes** updated projections to Google Sheets (approved automation)
- Loop generates finance summaries for executive review

### Payment Status
**System of Record**: **Google Sheets** (Payment Tracking sheet)

- Deposit received/due
- Final payment received/due
- Payment method
- Outstanding balances

**Secondary Sources**:
- Close may track payment stage
- ClickUp may have payment-related tasks

**Read/Write Rules**:
- Loop reads payment data from Google Sheets
- Loop may generate payment alerts
- Loop **does not modify payment status without approval**

---

## Partnerships & Referrals

### Partner Contact Information
**System of Record**: **Google Sheets** (Partner List sheet)

- Partner name and type (venue, planner, etc.)
- Contact information
- Relationship owner (assigned rep)
- Last contact date

**Secondary Sources**:
- Close may have partner contacts duplicated
- ClickUp may reference partner names

**Read/Write Rules**:
- Loop reads partner data from Google Sheets
- Loop may update "last contact" timestamp
- Loop may create ClickUp follow-up tasks
- Loop **does not modify partner contact info without approval**

### Referral Tracking
**System of Record**: **Google Sheets** (Referral Tracking sheet)

- Referral source
- Date referred
- Lead outcome
- Source performance scores

**Secondary Sources**:
- Close lead records may reference source
- Google Sheets source tracking may link here

**Read/Write Rules**:
- Loop reads referral data from Google Sheets
- Loop may update referral outcome when lead closes
- Loop may update source performance scores

---

## Workforce & Staffing

### Staff Roster
**System of Record**: **Google Sheets** (Staff Roster sheet)

- Staff member names
- Contact information
- Role/position
- Availability
- Hourly rate (if tracked)

**Secondary Sources**:
- Calendar may show staff assignments
- ClickUp may reference staff for tasks

**Read/Write Rules**:
- Loop reads staff roster from Google Sheets
- Loop **does not modify staff records without approval**
- Loop may flag staffing conflicts or gaps

### Staff Assignments
**System of Record**: **Google Calendar** (event-level assignments)

- Which staff are assigned to which events
- Event timing and location

**Secondary Sources**:
- Google Sheets may duplicate for reporting
- ClickUp may reference assignments

**Read/Write Rules**:
- Loop reads assignments from Calendar
- Loop may generate staffing recommendations
- Loop **does not modify assignments without approval**

### Labor Hours
**System of Record**: **Google Sheets** (Labor Tracking sheet)

- Worked hours by staff member
- Weekly/monthly aggregates
- Labor cost tracking

**Secondary Sources**:
- Calendar events provide scheduled hours
- Payroll system (if separate) may import data

**Read/Write Rules**:
- Loop reads labor data from Google Sheets
- Loop may generate labor reports and summaries
- Loop **does not modify labor records without approval**

---

## Procurement & Prep

### Recipe Database
**System of Record**: **Google Sheets** (Recipe/Ingredient sheet)

- Menu items
- Ingredient lists
- Quantities per serving
- Prep instructions

**Secondary Sources**:
- Event details sheets may reference recipes
- ClickUp may reference for prep tasks

**Read/Write Rules**:
- Loop reads recipe data from Google Sheets
- Loop uses recipe data to generate shopping lists
- Loop **does not modify recipes without approval**

### Shopping Lists
**System of Record**: **Generated by Loop** (transient)

- Aggregated ingredient needs
- Calculated quantities
- Organized by supplier/category

**Secondary Sources**:
- May be exported to Google Sheets for human use
- May be referenced in ClickUp prep tasks

**Read/Write Rules**:
- Loop generates shopping lists from recipes + event details
- Loop may write lists to Google Sheets or ClickUp
- Lists are regenerated as needed (not persistent authority)

---

## Task Management

### Task Assignments
**System of Record**: **ClickUp**

- Task descriptions
- Assignees
- Due dates
- Status (open, in progress, complete)
- Task dependencies

**Secondary Sources**:
- Google Sheets may summarize tasks for reporting
- Loop memory may track unresolved tasks

**Read/Write Rules**:
- Loop reads task status from ClickUp
- Loop **may create tasks** (approved automation)
- Loop **does not modify or delete tasks without approval**
- Loop may update task notes or descriptions if explicitly approved

---

## Social Media

### Published Content
**System of Record**: **Social Media Platforms** (YouTube, TikTok, Instagram, LinkedIn, Twitter)

- Post content
- Publish date/time
- Engagement metrics (likes, comments, views)

**Secondary Sources**:
- Google Sheets may track content calendar
- ClickUp may have content production tasks

**Read/Write Rules**:
- Loop reads engagement data from platforms
- Loop **does not publish content without approval**
- Loop may generate content drafts
- Loop may update Google Sheets content tracking

### Content Calendar
**System of Record**: **Google Sheets** (Content Calendar sheet)

- Planned posts
- Platform assignments
- Campaign associations
- Publish schedule

**Secondary Sources**:
- ClickUp may reference for production tasks
- Platforms show actual published content

**Read/Write Rules**:
- Loop reads content plan from Google Sheets
- Loop may generate publishing reminders
- Loop may update calendar with performance notes
- Loop **does not modify planned content without approval**

---

## Memory & System State

### Active Obligations
**System of Record**: **Loop Memory** (`memory/active/`)

- Unresolved tasks
- Pending approvals
- Outstanding follow-ups
- System-tracked obligations

**Secondary Sources**:
- ClickUp may have overlapping tasks
- Google Sheets may reference same obligations

**Read/Write Rules**:
- Loop owns this data
- Loop updates as obligations are created/resolved
- Loop exports to ClickUp or reporting as needed

### Corridor State
**System of Record**: **Loop Memory** (`memory/corridor/`)

- Last processed state for each corridor
- Recent summaries
- Trigger history

**Secondary Sources**:
- None (internal to loop)

**Read/Write Rules**:
- Loop owns and manages corridor state
- Used for continuity across sweeps

---

## Conflict Resolution Rules

### When Systems Disagree

If the same data exists in multiple places and conflicts:

1. **Identify the system of record** from this document
2. **Trust the system of record** as authoritative
3. **Flag the inconsistency** in logs and reports
4. **Suggest correction** to bring secondary systems in sync
5. **Do not auto-resolve** conflicts without human approval

### Example Conflict Scenarios

**Scenario**: Event guest count differs between Calendar and Google Sheets
- **System of Record**: Google Sheets (Event Details)
- **Resolution**: Trust Sheets value, flag Calendar discrepancy, suggest sync

**Scenario**: Lead contact info differs between Close and Google Sheets
- **System of Record**: Close CRM
- **Resolution**: Trust Close value, flag Sheets discrepancy, suggest update

**Scenario**: Staff assignment differs between Calendar and Google Sheets
- **System of Record**: Google Calendar
- **Resolution**: Trust Calendar value, flag Sheets discrepancy, suggest sync

---

## Data Flow Map

### Typical Data Flow for New Event

1. **Lead enters Close** (system of record for lead data)
2. **Opportunity progresses** (Close)
3. **Event booked** → Calendar event created (system of record for schedule)
4. **Event details added** → Google Sheets Event Details (system of record for requirements)
5. **Loop generates**:
   - Revenue projection → Google Sheets Finance (system of record for projections)
   - Staffing need → references Calendar + Sheets Roster
   - Shopping list → generated from Sheets Recipes + Event Details
   - Prep tasks → created in ClickUp (system of record for tasks)

### Typical Data Flow for Partner Referral

1. **Referral received** → logged in Google Sheets Referral Tracking (system of record)
2. **Lead created in Close** → Close CRM (system of record for lead)
3. **Source attribution added** → Google Sheets Source Tracking (system of record for attribution)
4. **Loop tracks**:
   - Referral outcome when lead closes
   - Partner performance score update
   - Partner relationship health

---

## System of Record Summary Table

| Data Type | System of Record | Secondary Sources | Loop Write Permission |
|-----------|-----------------|-------------------|---------------------|
| Leads & Opportunities | Close CRM | Sheets, ClickUp | Approval Required |
| Lead Source Attribution | Google Sheets | Close custom fields | Yes (approved) |
| Event Schedule | Google Calendar | Sheets, ClickUp | Approval Required |
| Event Details | Google Sheets | Calendar, ClickUp | Approval Required |
| Revenue Projections | Google Sheets | Close, Calendar | Yes (approved) |
| Payment Status | Google Sheets | Close, ClickUp | Approval Required |
| Partner Contacts | Google Sheets | Close | Approval Required |
| Referral Tracking | Google Sheets | Close | Yes (approved) |
| Staff Roster | Google Sheets | Calendar, ClickUp | Approval Required |
| Staff Assignments | Google Calendar | Sheets | Approval Required |
| Labor Hours | Google Sheets | Calendar | Approval Required |
| Recipe Database | Google Sheets | ClickUp | Approval Required |
| Shopping Lists | Loop (generated) | Sheets, ClickUp | Yes (transient) |
| Tasks | ClickUp | Sheets, Loop memory | Yes (create only) |
| Social Media Posts | Platforms | Sheets | Approval Required |
| Content Calendar | Google Sheets | ClickUp | Approval Required |
| Active Obligations | Loop Memory | ClickUp, Sheets | Yes (loop-owned) |
| Corridor State | Loop Memory | None | Yes (loop-owned) |

---

## Next Steps

1. Review [Role Map](role-map.md) to understand who owns which systems
2. Check [Approval Rules](approvals.md) for write permission details
3. Examine corridor-specific data handling in `corridors/[name]/rules.yaml`
