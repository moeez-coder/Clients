"""Generate a complete ICP config from four human inputs: industries (Clay/LinkedIn labels), countries,
revenue floor, seniority. Encodes the provider-mapping lessons from the first builds:

- Blitz lists legacy AND current LinkedIn industry labels as separate values; both must be included.
- DiscoLike has a 53-bucket taxonomy; only a few LinkedIn labels map cleanly.
- Catch-all LinkedIn labels (Business Consulting and Services, Strategic Management Services, ...) are never
  part of the core ICP: they become a keyword-gated candidates layer exported separately.
"""

COUNTRY_NAMES = {
    "US": "United States", "GB": "United Kingdom", "CA": "Canada", "AU": "Australia", "NZ": "New Zealand",
    "IE": "Ireland", "DE": "Germany", "FR": "France", "NL": "Netherlands", "ES": "Spain", "IT": "Italy",
    "SE": "Sweden", "DK": "Denmark", "NO": "Norway", "FI": "Finland", "CH": "Switzerland", "AT": "Austria",
    "BE": "Belgium", "SG": "Singapore", "AE": "United Arab Emirates", "IN": "India", "ZA": "South Africa",
}

# Current LinkedIn label -> extra legacy label(s) Blitz still carries as separate values.
LEGACY_LABELS = {
    "Marketing Services": ["Marketing and Advertising"],
    "Advertising Services": ["Marketing and Advertising"],
    "Business Consulting and Services": ["Management Consulting"],
    "Human Resources Services": ["Human Resources"],
    "Software Development": ["Computer Software"],
    "IT Services and IT Consulting": ["Information Technology and Services"],
    "Public Relations and Communications Services": ["Public Relations and Communications"],
    "Outsourcing and Offshoring Consulting": ["Outsourcing/Offshoring"],
    "Financial Services": [],
    "Staffing and Recruiting": [],
    "Executive Search Services": [],
    "Design Services": ["Design"],
    "Technology, Information and Internet": ["Internet"],
    "Hospitals and Health Care": ["Hospital & Health Care"],
    "Real Estate": [],
    "Accounting": [],
    "Legal Services": ["Law Practice"],
    "Insurance": [],
    "Retail": [],
    "Manufacturing": [],
    "Construction": [],
    "Education Administration Programs": ["Education Management"],
    "E-Learning Providers": ["E-Learning"],
}

# LinkedIn label -> DiscoLike bucket (only where the mapping is clean; others skip DiscoLike).
DISCOLIKE_BUCKETS = {
    "Marketing Services": "ADVERTISING_AND_MARKETING",
    "Advertising Services": "ADVERTISING_AND_MARKETING",
    "Public Relations and Communications Services": "ADVERTISING_AND_MARKETING",
    "Staffing and Recruiting": "HUMAN_RESOURCES",
    "Human Resources Services": "HUMAN_RESOURCES",
    "Executive Search Services": "HUMAN_RESOURCES",
    "Software Development": "SOFTWARE",
    "IT Services and IT Consulting": "IT_SERVICES",
    "Financial Services": "FINANCIAL_SERVICES",
    "Accounting": "ACCOUNTING",
    "Legal Services": "LEGAL",
    "Insurance": "INSURANCE",
    "Real Estate": "REAL_ESTATE",
    "Hospitals and Health Care": "HEALTHCARE",
    "Construction": "CONSTRUCTION",
    "Manufacturing": "MANUFACTURING",
    "Retail": "RETAIL",
    "Education Administration Programs": "EDUCATION",
    "E-Learning Providers": "EDUCATION",
    "Technology, Information and Internet": "SOFTWARE",
}

# Labels that are catch-alls on LinkedIn. Keyword gate precision measured at ~30%, so they are candidates, never core.
CATCH_ALL_LABELS = [
    "Business Consulting and Services", "Management Consulting", "Strategic Management Services",
    "Professional Services", "Professional Training and Coaching", "Operations Consulting",
    "Outsourcing and Offshoring Consulting", "Business Intelligence Platforms",
]

# Labels people usually mean together; new-icp prints these as suggestions, never adds them silently.
RELATED_LABELS = {
    "Staffing and Recruiting": ["Executive Search Services", "Human Resources Services"],
    "Executive Search Services": ["Staffing and Recruiting"],
    "Marketing Services": ["Advertising Services", "Public Relations and Communications Services"],
    "Advertising Services": ["Marketing Services", "Public Relations and Communications Services"],
    "Software Development": ["Technology, Information and Internet", "IT Services and IT Consulting"],
    "IT Services and IT Consulting": ["Software Development"],
    "Accounting": ["Financial Services"],
}

