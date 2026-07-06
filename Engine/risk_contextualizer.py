#risk_contextualizer
import json
import os
from asset_context import get_assets
from utils import now_utc
from business_matcher import find_matches
from nvd_live_fetch import fetch_latest_cves

# ==============================
# 🔹 OUTPUT DIRECTORY
# ==============================
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Outputs")


# ==============================
# 🔹 MULTIPLIERS
# ==============================
CRITICALITY_MULTIPLIER = {
    "High": 4,
    "Medium": 2,
    "Low": 1
}

EXPOSURE_MULTIPLIER = {
    True : 1.5,
    False: 1.0
}

SENSITIVITY_MULTIPLIER = {
    "Financial": 2.5,
    "PII": 2.0,
    "Public": 1.0,
    "Internal": 1.3,
    "None": 1.0
}

REVENUE_MULTIPLIER = {
    "High": 2.0,
    "Medium": 1.5,
    "Low": 1.0
}

BACKUP_MULTIPLIER = {
    True: 0.8,
    False: 1.5
}

REGULATORY_MULTIPLIER = {
    "High": 2.0,
    "Medium": 1.5,
    "Low": 1.0
}

CROWN_JEWEL_MULTIPLIER = {
    True: 2.0,
    False: 1.0
}
THIRD_PARTY_MULTIPLIER = {
    True: 1.3,
    False: 1.0
}
RISK_APPETITE = 1000000


# ==============================
# 🔹 DECISION ENGINE
# ==============================


def get_decision(exposure):
    if exposure >= 10000000:
        return "Immediate Remediation"

    elif exposure >= 5000000:
        return "Executive Review"

    elif exposure >= 1000000:
        return "Security Approval"

    else:
        return "Accept with Monitoring"


def get_decision_reason(exposure):

    if exposure >= 10000000:
        return (
            "Potential losses exceed $10M. "
            "Immediate remediation and executive escalation required."
        )

    elif exposure >= 5000000:
        return (
            "Potential losses exceed $5M. "
            "Executive review required before acceptance."
        )

    elif exposure >= 1000000:
        return (
            "Material business impact possible. "
            "Security leadership approval required."
        )

    else:
        return (
            "Exposure remains within organizational risk appetite. "
            "Monitoring and scheduled remediation acceptable."
        )


def get_business_impact_level(exposure):

    if exposure >= 10000000:
        return "Catastrophic"

    elif exposure >= 5000000:
        return "Severe"

    elif exposure >= 1000000:
        return "High"

    elif exposure >= 250000:
        return "Moderate"

    return "Low"

def get_risk_treatment(row):

    if row["business_risk"] >= 1000000:
        return "Mitigate"

    elif row["business_risk"] >= 300000:
        return "Reduce"

    elif row["business_risk"] >= 100000:
        return "Transfer"

    return "Accept"

def get_executive_severity(exposure):

    if exposure >= 5000000:
        return "Severe"

    elif exposure >= 2000000:
        return "High"

    elif exposure >= 500000:
        return "Moderate"

    return "Low"
def get_impact_type(cve):

    impacts = []

    if cve["confidentiality_impact"] != "NONE":
        impacts.append("Confidentiality")

    if cve["integrity_impact"] != "NONE":
        impacts.append("Integrity")

    if cve["availability_impact"] != "NONE":
        impacts.append("Availability")

    return ", ".join(impacts)



def get_business_impact(cve):

    c = cve["confidentiality_impact"]
    i = cve["integrity_impact"]
    a = cve["availability_impact"]

    if c == "HIGH" and i == "HIGH" and a == "HIGH":
        return "Enterprise Compromise"

    elif c == "HIGH" and i == "HIGH":
        return "Data Breach"

    elif c == "HIGH" and a == "HIGH":
        return "Data Theft & Service Disruption"

    elif c == "HIGH":
        return "Sensitive Data Exposure"

    elif a == "HIGH" and c == "NONE":
        return "Operational Downtime"

    elif i == "HIGH":
        return "Unauthorized Modification"

    return "Business Process Impact"

# ==============================
# 🔹 LLM BUSINESS EXPLANATION
# ==============================


def generate_llm_business_explanation(row):

    return (
        f"{row['cve_id']} is a {row['risk_level']} vulnerability affecting "
        f"{row['asset_name']}. This asset supports "
        f"{row['business_function']} and has an estimated financial exposure "
        f"of ${row['estimated_total_exposure']:,.0f}. "
        f"Because it is "
        f"{'internet exposed' if row['internet_exposed'] else 'internal'}, "
        f"successful exploitation could impact business operations, revenue, "
        f"customer trust, and regulatory compliance."
    )


