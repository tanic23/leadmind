import csv
import json
import time
from outreach_generator import generate_email, generate_sms, generate_followup

"""
bulk_outreach.py

Reads a CSV of leads and generates personalized outreach for each.

CSV format expected (leads.csv):
name, company, role, industry, pain_point, channel

Example:
Sarah,Acme Logistics,Head of Operations,Logistics,Manual route planning,email
James,TechFlow,VP Sales,SaaS,Low reply rates,sms
"""


def load_leads(filepath: str) -> list:
    leads = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads


def run_bulk_outreach(csv_path: str, rep: dict, output_path: str = "outreach_results.json"):
    leads = load_leads(csv_path)
    results = []

    for i, lead in enumerate(leads):
        channel = lead.get("channel", "email").strip().lower()
        print(f"[{i+1}/{len(leads)}] Generating {channel} for {lead.get('name')} at {lead.get('company')}...")

        try:
            if channel == "email":
                content = generate_email(lead, rep)
            elif channel == "sms":
                content = {"sms": generate_sms(lead, rep)}
            elif channel == "followup":
                content = {"followup": generate_followup(lead, rep)}
            else:
                content = {"error": f"Unknown channel: {channel}"}

            results.append({
                "lead": lead,
                "channel": channel,
                "content": content,
                "status": "generated"
            })

        except Exception as e:
            results.append({
                "lead": lead,
                "channel": channel,
                "content": None,
                "status": f"error: {str(e)}"
            })

        # Be kind to the API — small delay between calls
        time.sleep(0.5)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. Results saved to {output_path}")
    return results


if __name__ == "__main__":
    rep = {
        "name": "Alex",
        "title": "Account Executive",
        "company_context": "RouteAI — AI-powered route optimization that cuts delivery costs by 30%"
    }

    # Create a sample leads.csv if you don't have one
    sample_csv = "leads.csv"
    with open(sample_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "company", "role", "industry", "pain_point", "channel"])
        writer.writeheader()
        writer.writerows([
            {"name": "Sarah", "company": "Acme Logistics", "role": "Head of Ops", "industry": "Logistics", "pain_point": "Manual routing", "channel": "email"},
            {"name": "James", "company": "TechFlow", "role": "VP Sales", "industry": "SaaS", "pain_point": "Low reply rates", "channel": "sms"},
            {"name": "Maria", "company": "SwiftDeliver", "role": "COO", "industry": "E-commerce", "pain_point": "Rising delivery costs", "channel": "email"},
        ])

    run_bulk_outreach(sample_csv, rep)
