import requests
import os
from datetime import datetime, timedelta, UTC
try:
    from .product_inference import infer_products
except ImportError:
    from product_inference import infer_products


# Optional: set this env var for higher NVD rate limits (free to request from NVD).
NVD_API_KEY = os.environ.get("NVD_API_KEY")

# Normalizes verbose CPE product/vendor names down to simpler keywords,
# so they match more reliably against asset technology_stack entries.
# Extend this dictionary as you notice mismatches in testing.
NORMALIZATION = {
    "spring_framework": "spring",
    "spring_boot": "spring",
    "microsoft_windows": "windows",
    "oracle_database": "oracle",
    "active_directory": "active_directory",  # kept distinct on purpose
}


def normalize(name):
    return NORMALIZATION.get(name, name)


def _parse_cpe_match(cpe_match, products):
    """Pulls vendor/product out of a single cpeMatch entry."""
    if not cpe_match.get("vulnerable", False):
        return

    criteria = cpe_match.get("criteria", "")
    # CPE 2.3 format: cpe:2.3:part:vendor:product:version:update:edition:...
    parts = criteria.split(":")

    if len(parts) > 4:
        vendor = parts[3]
        product = parts[4]

        if vendor and vendor != "*":
            products.add(normalize(vendor.lower()))
        if product and product != "*":
            products.add(normalize(product.lower()))


def _walk_node(node, products):
    """
    Recursively walks a configuration node, since NVD nests 'children'
    inside 'nodes' for AND/OR logic (e.g. "Windows AND Apache Tomcat").
    A flat loop over node['cpeMatch'] alone misses these nested CVEs.
    """
    for cpe_match in node.get("cpeMatch", []):
        _parse_cpe_match(cpe_match, products)

    for child in node.get("children", []):
        _walk_node(child, products)


def extract_products(cve_item):
    """
    Extracts vendor/product info from a CVE's CPE configuration data,
    walking the full nested node/children tree.
    Returns a list of lowercase, normalized product name strings
    (e.g. ["spring", "oracle"]). This is what we match against an
    asset's technology_stack.
    """
    products = set()

    configurations = cve_item.get("configurations", [])

    for config in configurations:
        for node in config.get("nodes", []):
            _walk_node(node, products)

    return list(products)


def extract_cwe_ids(cve_item):
    """Returns CWE IDs (e.g. ['CWE-79', 'CWE-89']) for this CVE, if present."""
    cwe_ids = []
    for weakness in cve_item.get("weaknesses", []):
        for desc in weakness.get("description", []):
            value = desc.get("value", "")
            if value.startswith("CWE-"):
                cwe_ids.append(value)
    return cwe_ids


def fetch_latest_cves(results_per_page=10, days_back=7):
    """
    Fetches recent CVEs from NVD.

    NVD's API 2.0 has no generic 'sortBy' parameter. To reliably get
    *recent* CVEs (rather than whatever order the API happens to return),
    we filter by publication date range instead, per NVD's documented
    requirement that pubStartDate and pubEndDate must both be provided
    together (max 120-day range). We then sort the returned page
    client-side by 'published' to get newest-first ordering.
    """

    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    end = datetime.now(UTC)
    start = end - timedelta(days=days_back)

    params = {
        "resultsPerPage": results_per_page,
        "pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "pubEndDate": end.strftime("%Y-%m-%dT%H:%M:%S.000"),
    }

    headers = {}
    if NVD_API_KEY:
        headers["apiKey"] = NVD_API_KEY

    try:

        response = requests.get(url, params=params, headers=headers, timeout=60)

        response.raise_for_status()

        data = response.json()

        cves = []

        for item in data.get("vulnerabilities", []):

            cve = item["cve"]

            cve_id = cve["id"]

            # Prefer the English description; fall back gracefully.
            description = next(
                (d["value"] for d in cve.get("descriptions", []) if d.get("lang") == "en"),
                "No description available."
            )

            severity = "UNKNOWN"

            metrics = cve.get("metrics", {})

            if "cvssMetricV31" in metrics:
                severity = (
                    metrics["cvssMetricV31"][0]
                    ["cvssData"]["baseSeverity"]
                )

            elif "cvssMetricV30" in metrics:
                severity = (
                    metrics["cvssMetricV30"][0]
                    ["cvssData"]["baseSeverity"]
                )

            elif "cvssMetricV2" in metrics:
                severity = (
                    metrics["cvssMetricV2"][0]
                    .get("baseSeverity", "UNKNOWN")
                )

            published = cve.get("published", "Unknown")

            cvss = 0.0
            attack_vector = "UNKNOWN"

            if "cvssMetricV31" in metrics:
                cvss = metrics["cvssMetricV31"][0]["cvssData"]["baseScore"]
                attack_vector = metrics["cvssMetricV31"][0]["cvssData"]["attackVector"]

            elif "cvssMetricV30" in metrics:
                cvss = metrics["cvssMetricV30"][0]["cvssData"]["baseScore"]
                attack_vector = metrics["cvssMetricV30"][0]["cvssData"]["attackVector"]

            elif "cvssMetricV2" in metrics:
                cvss = metrics["cvssMetricV2"][0].get("cvssData", {}).get("baseScore", 0.0)
                attack_vector = metrics["cvssMetricV2"][0].get("cvssData", {}).get("accessVector", "UNKNOWN")

            # Exploitability/Impact sub-scores (separate from baseScore) — useful
            # for showing "how easy to exploit" vs "how bad if exploited" separately.
            exploitability_score = 0.0
            impact_score = 0.0

            if "cvssMetricV31" in metrics:
                exploitability_score = metrics["cvssMetricV31"][0].get("exploitabilityScore", 0.0)
                impact_score = metrics["cvssMetricV31"][0].get("impactScore", 0.0)
            elif "cvssMetricV30" in metrics:
                exploitability_score = metrics["cvssMetricV30"][0].get("exploitabilityScore", 0.0)
                impact_score = metrics["cvssMetricV30"][0].get("impactScore", 0.0)
            elif "cvssMetricV2" in metrics:
                exploitability_score = metrics["cvssMetricV2"][0].get("exploitabilityScore", 0.0)
                impact_score = metrics["cvssMetricV2"][0].get("impactScore", 0.0)

            # NEW: extract affected products/vendors from CPE data for asset matching
            products = extract_products(cve)
            if not products:
                products = infer_products(description)

            cwe_ids = extract_cwe_ids(cve)

            cves.append({
                "cve_id": cve_id,
                "severity": severity,
                "cvss": cvss,
                "attack_vector": attack_vector,
                "exploitability_score": exploitability_score,
                "impact_score": impact_score,
                "cwe_ids": cwe_ids,           # e.g. ["CWE-79"]
                "published": published,
                "description": description,
                "products": products   # e.g. ["apache", "tomcat"]
            })

        cves.sort(
                key=lambda x: x["published"],
                reverse=True
            )

        return cves

    except Exception as e:
        print("NVD ERROR:", e)
        return []


if __name__ == "__main__":
    for cve in fetch_latest_cves(10):
        print("\n")

        print(cve["cve_id"])

        print("Products:", cve["products"])

        print("Description:", cve["description"][:100])