# ==============================
# 🔹 MAIN CONTEXTUALIZER
# ==============================
def contextualize():

    # Load technical risk output
    with open(os.path.join(OUTPUT_DIR, "technical_risk.json"), "r", encoding="utf-8") as f:
        tech = json.load(f)

    assets = get_assets()
    contextual_results = []

    # ==============================
    # 🔹 PROCESS EACH ASSET + CVE
    # ==============================
    for asset in assets:
        criticality_factor = CRITICALITY_MULTIPLIER[asset["business_criticality"]]
        exposure_factor = EXPOSURE_MULTIPLIER[asset["internet_exposed"]]

        for cve in tech["results"]:
            base_risk = cve["risk_score"]


            exploitability_factor = 1.0

            if cve["attack_vector"] == "NETWORK":
                exploitability_factor += 0.5

            if cve["attack_complexity"] == "LOW":
                exploitability_factor += 0.3

            # 🔥 BUSINESS RISK CALCULATION
            sensitivity_factor = SENSITIVITY_MULTIPLIER[
                asset["data_sensitivity"]
            ]
            revenue_factor = REVENUE_MULTIPLIER[
                asset["revenue_dependency"]
            ]

            regulatory_factor = REGULATORY_MULTIPLIER[
                asset["regulatory_impact"]
            ]

            crown_factor = CROWN_JEWEL_MULTIPLIER[
                asset["crown_jewel"]
            ]
            third_party_factor = THIRD_PARTY_MULTIPLIER[
                asset["third_party_dependency"]
            ]
            backup_factor = BACKUP_MULTIPLIER[
                asset["backup_available"]
            ]

            business_risk = (
                base_risk
                * criticality_factor
                * exposure_factor
                * sensitivity_factor
                * revenue_factor
                * regulatory_factor
                * crown_factor
                * third_party_factor
                * backup_factor
                * exploitability_factor
            )
            
            severity_factor = (
                cve["base_score"] / 10
            )

            risk_factor = (
                severity_factor
                * criticality_factor
                * exposure_factor
                * exploitability_factor
            )

            risk_factor = min(
                risk_factor / 12,
                1.0
            )

            estimated_revenue_loss = (
                asset["asset_value"]
            * risk_factor
             * 0.30
            )

            estimated_regulatory_fine = (
                asset["asset_value"]
                * (regulatory_factor - 1)
                * 0.10
            )

            estimated_recovery_cost = (
                asset["asset_value"]
                 * (
                     asset["recovery_time_hours"] / 24
                 )
                 * 0.05
            )

            estimated_total_exposure = (
                estimated_revenue_loss
                + estimated_regulatory_fine
                + estimated_recovery_cost
            )
            priority_score = (
                business_risk * 0.4
                + estimated_total_exposure * 0.6
            )

            if asset["asset_type"] == "Identity Service":
                priority_score *= 1.2

            if asset["business_function"] == "Authentication":
                priority_score *= 1.2

            risk_appetite_breach = (
                "Yes"
                if estimated_total_exposure > RISK_APPETITE
                else "No"
            )

            attack_path_score = 1

            if asset["internet_exposed"]:
                    attack_path_score += 1

            if asset["crown_jewel"]:
                    attack_path_score += 1

            if asset["third_party_dependency"]:
                    attack_path_score += 1

            if cve["attack_complexity"] == "LOW":
                attack_path_score += 1

            board_reporting= (
                "Required"
                if estimated_total_exposure >= 3000000
                else "Not Required"
            )
            # 🔹 BASE ROW
            row = {
                "asset_id": asset["asset_id"],
                "asset_name": asset["asset_name"],
                "asset_type": asset["asset_type"],

                "business_function": asset["business_function"],
                "business_unit": asset["business_unit"],

                "owner": asset["owner"],
                "technology_stack": asset["technology_stack"],

                "cloud_provider": asset["cloud_provider"],

                "operating_system": asset["operating_system"],

                "network_zone": asset["network_zone"],

                "internet_exposed": asset["internet_exposed"],
                "business_criticality": asset["business_criticality"],
                "data_sensitivity": asset["data_sensitivity"],

                "revenue_dependency": asset["revenue_dependency"],
                "regulatory_impact": asset["regulatory_impact"],
                "recovery_time_hours": asset["recovery_time_hours"],

                "asset_value": asset["asset_value"],
                "users_affected": asset["users_affected"],

                "crown_jewel": asset["crown_jewel"],
                "third_party_dependency": asset["third_party_dependency"],
                "environment": asset["environment"],

                "cve_id": cve["cve_id"],
                "risk_appetite_breach": risk_appetite_breach,
                "priority_score": round(priority_score, 2),
                "board_reporting": board_reporting,
                "attack_path_score": attack_path_score,
                

                "base_risk": base_risk,
                "business_risk": round(business_risk, 2),

                "estimated_revenue_loss":
                    round(estimated_revenue_loss, 2),

                "estimated_regulatory_fine":
                    round(estimated_regulatory_fine, 2),

                "estimated_recovery_cost":
                    round(estimated_recovery_cost, 2),

                "estimated_total_exposure":
                    round(estimated_total_exposure, 2),

                "business_impact_level":
                    get_business_impact_level(
                        estimated_total_exposure
                    ),
                "estimated_revenue_loss":
                    round(estimated_revenue_loss, 2),

                "estimated_regulatory_fine":
                    round(estimated_regulatory_fine, 2),

                "estimated_recovery_cost":
                    round(estimated_recovery_cost, 2),

                "estimated_total_exposure":
                    round(estimated_total_exposure, 2),

                "business_impact_level":
                    get_business_impact_level(
                        estimated_total_exposure
                    ),

                "risk_level": cve["risk_level"],
                "remediation_sla": cve["remediation_sla"],

                "technical_impact":
                get_impact_type(cve),

                "business_impact":
                get_business_impact(cve),
                
                "matched_products": [],

                "technology_score": 0,

                "business_score": round(business_risk, 2),

                "reasoning": [],

                "confidence": "High"
            }

            # ==============================
            # 🔥 DECISION ENGINE
            # ==============================
            if row["risk_level"] == "Critical":
                row["recommended_action"] = (
                    "Immediate remediation required."
                )
            elif row["risk_level"] == "High":

                row["recommended_action"] = (
                    "Patch immediately and obtain security approval."
                )

            elif row["risk_level"] == "Medium":

                row["recommended_action"] = (
                    "Remediate in next release cycle."
                )

            else:

                row["recommended_action"] = (
                    "Accept risk and monitor."
                )


            row["decision"] = get_decision(
                estimated_total_exposure
            )

            row["decision_reason"] = get_decision_reason(
                estimated_total_exposure
            )

            row["business_impact_level"] = get_business_impact_level(
                estimated_total_exposure
            )
            row["risk_treatment"] = get_risk_treatment(row)

            row["executive_severity"] = get_executive_severity(
                estimated_total_exposure
            )

            # ==============================
            # 🔥 EXTRA INTELLIGENCE (FIXED INDENTATION)
            # ==============================
            row["attack_type"] = (
                "Remote Exploit"
                if row["internet_exposed"]
                else "Local/Internal"
            )

            row["confidence"] = (
                "High"
                if row["risk_level"] == "Critical"
                else "Medium"
            )



            # ==============================
            # 🤖 LLM EXPLANATION
            # ==============================
            row["llm_business_explanation"] = generate_llm_business_explanation(row)

            contextual_results.append(row)

    # ==============================
    # 🔹 SORT BY BUSINESS RISK
    # ==============================
    sorted_results = sorted(
        contextual_results,
        key=lambda x: x["priority_score"],
        reverse=True
    )
    top_asset_risks = {}

    for risk in sorted_results:
        asset = risk["asset_name"]
        if asset not in top_asset_risks:
            top_asset_risks[asset] = risk
    top_asset_risks = list(
        top_asset_risks.values()

    )
    # ==============================
    # 🔹 PRIORITY TAGGING
    # ==============================
    for i, r in enumerate(sorted_results):
        if i < 5:
            r["priority_tag"] = "Top Business Critical"
        elif i < 15:
            r["priority_tag"] = "High Business Risk"
        else:
            r["priority_tag"] = "Normal"

    # ==============================
    # 🔹 OUTPUT
    # ==============================
    output = {
        "metadata": {
            "scan_time": now_utc(),
            "engine": "contextual-risk-engine",
            "model": "business-context-adjusted",
            "total_assets":len(assets),
            "total_contextual_risks": len(sorted_results),
            "risk_appetite_threshold": RISK_APPETITE

        },
        "results": sorted_results,
        "top_asset_risks": top_asset_risks
    }

    # Write JSON output
    with open(os.path.join(OUTPUT_DIR, "contextual_risk.json"), "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    return output


# ==============================
# 🔹 RUN
# ==============================
if __name__ == "__main__":
    out = contextualize()

    print("Top Business Risks:\n")
    for r in out["top_asset_risks"]:
        print(r)