"""Doc 2 step 6: Campaign 8 (large device by business unit). For each curated 10,000+ HCP-facing device company:
(1) persona total = US people, C-Team..Manager, titles in C8_PERSONA, field/R&D excluded (Blitz /v2/search/people, company linkedin_url);
(2) BU weight = US people C-Team..Manager whose title contains the BU keyword (field reps excluded);
per-BU persona estimate = persona total x BU weight share. Writes 2026-11-18-doc-2-large-device.json."""
import json
from doc2_common import call, NOISE, FIELD
C8_PERSONA = ["Marketing", "Commercial Excellence", "Sales Operations", "Commercial Operations", "CRM", "Professional Education",
              "Medical Education", "Marketing Operations", "Digital Marketing", "Customer Engagement", "Product Marketing"]
EXC = NOISE + FIELD + ["Clinical", "Quality", "Regulatory", "Engineering", "Engineer", "Manufacturing", "Supply Chain", "R&D",
                       "Research", "Inside Sales", "Customer Service", "Communications", "Sales Representative", "Sales Manager"]
LI = "https://www.linkedin.com/company/"
CO = {  # name: (linkedin slugs, business units / keywords)
 "Medtronic": (["medtronic", "covidien-2"], ["Cardiac Rhythm", "Structural Heart", "Coronary", "Peripheral Vascular", "Neuromodulation", "Pain", "Spine", "Neurovascular", "Surgical", "ENT", "Pelvic", "Diabetes"]),
 "Abbott (medical devices)": (["abbott-"], ["Electrophysiology", "Structural Heart", "Vascular", "Heart Failure", "Neuromodulation", "Diabetes", "Rhythm"]),
 "Stryker": (["stryker"], ["Spine", "Neurovascular", "Endoscopy", "Joint Replacement", "Trauma", "Instruments", "Sports Medicine", "CMF", "Mako"]),
 "Boston Scientific": (["boston-scientific", "bsc-urology"], ["Electrophysiology", "Watchman", "Interventional Cardiology", "Peripheral", "Urology", "Endoscopy", "Neuromodulation", "Cardiac Rhythm"]),
 "BD": (["bd1"], ["Interventional", "Urology", "Peripheral", "Surgery", "Medication Delivery", "Pharmacy", "Vascular Access"]),
 "Zimmer Biomet": (["zimmerbiomet"], ["Knee", "Hip", "Sports Medicine", "Trauma", "CMF", "ROSA", "Extremities"]),
 "Edwards Lifesciences": (["edwards-lifesciences"], ["TAVR", "Transcatheter", "Surgical Structural", "Mitral", "Tricuspid", "Critical Care"]),
 "Intuitive": (["intuitivesurgical"], ["General Surgery", "Urology", "Gynecology", "Thoracic", "Colorectal", "Ion"]),
 "Baxter": (["baxter-healthcare"], ["Pharmaceuticals", "Medical Products", "Infusion", "Front Line Care", "Surgical", "Renal"]),
 "GE HealthCare": (["gehealthcare"], ["Ultrasound", "Imaging", "Patient Care", "Pharmaceutical Diagnostics", "MR", "CT"]),
 "Siemens Healthineers (incl. Varian)": (["siemens-healthineers", "varian-medical-systems"], ["Imaging", "Radiation Oncology", "Varian", "Ultrasound", "Advanced Therapies", "Diagnostics"]),
 "Philips (health)": (["philips"], ["Image Guided Therapy", "Ultrasound", "Sleep", "Respiratory", "Monitoring", "Precision Diagnosis"]),
 "Olympus": (["olympus"], ["Gastrointestinal", "GI", "Urology", "ENT", "Respiratory", "Surgical", "Endoscopy"]),
 "Smith+Nephew": (["smith-&-nephew", "smithnephew"], ["Sports Medicine", "Orthopaedics", "Reconstruction", "Wound", "ENT", "Trauma"]),
 "Teleflex": (["teleflex"], ["Interventional", "Urology", "Vascular", "Anesthesia", "Surgical", "Emergency"]),
 "Dexcom": (["dexcom"], ["Diabetes", "CGM", "Endocrinology", "Primary Care"]),
 "ResMed": (["resmed"], ["Sleep", "Respiratory", "SaaS"]),
 "Align Technology": (["align-technology"], ["Invisalign", "iTero", "Orthodontic", "GP"]),
 "Dentsply Sirona": (["dentsplysirona"], ["Implants", "Orthodontics", "Endodontics", "Equipment", "Restorative"]),
 "Solventum": (["solventumhealth"], ["MedSurg", "Dental", "Wound", "Infection Prevention"]),
 "Cook Medical": (["cookmedical"], ["Vascular", "Endoscopy", "Urology", "Reproductive", "Aortic", "Interventional"]),
 "B. Braun (US)": (["b--braun-medical-inc.-us"], ["Surgical", "Regional Anesthesia", "Pain", "Renal", "Infusion", "Aesculap"]),
}
out, used = {}, 0
def cnt(urls, inc, exc):
    global used
    r = call("/v2/search/people", {"company": {"linkedin_url": urls}, "people": {"job_title": {"include": inc, "exclude": exc},
             "job_level": ["C-Team", "VP", "Director", "Manager"], "location": {"country_code": ["US"]}}, "max_results": 1})
    used += r.get("fair_usage", {}).get("records_used", 0)
    return r.get("total_results") or 0
for name, (slugs, bus) in CO.items():
    urls = [LI + s for s in slugs]
    tot = cnt(urls, C8_PERSONA, EXC)
    w = {bu: cnt(urls, [bu], NOISE + FIELD + ["Engineer", "Quality", "Regulatory", "Manufacturing", "Supply Chain", "R&D", "Sales Representative", "Sales Manager"]) for bu in bus}
    sw = sum(w.values()) or 1
    out[name] = {"linkedin_urls": urls, "persona_total": tot, "bu_weight": w, "bu_persona_est": {bu: round(tot * v / sw) for bu, v in w.items()}}
    print(name, tot, out[name]["bu_persona_est"], "used", used, flush=True)
out["_meta"] = {"persona_titles": C8_PERSONA, "persona_exclude": EXC, "records_used": used}
json.dump(out, open("2026-11-18-doc-2-large-device.json", "w"), indent=1)
