"""Company-level ICP fit: core industries pass outright; catch-all industries pass only with marketing keywords."""


def classify_company_fit(icp, industry, keyword_fit):
    """Return (status, reason) with status in {'fit', 'candidate', 'unfit', 'unknown'}.

    'candidate' = catch-all consulting industry whose profile mentions marketing keywords; precision of that
    signal measured at ~30%, so candidates are exported separately for review rather than into the main list.

    industry may be a single label or a comma-joined list (DiscoLike). keyword_fit is True/False when the
    company was checked against the keyword search, None when it was not.
    """
    rules = icp["fit"]
    if not industry:
        return "unknown", "industry unknown"
    labels = [p.strip() for p in str(industry).split(",") if p.strip()]
    if any(l in rules["core_industries"] for l in labels):
        return "fit", "core industry"
    if any(l in rules["keyword_gated_industries"] for l in labels):
        if keyword_fit is True:
            return "candidate", "consulting with marketing keywords"
        if keyword_fit is False:
            return "unfit", "consulting without marketing keywords"
        return "unknown", "consulting, keywords not checked"
    return "unfit", "industry outside ICP"
