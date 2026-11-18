"""Shared filters for the Doc 2 sizing (2026-11-18). Health Link Dimensions, tracking_clients 8f80aeaa-1ca1-4b9a-9f27-756c2a5be696.
Blitz API (https://api.blitz-api.ai), counts with max_results: 1 unless stated. Exact enum labels as in tam_counts.py."""
import json, os, time, urllib.request, urllib.error

def call(path, body):
    for a in range(6):
        try:
            r = urllib.request.Request("https://api.blitz-api.ai" + path, data=json.dumps(body).encode(),
                headers={"x-api-key": os.environ["BLITZ_API_KEY"], "Content-Type": "application/json"})
            return json.load(urllib.request.urlopen(r, timeout=120))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504): time.sleep(2 ** a); continue
            return {"_error": e.code, "_body": e.read()[:500].decode(errors="replace"), "fair_usage": {"records_used": 0}}
    return {"_error": "retries", "fair_usage": {"records_used": 0}}

# ---------------- exclusions ----------------
# Known HLD clients (task brief) + their main operating aliases. Agency clients are handled in the agency section.
CLIENTS_PHARMA = ["AstraZeneca", "Alexion", "AbbVie", "Allergan", "Gilead", "Kite Pharma", "Takeda", "Incyte",
                  "Bausch", "Salix Pharmaceuticals", "Octapharma"]
# DNC accounts (context/2026-11-12-dnc-accounts.csv) that are pharma / biotech / device manufacturers.
# Names written so Blitz's "all words of a keyword" match hits the company and nothing else.
DNC_PHARMA = ["American Regent", "ANI Pharmaceuticals", "Apellis", "ARS Pharmaceuticals", "Assertio", "Aucta", "Azurity",
              "Belmar Pharma", "Bracco", "Cosette", "Day One Biopharmaceuticals", "Egetis", "Eton Pharmaceuticals", "Harrow",
              "IBSA", "IDEAYA", "Ionis", "NervGen", "Noven", "Revolution Medicines", "Verona Pharma", "Syneos"]
DNC_DEVICE = ["LifeScan", "Pulmonx", "AROS Surgical", "Procter", "Munchkin", "Inform Diagnostics", "InterVenn", "Swift Medical", "Bracco"]
EXCL_PHARMA = CLIENTS_PHARMA + DNC_PHARMA            # 33 names
# large non-buyers that dominate the pharma/biotech industry tags (found in the 2026-11-18 fit samples):
# animal health, government/research institutes, associations, research tools, CROs/CDMOs
NOISE_CO = ["National Institutes of Health", "Zoetis", "Elanco", "Bio-Rad", "Novonesis", "Neuralink", "PhRMA", "Pharmacopeia",
            "Precision Medicine Group", "10x Genomics", "Twist Bioscience", "Thermo Fisher", "Illumina", "IQVIA",
            "Charles River", "Labcorp", "Parexel"]   # 17, so NOISE_CO + EXCL_PHARMA = 50 (Blitz cap)
EXCL_DEVICE = DNC_DEVICE + ["HealthLink Dimensions"]

# ---------------- company universes ----------------
PHARMA_IND = ["Pharmaceutical Manufacturing", "Pharmaceuticals", "Biotechnology Research", "Biotechnology"]
PHARMA_SIZES = ["201-500", "501-1000", "1001-5000", "5001-10000", "10001+"]
# CROs, CDMOs, research-tools companies, staffing (doc 2 "Filtered out")
PHARMA_KW_EXCL = ["contract research organization", "CRO", "CDMO", "contract development and manufacturing",
                  "contract manufacturing organization", "contract manufacturer", "staffing", "recruitment", "recruiting",
                  "life science tools", "research reagents", "reagents", "laboratory equipment", "lab supplies",
                  "compounding pharmacy", "specialty pharmacy", "clinical trial services", "API manufacturer",
                  "active pharmaceutical ingredients"]
DEVICE_IND = ["Medical Equipment Manufacturing", "Medical Device"]
DEVICE_SIZES_C7 = ["51-200", "201-500", "501-1000", "1001-5000", "5001-10000"]
# distributors, lab / diagnostics with no specialist promotion (doc 2 Campaign 7 "Filtered out")
DEVICE_KW_EXCL = ["distributor", "distribution", "wholesale", "clinical laboratory", "laboratory services", "reference laboratory",
                  "diagnostic laboratory", "in vitro diagnostics", "IVD", "staffing", "contract manufacturing", "CDMO", "dental lab",
                  "repair services", "refurbished"]

