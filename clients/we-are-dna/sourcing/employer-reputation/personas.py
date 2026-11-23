"""Persona definitions for Doc 1 Campaigns 1-3 (We Are DNA), shared by the preview and full pulls.
Blitz cascades (POST /v2/search/waterfall-icp-keyword, UK only, no headline search) and the strict title regexes
that decide whether a returned person really is the persona. Tier 1 is preferred; tier 2 is the doc's fallback."""
import re
X_COMMON = ["Assistant", "PA to", "EA to", "Intern", "Graduate", "Apprentice", "Non-Executive", "Non Executive", "Advisor",
            "Adviser", "Board Member", "Deputy", "Regional", "Area", "Store", "Branch", "Site", "Coordinator", "Co-ordinator",
            "Administrator", "Consultant", "Trainee"]
GB = {"country_code": ["GB"]}
CASCADES = {
 "c1": [{"include_title": ["CEO", "Chief Executive Officer", "Chief Executive", "Group Chief Executive", "Managing Director",
                           "Group Managing Director", "Managing Partner", "Senior Partner"],
         "exclude_title": X_COMMON + ["Sales", "Account", "Client", "Partner Manager", "Business Partner"], "location": GB, "include_headline_search": False},
        {"include_title": ["Chief Operating Officer", "COO", "Chief Financial Officer", "CFO"],
         "exclude_title": X_COMMON + ["Sales", "Business Partner", "to the COO", "to the CFO"], "location": GB, "include_headline_search": False}],
 "c2": [{"include_title": ["Chief People Officer", "Chief HR Officer", "Chief Human Resources Officer", "People Director",
                           "HR Director", "Human Resources Director", "Director of People", "Director of HR", "Director of Human Resources",
                           "Group People Director", "Group HR Director", "People and Culture Director", "Director of People and Culture"],
         "exclude_title": X_COMMON + ["Business Partner", "Talent Acquisition", "Recruitment", "Resourcing", "Reward", "Payroll", "Learning", "Systems", "Operations Manager"],
         "location": GB, "include_headline_search": False},
        {"include_title": ["Head of People", "Head of People and Culture", "Head of HR", "Head of Human Resources", "VP People", "VP HR", "Head of People & Culture"],
         "exclude_title": X_COMMON + ["Business Partner", "Talent Acquisition", "Recruitment", "Resourcing", "Reward", "Payroll", "Learning", "Systems", "Analytics"],
         "location": GB, "include_headline_search": False}],
 "c3": [{"include_title": ["Head of Talent Acquisition", "Director of Talent Acquisition", "Talent Acquisition Director",
                           "Head of Resourcing", "Resourcing Director", "Head of Recruitment", "Recruitment Director", "Head of Talent",
                           "Global Head of Talent Acquisition", "VP Talent Acquisition", "Director of Talent"],
         "exclude_title": X_COMMON + ["Partner", "Sourcer", "Recruiter", "Specialist", "Executive", "Officer", "Development", "Management", "Learning"],
         "location": GB, "include_headline_search": False},
        {"include_title": ["Talent Acquisition Manager", "Talent Acquisition Lead", "Resourcing Manager", "Recruitment Manager", "Resourcing Lead",
                           "Recruitment Lead", "Senior Talent Acquisition Manager", "Head of Talent Acquisition and Employer Brand"],
         "exclude_title": X_COMMON + ["Partner", "Sourcer", "Recruiter", "Specialist", "Executive", "Officer"],
         "location": GB, "include_headline_search": False}]}
BAD = re.compile(r"\b(assistant|pa to|ea to|intern|graduate|apprentice|non[- ]?executive|advis[eo]r|deputy|regional|area|store|branch|"
                 r"coordinator|co-ordinator|administrator|consultant|trainee|interim deputy)\b", re.I)
TIER1 = {
 "c1": re.compile(r"\b(ceo|chief executive|managing director|group md|managing partner|senior partner)\b", re.I),
 "c2": re.compile(r"\b(chief people( (and|&) [a-z ]+)? officer|cpo|chro|chief (hr|human resources) officer|(group |global )?(people|hr|human resources)( (and|&) [a-z]+)? director|"
                  r"(group |global )?director of (people|hr|human resources)\b)", re.I),
 "c3": re.compile(r"\b(head of (talent( acquisition)?|resourcing|recruitment)|(talent acquisition|resourcing|recruitment) director|"
                  r"director of (talent( acquisition)?|resourcing|recruitment)|vp,? talent acquisition)\b", re.I)}
