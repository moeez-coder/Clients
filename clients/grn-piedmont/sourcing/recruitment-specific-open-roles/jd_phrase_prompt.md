<!-- Prompt supplied by Moe on 2026-11-16 for the {Job_Description} phrase, plus the working constraints given to the sub-agents that ran it. -->

# Task

You get a batch file `in_NN.json`: a JSON array of objects `{"id", "title", "job_description"}`. For EACH object, run the prompt below against its `job_description` and produce one phrase. Also produce a cleaned role title. Write `out_NN.json` in the same folder: a JSON array, same order, one object per input: `{"id": <same>, "role": <clean title>, "phrase": <the phrase>}`.

## The prompt (from the user, apply it exactly, once per job description)

You are extracting one specific requirement from a job description to complete this sentence: "looks like you need someone with ___"

Steps:

1. Read the full job description.

2. Identify the single most specific, distinctive requirement mentioned, a skill, tool, certification, years of experience, technology, or qualification. Prefer something concrete and technical over something generic like "strong communication skills" or "team player."

3. Write it as a short phrase that completes the sentence "looks like you need someone with ___" so it reads naturally out loud.

Rules:

- Output only the phrase, nothing else, no quotes, no period at the end, no explanation.

- Start with a lowercase word unless it begins with a proper noun (a brand, software name, or certification).

- Keep it to one line, ideally under 12 words.

- Do not copy a full sentence from the JD, condense it into a natural phrase.

- If the JD lists several strong candidates, pick the one that sounds most specific to this role, not the most generic one.

Examples of good output:

experience programming Allen-Bradley PLCs in an industrial automation environment

a PE license and background leading HVAC controls projects

5+ years managing electrical projects on commercial construction sites

hands-on experience with SCADA systems and process controls troubleshooting

Two more phrases the user confirmed as working well:

heavy civil ironworking experience with welding and rigging

3-5 years of wireless telecom construction experience with TMO, AT&T, or Verizon

## Extra constraints

- Only use requirements that are actually stated in that job description. Never invent a number of years, a tool or a certification.
- A phrase may start with a digit (e.g. "5+ years ...").
- No em dashes. At most 14 words. A phrase beginning with "a" or "an" is fine when it names a credential (see the PE license example).
- `role`: the clean job title in Title Case from `title`: drop locations, site or division names, shifts, requisition codes, brackets, words like Onsite or Hybrid; natural order ("Director, Quality" becomes "Director of Quality", "Manager - Manufacturing" becomes "Manufacturing Manager"); write "Senior" not "Sr."; keep acronyms uppercase.

## How to work

- Read each job description yourself and write the phrase by judgment. Do not write a script or template that generates phrases.
- Use the Write tool for the output file. Then run a short python check: the file parses; same count and same ids in order as the input; every phrase is non-empty, one line, at most 14 words, no trailing period, no quotes, no em dash. Fix failures and re-check.
- Use only uniquely named files (include your batch number) if you need scratch files; other agents share this folder.
- Reply with only: the count written, and the ids where the job description gave nothing specific.
