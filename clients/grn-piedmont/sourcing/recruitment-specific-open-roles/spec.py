"""Filter spec for the GRN Piedmont Recruitment Specific pull (2026-11-16). Shared by build_companies.py and pull_people.py."""
import re

# Titles that match a role keyword but are not a role GRN Piedmont places (read from the pulled postings).
TITLE_NOISE = re.compile(r"\b(hotel|restaurant|retail|marketing|people operations|it operations|business development|"
                         r"collection|revenue|customer|clinical|nurs\w*|pharmac\w*|dealer\w*|leasing|property|"
                         r"e-?commerce|digital|software|data engineering|cyber|security operations|call center|contact center|"
                         r"brand|merchandis\w*|hr operations|payroll|legal|event|creative|content|social|"
                         r"associate|junior|jr|apprentice|coordinator|clerk|specialist|representative|"
                         r"part[- ]time|temporary|seasonal|farm manager)\b", re.I)
# Company names that are clearly outside the ICP (agencies slip past is_agency; dealers, retailers, government).
COMPANY_NOISE = re.compile(r"\b(staffing|recruit\w*|talent|search group|executive search|personnel|autonation|"
                           r"tire|dealership|motors|hotel|resort|city of|county|university|college|school|hospital|"
                           r"airport authority|global recruiters|grn|automotive group|automotive enterprises|department of)\b", re.I)
# Fire & life safety gate: the company keyword screen lets general/mechanical/civil contractors through,
# so a posting only stays if the company name or the job title is plainly fire & life safety.
FLS_GATE = re.compile(r"\b(fire|sprinkler|suppression|life safety|alarm)\b", re.I)
# Client Do-Not-Contact list (context/dnc-list.csv) + its named acquisitions family.
DNC = re.compile(r"\b(superhero fire|capital fire protection|wilbert plastic|baxter enterprises|hytek|surteco|autoneum)\b", re.I)

PER_COMPANY = {"mfg": 2, "fire-life-safety": 4}  # TAM/SAM inverse rule, see ../tam/2026-11-16-tam-read.query.md

OPS = ["Chief Operating Officer", "COO", "VP Operations", "Vice President Operations", "VP Manufacturing",
       "Vice President Manufacturing", "SVP Operations", "EVP Operations"]
TIER1 = {
    "operations-plant-leadership": OPS,
    "engineering-quality": ["VP Engineering", "Vice President Engineering", "Chief Technology Officer", "CTO",
                            "VP Quality", "Vice President Quality"] + OPS[:4],
    "supply-chain-purchasing": ["VP Supply Chain", "Vice President Supply Chain", "Chief Supply Chain Officer",
                                "Chief Procurement Officer", "VP Procurement", "VP Purchasing"] + OPS[:4],
    "executive-finance-hr": ["Chief Executive Officer", "CEO", "[President]", "[Owner]", "Chief Financial Officer", "CFO",
                             "Chief Human Resources Officer", "CHRO"],
    "fire-life-safety": OPS[:4] + ["[President]", "President CEO", "Chief Executive Officer", "CEO", "[Owner]"],
}
# Exact-match brackets on President/Owner: unbracketed they matched "Vice President of ..." and "Product Owner".
TIER2 = ["Chief Executive Officer", "CEO", "[President]", "President CEO", "[Owner]", "[Founder]", "Founder CEO",
         "Owner President", "President Owner"]
TIER3 = ["Chief Human Resources Officer", "CHRO", "Chief People Officer", "VP Human Resources",
         "Vice President Human Resources", "VP People"]
PEOPLE_EXCLUDE = ["Manager", "Director", "Assistant", "Coordinator", "Recruiter", "Former", "Sales", "Retired", "Intern"]