def pharma_co(excl_names=True, kw_excl=True, sizes=None):
    c = {"industry": {"include": PHARMA_IND}, "employee_range": sizes or PHARMA_SIZES, "hq": {"country_code": ["US"]}}
    if kw_excl: c["keywords"] = {"exclude": PHARMA_KW_EXCL}
    c["name"] = {"exclude": NOISE_CO + (EXCL_PHARMA if excl_names else [])}
    return c

def device_co(excl_names=True, sizes=None):
    c = {"industry": {"include": DEVICE_IND}, "employee_range": sizes or DEVICE_SIZES_C7, "hq": {"country_code": ["US"]},
         "keywords": {"exclude": DEVICE_KW_EXCL}}
    if excl_names: c["name"] = {"exclude": EXCL_DEVICE}
    return c

# ---------------- persona title maps ----------------
NOISE = ["Intern", "Assistant", "Coordinator", "Recruiter", "Talent", "Human Resources", "Finance", "Accounting", "Legal",
         "Facilities", "Administrative", "Executive Assistant"]
RND = ["Clinical", "R&D", "Research", "Biostatistics", "Statistic", "Bioinformatics", "Translational", "Discovery",
       "Computational Biology", "Pharmacovigilance", "Drug Safety", "Quality", "Manufacturing", "Regulatory", "Medical Affairs",
       "Medical Science", "HEOR", "Health Economics", "Real World", "Supply Chain"]
RND_SHORT = ["Clinical", "R&D", "Research", "Statistic", "Pharmacovigilance", "Quality", "Manufacturing", "Regulatory",
             "Medical Affairs", "Medical Science", "HEOR", "Real World", "Supply Chain"]
FIELD = ["Regional", "District", "Area", "Territory", "Representative", "Specialist", "Key Account", "Account Manager",
         "Account Executive", "Business Development"]

# priority order (each later persona excludes earlier personas' words): Access > D&A > CommOps > Omni > Brand
ACCESS = ["Market Access", "Payer", "Managed Markets", "Managed Care", "Trade Relations", "Trade Strategy", "Trade and Distribution",
          "National Accounts", "National Account", "IDN", "Health System Accounts", "Health Systems", "Organized Customers",
          "Access Analytics", "Account Insights", "Pricing", "Contracting", "Access Strategy"]
ACCESS_EXCL = NOISE + ["Reimbursement", "Hub", "Patient Services", "Patient Support", "Case Manager", "Field Access",
                       "Medical", "Clinical", "Regulatory", "Manufacturing", "Supply Chain", "Procurement", "Purchasing"]
DA = ["Analytics", "Insights", "Data Strategy", "Data Science", "Data Scientist", "Measurement", "Third-Party Data",
      "Third Party Data", "Data Engineering", "Data Engineer", "Chief Data Officer", "Business Intelligence", "Forecasting",
      "Data and Analytics", "Data & Analytics", "Commercial Data"]
DA_EXCL = NOISE + RND + ["Early Career", "Market Access", "Payer", "Access Analytics", "Account Insights", "Pricing"]
COMMOPS = ["Commercial Operations", "Commercial Excellence", "Commercial Effectiveness", "Sales Operations",
           "Sales Force Effectiveness", "Sales Effectiveness", "CRM", "Targeting", "Alignment", "Incentive Compensation",
           "Field Operations", "Data Stewardship", "Customer Master", "Master Data", "Field Force"]
COMMOPS_SALES_LEAD = COMMOPS + ["Vice President of Sales", "VP Sales", "VP, Sales", "Vice President, Sales",
                                "Head of Sales", "National Sales", "Chief Commercial Officer", "Head of US Sales"]
COMMOPS_EXCL = NOISE + RND_SHORT + FIELD + ["Analytics", "Insights", "Data Science", "Market Access", "Payer", "Trade",
                                      "Managed Markets", "National Accounts", "Pricing", "Contracting", "Inside Sales"]
OMNI = ["Omnichannel", "Omni-channel", "Multichannel", "Multi-channel", "Customer Engagement", "HCP Marketing",
        "HCP Engagement", "Digital Marketing", "Digital Strategy", "Digital Engagement", "Marketing Operations",
        "Marketing Technology", "Martech", "Media", "Customer Experience", "Engagement Strategy"]
OMNI_EXCL = NOISE + RND + ["Analytics", "Insights", "Data Science", "Market Access", "Payer", "Commercial Operations",
                           "Sales Operations", "CRM", "Media Relations", "Public Relations", "Information Technology",
                           "Digital Health", "Digital Transformation", "Social Media", "Communications"]
BRAND = ["Chief Marketing Officer", "Marketing", "Brand", "Franchise", "Launch"]
BRAND_EXCL = NOISE + RND_SHORT + ["Analytics", "Insights", "Market Access", "Payer", "Trade", "Managed Markets", "Commercial Operations",
                            "Sales Operations", "CRM", "Omnichannel", "Multichannel", "Customer Engagement", "HCP Marketing",
                            "Digital", "Marketing Operations", "Marketing Technology", "Media", "Customer Experience",
                            "Sales", "Business Development", "Engineering", "Engineer", "Software"]