TIER2 = {
 "c1": re.compile(r"\b(coo|chief operat(ing|ions) officer|cfo|chief financial officer)\b", re.I),
 "c2": re.compile(r"\b(head of (people|hr|human resources)( (and|&) culture)?|vp,? (people|hr))\b", re.I),
 "c3": re.compile(r"\b(talent acquisition|resourcing|recruitment) (manager|lead)\b", re.I)}
# words that, in the title, mean the person belongs to another campaign's persona (keeps the three lists disjoint)
OTHER = {"c1": re.compile(r"\b(people|hr|human resources|talent|recruit|resourcing|sales|marketing|commercial|it|technology)\b", re.I),
         "c2": re.compile(r"\b(talent acquisition|recruit|resourcing|business partner|partnering|payroll|learning|l&d)\b", re.I),
         "c3": re.compile(r"\b(partner|sourcer|recruiter\b|specialist|coordinator|commercial|workforce planning)\b", re.I)}
def classify(camp, title):
    t = title or ""
    if BAD.search(t): return "removed: title not the persona (junior/advisory/regional)"
    if TIER1[camp].search(t) and not (camp == "c1" and OTHER["c1"].search(t)) and not (camp != "c1" and OTHER[camp].search(t)): return "1"
    if TIER2[camp].search(t) and not OTHER[camp].search(t): return "2"
    return "removed: title not the persona"

# --- Widening pass (Moe, 2026-11-23: "run them"), only on companies with no launch-set lead after the first pull ---
# C1 tier 3: the company's top person under another title: Founder/Co-founder/Owner/Chair, Partner (law and accounting),
#            a plain "Director" (51-200 staff only). C2 tier 3: HR / People / People and Culture Manager.
WIDEN_CASCADES = {
 "c1": [{"include_title": ["Founder", "Co-Founder", "Owner", "Chairman", "Executive Chairman", "Chair", "Partner", "Director", "Proprietor"],
         "exclude_title": X_COMMON + ["Associate", "Sales", "Account", "Business Partner", "Talent Partner", "People Partner", "Non-Exec"],
         "location": GB, "include_headline_search": False}],
 "c2": [{"include_title": ["HR Manager", "Human Resources Manager", "People Manager", "People and Culture Manager", "People & Culture Manager",
                           "Senior HR Manager", "HR & Payroll Manager", "HR Lead", "People Lead"],
         "exclude_title": X_COMMON + ["Business Partner", "Recruitment", "Talent Acquisition", "Payroll Officer", "Systems", "Learning"],
         "location": GB, "include_headline_search": False}]}
TIER3 = {
 "c1": re.compile(r"^\s*((co-?\s?)?founder|owner|proprietor|(executive )?chair(man|woman|person)?)\b|\b((co-?\s?)?founder|owner|(executive )?chair(man|woman|person)?)\s*$"
                  r"|^\s*((co-?\s?)?founder|owner)\s*(and|&|/|,)\s*(director|ceo|managing director|chair(man)?)\s*$", re.I),
 "c1_partner": re.compile(r"^\s*(equity |senior |salaried )?partner\s*$", re.I),
 "c1_director": re.compile(r"^\s*(company |group )?director\s*$", re.I),
 "c2": re.compile(r"\b(senior )?(hr|human resources|people|people (and|&) culture|hr (and|&) payroll)\s+(manager|lead)\b", re.I)}
def classify_widen(camp, title, sector, size_band):
    t = title or ""
    if BAD.search(t) or re.search(r"non[- ]?exec|business partner|recruit", t, re.I): return None
    if camp == "c1" and re.search(r"\bowner\b", t, re.I) and not re.fullmatch(r"\s*(co-?\s?owner|owner|business owner|franchise owner|(co-?\s?)?founder\s*(and|&|/)\s*owner|owner\s*(and|&|/|,)\s*(director|managing director|ceo|founder))\s*", t, re.I): return None
    if camp == "c1" and re.search(r"\b(product|technical|concession|process|data|service|system|committee|board|advisory|council|of the|of colleague)\b", t, re.I): return None
    if camp == "c1":
        if TIER3["c1"].search(t): return "3"
        if sector == "Law, accounting" and TIER3["c1_partner"].search(t): return "3"
        if size_band == "51-200" and TIER3["c1_director"].search(t): return "3"
    if camp == "c2" and TIER3["c2"].search(t) and not OTHER["c2"].search(t): return "3"
    return None
