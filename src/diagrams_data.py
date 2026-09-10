# One architecture diagram per build. Columns flow left to right.
# '|' splits a node label onto two lines.
DGM = {
"venue-integration": ([["TableList|reservations", "Union / Toast|checks"],
                       ["Scoring|matcher"],
                       ["Table minimums", "No-shows", "Revenue|by section"]],
                      "nightly, one business date at a time"),

"venue-table-spend-demo": ([["Orders"], ["Checks"], ["Selections"],
                            ["Spend|per table", "Minimum|met or missed"]],
                           "the walk the sales screen will not do"),

"hr-compliance-automation": ([["Dropbox|scans", "Roster|export"],
                              ["Weekly job"],
                              ["Sheet|snapshot", "Expiry|alert drafts"]],
                             "unattended, every Thursday"),

"spark-ai-workflow-orchestration": ([["Support", "Surveys", "Sales notes"],
                                     ["Classify|and summarize"],
                                     ["Weekly digest|by product area"]],
                                    "thousands of items a month"),

"geolocation-radius-validation": ([["Live API|response"],
                                   ["Independent|Haversine check"],
                                   ["Inside radius", "Flagged"]],
                                  "ground truth computed separately from the code under test"),

"legacy-data-migration-automation": ([["CSV export", "CRM export"],
                                      ["Normalize|and validate"],
                                      ["Imported", "Review queue|with reason"]],
                                     "nothing ambiguous is guessed"),

"salesforce-productboard-two-way-sync": ([["Salesforce|opportunity"],
                                          ["Field map,|retry, error queue"],
                                          ["Product|feature note"]],
                                         "and the reverse path writes status back"),

"requirements-to-architecture-translator": ([["Business ask|in plain English"],
                                             ["Versioned|prompt template"],
                                             ["Spec sheet", "Shared|design canvas"]],
                                            "first draft before the call ends"),

"config-review-ai-agent": ([["Live account|configuration"],
                            ["Agent|plus rubric"],
                            ["Ranked gaps", "Specific fix|per gap"]],
                           "severity-weighted, not a static checklist"),

"ai-workflow-orchestration-pipeline": ([["Ingest"], ["Normalize"], ["Classify"], ["Summarize"], ["Deliver"]],
                                       "five swappable stages, configured per customer"),

"integration-triage-diagnostic": ([["Reported|symptom"],
                                   ["Branching|questions"],
                                   ["Root cause", "Exact fix"]],
                                  "the path taken is recorded on every run"),

"customer-health-risk-dashboard": ([["Active usage", "Integration|depth", "Admin|engagement"],
                                    ["Weighted|score"],
                                    ["Risk band", "Recommended|intervention"]],
                                   "signals that actually predicted retention"),

"tool-consolidation-roi-model": ([["Four overlapping|tool licences"],
                                  ["Consolidation|model"],
                                  ["Monthly saving", "Integrations|retired"]],
                                 "a business case, not a pitch"),

"analytics-warehouse-pipeline": ([["App database", "Billing", "CRM"],
                                  ["Incremental|ETL"],
                                  ["Dimensional|schema"],
                                  ["Self-serve|queries"]],
                                 "three exports and an afternoon becomes one query"),

"colleague-ai-productivity-agent": ([["Question|type"],
                                     ["Matched template|plus data source"],
                                     ["Grounded|answer"]],
                                    "versioned prompts, so quality stays consistent"),

"internal-ops-document-automation": ([["Policy content", "Brand tokens"],
                                      ["Layout|template"],
                                      ["Branded PDF"]],
                                     "swap the branding, reuse the template"),

"board-update-auto-draft": ([["Metrics where|they already live"],
                             ["Template|plus draft"],
                             ["Narrative", "Flagged|movements"]],
                            "the system drafts, it never sends"),

"meeting-followthrough-agent": ([["Raw meeting|notes"],
                                 ["Extract|commitments"],
                                 ["Owned items", "Nudge at|the due date"]],
                                "sentences with no owner are flagged, not guessed"),

"vendor-renewal-radar": ([["Contract|records"],
                          ["Daily|date check"],
                          ["Alerts at|45, 14, 3 days"]],
                         "one view instead of every vendor portal"),

"job-discovery-app": ([["Resume|upload"],
                       ["Parse|and score"],
                       ["Ranked queue", "Daily|refill"]],
                      "the queue learns from what you swipe"),

"visa-appointment-checker-bot": ([["Consulate|pages"],
                                  ["Poll|and diff"],
                                  ["Instant|phone alert"]],
                                 "runs unattended on a schedule"),
}

SHOTS = {
 "venue-table-spend-demo": ("/assets/shots/venue-table-spend.jpg", "The generated report for one recorded Friday night"),
 "hr-compliance-automation": ("/assets/shots/hr-compliance.jpg", "The weekly compliance snapshot, rendered from synthetic data"),
}
