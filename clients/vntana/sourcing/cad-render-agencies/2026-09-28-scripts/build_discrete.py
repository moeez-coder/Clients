import csv,glob,collections
D='/home/user/Clients/clients/vntana/sourcing/cad-render-agencies/'
base=list(csv.DictReader(open(D+'2026-09-28-agency-clients.csv')))
M={}
for f in sorted(glob.glob('mfg/out_m*.csv')):
    rows=list(csv.reader(open(f,encoding='utf8',errors='ignore')))
    for r in rows[1:]:
        if len(r)>=6: M[r[0]]={'manufacturing_type':r[1],'what_they_make':r[2],'mfg_confidence':r[3],'mfg_evidence_url':r[4],'mfg_note':r[5]}
need=[b for b in base if b['physical_product_maker']!='no']
print('classified',sum(1 for b in need if b['client_name'] in M),'/',len(need))
VALID={'discrete','process','mixed','not_manufacturer','unknown'}
out=[]
for b in base:
    m=M.get(b['client_name']) if b['physical_product_maker']!='no' else {'manufacturing_type':'not_manufacturer','what_they_make':'-','mfg_confidence':b['classification_confidence'],'mfg_evidence_url':'-','mfg_note':'carried from 2026-09-28 classification (physical_product_maker=no); not re-checked'}
    m=dict(m or {'manufacturing_type':'unknown','what_they_make':'-','mfg_confidence':'low','mfg_evidence_url':'-','mfg_note':'not classified'})
    if m['manufacturing_type'] not in VALID: m['manufacturing_type']='unknown'
    t=m['manufacturing_type']
    m['is_discrete_manufacturer']={'discrete':'yes','mixed':'partly','process':'no','not_manufacturer':'no'}.get(t,'unknown')
    import re
    if b['pitch_priority']=='P1' and b['client_name'] not in ('Honda','Kawasaki','Mitsubishi Heavy Industries') and re.search(r'\b(aircraft|jets?|aerospace|avionics|defen[cs]e|missiles?|helicopters?|munitions|military)\b',m.get('what_they_make','')+' '+m.get('mfg_note',''),re.I):
        b=dict(b,pitch_priority='P3'); m['mfg_note']='aerospace/defense = VNTANA ICP disqualifier, P1->P3; '+m.get('mfg_note','')
    out.append({**b,**{k:(v if v not in ('',None) else '-') for k,v in m.items()}})
po={'P1':0,'P2':1,'P3':2,'SKIP':3,'EXCLUDE':4}; do={'yes':0,'partly':1,'unknown':2,'no':3}
out.sort(key=lambda r:(do[r['is_discrete_manufacturer']],po[r['pitch_priority']],-int(r['n_agencies']),r['client_name'].lower()))
cols=['client_name','likely_company','is_discrete_manufacturer','manufacturing_type','what_they_make','mfg_confidence','mfg_evidence_url','mfg_note']+[k for k in base[0] if k not in('client_name','likely_company')]
w=csv.DictWriter(open(D+'2026-10-02-agency-clients-discrete.csv','w',newline=''),fieldnames=cols); w.writeheader(); w.writerows(out)
print(collections.Counter(r['is_discrete_manufacturer'] for r in out))
print(collections.Counter(r['manufacturing_type'] for r in out))
disc=[r for r in out if r['is_discrete_manufacturer']=='yes']
print('discrete by priority',collections.Counter(r['pitch_priority'] for r in disc))
print('discrete by segment',collections.Counter(r['vntana_segment'] for r in disc).most_common())
print('discrete conf',collections.Counter(r['mfg_confidence'] for r in disc))
print('P1 not discrete',[(r['client_name'],r['manufacturing_type']) for r in out if r['pitch_priority']=='P1' and r['is_discrete_manufacturer']!='yes'][:40])
print('process examples',[r['client_name'] for r in out if r['manufacturing_type']=='process'][:30])
