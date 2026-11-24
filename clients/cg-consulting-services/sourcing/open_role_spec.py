"""Filter spec for the 4 recruiter-specific open-role segments (C&G, Moe's brief 2026-11-05).

Shared by pull_open_roles.py and build_open_roles.py so the query on disk is exactly what ran.
Industry labels are copied verbatim from the Blitz /v2/jobs/search OpenAPI enum (docs.blitz-api.ai,
read 2026-11-05). Title matching in Blitz is keyword-based: all words of a phrase must appear, in any
order, whole words, no stemming/abbreviation expansion. So each role is listed in its common variants.
"""

SIZES = ["51-200", "201-500", "501-1000", "1001-5000"]
JOB_TITLE_EXCLUDE = ["Sales", "Warehouse", "Intern", "Internship"]
DATE_POSTED_DAYS = 30

LS_INDUSTRIES = [
    "Pharmaceutical Manufacturing", "Pharmaceuticals", "Biotechnology Research", "Biotechnology",
    "Medical Equipment Manufacturing", "Medical Device", "Medical and Diagnostic Laboratories",
    "Research Services",
]

# ICP-form verticals Technology, Finance, Healthcare, Retail, Education, Consulting -> exact Blitz labels.
# Technology/Finance/Education/Retail = the Security and Data Bench list (spec.py, 2026-10-23) for consistency;
# Healthcare + Consulting added per the ICP form. "IT Services and IT Consulting" deliberately left out:
# it is dominated by IT staffing/outsourcing shops, i.e. C&G's competitors (is_agency only drops confirmed agencies).
TECH_INDUSTRIES = [
    # Technology
    "Software Development", "Computer Software", "IT System Custom Software Development",
    "Data Infrastructure and Analytics", "Data Security Software Products", "Computer and Network Security",
    "Embedded Software Products", "Mobile Computing Software Products", "Desktop Computing Software Products",
    "Technology; Information and Internet", "Internet", "Internet Marketplace Platforms",
    # Finance
    "Financial Services", "Banking", "Capital Markets", "Investment Management", "Insurance", "Insurance Carriers",
    # Healthcare
    "Hospitals and Health Care", "Hospital and Health Care", "Hospitals",
    # Retail
    "Retail", "Online and Mail Order Retail", "Retail Apparel and Fashion", "Retail Groceries",
    "Retail Health and Personal Care Products", "Retail Furniture and Home Furnishings",
    "Retail Appliances; Electrical; and Electronic Equipment", "Retail Luxury Goods and Jewelry",
    # Education
    "Education", "E-learning", "E-Learning Providers", "Education Management", "Higher Education",
    # Consulting
    "Business Consulting and Services", "Management Consulting",
]

# DC -> Boston corridor. hq.state is a keyword match on the full state name.
NORTHEAST_STATES = ["District of Columbia", "Maryland", "Delaware", "Pennsylvania", "New Jersey",
                    "New York", "Connecticut", "Rhode Island", "Massachusetts"]

# Fallback tier for every segment (Moe's rule): Head of Talent / Talent Director / Director of TA / VP People.
FALLBACK_TITLES = [
    "Head of Talent", "Talent Director", "Director Talent Acquisition", "Director of Talent",
    "VP People", "VP of People", "Vice President People", "Vice President of People",
    "VP Talent", "Vice President Talent", "Chief People Officer",
]
PEOPLE_EXCLUDE = ["Sales", "Warehouse", "Intern", "Assistant", "Coordinator", "Former", "Recruiter"]


def _leads(families, heads=("Head", "Director", "VP", "Vice President", "SVP")):
    return [f"{h} {f}" for f in families for h in heads]


SEGMENTS = {
    "recruiter-open-role-ls-clinical-data": {
        "name": "LS Clinical & Data",
        "industries": LS_INDUSTRIES,
        "job_titles": [
            "Biostatistician", "Biostatistics", "Statistician", "Statistical Programmer", "Statistical Programming",
            "Clinical Data Manager", "Clinical Data", "Clinical Data Management", "Clinical Programmer",
            "Clinical Programming", "Pharmacovigilance", "Drug Safety", "Safety Scientist", "Data Scientist",
            "SAS Programmer",
        ],
        "tier1": _leads(["Biostatistics", "Statistics", "Statistical Programming", "Clinical Data Management",
                         "Clinical Data", "Data Management", "Drug Safety", "Pharmacovigilance",
                         "Patient Safety", "Data Science"]),
        "per_company": 3,
        "job_cap": 5000,
    },
    "recruiter-open-role-ls-regulatory-quality": {
        "name": "LS Regulatory & Quality",
        "industries": LS_INDUSTRIES,
        "job_titles": [
            "Regulatory Affairs", "Regulatory", "Quality Control", "QC", "Quality Assurance", "QA",
            "Lab Technician", "Laboratory Technician", "Lab Tech", "Quality Specialist", "Quality Engineer",
            "QC Analyst", "QC Chemist", "QC Microbiologist", "Quality Analyst",
        ],
        "tier1": _leads(["Regulatory Affairs", "Regulatory", "Quality", "Quality Assurance", "Quality Control",
                         "QA", "QC", "Lab Operations", "Laboratory Operations", "Laboratory"]),
        "per_company": 3,  # Moe: 2-3; 3 taken because the per-company pool is small (see .query.md)
        "job_cap": 5000,
    },
    "recruiter-open-role-ls-medical-affairs": {
        "name": "LS Medical Affairs",
        "industries": LS_INDUSTRIES,
        "job_titles": [
            "Medical Affairs", "Medical Science Liaison", "MSL", "Medical Director", "Medical Information",
            "Medical Writer", "Medical Writing", "Medical Scientist", "Medical Communications",
        ],
        "tier1": _leads(["Medical Affairs", "Medical Information", "Medical Writing", "Medical Communications"])
                 + ["Chief Medical Officer", "CMO", "Head Medical"],
        "per_company": 3,
        "job_cap": 5000,
    },
    "recruiter-open-role-tech-eng-security-data": {
        "name": "Tech Eng, Security & Data",
        "industries": TECH_INDUSTRIES,
        "job_titles": [
            "Software Engineer", "Software Developer", "Developer", "Data Engineer", "Data Scientist",
            "Security Engineer", "Cybersecurity", "Cyber Security", "Information Security", "Project Manager",
            "DevOps", "Cloud Engineer", "Site Reliability Engineer", "Full Stack", "Backend Engineer",
            "Frontend Engineer", "Machine Learning Engineer", "Data Analyst", "Security Analyst",
        ],
        "tier1": ["CTO", "Chief Technology Officer", "CISO", "Chief Information Security Officer",
                  "CIO", "Chief Information Officer"]
                 + _leads(["Engineering", "Software Engineering", "Data", "Data Engineering", "Data Science",
                           "Information Security", "Security", "Cybersecurity", "PMO", "Technology"],
                          heads=("Head", "Director", "VP", "Vice President")),
        "per_company": 1,
        "job_cap": 5000,
    },
}
