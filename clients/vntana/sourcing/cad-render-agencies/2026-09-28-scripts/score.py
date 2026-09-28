import json,re,collections
M=json.load(open('merged.json'))
R=re.compile(r'\b(render(s|ing|ings)?|CGI|photo-?realistic|3D visuali[sz]ation|product visuali[sz]ation|3D animations?|product animations?|technical animations?|industrial animations?|3D product|3D modell?ing|3D configurator|virtual photography)\b',re.I)
C=re.compile(r'\b(CAD|SolidWorks|Creo|CATIA|Siemens NX|Inventor|STEP files?|engineering (data|files|drawings|models)|native CAD|from CAD)\b')
P=re.compile(r'\b(products?|industrial|manufactur\w*|machinery|machines?|equipment|engineering|B2B|technical|automotive|e-?commerce|packaging|consumer goods|furniture|appliances?|medical devices?|brands?)\b',re.I)
ARCH=re.compile(r'\b(architectur\w*|archviz|real estate|interior design|interiors?|BIM|property|floor ?plans?|landscape|residential)\b',re.I)
AGIND={'advertising services','marketing services','design services','graphic design','animation and post-production','media production','photography','design','marketing & advertising','marketing and advertising','animation','media production','motion pictures and film','entertainment providers','information services','it services and it consulting','software development','industrial design'}
BADIND=re.compile(r'(higher education|education|staffing|computer games|government|hospital|real estate|construction|architecture)',re.I)
out=[]
for k,r in M.items():
    t=r['text'] or ''; ind=(r['industry'] or '').lower()
    if '/school/' in k or BADIND.search(ind): continue
    if not R.search(t): continue
    nr=len(set(m.group(0).lower() for m in R.finditer(t))); nc=bool(C.search(t)); np_=len(set(m.group(0).lower() for m in P.finditer(t))); na=len(set(m.group(0).lower() for m in ARCH.finditer(t)))
    agency = ind in AGIND or re.search(r'(studio|cgi|3d|render|visual|agency|creative|media|design|animation|pixel)',r['name'],re.I)
    if not agency: continue
    if na>=2 and na>=np_: continue  # archviz-dominant
    if np_==0: continue
    score=nr*2+np_+(4 if nc else 0)-na
    tier='A' if (nc and nr>=2) or (nr>=3 and np_>=3) else 'B' if nr>=2 or np_>=3 else 'C'
    r['cad_mention']='yes' if nc else 'no'; r['render_terms']='; '.join(sorted(set(m.group(0).lower() for m in R.finditer(t))))
    r['score']=score; r['tier']=tier; out.append(r)
out.sort(key=lambda r:(-r['score']))
print(len(out),collections.Counter(r['tier'] for r in out))
print(collections.Counter(r['hq_country'] for r in out).most_common(12))
json.dump(out,open('scored.json','w'))
for r in out[:50]: print(r['tier'],r['score'],r['name'],'|',r['industry'],'|',r['hq_country'],'|',r['employees'])