SENIORITY_MAPS = {
    "director_plus": {
        "clay": ["C-suite", "VP", "Director", "Head", "Founder", "Owner", "Partner", "Board Member"],
        "blitz": ["C-Team", "VP", "Director"],
        "discolike": ["executive", "vp", "director"],
    },
    "vp_plus": {
        "clay": ["C-suite", "VP", "Founder", "Owner", "Partner", "Board Member"],
        "blitz": ["C-Team", "VP"],
        "discolike": ["executive", "vp"],
    },
    "manager_plus": {
        "clay": ["C-suite", "VP", "Director", "Head", "Manager", "Founder", "Owner", "Partner", "Board Member"],
        "blitz": ["C-Team", "VP", "Director", "Manager"],
        "discolike": ["executive", "vp", "director", "manager"],
    },
}

CLAY_REVENUE_BUCKETS = [("0-500K", 0), ("500K-1M", 500_000), ("1M-5M", 1_000_000), ("5M-10M", 5_000_000), ("10M-25M", 10_000_000),
                        ("25M-75M", 25_000_000), ("75M-200M", 75_000_000), ("200M-500M", 200_000_000), ("500M-1B", 500_000_000),
                        ("1B-10B", 1_000_000_000), ("10B-100B", 10_000_000_000), ("100B-1T", 100_000_000_000)]

DEFAULT_KEYWORDS = {
    "ADVERTISING_AND_MARKETING": ["marketing agency", "advertising agency", "branding agency", "creative agency", "digital agency",
                                  "public relations agency", "media buying", "media planning", "performance marketing",
                                  "demand generation agency", "content marketing agency", "growth marketing agency"],
    "HUMAN_RESOURCES": ["staffing agency", "recruitment agency", "executive search", "talent acquisition", "RPO", "temporary staffing",
                        "contract staffing", "headhunting"],
}


def map_industries(clay_labels):
    """Split human-chosen LinkedIn/Clay labels into core vs catch-all and expand per provider."""
    core, catch_all, unmapped = [], [], []
    for label in clay_labels:
        if label in CATCH_ALL_LABELS:
            catch_all.append(label)
        else:
            core.append(label)
            if label not in LEGACY_LABELS:
                unmapped.append(label)

    def expand(labels):
        # primary labels first, then the legacy variants Blitz still carries as separate values
        out = list(labels)
        for l in labels:
            for v in LEGACY_LABELS.get(l, []):
                if v not in out:
                    out.append(v)
        return out

    core_blitz = expand(core)
    gated_blitz = expand(catch_all)
    disco = []
    for l in core:
        b = DISCOLIKE_BUCKETS.get(l)
        if b and b not in disco:
            disco.append(b)
    return {
        "clay": list(clay_labels),
        "core_clay": core,
        "core_blitz": core_blitz,
        "blitz": core_blitz + [g for g in gated_blitz if g not in core_blitz],
        "catch_all": gated_blitz,
        "discolike": disco,
        "unmapped": unmapped,
    }


def build_icp(name, industries, countries, revenue_min_usd, seniority="director_plus", person_countries=None, keywords=None):
    if seniority not in SENIORITY_MAPS:
        raise ValueError(f"seniority must be one of {sorted(SENIORITY_MAPS)}")
    bad = [c for c in list(countries) + list(person_countries or []) if c not in COUNTRY_NAMES]
    if bad:
        raise ValueError(f"unknown country code(s) {bad}; known: {sorted(COUNTRY_NAMES)}")
    m = map_industries(industries)
    revenue_min_usd = int(revenue_min_usd or 0)
    buckets = [b for b, lo in CLAY_REVENUE_BUCKETS if lo >= revenue_min_usd] if revenue_min_usd else [b for b, _ in CLAY_REVENUE_BUCKETS]
    persons = list(person_countries or countries)
    kw = list(keywords) if keywords is not None else [k for b in m["discolike"] for k in DEFAULT_KEYWORDS.get(b, [])]
    return {
        "name": name,
        "company_hq_countries": list(countries),
        "person_countries": persons,
        "revenue_min_usd": revenue_min_usd,
        "seniority": seniority,
        "industries": {"clay": m["clay"], "blitz": m["blitz"], "discolike": m["discolike"], "discolike_optional": []},
        "seniority_map": SENIORITY_MAPS[seniority],
        "clay_revenue_buckets": buckets,
        "clay_country_names": {c: COUNTRY_NAMES[c] for c in sorted(set(list(countries) + persons), key=lambda c: (list(countries) + persons).index(c))},
        "discolike_employee_floor": 11 if revenue_min_usd >= 1_000_000 else None,
        "fit": {
            "core_industries": m["core_blitz"] + m["discolike"],
            "keyword_gated_industries": m["catch_all"],
            "keywords": kw if m["catch_all"] else [],
        },
        "_mapping_notes": {"unmapped_labels": m["unmapped"], "catch_all_labels": m["catch_all"]},
    }
