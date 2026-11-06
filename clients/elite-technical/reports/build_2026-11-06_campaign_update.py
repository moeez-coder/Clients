"""Builds reports/2026-11-06-elite-campaign-update.pdf (client-facing, for Joseph Monaco).
Numbers are HeyReach get_overall_stats per campaign, pulled 2026-11-06 ~12:50 UTC, and the repo's lead counts."""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

OUT = '/home/user/Clients/clients/elite-technical/reports/2026-11-06-elite-campaign-update.pdf'
NAVY = colors.HexColor('#1F3A5F'); LIGHT = colors.HexColor('#EEF2F7'); GREEN = colors.HexColor('#2E7D4F'); GREY = colors.HexColor('#5A6270')
ss = getSampleStyleSheet()
H1 = ParagraphStyle('h1', parent=ss['Title'], fontName='Helvetica-Bold', fontSize=20, textColor=NAVY, alignment=0, spaceAfter=4)
SUB = ParagraphStyle('sub', parent=ss['Normal'], fontSize=10, textColor=GREY, spaceAfter=14)
H2 = ParagraphStyle('h2', parent=ss['Heading2'], fontName='Helvetica-Bold', fontSize=13.5, textColor=NAVY, spaceBefore=14, spaceAfter=6)
B = ParagraphStyle('b', parent=ss['Normal'], fontSize=10, leading=14, spaceAfter=5)
BUL = ParagraphStyle('bul', parent=B, leftIndent=12, bulletIndent=2, spaceAfter=3)
SM = ParagraphStyle('sm', parent=B, fontSize=8.5, leading=11, textColor=GREY)
CELL = ParagraphStyle('cell', parent=B, fontSize=8, leading=10, spaceAfter=0)
CELLB = ParagraphStyle('cellb', parent=CELL, fontName='Helvetica-Bold', textColor=colors.white)

def bullets(items): return [Paragraph(t, BUL, bulletText='•') for t in items]
def table(rows, widths, hl_rows=()):
    data = [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [('BACKGROUND', (0, 0), (-1, 0), NAVY), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
          ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT]),
          ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor('#C9D1DC')),
          ('TOPPADDING', (0, 0), (-1, -1), 4), ('BOTTOMPADDING', (0, 0), (-1, -1), 4)]
    for r in hl_rows: st.append(('BACKGROUND', (0, r), (-1, r), colors.HexColor('#E3F1E8')))
    t.setStyle(TableStyle(st)); return t

s = []
s += [Paragraph('Elite Technical: LinkedIn Outreach Update', H1),
      Paragraph('Prepared by Algo Acquisition for Joseph Monaco. Results as of November 6, 2026, 6:50 AM Central Time.', SUB)]

s += [Paragraph('At a glance', H2)]
s += bullets([
    '<b>898 connection requests</b> sent so far across 6 campaigns. <b>88 accepted (9.8%)</b>, 15 conversations started.',
    'The campaign built on <b>live technical hiring</b> got the most interest: <b>14.2% acceptance</b>, about twice the federal contract campaigns (5.9% to 7.6%).',
    'So we moved everything toward hiring signals. The federal contract and candidate fraud campaigns are paused, and two new <b>open-role recruiter campaigns</b> are live, with six more ready to go.',
    'Reply numbers are still early: 1 reply so far. Most accepted connections were made in the last 4 days and are only now getting the follow-up messages.',
])

s += [Paragraph('What has run so far', H2)]
rows = [['Campaign', 'Who we contacted', 'Dates', 'Sent', 'Accepted', 'Rate', 'Convos', 'Replies', 'Status'],
        ['Cleared Talent for New Federal Contracts (v1)', 'IT and engineering leaders at companies with a new federal award', 'Oct 30 to Nov 5', '73', '5', '6.8%', '3', '0', 'Paused'],
        ['Cleared Talent for New Federal Contracts (v2)', 'Same audience, second sender group', 'Oct 30 to Nov 5', '92', '7', '7.6%', '3', '0', 'Paused'],
        ['Federal Contracts, 12-month awards', 'Wider award window, 2 to 3 contacts per company', 'Oct 30 to Nov 5', '170', '10', '5.9%', '1', '1', 'Paused'],
        ['Candidate Fraud in Technical Hiring', 'Talent leaders at companies hiring remote or hybrid tech roles', 'Nov 2 to Nov 5', '415', '59', '<b>14.2%</b>', '7', '0', 'Paused'],
        ['Recruiter: Cybersecurity Open Roles', 'Security hiring managers with a live security job post', 'Live since Nov 5', '148', '7', 'Day 1', '1', '0', '<b>Live</b>'],
        ['Recruiter: IT Infrastructure and Support Open Roles', 'IT hiring managers with a live IT job post', 'Live since Nov 6', '0', '0', 'Starting', '0', '0', '<b>Live</b>'],
        ['<b>Total</b>', '', '', '<b>898</b>', '<b>88</b>', '<b>9.8%</b>', '<b>15</b>', '<b>1</b>', '']]
