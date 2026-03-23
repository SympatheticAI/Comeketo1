# Business Map — Functional Corridors

This document defines the business structure as understood by the system. Each corridor represents a functional area with its own data sources, triggers, outputs, and approval requirements.

---

## Corridor 1: Sales

### Purpose
Manage lead lifecycle from initial contact through conversion, with focus on source attribution, ownership, follow-up timing, and tasting-linked conversion.

### Primary Data Sources
- **Close CRM**: Leads, opportunities, contacts, activities
- **Google Sheets**: Lead source tracking, attribution data
- **Google Calendar**: Tasting appointments, consultation meetings

### Key Business Objects
- **Lead**: Potential client with contact information
- **Opportunity**: Qualified lead with event details
- **Tasting**: Scheduled food/service demonstration
- **Source**: Where the lead originated (referral, web, event, partner)
- **Rep**: Assigned salesperson

### Typical Triggers
- New lead created in Close
- Lead inactive for 7+ days (stale detection)
- Tasting scheduled (conversion opportunity)
- Opportunity stage change
- Partner referral received

### Corridor Logic
**Stale Lead Detection**:
- Identify leads with no activity in threshold window (configurable, default 7 days)
- Check for scheduled follow-ups or pending tasks
- Generate follow-up reminder or draft outreach

**Source Attribution**:
- Track lead origin (referral source, venue, planner, marketing campaign)
- Link source to conversion outcomes
- Score source quality over time

**Tasting Conversion Tracking**:
- Monitor leads with scheduled tastings
- Track conversion rate from tasting to booking
- Identify patterns in tasting-to-close timing

**Rep Load Balancing**:
- Track lead distribution across sales reps
- Identify uneven workloads
- Suggest reassignment if needed

### Allowed Outputs
- **Observation Mode**: Lead summaries, stale lead reports, source performance
- **Draft Mode**: Follow-up email drafts, task suggestions
- **Approved Automation**: ClickUp task creation, internal notes, lead tagging

### Approval Required For
- Sending outbound client communication
- Changing lead ownership
- Modifying opportunity value or stage
- Archiving or deleting leads

---

## Corridor 2: Operations

### Purpose
Ensure event readiness through job intake, complexity assessment, staffing coordination, and logistical preparation.

### Primary Data Sources
- **Google Calendar**: Event/job schedule with timing and location
- **Google Sheets**: Event details, client requirements, equipment needs
- **ClickUp**: Task tracking for event preparation

### Key Business Objects
- **Event/Job**: Scheduled catering engagement
- **Complexity Score**: Assessment of event difficulty (guest count, menu, location, equipment)
- **Staffing Requirement**: Number and type of staff needed
- **Prep Checklist**: Food, equipment, transport requirements
- **Event Timeline**: Setup, service, breakdown schedule

### Typical Triggers
- Event created or updated in calendar
- Event approaching (7 days, 3 days, 1 day alerts)
- Staffing shortfall detected
- Equipment conflict identified
- Prep checklist incomplete

### Corridor Logic
**Event Complexity Assessment**:
- Analyze guest count, menu type, location distance, equipment needs
- Generate complexity score (1-10)
- Flag high-complexity events for additional attention

**Staffing Recommendation**:
- Calculate required staff based on complexity, guest count, service type
- Check staff availability against scheduled events
- Identify conflicts or shortfalls

**Event Readiness Monitoring**:
- Track completion of prep tasks
- Alert on missing information (menu finalization, headcount confirmation)
- Generate day-of operational summary

**Logistics Coordination**:
- Identify transport requirements
- Check equipment availability
- Flag travel time and setup duration

### Allowed Outputs
- **Observation Mode**: Event readiness reports, staffing summaries, complexity scores
- **Draft Mode**: Prep checklists, staffing recommendations, timeline drafts
- **Approved Automation**: ClickUp task creation, calendar event tagging, internal alerts

### Approval Required For
- Modifying event details in calendar
- Changing staffing assignments
- Canceling or rescheduling events
- Client communication about logistics

