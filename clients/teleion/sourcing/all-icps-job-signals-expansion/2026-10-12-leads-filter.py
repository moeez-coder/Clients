import csv,re,collections,os,pickle
exec(open('people2.py').read().split("rows=[];drop")[0])
RANK=r"(evp|svp|vp|executive vice president|senior vice president|managing director|md|group|global|enterprise|corporate|firmwide|firm-wide|chief)"
CORE={ # normalized core -> group
 'chief compliance officer':1,'chief risk officer':1,'chief risk and compliance officer':1,'chief compliance and risk officer':1,'chief bsa officer':1,'bsa officer':1,'bsa aml officer':1,'chief aml officer':1,'chief aml bsa officer':1,'bsa aml compliance officer':1,'chief bsa aml officer':1,'chief bsa aml and compliance officer':1,'bank secrecy act officer':1,'chief bank secrecy act officer':1,
 'chief information officer':2,'cio':2,'chief information security officer':2,'ciso':2,'chief model risk officer':2,'chief information and security officer':2,
 'treasurer':3,'corporate treasurer':3,'chief financial officer':3,'cfo':3,'chief accounting officer':3,
 'chief executive officer':4,'ceo':4,'president':4,'chief human resources officer':4,'chro':4,'chief people officer':4,'chairman':4,'chair':4,'board chair':4,'chairman of the board':4,'chair of the board':4,'chairwoman':4,'chairperson':4,
}
ABBR={'sr':'senior','sr.':'senior'}
def parts(t,cname,croot):
    t=t.lower()
    t=re.sub(r"\(.*?\)","",t)
    t=re.sub(r"[^a-z0-9&/,|\- ]"," ",t)
    pieces=re.split(r"\s*(?:&|/|,|\||\band\b|\s-\s|\bat\b|\bof\b)\s*",t)
    return [re.sub(r"\s+"," ",p).strip() for p in pieces if p.strip()]
def strict(t,cname,dom):
    if BAD.search(t): return None
    ps=parts(t,cname,dom)
    cn=re.sub(r"[^a-z0-9 ]","",(cname or '').lower());roots={w for w in cn.split() if len(w)>2}|{re.sub(r"\.(com|org|net|bank)$","",dom.split('.')[0]) if dom else ''}
    groups=[];
    for p in ps:
        if p in('evp','svp','vp','executive vice president','senior vice president','managing director','md','group','global','enterprise','corporate','firmwide','the','chief') or p=='': continue
        # strip leading rank words
        q=re.sub(r"^(evp|svp|executive vice president|senior vice president|managing director|group|global|enterprise|corporate|firmwide)\s+","",p)
        q=re.sub(r"\s+(evp|svp|executive vice president|senior vice president|managing director)$","",q)
        if q in CORE: groups.append(CORE[q]);continue
        if q in('bsa','aml','bsa aml','aml bsa','compliance','risk','chief'): continue
        # company name pieces
        words=set(q.split())
        if words and words<= roots|{'inc','corp','the','financial','bank','group','holdings','company','co','na','n','a'}: continue
        return None
    return groups or None
rows=[];drop=collections.Counter()
for x in r:
    t=x['Job Title'] or ''
    d=nd(x['Domain'] or x['Company Domain']);co=comp.get(d)
    name=x['Company Name'] or (co['company_name'] if co else '')
    g=strict(t,name,d)
    if not g: drop['not company-level title']+=1;continue
    if d in contacted: drop['contacted']+=1;continue
    if any(k in (name or '').lower() for k in dnc): drop['DNC']+=1;continue
    n=sorted(set(g))[0]
    gname,note=CAT[n-1][1],CAT[n-1][3]
    rows.append({'linkedin_url':x['LinkedIn Profile'] or '-','first_name':x['First Name'] or '-','last_name':x['Last Name'] or '-','full_name':x['Full Name'] or '-','job_title':t,'persona_group':gname,'also_matches':'; '.join(CAT[i-1][1] for i in sorted(set(g)) if i!=n) or '-','caller_note':note,'company_name':name or '-','company_domain':d or '-','segment':x['Segment'] or (co['segment'] if co else '-'),'location':x['Location'] or '-','signal_codes':x['Signal Codes'] or (co['signal_codes'] if co else '-'),'signals_triggers':x['Signals Triggers'] or (co['signals_triggers'] if co else '-'),'signal_notes':x['Notes'] or (co['notes'] if co else '-')})
print(len(r),len(rows),dict(drop))
print(collections.Counter(o['persona_group'] for o in rows))
cc=collections.Counter(o['company_name'] for o in rows);print(len(cc),cc.most_common(10))
print('titles',collections.Counter(o['job_title'] for o in rows).most_common(15))
pickle.dump(rows,open('rows3.pkl','wb'))
