import re,json,glob,collections
FUNC=r'(sales|marketing|finance|financial|human resources|\bhr\b|\bit\b|information|procurement|supply|purchasing|quality|engineering|technology|product|legal|customer|service|aftermarket|parts|business development|strategy|digital|operations|manufacturing|logistics|channel|dealer|commercial|revenue|growth|innovation|research|safety|compliance|communications?|public|investor|corporate development|real estate|facilities|data|analytics|transformation)'
BAD=re.compile(r'((?:product|process|project|scrum|digital|data|service|system|business|program|platform|sales|marketing|content|account|solution|risk|quality|brand)\s+owner|owner\s*[-–—,]?\s*(?:product|process|data)|\bdealer\b|\bdistributor\b|\bfranchise\b|\bto (the )?(ceo|president|chairman|founder|owner|md|managing director)\b|\b(pa|ea|secretary|chief of staff|office manager|committee|council|alumni|honorary|emeritus)\b|\b(assistant|associate|deputy|interim|former|ex-|retired|advisor|adviser|consultant|board member|non-executive|trustee|student|intern)\b)',re.I)
def score(title):
    t=(title or '').lower().strip()
    if not t or BAD.search(t): return 0,None
    gm=bool(re.search(r'general manager|\bgm\b',t)); vp=bool(re.search(r'vice[- ]president|\bvp\b|\bsvp\b|\bevp\b|\bavp\b',t))
    if re.search(r'(founder|co-?founder|\bceo\b|chief executive|\bowner\b|proprietor)',t) or (re.search(r'(chairman|chairwoman|chairperson)',t) and not re.search(r'(of the board|board)',t)):
        if re.search(r'(chief (technology|financial|operating|marketing|revenue|digital|information|product|commercial) officer)',t) and not re.search(r'(founder|ceo|chief executive|owner)',t): return 0,None
        if re.search(r'(ceo|chief executive)[^,]*(of|,|-|–|—)\s*(the )?[a-z &]*'+FUNC,t) and not re.search(r'(group|company|corporation|holdings|division|business unit)',t): pass
        return 100,'1_founder_ceo_owner'
    if re.search(r'\bpresident\b',t) and not vp and gm: return 90,'2_president'
    if re.search(r'(chairman|chairwoman|chairperson)',t) and not vp: return 75,'5_chair'
    if gm and not re.search(r'(general manager|\bgm\b).*\b'+FUNC,t):
        return (70 if (vp or True) else 0),'4_general_manager'
    if re.search(r'(division|group|business unit|segment|platform|brand)\s+(president|head|leader|general manager)',t) or re.search(r'\bpresident\b.*\b(division|group|business unit|segment|brand)\b',t) and not vp:
        return 80,'3_division_head'
    if re.search(r'\bpresident\b',t) and not vp:
        if re.search(r'president[,\s\-–—&/(]*(of |for )?(the )?'+FUNC,t) and not re.search(r'(ceo|chief executive)',t): return 0,None
        return 90,'2_president'
    if re.search(r'managing director',t):
        if re.search(r'managing director[,\s\-–—&/(]*(of |for )?(the )?'+FUNC,t): return 0,None
        return 85,'2_managing_director'
    return 0,None