---

## Corridor 3: Finance

### Purpose
Maintain cash flow visibility through revenue projections, expense tracking, payment monitoring, and reconciliation support.

### Primary Data Sources
- **Google Sheets**: Financial tracking, projected revenue, expenses
- **Close**: Deal values, expected close dates
- **Google Calendar**: Booked events with payment schedules

### Key Business Objects
- **Projected Revenue**: Expected income from booked events
- **Expected Expense**: Anticipated costs (food, labor, equipment)
- **Payment Schedule**: Deposit and final payment timing
- **Cash Flow Projection**: Weekly/monthly income and outflow forecast

### Typical Triggers
- New event booked (revenue projection update)
- Payment due date approaching
- Missed or late payment detected
- Large expense upcoming
- Weekly reconciliation cycle

### Corridor Logic
**Revenue Projection**:
- Extract deal values from Close
- Map to event dates from calendar
- Generate weekly/monthly revenue forecast

**Payment Monitoring**:
- Track deposit and final payment schedules
- Alert on upcoming due dates
- Flag late or missing payments

**Expense Visibility**:
- Identify recurring costs (payroll, supplies, overhead)
- Track event-specific expenses
- Project cash needs for upcoming period

**Weekly Reconciliation Support**:
- Generate expected vs actual comparison
- Highlight discrepancies
- Produce finance summary for owner review

### Allowed Outputs
- **Observation Mode**: Cash flow projections, payment alerts, expense summaries
- **Draft Mode**: Reconciliation reports, payment reminders
- **Approved Automation**: Internal financial alerts, forecast updates

### Approval Required For
- Modifying financial records
- Sending payment reminders to clients
- Updating revenue projections
- Making expense commitments

---

## Corridor 4: Partnerships

### Purpose
Manage venue, planner, and referral source relationships through systematic check-ins, performance tracking, and relationship maintenance.

### Primary Data Sources
- **Google Sheets**: Partner contact list, relationship history, referral tracking
- **Close**: Leads attributed to specific partners
- **Google Calendar**: Partner meetings and check-ins

### Key Business Objects
- **Partner**: Venue, event planner, or referral source
- **Partner Type**: Venue, planner, past client, industry contact
- **Referral Count**: Number of leads from partner
- **Conversion Rate**: Quality of partner referrals
- **Last Contact**: Most recent interaction date
- **Assigned Rep**: Relationship owner

### Typical Triggers
- Partner inactive for 14+ days (relationship drift)
- New referral from partner
- Partner check-in scheduled
- Seasonal venue opportunity
- Partner performance review cycle

### Corridor Logic
**Relationship Drift Detection**:
- Identify partners with no recent contact
- Generate check-in reminders for assigned reps
- Prioritize high-value partners

**Referral Source Performance**:
- Track lead volume by partner
- Monitor conversion quality
- Identify top-performing relationships

**Systematic Outreach**:
- Maintain regular contact cadence
- Generate personalized check-in prompts
- Track relationship health over time

**Venue Coordination**:
- Link venues to events
- Track venue preferences and restrictions
- Identify repeat venue opportunities

### Allowed Outputs
- **Observation Mode**: Partner activity reports, referral performance, drift alerts
- **Draft Mode**: Check-in email drafts, meeting agenda suggestions
- **Approved Automation**: ClickUp follow-up tasks, relationship logging

### Approval Required For
- Sending partner communication
- Modifying partner records
- Scheduling meetings on behalf of reps
- Changing relationship ownership

---

## Corridor 5: Workforce

### Purpose
Optimize labor allocation through scheduling, conflict detection, seasonal pressure monitoring, and staff utilization tracking.

### Primary Data Sources
- **Google Sheets**: Staff roster, availability, labor hours
- **Google Calendar**: Event schedule with staffing assignments
- **ClickUp**: Staff task assignments

### Key Business Objects
- **Staff Member**: Employee or contractor
- **Availability**: When staff can work
- **Assignment**: Staff allocated to specific event
- **Labor Hours**: Tracked work time
- **Seasonal Pressure**: Busy period identification

