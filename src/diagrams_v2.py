# One architecture diagram per build, written so a non-technical reader
# understands it at a glance and a technical reader still finds it accurate.
#
# Each entry:
#   zones   : 3 or 4 plain-language headings, 3 words max
#   cols    : one list of nodes per zone, max 3 nodes per list
#   caption : one short line, under 60 characters
#
# A node is {"label": ..., "sub": ... or None, "icon": ...}
#   label : 1-3 words, plain English, what a normal person calls this thing
#   sub   : optional detail line for a technical reader (product names live here)
#   icon  : calendar receipt document folder cloud database table gear robot
#           chart alert mail person phone search clock check money code filter

DGM = {

"venue-integration": {
    "zones": ["What we had", "What I built", "What owners see"],
    "cols": [
        [
            {"label": "Table bookings", "sub": "from TableList", "icon": "calendar"},
            {"label": "Sales receipts", "sub": "from Toast or Union POS", "icon": "receipt"},
        ],
        [
            {"label": "Matching engine", "sub": "scores table, time, party", "icon": "gear"},
            {"label": "Reason for each match", "sub": "so a number can be traced", "icon": "document"},
        ],
        [
            {"label": "Who hit the minimum", "sub": None, "icon": "money"},
            {"label": "Who never showed up", "sub": None, "icon": "alert"},
            {"label": "Which section earned", "sub": "revenue by section", "icon": "chart"},
        ],
    ],
    "caption": "Runs nightly, one business date at a time",
},

"venue-table-spend-demo": {
    "zones": ["Inside the POS", "What I built", "What managers see"],
    "cols": [
        [
            {"label": "Table orders", "sub": "where the table is named", "icon": "receipt"},
            {"label": "Receipts and items", "sub": "checks and selections", "icon": "table"},
        ],
        [
            {"label": "Adds up a table", "sub": "across all its orders", "icon": "gear"},
            {"label": "Drops voided payments", "sub": "so nothing double counts", "icon": "filter"},
        ],
        [
            {"label": "What the table spent", "sub": None, "icon": "money"},
            {"label": "Minimum met or missed", "sub": None, "icon": "check"},
            {"label": "Every item ordered", "sub": None, "icon": "document"},
        ],
    ],
    "caption": "The tally no sales screen will do for you",
},

"hr-compliance-automation": {
    "zones": ["Where it lives", "What I built", "What managers get"],
    "cols": [
        [
            {"label": "Scanned paperwork", "sub": "phone photos in Dropbox", "icon": "folder"},
            {"label": "Staff list", "sub": "newest scheduling export", "icon": "person"},
        ],
        [
            {"label": "Weekly job", "sub": "reads filenames, not scans", "icon": "clock"},
            {"label": "Rebuilt from scratch", "sub": "so it cannot drift", "icon": "gear"},
        ],
        [
            {"label": "Up to date tracker", "sub": "one row per employee", "icon": "table"},
            {"label": "Reminder emails", "sub": "drafted, never sent", "icon": "mail"},
        ],
    ],
    "caption": "Unattended, every Thursday, across two venues",
},

"spark-ai-workflow-orchestration": {
    "zones": ["What customers said", "What I built", "What leadership gets"],
    "cols": [
        [
            {"label": "Support tickets", "sub": None, "icon": "mail"},
            {"label": "Survey comments", "sub": None, "icon": "chart"},
            {"label": "Sales call notes", "sub": None, "icon": "document"},
        ],
        [
            {"label": "Reads and tags it", "sub": "to their own taxonomy", "icon": "robot"},
            {"label": "Groups into themes", "sub": "Spark AI plus LangChain", "icon": "filter"},
        ],
        [
            {"label": "Weekly summary", "sub": "split by product area", "icon": "document"},
            {"label": "Their team runs it", "sub": "handed over, not hosted", "icon": "person"},
        ],
    ],
    "caption": "Thousands of comments a month, all read",
},

"geolocation-radius-validation": {
    "zones": ["What we shipped", "How I checked", "What we promised"],
    "cols": [
        [
            {"label": "Live search results", "sub": "articles near a place", "icon": "search"},
        ],
        [
            {"label": "Distance re-measured", "sub": "my own maths, written apart", "icon": "gear"},
            {"label": "Edge cases replayed", "sub": "zero radius, boundary", "icon": "filter"},
        ],
        [
            {"label": "Genuinely nearby", "sub": None, "icon": "check"},
            {"label": "Wrongly included", "sub": "caught before launch", "icon": "alert"},
        ],
    ],
    "caption": "Checked against maths written separately",
},

"legacy-data-migration-automation": {
    "zones": ["What they had", "What I built", "What they got"],
    "cols": [
        [
            {"label": "Spreadsheet exports", "sub": "years of old records", "icon": "table"},
            {"label": "Salesforce dumps", "sub": None, "icon": "cloud"},
        ],
        [
            {"label": "Tidies and checks", "sub": "names, dates, emails", "icon": "filter"},
            {"label": "Logs every decision", "sub": "moved or rejected, with why", "icon": "document"},
        ],
        [
            {"label": "Moved the same day", "sub": None, "icon": "check"},
            {"label": "Held for a human", "sub": "with the reason attached", "icon": "alert"},
        ],
    ],
    "caption": "Nothing questionable is quietly guessed",
},

"salesforce-productboard-two-way-sync": {
    "zones": ["Where sales works", "What I built", "What teams see"],
    "cols": [
        [
            {"label": "Customer request", "sub": "logged in Salesforce", "icon": "document"},
        ],
        [
            {"label": "Copies it across", "sub": "field map, retry, error queue", "icon": "gear"},
            {"label": "Sends decisions back", "sub": "status onto the record", "icon": "robot"},
        ],
        [
            {"label": "Request on the list", "sub": "nobody retypes it", "icon": "table"},
            {"label": "Sales sees the call", "sub": "roadmap status, back in CRM", "icon": "check"},
        ],
    ],
    "caption": "Both teams, one list, updated both ways",
},

"requirements-to-architecture-translator": {
    "zones": ["What someone asks", "What I built", "What you get"],
    "cols": [
        [
            {"label": "The ask in plain words", "sub": "typed into a web box", "icon": "person"},
        ],
        [
            {"label": "Saved instructions", "sub": "version controlled prompt", "icon": "code"},
        ],
        [
            {"label": "First draft spec", "sub": "systems, fields, edge cases", "icon": "document"},
            {"label": "On a shared canvas", "sub": "dropped into Figma", "icon": "cloud"},
        ],
    ],
    "caption": "A first draft before the call ends",
},

"config-review-ai-agent": {
    "zones": ["What we check", "What I built", "What reviewers get"],
    "cols": [
        [
            {"label": "How it is set up", "sub": "pulled live from the API", "icon": "gear"},
        ],
        [
            {"label": "Expert reviewer", "sub": "an agent plus a rubric", "icon": "robot"},
            {"label": "Weighs by severity", "sub": "not a flat checklist", "icon": "filter"},
        ],
        [
            {"label": "Ranked list of gaps", "sub": None, "icon": "chart"},
            {"label": "The fix for each", "sub": "becomes the review agenda", "icon": "check"},
        ],
    ],
    "caption": "Every account gets the same expert review",
},

"ai-workflow-orchestration-pipeline": {
    "zones": ["What comes in", "What it does", "What comes out"],
    "cols": [
        [
            {"label": "Raw feedback", "sub": "tickets, surveys, notes", "icon": "mail"},
        ],
        [
            {"label": "Tidied up", "sub": "one common shape", "icon": "filter"},
            {"label": "Tagged and grouped", "sub": "LangChain, swappable model", "icon": "robot"},
        ],
        [
            {"label": "Summary per theme", "sub": None, "icon": "document"},
            {"label": "Sent to the team", "sub": "seconds, not a week", "icon": "check"},
        ],
    ],
    "caption": "Five swappable stages, set up per customer",
},

"integration-triage-diagnostic": {
    "zones": ["What broke", "What I built", "What you get"],
    "cols": [
        [
            {"label": "The symptom", "sub": "what the customer reports", "icon": "alert"},
        ],
        [
            {"label": "Guided questions", "sub": "the ones a senior asks", "icon": "search"},
            {"label": "Path recorded", "sub": "so the next person sees it", "icon": "document"},
        ],
        [
            {"label": "The actual cause", "sub": None, "icon": "check"},
            {"label": "The exact fix", "sub": None, "icon": "gear"},
        ],
    ],
    "caption": "Anyone can walk the expert path",
},

"customer-health-risk-dashboard": {
    "zones": ["What we track", "What I built", "What teams see"],
    "cols": [
        [
            {"label": "How much they use it", "sub": "active usage", "icon": "chart"},
            {"label": "How well connected", "sub": "integration depth", "icon": "gear"},
            {"label": "Are admins active", "sub": None, "icon": "person"},
        ],
        [
            {"label": "Health score", "sub": "weighted, from real signals", "icon": "gear"},
        ],
        [
            {"label": "Accounts slipping", "sub": "months before renewal", "icon": "alert"},
            {"label": "What to say to them", "sub": "one action per account", "icon": "mail"},
        ],
    ],
    "caption": "Warning months before the renewal call",
},

"tool-consolidation-roi-model": {
    "zones": ["Their current spend", "What I built", "What sales shows"],
    "cols": [
        [
            {"label": "Four overlapping tools", "sub": "licences and integrations", "icon": "money"},
        ],
        [
            {"label": "Cost comparison", "sub": "today versus one platform", "icon": "chart"},
        ],
        [
            {"label": "Monthly saving", "sub": None, "icon": "money"},
            {"label": "Connections dropped", "sub": "integrations retired", "icon": "check"},
        ],
    ],
    "caption": "A business case with a real number",
},

"analytics-warehouse-pipeline": {
    "zones": ["Where it lived", "What I built", "What they get"],
    "cols": [
        [
            {"label": "Product usage", "sub": "the app database", "icon": "database"},
            {"label": "Billing records", "sub": "account tier", "icon": "money"},
            {"label": "Renewal outcomes", "sub": "Salesforce", "icon": "cloud"},
        ],
        [
            {"label": "Nightly gathering", "sub": "incremental ETL job", "icon": "clock"},
            {"label": "One tidy table set", "sub": "fact and dimension tables", "icon": "table"},
        ],
        [
            {"label": "Ask it yourself", "sub": "one query, no engineer", "icon": "search"},
        ],
    ],
    "caption": "An afternoon of spreadsheets becomes a query",
},

"colleague-ai-productivity-agent": {
    "zones": ["What you ask", "What I built", "What you get"],
    "cols": [
        [
            {"label": "A team question", "sub": "one of six common kinds", "icon": "person"},
        ],
        [
            {"label": "Matched template", "sub": "versioned per question type", "icon": "code"},
            {"label": "Pulls the real data", "sub": "account and feature data", "icon": "database"},
        ],
        [
            {"label": "A grounded answer", "sub": "same quality for everyone", "icon": "check"},
        ],
    ],
    "caption": "One shared assistant, not six private tabs",
},

"internal-ops-document-automation": {
    "zones": ["Written once", "What I built", "What staff get"],
    "cols": [
        [
            {"label": "Policy text", "sub": "handbooks, pay tables", "icon": "document"},
            {"label": "Branding", "sub": "logo, colours, fonts", "icon": "folder"},
        ],
        [
            {"label": "Layout template", "sub": "built once in ReportLab", "icon": "gear"},
        ],
        [
            {"label": "Finished handbook", "sub": "branded PDF, both venues", "icon": "document"},
        ],
    ],
    "caption": "Change the words, the documents rebuild",
},

"board-update-auto-draft": {
    "zones": ["Where numbers live", "What I built", "What execs get"],
    "cols": [
        [
            {"label": "Weekly metrics", "sub": "the 5 to 8 already tracked", "icon": "chart"},
        ],
        [
            {"label": "Scheduled gather", "sub": "runs before each cycle", "icon": "clock"},
            {"label": "Writes a first draft", "sub": "Claude, from a template", "icon": "robot"},
        ],
        [
            {"label": "A written update", "sub": "the exec edits, not builds", "icon": "document"},
            {"label": "Unusual movements", "sub": "flagged for explanation", "icon": "alert"},
        ],
    ],
    "caption": "It drafts, it never sends",
},

"meeting-followthrough-agent": {
    "zones": ["What was said", "What I built", "What happens next"],
    "cols": [
        [
            {"label": "Meeting notes", "sub": "pasted or pulled in", "icon": "document"},
        ],
        [
            {"label": "Finds the promises", "sub": "who owes what by when", "icon": "search"},
            {"label": "No owner named", "sub": "flagged, never guessed", "icon": "alert"},
        ],
        [
            {"label": "A list with owners", "sub": None, "icon": "check"},
            {"label": "Nudge on the day", "sub": "Slack or email", "icon": "clock"},
        ],
    ],
    "caption": "Nothing said out loud gets dropped",
},

"vendor-renewal-radar": {
    "zones": ["What we sign", "What I built", "What you get"],
    "cols": [
        [
            {"label": "Contract details", "sub": "vendor, date, notice, cost", "icon": "document"},
        ],
        [
            {"label": "Daily date check", "sub": "days left versus notice", "icon": "clock"},
        ],
        [
            {"label": "Warning at 45 days", "sub": None, "icon": "alert"},
            {"label": "Then 14, then 3", "sub": "colour coded by urgency", "icon": "alert"},
            {"label": "One list, all vendors", "sub": "instead of every portal", "icon": "table"},
        ],
    ],
    "caption": "Nothing renews by accident",
},

"job-discovery-app": {
    "zones": ["What you upload", "What I built", "What you get"],
    "cols": [
        [
            {"label": "Your resume", "sub": "uploaded once", "icon": "document"},
        ],
        [
            {"label": "Reads your resume", "sub": "into skills and roles", "icon": "robot"},
            {"label": "Scores each posting", "sub": "against live jobs", "icon": "chart"},
        ],
        [
            {"label": "A short ranked list", "sub": "swipe through it daily", "icon": "phone"},
            {"label": "Queue refills nightly", "sub": "a daily cron job", "icon": "clock"},
        ],
    ],
    "caption": "It learns from what you swipe",
},

"visa-appointment-checker-bot": {
    "zones": ["What it watches", "What I built", "What you get"],
    "cols": [
        [
            {"label": "Consulate pages", "sub": "several sites at once", "icon": "cloud"},
        ],
        [
            {"label": "Checks on a timer", "sub": "a cron schedule", "icon": "clock"},
            {"label": "Spots what changed", "sub": "diffed against last check", "icon": "filter"},
        ],
        [
            {"label": "A text to your phone", "sub": "Telegram, instantly", "icon": "phone"},
        ],
    ],
    "caption": "Runs unattended, day and night",
},

}

SHOTS = {
 "venue-table-spend-demo": ("/assets/shots/venue-table-spend.jpg", "The generated report for one recorded Friday night"),
 "hr-compliance-automation": ("/assets/shots/hr-compliance.jpg", "The weekly compliance snapshot, rendered from synthetic data"),
}
