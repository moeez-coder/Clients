# 2026-10-27 HeyReach wave 2: Security and Data Bench (C&G)

- **Client:** C&G Consulting Services (`4ca09bb2-25f9-4410-b269-9c8bcb816881`)
- **Config:** `09be87f3-0db4-4e2d-842d-b70af7d29d7c`
- **Campaign:** `c8855ae2-5c95-419b-8d8e-000c13cc757a`
- **Purpose:** expanding the existing segment's outreach. Moe asked for about 2,500 more leads in the live campaign.

## Selection

```
python3 build_wave.py 2026-10-23-3-leads.csv 2026-10-27-heyreach-wave2.csv 2500 2026-10-23-2-heyreach-wave1.csv --drop-odd-names
```

- **Source:** the complete Haiku-qualified snapshot `2026-10-23-3-leads.csv`, QUALIFIED leads within the 3-per-company cap.
- **Excluded:** every lead in wave 1, including the 7 blacklisted.
- **Order:** Northeast first, then `qualified_rank`, then company name.
- **New this wave, `--drop-odd-names`:** wave 1 showed HeyReach greets with the LinkedIn-resolved first name, not the cleaned one we send. So raw names that would render badly in `{FIRST_NAME}` are now **dropped**, not cleaned: bracketed nicknames, middle or trailing initials, ALL-CAPS, honorifics or symbols. **72 dropped.**
- **Not-a-person filter:** 4 dropped. 2 were genuine non-people (American Capital, "CIO FAIRWAY MARKET"). 2 were false positives: Simon Pearce at Simon Pearce, Angelo Picatagi at TPG Angelo Gordon.

## Result

`2026-10-27-heyreach-wave2.csv`: **2,500 leads at 2,240 companies.**
- 0 overlap with wave 1, 0 duplicates, all QUALIFIED in `-3`.
- **Location:** 678 in the Northeast. That is every remaining Northeast lead within the cap; the other 1,822 are elsewhere in the US.
- **Rank at their company:**

  | Rank | Leads |
  |---|---|
  | 1 | 1,979 |
  | 2 | 331 |
  | 3 | 190 |

  Rank-2 and rank-3 leads are the second or third person at companies already contacted in wave 1, still within the cap.
- **By role:**

  | Role | Leads |
  |---|---|
  | CTO | 907 |
  | CIO | 766 |
  | VP Engineering | 372 |
  | CISO | 264 |
  | VP of Data | 101 |
  | Head of Data | 47 |
  | Head of IT | 43 |

- **Pacing:** at ~250 connection requests a day this is about 10 sending days. Fewer senders, or senders on cooldown, stretch that.

## Push

Not yet pushed. It waits on Moe's choice of campaign, because two campaigns share list `1056840` (see README History, 2026-10-27).

## Known limits

Same as wave 1: no DNC check (`Non_Connect` file not loaded), and Haiku verdicts made without web access.