### Typical Triggers
- Event scheduled requiring staff
- Staffing conflict detected (double-booking)
- Seasonal busy period approaching
- Labor hour threshold exceeded
- Weekly labor report cycle

### Corridor Logic
**Scheduling Conflict Detection**:
- Identify staff assigned to overlapping events
- Flag over-allocation
- Suggest alternative assignments

**Seasonal Pressure Monitoring**:
- Analyze historical busy periods
- Predict upcoming high-demand windows
- Alert on potential staffing shortfalls

**Labor Hour Tracking**:
- Aggregate staff hours by week/month
- Track against budgets or thresholds
- Generate labor cost projections

**Staffing Optimization**:
- Match staff skills to event requirements
- Balance workload across team
- Identify understaffed or overstaffed periods

### Allowed Outputs
- **Observation Mode**: Conflict alerts, labor reports, pressure forecasts
- **Draft Mode**: Staffing recommendations, schedule adjustments
- **Approved Automation**: Internal scheduling alerts, labor summaries

### Approval Required For
- Modifying staff assignments
- Changing availability records
- Sending communication to staff
- Altering labor budgets

---

## Corridor 6: Procurement

### Purpose
Support food and supply preparation through shopping list generation, quantity extraction, prep requirement identification, and chef coordination.

### Primary Data Sources
- **Google Sheets**: Recipe databases, ingredient lists, supplier information
- **Google Calendar**: Event schedule with menu details
- **ClickUp**: Prep task tracking

### Key Business Objects
- **Menu**: Food items for specific event
- **Ingredient**: Required food/supply item
- **Quantity**: Amount needed based on guest count
- **Shopping List**: Aggregated procurement needs
- **Prep Requirement**: Cooking/preparation tasks

### Typical Triggers
- Event menu finalized
- Guest count confirmed
- Event approaching (prep window opens)
- Multiple events on same day (shared prep)
- Unusual ingredient or quantity detected

### Corridor Logic
**Shopping List Generation**:
- Extract menus from event details
- Calculate quantities based on guest count
- Aggregate across concurrent events
- Organize by supplier or category

**Prep Requirement Extraction**:
- Identify preparation tasks from menu
- Estimate prep time based on complexity
- Generate chef task list

**Shared Prep Coordination**:
- Identify overlapping events
- Consolidate ingredient needs
- Optimize batch preparation

**Inventory Alerts**:
- Flag unusual or high-volume needs
- Alert on missing information
- Identify specialty items requiring advance order

### Allowed Outputs
- **Observation Mode**: Shopping lists, prep summaries, quantity calculations
- **Draft Mode**: ClickUp prep tasks, chef briefings
- **Approved Automation**: Shopping list generation, prep alerts

### Approval Required For
- Modifying event menus
- Changing guest counts
- Placing supplier orders
- Altering prep schedules

---

## Corridor 7: Marketing / Media

### Purpose
Support brand visibility and audience intelligence through content coordination, social media monitoring, trend capture, and feedback integration.

### Primary Data Sources
- **Social Media APIs**: YouTube, TikTok, Instagram, LinkedIn, Twitter
- **Google Sheets**: Content calendar, campaign tracking
- **ClickUp**: Content production tasks

### Key Business Objects
- **Post**: Social media content item
- **Campaign**: Coordinated content series
- **Engagement**: Likes, comments, shares, views
- **Trend**: Recurring theme or pattern in audience response
- **Competitor**: Other businesses in same space
- **Audience Signal**: Feedback or interest indicator

### Typical Triggers
- Content scheduled for publication
- Engagement spike on post
- Trend detected in audience behavior
- Competitor activity observed
- Campaign performance review cycle
- Event approaching (promotion opportunity)

### Corridor Logic
**Content Coordination**:
- Track content calendar across platforms
- Generate posting reminders
- Coordinate event promotion

**Audience Intelligence**:
- Monitor engagement patterns
- Identify high-performing content types
- Extract audience interest signals