s += [table(rows, [1.4*inch, 1.6*inch, 0.75*inch, 0.45*inch, 0.68*inch, 0.6*inch, 0.6*inch, 0.6*inch, 0.6*inch], hl_rows=(4,))]
s += [Spacer(1, 4), Paragraph('Sent = connection requests. Rate = accepted divided by sent. A new campaign starts low because people take a few days to accept, so the Cybersecurity number will rise. Convos = people who received at least one message after accepting.', SM)]

s += [Paragraph('How we changed strategy', H2)]
s += [Paragraph('<b>What the first week showed.</b> The federal contract campaigns reached the right companies, but the trigger (a new contract award) did not get much attention: about 1 in 15 people accepted. The candidate fraud campaign, aimed at companies actively hiring technical people, did twice as well, with about 1 in 7 accepting. The companies that respond are the ones hiring right now.', B),
      Paragraph('<b>What we changed.</b> We paused the lower-interest campaigns and rebuilt around the strongest signal: a specific, live job post.', B)]
s += bullets([
    '<b>Every lead is tied to a real job post</b> at their company, posted in the last 30 days. The first message names that exact role, so it reads as relevant from the first line.',
    '<b>We message the hiring manager for that role</b>, for example the Director of IT for an IT job or the security lead for a security job. A talent leader is used only when no hiring manager can be found.',
    '<b>We use a proven sequence.</b> This open-role sequence produced a <b>19.4% reply rate</b> for two other staffing firms we run campaigns for. It is short: a connection request, then three short messages two days apart, offering to send a matching candidate profile.',
    '<b>We split by role family</b> so each message fits the reader: Cybersecurity, IT Infrastructure, Software, Data and AI, Cloud, Enterprise Apps, Electrical and Controls, and Mechanical and Manufacturing.',
    '<b>Your rules stay in place</b>: $100M to $1B revenue, 501 to 10,000 employees, US based, no staffing firms, education, government or nonprofits, and none of your past clients from your do-not-contact list.',
    '<b>We check every lead against their live LinkedIn profile before launch.</b> We removed 142 people who had changed jobs or whose names would not print cleanly in the message.',
])
s += [Paragraph('<b>Why Cybersecurity and IT went first.</b> Three of the five dream companies you named are security firms (Varonis, Tenable, Commvault). Your target titles lead with IT leadership, and your Top Secret facility clearance is a real edge for security hiring.', B)]

s += [KeepTogether([Paragraph('What is live and what is queued', H2),
      table([['Campaign', 'Leads', 'Companies', 'Status'],
             ['Recruiter: Cybersecurity Open Roles', '1,402', '450', '<b>Live</b> since Nov 5'],
             ['Recruiter: IT Infrastructure and Support', '2,774', '912', '<b>Live</b> since Nov 6'],
             ['Recruiter: Software Engineering', '4,836', '866', 'Next to launch'],
             ['Recruiter: Data and AI', '2,837', '805', 'Built, queued'],
             ['Recruiter: Electrical, Controls and Embedded', '2,859', '607', 'Built, queued'],
             ['Recruiter: Mechanical, Manufacturing and Quality', '3,675', '759', 'Built, queued'],
             ['Recruiter: Enterprise Applications (ERP/CRM)', '513', '230', 'Built, queued'],
             ['Recruiter: Cloud and DevOps', '406', '239', 'Built, queued']],
            [3.0*inch, 0.8*inch, 0.9*inch, 1.9*inch], hl_rows=(1, 2))])]
s += [Spacer(1, 4), Paragraph('About 19,000 hiring managers in total, at companies with an open technical role posted in the last 30 days. Sending runs at about 190 connection requests a day across 11 LinkedIn profiles, 7 days a week. We launch the queued campaigns one at a time as the live ones work through their lists, so each one gets a clean read.', B)]

s += [Paragraph('What we need from you', H2)]
s += bullets([
    '<b>A candidate profile ready for each reply.</b> The first message offers a candidate who fits the open role. When someone says yes, we pass them to you (Joseph, Phil, Mike or Jeff) right away, and a quick, specific profile is what turns that reply into a meeting.',
    '<b>Tell us about any companies to skip</b> that are not on your do-not-contact list yet, such as current clients or companies in active talks.',
    '<b>Tell us which role families you can fill fastest.</b> We will move those campaigns up the queue.',
])
s += [Spacer(1, 8), Paragraph('Next update: once the two live campaigns have a full week of follow-up messages out.', SM)]

def footer(c, d):
    c.saveState(); c.setFont('Helvetica', 8); c.setFillColor(GREY)
    c.drawString(0.6*inch, 0.45*inch, 'Algo Acquisition  |  Elite Technical outreach update  |  November 6, 2026')
    c.drawRightString(letter[0]-0.6*inch, 0.45*inch, f'Page {d.page}'); c.restoreState()
SimpleDocTemplate(OUT, pagesize=letter, leftMargin=0.6*inch, rightMargin=0.6*inch, topMargin=0.6*inch, bottomMargin=0.7*inch,
                  title='Elite Technical: LinkedIn Outreach Update', author='Algo Acquisition').build(s, onFirstPage=footer, onLaterPages=footer)
print(OUT)