LV = {"influencers": ["C-Team", "VP"], "decision_makers": ["Director"], "advocates": ["Manager"]}

PHARMA_CELLS = {  # campaign -> level -> (include, exclude)
 "c5_market_access": {lv: (ACCESS, ACCESS_EXCL) for lv in LV},
 "c4_data_analytics": {lv: (DA, DA_EXCL) for lv in LV},
 "c3_commops_field": {"influencers": (COMMOPS_SALES_LEAD, COMMOPS_EXCL), "decision_makers": (COMMOPS_SALES_LEAD, COMMOPS_EXCL),
                      "advocates": (COMMOPS, COMMOPS_EXCL)},
 "c2_media_omni": {lv: (OMNI, OMNI_EXCL) for lv in LV},
 "c1_brand_marketing": {lv: (BRAND, BRAND_EXCL) for lv in LV},
}

# Campaign 7 (specialist device) and Campaign 8 (large device) personas
DEV_INF = ["Marketing", "Commercial Operations", "Sales", "Commercial", "Professional Education"]
DEV_DM = ["Marketing", "Marketing Operations", "Commercial Operations", "Professional Education", "Medical Education",
          "Commercial Excellence", "Sales Operations", "Digital Marketing", "CRM"]
DEV_ADV = ["Marketing Operations", "CRM", "Sales Operations", "Commercial Operations", "Professional Education",
           "Marketing Manager", "Product Marketing", "Digital Marketing", "Commercial Excellence"]
DEV_EXCL = NOISE + FIELD + ["Clinical", "Quality", "Regulatory", "Engineering", "Engineer", "Manufacturing", "Supply Chain",
                            "R&D", "Research", "Inside Sales", "Customer Service", "Sales Representative"]
DEVICE_CELLS = {"influencers": (DEV_INF, DEV_EXCL), "decision_makers": (DEV_DM, DEV_EXCL), "advocates": (DEV_ADV, DEV_EXCL)}

def people_body(comp, inc, exc, levels, recent=False):
    assert len(inc) <= 50 and len(exc) <= 50, (len(inc), len(exc))
    p = {"job_title": {"include": inc, "exclude": exc}, "job_level": levels, "location": {"country_code": ["US"]}}
    if recent: p["is_recent_hire"] = True
    return {"company": comp, "people": p, "max_results": 1}

def jobs_company(ind, sizes):
    return {"is_agency": False, "industry": {"include": ind}, "size": {"include": sizes}, "hq": {"country_code": {"include": ["US"]}}}

# open-role titles per campaign (job title keyword match), for the hiring pool
JOB_TITLES = {
 "c1_brand_marketing": ["Brand Manager", "Brand Director", "Brand Lead", "Product Manager, Marketing", "Marketing Director",
                        "Director, Marketing", "Head of Marketing", "Franchise", "Brand Marketing", "Marketing Manager",
                        "VP Marketing", "Vice President, Marketing", "Launch Lead", "Associate Director, Marketing"],
 "c2_media_omni": ["Omnichannel", "Omni-channel", "Multichannel", "Customer Engagement", "HCP Marketing", "HCP Engagement",
                   "Digital Marketing", "Marketing Operations", "Media", "Marketing Technology", "Digital Strategy"],
 "c3_commops_field": ["Commercial Operations", "Sales Operations", "Commercial Excellence", "Sales Force Effectiveness", "CRM",
                      "Targeting", "Alignment", "Incentive Compensation", "Field Operations", "Data Stewardship",
                      "National Sales Director", "Head of Sales", "VP Sales", "Vice President, Sales"],
 "c4_data_analytics": ["Commercial Analytics", "Marketing Analytics", "Insights", "Data Strategy", "Commercial Data",
                       "Third Party Data", "Data Science", "Forecasting", "Business Intelligence", "Analytics"],
 "c5_market_access": ["Market Access", "Payer", "Managed Markets", "Trade Relations", "National Account", "IDN",
                      "Health System", "Access Analytics", "Account Insights", "Pricing and Contracting", "Organized Customers"],
 "c7_device": ["Marketing Operations", "CRM", "Product Marketing", "Marketing Manager", "Commercial Operations",
               "Sales Operations", "Digital Marketing", "Professional Education", "Marketing Director", "Commercial Excellence"],
}
JOB_EXCL = ["Intern", "Internship", "Warehouse", "Clinical", "Medical Science", "Regulatory", "Manufacturing", "Quality",
            "Representative", "Territory", "Reimbursement", "Patient Services", "Research", "R&D", "Laboratory"]
