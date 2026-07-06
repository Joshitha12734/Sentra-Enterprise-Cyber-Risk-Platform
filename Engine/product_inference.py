import re

# Common enterprise technologies that may appear in CVE descriptions
KNOWN_PRODUCTS = {
    "apache",
    "tomcat",
    "spring",
    "spring boot",
    "nginx",
    "oracle",
    "mysql",
    "postgresql",
    "postgres",
    "docker",
    "kubernetes",
    "wordpress",
    "windows",
    "linux",
    "exchange",
    "gitlab",
    "jenkins",
    "php",
    "python",
    "java",
    "flowise",
    "flowiseai",
    "capgo",
    "redis",
    "mongodb",
    "elasticsearch",
    "grafana",
    "prometheus",
    "rabbitmq",
    "kafka",
    "openssl",
    "vmware",
    "citrix",
    "jira",
    "confluence",
    "keycloak",
    "okta"
}
STOPWORDS = {
    "in",
    "and",
    "or",
    "the",
    "a",
    "an",
    "of",
    "for",
    "to",
    "with",
    "by",
    "before",
    "through",
    "prior",
    "plugin",
    "version",
    "versions",
    "contains",
    "allows",
    "allow",
    "using",
    "multiple",
    "remote",
    "local",
    "attack",
    "attacker",
    "code",
    "execution",
    "file",
    "files",
    "data",
    "manager",
    "attribute",
    "all",
    "component"
}


def infer_products(description):
    """
    Infer affected products when NVD does not provide CPE data.
    """

    description = description.lower()

    found = set()

    # -----------------------------
    # Step 1: Match known products
    # -----------------------------
    for product in KNOWN_PRODUCTS:

        if product in description:
            found.add(product)

    # -----------------------------
    # Step 2: Look for
    # "XYZ before"
    # "XYZ through"
    # "XYZ prior to"
    # -----------------------------
    patterns = [

        r"([a-zA-Z0-9_-]+)\s+before",

        r"([a-zA-Z0-9_-]+)\s+through",

        r"([a-zA-Z0-9_-]+)\s+prior",

        r"([a-zA-Z0-9_-]+)\s+plugin",

        r"([a-zA-Z0-9_-]+)\s+version"

    ]

    for pattern in patterns:

        matches = re.findall(pattern, description)
        for match in matches:

            product = match.lower().strip()

            if (
                len(product) < 3
                or product in STOPWORDS
            ):
                continue

            found.add(product)

    return sorted(found)

if __name__ == "__main__":

    samples = [

        "Capgo before 12.128.2 contains a broken authentication vulnerability.",

        "Flowise through 2.2.7 contains a SQL Injection vulnerability.",

        "The WordPress plugin allows remote code execution.",

        "Apache Tomcat allows privilege escalation."

    ]

    for text in samples:

        print(text)

        print(infer_products(text))

        print("-" * 60)