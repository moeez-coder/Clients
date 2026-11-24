"""The 5 GRN MPC segment sequences (2026-11-24). Base = the live 734516/756466 copy (verbatim from HeyReach, read 2026-11-24);
per segment only the role-family slot in messages 2 and 3 changes (SOP open-role-moe-mpc.md section 3), and message 1's
"fresh one" sentence comes from the {Open_Line} custom field so reposted 60+ day roles can say so.
Usage: python3 sequence.py  -> prints each segment's text and writes sequences.json (HeyReach v2 sequence JSON per segment)."""
import json, os
SLOTS = {  # segment: (message 2 slot, message 3 slot)
    "executive": ("senior leadership", "Senior leadership roles"),
    "operations-plant": ("plant or operations leadership", "Plant and operations leadership roles"),
    "engineering-quality": ("engineering or quality leadership", "Engineering and quality leadership roles"),
    "supply-chain-purchasing": ("supply chain or purchasing", "Supply chain and purchasing roles"),
    "ehs-maintenance": ("EHS or maintenance leadership", "EHS and maintenance leadership roles"),
}
NAMES = {"executive": "US | Recruiter | MPC Executive | Moe v1", "operations-plant": "US | Recruiter | MPC Ops & Plant | Moe v1",
         "engineering-quality": "US | Recruiter | MPC Eng & Quality | Moe v1", "supply-chain-purchasing": "US | Recruiter | MPC Supply Chain | Moe v1",
         "ehs-maintenance": "US | Recruiter | MPC EHS & Maint | Moe v1"}
OPEN_FRESH = "Not sure if that's a fresh one or something you've had open for a bit, but either way I have a candidate who fits that pretty closely."
OPEN_REPOST = "Looks like it's been reposted a few times since {month}, so I'm guessing it's still open. I have a candidate who fits that pretty closely."
def msgs(seg):
    s2, s3 = SLOTS[seg]
    m1 = ("Hey {FIRST_NAME}, thanks for connecting.\n\nSaw {Company_Name} has a {Job_Title_Open_} role listed, looks like you need someone with {Job_Description}.\n\n"
          "{Open_Line}\n\nWant me to send their profile over so you can take a look?")
    f1 = "Hey there, thanks for connecting.\n\nSaw your team has a leadership role listed.\n\n" + OPEN_FRESH + "\n\nWant me to send their profile over so you can take a look?"
    m2 = (f"Hey {{FIRST_NAME}}, following up on this, didn't want it to get buried in your inbox.\n\nIf the {{Job_Title_Open_}} role or any other {s2} role is still open, "
          "happy to send over a candidate or two who could be a fit.\n\nWorth a quick look, even just to compare against who's already in your pipeline?")
    f2 = (f"Hey there, following up on this, didn't want it to get buried in your inbox.\n\nIf you have a {s2} role still open, happy to send over a candidate or two "
          "who could be a fit.\n\nWorth a quick look, even just to compare against who's already in your pipeline?")
    m3 = (f"No worries if the timing's off, {{FIRST_NAME}}.\n\n{s3} sometimes sit for a while or get filled quietly, so if it's still open I'll send a profile over, "
          "and if not, no hard feelings.\n\nJust let me know either way.")
    f3 = m3.replace(", {FIRST_NAME}", "")
    return (m1, f1), (m2, f2), (m3, f3)
def heyreach_json(seg):
    (m1, f1), (m2, f2), (m3, f3) = msgs(seg)
    end = lambda d=0, u="HOUR": {"nodeType": "END", "actionDelay": d, "actionDelayUnit": u}
    msg = lambda m, f, d, nxt: {"nodeType": "MESSAGE", "actionDelay": d, "actionDelayUnit": "DAY",
                                "payload": {"messageVersions": [{"type": "TEXT", "message": m}], "fallbackMessage": f},
                                "conditionalNode": end(), "unconditionalNode": nxt}
    return {"nodeType": "CONNECTION_REQUEST", "actionDelay": 0, "actionDelayUnit": "HOUR",
            "payload": {"messages": [], "fallbackMessage": None, "toBeWithdrawnAfterDays": 21},
            "conditionalNode": msg(m1, f1, 1, msg(m2, f2, 2, msg(m3, f3, 2, end(1, "DAY")))), "unconditionalNode": end(1, "DAY")}
def text(seg):
    (m1, _), (m2, _), (m3, _) = msgs(seg)
    return f"Connection request: blank (no note).\n\nMessage 1 (1 day after accepting):\n{m1}\n\nMessage 2 (2 days later):\n{m2}\n\nMessage 3 (2 days later):\n{m3}"
if __name__ == "__main__":
    json.dump({s: {"name": NAMES[s], "sequence": heyreach_json(s), "text": text(s)} for s in SLOTS},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sequences.json"), "w"), indent=1)
    print(text("executive"))
