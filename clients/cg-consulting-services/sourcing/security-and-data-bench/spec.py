"""Filter spec for the Security and Data Bench segment (C&G, sourcing config 09be87f3).

Shared by the sizing and pull scripts so the query on disk is exactly what ran.
Industry labels are copied verbatim from docs/clay/industry-taxonomy.txt and
docs/blitz-api/company-search-industries.txt (PR #7); the two enums differ in
punctuation and legacy labels, hence two lists.
"""

# Software / tech, fintech + banking + insurance, education + ed publishing, retail.
CLAY_INDUSTRIES = [
    "Software Development", "IT System Custom Software Development", "Data Infrastructure and Analytics",
    "Data Security Software Products", "Computer and Network Security", "Embedded Software Products",
    "Mobile Computing Software Products", "Desktop Computing Software Products",
    "Technology, Information and Internet", "Internet Marketplace Platforms",
    "Financial Services", "Banking", "Capital Markets", "Investment Management",
    "Insurance", "Insurance Carriers",
    "Education", "E-Learning", "E-Learning Providers", "Education Management",
    "Book and Periodical Publishing", "Book Publishing",
    "Retail", "Online and Mail Order Retail", "Retail Apparel and Fashion", "Retail Groceries",
    "Retail Health and Personal Care Products", "Retail Furniture and Home Furnishings",
    "Retail Appliances, Electrical, and Electronic Equipment", "Retail Luxury Goods and Jewelry",
]
BLITZ_INDUSTRIES = [
    "Software Development", "Computer Software", "IT System Custom Software Development",
    "Data Infrastructure and Analytics", "Data Security Software Products", "Computer and Network Security",
    "Embedded Software Products", "Mobile Computing Software Products", "Desktop Computing Software Products",
    "Technology; Information and Internet", "Internet", "Internet Marketplace Platforms",
    "Financial Services", "Banking", "Capital Markets", "Investment Management",
    "Insurance", "Insurance Carriers",
    "Education", "E-learning", "E-Learning Providers", "Education Management",
    "Book and Periodical Publishing", "Book Publishing", "Publishing",
    "Retail", "Online and Mail Order Retail", "Retail Apparel and Fashion", "Retail Groceries",
    "Retail Health and Personal Care Products", "Retail Furniture and Home Furnishings",
    "Retail Appliances; Electrical; and Electronic Equipment", "Retail Luxury Goods and Jewelry",
]

EMPLOYEE_RANGES_BLITZ = ["201-500", "501-1000", "1001-5000"]
EMPLOYEE_RANGES_CLAY = ["201-500", "501-1,000", "1,001-5,000"]
REVENUE_MIN_USD = 20_000_000
# Clay revenue is a bucket enum; 25M+ is the closest bucket floor to $20M (10M-25M would let in <$20M).
CLAY_REVENUE_BUCKETS = ["25M-75M", "75M-200M", "200M-500M", "500M-1B", "1B-10B", "10B-100B", "100B-1T"]

# Persona e399896d: CIO, CTO, CISO, VP Engineering, VP of Data, Head of Data, Head of IT —
# plus the spelled-out / punctuation variants of those same seven roles, nothing wider.
TITLE_KEYWORDS = [
    "CIO", "Chief Information Officer",
    "CTO", "Chief Technology Officer",
    "CISO", "Chief Information Security Officer",
    "VP Engineering", "VP of Engineering", "Vice President of Engineering", "Vice President, Engineering",
    "SVP Engineering", "SVP of Engineering",
    "VP of Data", "VP Data", "Vice President of Data", "Vice President, Data",
    "Head of Data",
    "Head of IT", "Head of Information Technology",
]
TITLE_EXCLUDE = ["Assistant", "Intern", "Executive Assistant", "Advisor", "Former", "Recruiter", "Sales"]
