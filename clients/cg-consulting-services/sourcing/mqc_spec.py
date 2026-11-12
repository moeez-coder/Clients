"""Filter spec for C&G's MQC campaign (reply-only test), 2026-11-12. Shared by pull_mqc.py / build_mqc.py.

Why this audience (reasoning in the README "MQC campaign" section):
  - Persona = the people who actually buy from staffing agencies: talent-acquisition / recruiting leaders,
    with HR leaders as the fallback (smaller companies often have no dedicated TA head). The live campaigns
    target CTO/CISO/VP Eng (Bench: 3.8% acceptance, 5 replies in 52 conversations, all "not hiring") or the
    hiring manager (open-role MPC). Nobody in the live campaigns is aimed at TA as the primary persona.
  - Companies = Northeast (DC->Boston, C&G is in NJ) life-sciences and tech employers with 51-1,000 staff and
    a live posting in a C&G role family in the last 30 days, that are NOT already in any CG campaign
    (company-level exclusion, so a reply here can't be credited to a touch from another campaign).
  - 1 contact per company: the pool is large and the goal is learning per-variant reply rates across many
    independent companies, not depth at one account.
Industry labels are exact Blitz enum values reused from open_role_spec.py. Business Consulting / Management
Consulting are dropped (catch-all labels, mostly agencies and consultancies = competitors or non-buyers).
"""
from open_role_spec import LS_INDUSTRIES, TECH_INDUSTRIES, NORTHEAST_STATES, SEGMENTS, JOB_TITLE_EXCLUDE

INDUSTRIES = LS_INDUSTRIES + [i for i in TECH_INDUSTRIES
                              if i not in ("Business Consulting and Services", "Management Consulting")]
SIZES = ["51-200", "201-500", "501-1000"]
DATE_POSTED_DAYS = 30
# any C&G role family counts as "hiring in C&G's lane"
_ALL = sorted({t for s in SEGMENTS.values() for t in s["job_titles"]})
# Blitz caps title.include at 50. Its match is "all words present", so a phrase whose words contain another
# listed phrase's words is redundant (e.g. "Clinical Data Manager" is covered by "Clinical Data"): drop those.
JOB_TITLES = [t for t in _ALL if not any(o != t and set(o.lower().split()) < set(t.lower().split()) for o in _ALL)]

TA_TITLES = [  # tier 1: talent acquisition / recruiting leadership
    "Talent Acquisition Manager", "Manager Talent Acquisition", "Director Talent Acquisition",
    "Head of Talent Acquisition", "Head Talent Acquisition", "VP Talent Acquisition",
    "Vice President Talent Acquisition", "Talent Acquisition Lead", "Talent Acquisition Leader",
    "Recruiting Manager", "Director of Recruiting", "Head of Recruiting", "Recruitment Manager",
    "Head of Talent", "Director of Talent", "Talent Director", "VP Talent", "Vice President Talent",
]
HR_TITLES = [  # tier 2: HR / people leadership (often owns hiring at 51-1,000 staff)
    "HR Director", "Director of Human Resources", "Director Human Resources", "Head of HR",
    "Head of Human Resources", "Head of People", "VP Human Resources", "Vice President Human Resources",
    "VP People", "VP of People", "Vice President People", "Chief People Officer", "Chief Human Resources Officer",
    "HR Manager", "Human Resources Manager", "People Operations Manager", "Director of People",
]
PEOPLE_EXCLUDE = ["Sales", "Intern", "Assistant", "Coordinator", "Former", "Recruiter", "Specialist",
                  "Partner", "Generalist", "Payroll", "Benefits", "Sourcer", "Freelance", "Consultant",
                  "Account", "Donor", "Student", "Patient"]  # last four added after the NE pass: "Account Manager - Donor Recruitment"
PER_COMPANY = 1
MAX_NEW_COMPANIES = 900
