try:
    from .asset_context import get_assets
except ImportError:
    from asset_context import get_assets


def normalize(values):
    """
    Convert values to lowercase and remove duplicates.
    """
    return {v.strip().lower() for v in values if v}


def jaccard_similarity(set1, set2):
    """
    Computes Jaccard similarity between two sets.
    """

    if not set1 and not set2:
        return 0.0

    intersection = set1 & set2
    union = set1 | set2

    return len(intersection) / len(union)


def classify_confidence(score):

    if score >= 0.75:
        return "High"

    elif score >= 0.40:
        return "Medium"

    return "Low"
def business_criticality_score(asset):

    mapping = {
        "High": 0.20,
        "Medium": 0.10,
        "Low": 0.05
    }

    return mapping.get(
        asset["business_criticality"],
        0
    )

def internet_exposure_score(asset):

    return 0.10 if asset["internet_exposed"] else 0

def production_score(asset):

    return (
        0.10
        if asset["environment"] == "Production"
        else 0
    )
def crown_jewel_score(asset):

    return 0.10 if asset["crown_jewel"] else 0

def asset_value_score(asset):

    value = asset["asset_value"]

    if value >= 8000000:
        return 0.15

    elif value >= 5000000:
        return 0.10

    elif value >= 2000000:
        return 0.05

    return 0

def calculate_business_score(asset, technology_score):

    score = technology_score

    score += business_criticality_score(asset)

    score += internet_exposure_score(asset)

    score += production_score(asset)

    score += crown_jewel_score(asset)

    score += asset_value_score(asset)

    return round(
        min(score, 1.0),
        2
    )

def classify_priority(score):

    if score >= 0.85:
        return "Critical"

    elif score >= 0.65:
        return "High"

    elif score >= 0.40:
        return "Medium"

    return "Low"
def generate_reasoning(asset, matched_products):

    reasons = []

    reasons.append(
        f"Matched technology: {', '.join(matched_products)}"
    )

    if asset["internet_exposed"]:
        reasons.append(
            "Internet-facing asset"
        )

    if asset["environment"] == "Production":
        reasons.append(
            "Production environment"
        )

    if asset["business_criticality"] == "High":
        reasons.append(
            "High business criticality"
        )

    if asset["crown_jewel"]:
        reasons.append(
            "Crown jewel asset"
        )

    if asset["asset_value"] >= 5000000:
        reasons.append(
            f"High-value asset (${asset['asset_value']:,.0f})"
        )

    return reasons

def match_single_cve(cve, assets):

    matches = []

    cve_products = normalize(cve.get("products", []))

    for asset in assets:

        asset_stack = normalize(asset["technology_stack"])

        score = jaccard_similarity(
            cve_products,
            asset_stack
        )

        if score == 0:
            continue

        matched = sorted(
            list(cve_products & asset_stack)
        )
        technology_score = round(score, 2)

        business_score = calculate_business_score(
            asset,
            technology_score
        )

        priority = classify_priority(
            business_score
        )
        reasoning = generate_reasoning(
            asset,
            matched
        )

        matches.append({
            "asset_id": asset["asset_id"],

            "asset_name": asset["asset_name"],

            "business_unit": asset["business_unit"],

            "business_function": asset["business_function"],

            "owner": asset["owner"],

            "cloud_provider": asset["cloud_provider"],

            "operating_system": asset["operating_system"],

            "network_zone": asset["network_zone"],

            "technology_stack": asset["technology_stack"],

            "matched_products": matched,

            "technology_score": technology_score,

            "business_score": business_score,

            "priority": priority,

            "reasoning": reasoning,

            "confidence": classify_confidence(score),

            "internet_exposed": asset["internet_exposed"],

            "crown_jewel": asset["crown_jewel"],

            "asset_value": asset["asset_value"],

            "estimated_total_exposure": asset["asset_value"] * business_score,

            "risk_level": priority,

            "business_impact": (
                "Enterprise Compromise"
                if priority == "Critical"
                else "Business Disruption"
                if priority == "High"
                else "Operational Impact"
            ),

            "board_reporting": (
                "Required"
                if priority in ["Critical", "High"]
                else "Not Required"
            ),

            "risk_appetite_breach": (
                "Above Appetite"
                if priority in ["Critical", "High"]
                else "Within Appetite"
            ),

            "decision": (
                "Immediate Remediation"
                if priority == "Critical"
                else "Remediate within SLA"
                if priority == "High"
                else "Monitor"
            ),

            "recommended_action": (
                "Immediately patch and isolate the affected asset."
                if priority == "Critical"
                else "Schedule remediation and increase monitoring."
                if priority == "High"
                else "Continue monitoring."
            ),

            "cve_id": cve["cve_id"],

            "severity": cve["severity"],

            "cvss": cve["cvss"],

            "published": cve["published"],

            "description": cve["description"]
        })
    return matches

def find_matches(cves):

    assets = get_assets()

    all_matches = []

    for cve in cves:

        all_matches.extend(
            match_single_cve(
                cve,
                assets
            )
        )

    return sorted(
        all_matches,
        key=lambda x: x["business_score"],
        reverse=True
    )

if __name__ == "__main__":

    from nvd_live_fetch import fetch_latest_cves

    cves = fetch_latest_cves(10)
    print("\nLATEST CVEs\n")

    for cve in cves:
        print(cve["cve_id"])
        print(cve["products"])
        print("-" * 40)

    matches = find_matches(cves)

    print("\nBUSINESS MATCHES\n")

    for match in matches:

        print("=" * 60)

        print(match["asset_name"])

        print(match["cve_id"])

        print(match["matched_products"])
        print("Technology Score :", match["technology_score"])

        print("Enterprise Risk Score   :", match["business_score"])

        print("Priority         :", match["priority"])

        print("Confidence       :", match["confidence"])
        print("\nReasoning:")
        for reason in match["reasoning"]:
            print("•", reason)