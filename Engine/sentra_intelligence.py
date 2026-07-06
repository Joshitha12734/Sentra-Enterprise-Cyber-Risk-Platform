import json
import os

OUTPUT_DIR = "Outputs"


def load_contextual_risks():
    """
    Loads the contextual risk engine output.
    """

    path = os.path.join(OUTPUT_DIR, "contextual_risk.json")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data["results"]


class SentraIntelligence:

    def __init__(self):

        self.risks = load_contextual_risks()

    ####################################################
    # Executive Summary
    ####################################################

    def executive_summary(self, risk):
        return f"""
    ### Executive Overview

    The highest priority enterprise risk is **{risk['cve_id']}**, affecting the **{risk['asset_name']}**.

    ### Business Impact

    • Risk Level: **{risk['risk_level']}**

    • Estimated Enterprise Exposure:
    **${risk['estimated_total_exposure']:,.0f}**

    • Business Impact:
    **{risk['business_impact']}**

    • Executive Decision:
    **{risk['decision']}**

    ### Why this matters

    This vulnerability affects a business-critical asset supporting
    **{risk['business_function']}**.

    Successful exploitation could significantly impact business operations,
    regulatory compliance, customer trust, and financial performance.

    ### Recommendation

    {risk['recommended_action']}
"""
    
    def risk_card(self, risk):

        return f"""
    ## 🚨 Enterprise Risk Summary

    **Asset**
    {risk['asset_name']}

    **CVE**
    {risk['cve_id']}

    **Risk Level**
    {risk['risk_level']}

    **Business Impact**
    {risk['business_impact']}

    **Estimated Exposure**
    ${risk['estimated_total_exposure']:,.0f}

    **Executive Decision**
    {risk['decision']}

    **Recommendation**
    {risk['recommended_action']}
    """
        
    ####################################################
    # Remediation
    ####################################################

    def remediation(self, risk):

        actions = []

        if risk["risk_level"] == "Critical":

            actions.extend([
                "Immediately isolate affected asset.",
                "Deploy vendor patch immediately.",
                "Notify SOC and CISO.",
                "Enable continuous monitoring.",
                "Verify exploit attempts."
            ])

        elif risk["risk_level"] == "High":

            actions.extend([
                "Schedule emergency patch.",
                "Increase monitoring.",
                "Review firewall rules.",
                "Notify asset owner."
            ])

        else:

            actions.extend([
                "Patch during maintenance window.",
                "Continue monitoring."
            ])

        return actions

    ####################################################
    # Board Report
    ####################################################

    def board_summary(self):

        total = len(self.risks)

        critical = sum(
            r["risk_level"] == "Critical"
            for r in self.risks
        )

        exposure = sum(
            r["estimated_total_exposure"]
            for r in self.risks
        )

        return {

            "total_assets": total,

            "critical_risks": critical,

            "enterprise_exposure": exposure
        }

    ####################################################
    # Enterprise Search
    ####################################################

    def search(self, question):

        q = question.lower()

        for risk in self.risks:

            if risk["asset_name"].lower() in q:

                return risk

            if risk["cve_id"].lower() in q:

                return risk

        return None
    
    def get_highest_risk(self):
        return max(
            self.risks,
            key=lambda r: r["estimated_total_exposure"]
        )
    
    def get_highest_exposure(self):
        risk = max(
            self.risks,
            key=lambda r: r["estimated_total_exposure"]
        )

        return (
            f"Highest Financial Exposure\n\n"
            f"Asset: {risk['asset_name']}\n"
            f"CVE: {risk['cve_id']}\n"
            f"Exposure: ${risk['estimated_total_exposure']:,.0f}"
        )
    
    def get_board_risks(self):

        board = [
            r for r in self.risks
            if r["board_reporting"] == "Required"
        ]

        if not board:
            return "No board-reportable risks."

        response = "Board Reportable Risks\n\n"

        for risk in board:

            response += (
                f"• {risk['asset_name']} "
                f"({risk['cve_id']})\n"
            )

        return response
    
    def get_statistics(self):

        total = len(self.risks)

        critical = sum(
            r["risk_level"] == "Critical"
            for r in self.risks
        )

        high = sum(
            r["risk_level"] == "High"
            for r in self.risks
        )
        medium = sum(
            r["risk_level"] == "Medium"
            for r in self.risks
        )

        low = sum(
            r["risk_level"] == "Low"
            for r in self.risks
        )

        return (
            "Enterprise Risk Statistics\n\n"
            f"Total Risks: {total}\n"
            f"Critical Risks: {critical}\n"
            f"High Risks: {high}\n"
            f"Medium Risks: {medium}\n"
            f"Low Risks: {low}"
        )
    
    def get_asset(self, asset):

        for risk in self.risks:

            if asset.lower() in risk["asset_name"].lower():

                return risk

        return None
    
    def get_cve(self, cve):

        for risk in self.risks:

            if cve.lower() == risk["cve_id"].lower():

                return risk

        return None
    
    def answer_question(self, question):

        q = question.lower()

        if (
            ("highest" in q or "top" in q or "biggest" in q or "worst" in q)
            and
            (
                "risk" in q
                or "vulnerability" in q
                or "issue" in q
                or "problem" in q
            )
        ):

            risk = self.get_highest_risk()

            return self.risk_card(risk)

        if (
            (
                "highest" in q
                or "largest" in q
                or "maximum" in q
                or "biggest" in q
            )
            and
            (
                "exposure" in q
                or "financial" in q
                or "loss" in q
            )
        ):

            return self.get_highest_exposure()

        if any(word in q for word in [
            "board",
            "executive",
            "management",
            "leadership"
        ]):

            return self.get_board_risks()
        if any(word in q for word in [
            "statistics",
            "stats",
            "summary",
            "overview"
        ]):

            return self.get_statistics()

        for risk in self.risks:

            if risk["asset_name"].lower() in q:

                return self.risk_card(risk)

            if risk["cve_id"].lower() in q:

                return self.risk_card(risk)
            

        return None