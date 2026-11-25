import re, sys
src = open("2026-11-18-doc-1-v3.md").read()
body = src[src.index("# We Are DNA Campaign Plan, Doc 1"):]
i_c1 = body.index("## Campaign 1:"); i_c6 = body.index("## Campaign 6:"); i_bl = body.index("## Before launch"); i_of = body.index("## Offers for your feedback")
intro, c1_5, c6_10, before, offers = body[:i_c1], body[i_c1:i_c6], body[i_c6:i_bl], body[i_bl:i_of], body[i_of:]

def rep(s, old, new, count=1):
    assert s.count(old) == count, (old[:70], s.count(old))
    return s.replace(old, new)

# ---------- Doc 1 ----------
d1i = intro
d1i = rep(d1i, "This plan covers ten LinkedIn campaigns", "This plan covers five LinkedIn campaigns")
old_sector = d1i[d1i.index("Campaigns 5 to 8 are sector campaigns"):d1i.index("Across every campaign:")]
new_sector = ("Campaign 5 is a sector campaign for health, care, veterinary and dental groups that are growing by acquisition. "
  "It starts from a board-level event that is already public, an acquisition programme. Events like these usually point to an attraction and retention problem, "
  "and that is exactly what your EVP and Employer Brand work fixes. We speak to the CEO and the most senior people leaders, we never lead with job adverts, and we never offer candidates.\n\n"
  "Our other sector campaigns (retail and hospitality, manufacturing and engineering, financial services) and the two campaigns built on other buying signals from your ICP form "
  "(new private equity investment, and a new CEO or people leader) are in a separate plan, Doc 2. Law and accounting firms are reached through Campaigns 1 to 3.\n\n")
d1i = d1i.replace(old_sector, new_sector)
d1i = rep(d1i, "Campaigns 5 to 10 use a free AI visibility audit as the starting offer", "Campaign 5 uses a free AI visibility audit as the starting offer, as do all the campaigns in Doc 2")
d1b = before
d1b = rep(d1b, "- **Gender pay gap figures:** campaigns 7 and 8 quote", "- **Gender pay gap figures:** two of the sector campaigns in Doc 2 (manufacturing and financial services) quote")
d1b = rep(d1b, "then the sector campaigns (5 to 8)", "then the sector campaigns (Campaign 5 here and Campaigns 1 to 3 in Doc 2)")
d1b = rep(d1b, "A company only enters Campaign 9 or 10 if", "A company only enters Doc 2's private equity or new-leader campaign if")
d1o = rep(offers, "(the starting offer in Campaigns 5 to 10)", "(the starting offer in Campaign 5 and in every Doc 2 campaign)")
doc1 = d1i + c1_5 + d1b + d1o

# ---------- Doc 2 ----------
c = c6_10
for old, new in [(6,1),(7,2),(8,3),(9,4),(10,5)]:
    c = rep(c, f"## Campaign {old}:", f"## Campaign {new}:")
c = rep(c, "- **No overlap with Campaigns 1 to 8:** a company already in an employer reputation or sector campaign that month is skipped here.",
           "- **No overlap with other campaigns:** a company already in one of Doc 1's employer reputation campaigns, or in any sector campaign, that month is skipped here.")
assert not re.search(r"[Cc]ampaigns? (6|7|8|9|10)\b", c), re.findall(r".{30}[Cc]ampaigns? (?:6|7|8|9|10)\b.{20}", c)
d2i = ("# We Are DNA Campaign Plan, Doc 2\n\n"
  "This plan covers five LinkedIn campaigns, built from your ICP form. It sits alongside Doc 1 (Nov 12, 2026), which holds the employer reputation campaigns, Casual Connections "
  "and the health and care buy-and-build campaign. In Doc 1 these five were Campaigns 6 to 10; nothing in them has changed except their numbers.\n\n"
  "Campaigns 1 to 3 are sector campaigns, one per sector: retail and hospitality, manufacturing and engineering, and financial services (health and care is Doc 1's Campaign 5, "
  "and law and accounting firms are reached through Doc 1's Campaigns 1 to 3). Each one starts from a board-level event that is already public, such as a results statement "
  "that names people costs, or a gender pay gap report. Events like these usually point to an attraction and retention problem, and that is exactly what your EVP and Employer "
  "Brand work fixes. We speak to the CEO and the most senior people leaders, we never lead with job adverts, and we never offer candidates.\n\n"
  "Campaigns 4 and 5 reach the same five sectors through a different buying signal from your ICP form:\n\n"
  "- new private equity investment\n- a new CEO or people leader\n\n")
across = intro[intro.index("Across every campaign:"):]
across = rep(across, "Campaigns 1 to 3 start with a free reputation snapshot (Offer 8), which includes what AI tools tell candidates about the company. Campaigns 5 to 10 use a free AI visibility audit as the starting offer, and Campaign 4 has no offer by design.",
  "every campaign in this plan uses a free AI visibility audit as the starting offer (Doc 1's employer reputation campaigns use the reputation snapshot, Offer 8).")
d2b = before
d2b = rep(d2b, "- **Gender pay gap figures:** campaigns 7 and 8 quote", "- **Gender pay gap figures:** Campaigns 2 and 3 quote")
d2b = rep(d2b, "the employer reputation campaigns (1 to 3) take priority, then the sector campaigns (5 to 8). Campaign 4 skips anyone already in another campaign. A company only enters Campaign 9 or 10 if",
  "Doc 1's employer reputation campaigns (1 to 3) take priority, then the sector campaigns (Doc 1's Campaign 5 and Campaigns 1 to 3 here). Doc 1's Casual Connections campaign skips anyone already in another campaign. A company only enters Campaign 4 or 5 here if")
d2b = rep(d2b, "- **Campaign 4 senders:**", "- **Doc 1 Campaign 4 senders:**")
d2b = rep(d2b, "before Campaign 4 can start", "before Doc 1's Campaign 4 can start")
d2b = rep(d2b, "- **Reputation snapshot:** Campaigns 1 to 3 offer", "- **Reputation snapshot:** Doc 1's Campaigns 1 to 3 offer")
d2o = offers
d2o = rep(d2o, "Offers 4, 5, 8 and 9 are the ones Campaigns 1 to 3 use.", "Offers 4, 5, 8 and 9 are the ones Doc 1's Campaigns 1 to 3 use; every campaign in this plan starts with Offer 1.")
d2o = rep(d2o, "(the starting offer in Campaigns 5 to 10)", "(the starting offer in every campaign in this plan, and in Doc 1's Campaign 5)")
d2o = rep(d2o, "This is the promise in Campaign 2.", "This is the promise in Doc 1's Campaign 2.")
d2o = rep(d2o, "This is the promise in Campaign 1.", "This is the promise in Doc 1's Campaign 1.")
d2o = rep(d2o, "This is the promise in Campaign 3.", "This is the promise in Doc 1's Campaign 3.")
d2o = rep(d2o, "(the starting offer in Campaigns 1 to 3)", "(the starting offer in Doc 1's Campaigns 1 to 3)")
doc2 = d2i + across + c + d2b + d2o
for name, d in [("doc1", doc1), ("doc2", doc2)]:
    assert "—" not in d and "–" not in d, name + " has em/en dash"
    open(f"/tmp/claude-0/-home-user/0a7ce3c0-ead6-5305-bf68-d41e04bd4208/scratchpad/split/{name}.md", "w").write(d)
    print(name, len(d.splitlines()), "lines", [l for l in d.splitlines() if l.startswith("## ")])