**Trend Detection**:
- Analyze recurring themes in comments/engagement
- Spot emerging topics in industry
- Flag brand opportunities

**Competitor Observation**:
- Monitor competitor social activity
- Identify differentiation opportunities
- Track market positioning

**Social-to-Business Feedback**:
- Extract insights relevant to sales messaging
- Identify partnership opportunities from audience
- Inform event packaging based on audience preferences

### Allowed Outputs
- **Observation Mode**: Engagement reports, trend summaries, audience insights
- **Draft Mode**: Post drafts, campaign suggestions, content ideas
- **Approved Automation**: Internal content alerts, performance summaries

### Approval Required For
- Publishing social media posts
- Responding to comments/messages
- Changing brand messaging
- Running paid campaigns

---

## Corridor 8: Executive

### Purpose
Provide owner/executive visibility through high-level summaries, exception alerting, decision support, and system health monitoring.

### Primary Data Sources
- **All Corridors**: Aggregated outputs from sales, operations, finance, partnerships, workforce, procurement, marketing
- **System Logs**: Health monitoring, approval queues, mismatch detection

### Key Business Objects
- **Daily Brief**: Morning summary of key information
- **Weekly Summary**: Comprehensive business state review
- **Urgent Exception**: Time-sensitive alert requiring attention
- **Decision Recommendation**: System suggestion for executive action
- **Approval Queue**: Pending high-stakes actions awaiting review

### Typical Triggers
- Daily brief schedule (morning delivery)
- Weekly summary cycle (Monday morning)
- Urgent exception detected in any corridor
- Approval queue item added
- System health issue
- Shadow mode mismatch requiring review

### Corridor Logic
**Daily Brief Generation**:
- Aggregate key events from all corridors
- Highlight urgent items and exceptions
- Provide snapshot of business state

**Weekly Summary**:
- Comprehensive review of business activity
- Trend identification across corridors
- Performance metrics and insights

**Exception Escalation**:
- Identify high-impact issues from corridor monitoring
- Escalate time-sensitive decisions
- Provide context and recommendations

**Approval Management**:
- Present pending approvals with context
- Track approval/rejection patterns
- Identify approval bottlenecks

**System Health Reporting**:
- Monitor integration status
- Track prediction accuracy
- Report shadow mode comparison results

### Allowed Outputs
- **Observation Mode**: All reporting and summaries
- **Draft Mode**: Decision recommendations
- **Approved Automation**: Daily brief delivery, alert notifications

### Approval Required For
- Executive corridor has no autonomous execution
- All outputs are informational or advisory

---

## Corridor Integration Points

### Cross-Corridor Dependencies
- **Sales → Operations**: Booked events flow from Close to calendar
- **Sales → Finance**: Deal values inform revenue projections
- **Operations → Workforce**: Events drive staffing needs
- **Operations → Procurement**: Events generate shopping lists
- **Partnerships → Sales**: Referrals create leads
- **Marketing → Sales**: Audience signals inform messaging
- **All Corridors → Executive**: Roll up to executive visibility

### Shared Data Objects
- **Event**: Referenced by sales, operations, finance, workforce, procurement
- **Lead/Client**: Referenced by sales, partnerships, marketing, executive
- **Staff**: Referenced by operations, workforce, finance
- **Partner**: Referenced by sales, partnerships, marketing

### Trigger Cascade
Certain events trigger multi-corridor responses:
- **New Event Booked**: Sales updates Close → Operations adds to calendar → Finance updates projections → Workforce assesses staffing → Procurement generates shopping list
- **Lead Referral**: Partnerships logs referral → Sales creates lead in Close → Marketing notes source for campaign feedback
- **Payment Received**: Finance updates records → Executive brief includes update

---

## Next Steps

1. Review [System of Records](system-of-records.md) for data authority mapping
2. Examine [Role Map](role-map.md) for human ownership structure
3. Check [Approval Rules](approvals.md) for execution gates per corridor
4. See corridor-specific documentation in `corridors/[name]/corridor.md`
