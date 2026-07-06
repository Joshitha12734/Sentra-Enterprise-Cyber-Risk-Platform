def get_assets():
    return [

        {
            "asset_id": "A1",
            "asset_name": "Customer Portal",
            "asset_type": "Web Application",

            "business_function": "Customer Management",
            "business_unit": "Sales",

            "owner": "Application Security Team",

            "business_criticality": "High",
            "data_sensitivity": "PII",

            "internet_exposed": True,

            "revenue_dependency": "High",
            "regulatory_impact": "High",

            "users_affected": 50000,

            "environment": "Production",

            "asset_value": 5000000,
            "recovery_time_hours": 4,
            "crown_jewel": True,
            "third_party_dependency": False,
            "backup_available": True,
            "technology_stack": [
                "apache",
                "tomcat",
                "spring",
                "mysql"
            ],

            "operating_system": "Linux",

            "cloud_provider": "AWS",

            "network_zone": "DMZ"
        },

        {
            "asset_id": "A2",
            "asset_name": "Customer Database",
            "asset_type": "Database",

            "business_function": "Customer Data Storage",
            "business_unit": "Sales",

            "owner": "Database Team",

            "business_criticality": "High",
            "data_sensitivity": "PII",

            "internet_exposed": False,

            "revenue_dependency": "High",
            "regulatory_impact": "High",

            "users_affected": 50000,

            "environment": "Production",

            "asset_value": 8000000,
            "recovery_time_hours": 2,

            "crown_jewel": True,
            "third_party_dependency": False,
            "backup_available": True,
            "technology_stack": [
                "oracle",
                "linux"
            ],

            "operating_system": "Oracle Linux",

            "cloud_provider": "AWS",

            "network_zone": "Internal"
        },

        {
            "asset_id": "A3",
            "asset_name": "Payment Gateway",
            "asset_type": "Payment Service",

            "business_function": "Revenue Processing",
            "business_unit": "Finance",

            "owner": "Payments Team",

            "business_criticality": "High",
            "data_sensitivity": "Financial",

            "internet_exposed": True,

            "revenue_dependency": "High",
            "regulatory_impact": "High",

            "users_affected": 30000,

            "environment": "Production",

            "asset_value": 10000000,
            "recovery_time_hours": 1,

            "crown_jewel": True,
            "third_party_dependency": True,
            "backup_available": True,
            "technology_stack": [
                "nginx",
                "spring",
                "oracle",
                "java"
            ],

            "operating_system": "Linux",

            "cloud_provider": "Azure",

            "network_zone": "PCI"
        },

        {
            "asset_id": "A4",
            "asset_name": "Analytics Platform",
            "asset_type": "Cloud Platform",

            "business_function": "Business Intelligence",
            "business_unit": "Operations",

            "owner": "Cloud Security Team",

            "business_criticality": "Medium",
            "data_sensitivity": "Internal",

            "internet_exposed": True,

            "revenue_dependency": "Medium",
            "regulatory_impact": "Medium",

            "users_affected": 5000,

            "environment": "Production",

            "asset_value": 3000000,
            "recovery_time_hours": 8,

            "crown_jewel": False,
            "third_party_dependency": True,
            "backup_available": True,
            "technology_stack": [
                "kubernetes",
                "docker",
                "postgresql",
                "python"
            ],

            "operating_system": "Linux",

            "cloud_provider": "AWS",

            "network_zone": "Internal"
        },

        {
            "asset_id": "A5",
            "asset_name": "HR Management System",
            "asset_type": "Internal Application",

            "business_function": "Employee Operations",
            "business_unit": "Human Resources",

            "owner": "HR Technology Team",

            "business_criticality": "Medium",
            "data_sensitivity": "PII",

            "internet_exposed": False,

            "revenue_dependency": "Low",
            "regulatory_impact": "High",

            "users_affected": 2000,

            "environment": "Production",

            "asset_value": 1500000,
            "recovery_time_hours": 12,

            "crown_jewel": False,
            "third_party_dependency": False,
            "backup_available": True,
            "technology_stack": [
                "iis",
                "sql_server",
                "dotnet"
            ],

            "operating_system": "Windows Server 2022",

            "cloud_provider": "Azure",

            "network_zone": "Corporate"
        },

        {
            "asset_id": "A6",
            "asset_name": "Developer Platform",
            "asset_type": "Internal Tool",

            "business_function": "Engineering Operations",
            "business_unit": "Engineering",

            "owner": "Platform Engineering Team",

            "business_criticality": "Medium",
            "data_sensitivity": "Internal",

            "internet_exposed": False,

            "revenue_dependency": "Medium",
            "regulatory_impact": "Low",

            "users_affected": 500,

            "environment": "Production",

            "asset_value": 2000000,
            "recovery_time_hours": 6,

            "crown_jewel": False,
            "third_party_dependency": False,
            "backup_available": True,
            "technology_stack": [
                "gitlab",
                "docker",
                "kubernetes",
                "jenkins"
            ],

            "operating_system": "Linux",

            "cloud_provider": "AWS",

            "network_zone": "Engineering"
        },

        {
            "asset_id": "A7",
            "asset_name": "Customer Support Portal",
            "asset_type": "Support Platform",

            "business_function": "Customer Support",
            "business_unit": "Customer Success",

            "owner": "Customer Success Team",

            "business_criticality": "Medium",
            "data_sensitivity": "PII",

            "internet_exposed": True,

            "revenue_dependency": "Medium",
            "regulatory_impact": "High",

            "users_affected": 25000,

            "environment": "Production",

            "asset_value": 2500000,
            "recovery_time_hours": 8,

            "crown_jewel": False,
            "third_party_dependency": False,
            "backup_available": True,
            "technology_stack": [
                "apache",
                "php",
                "mysql"
            ],

            "operating_system": "Linux",

            "cloud_provider": "AWS",

            "network_zone": "DMZ"
        },

        {
            "asset_id": "A8",
            "asset_name": "Testing Environment",
            "asset_type": "Test Infrastructure",

            "business_function": "Software Testing",
            "business_unit": "Engineering",

            "owner": "QA Team",

            "business_criticality": "Low",
            "data_sensitivity": "None",

            "internet_exposed": False,

            "revenue_dependency": "Low",
            "regulatory_impact": "Low",

            "users_affected": 0,

            "environment": "Non-Production",

            "asset_value": 500000,
            "recovery_time_hours": 24,

            "crown_jewel": False,
            "third_party_dependency": False,
            "backup_available": True,
            "technology_stack": [
                "docker",
                "kubernetes",
                "python"
            ],

            "operating_system": "Linux",

            "cloud_provider": "AWS",

            "network_zone": "Testing"
        },

        {
            "asset_id": "A9",
            "asset_name": "Corporate Identity Provider",
            "asset_type": "Identity Service",

            "business_function": "Authentication",
            "business_unit": "Security",

            "owner": "IAM Team",

            "business_criticality": "High",
            "data_sensitivity": "PII",

            "internet_exposed": True,

            "revenue_dependency": "Medium",
            "regulatory_impact": "High",

            "users_affected": 10000,

            "environment": "Production",

            "asset_value": 7000000,
            "recovery_time_hours": 2,

            "crown_jewel": True,
            "third_party_dependency": False,
            "backup_available": True,
            "technology_stack": [
                "active_directory",
                "windows",
                "kerberos"
            ],

            "operating_system": "Windows Server 2022",

            "cloud_provider": "On-Prem",

            "network_zone": "Corporate"
        },

        {
            "asset_id": "A10",
            "asset_name": "Corporate Email Platform",
            "asset_type": "Messaging Service",

            "business_function": "Corporate Communication",
            "business_unit": "IT",

            "owner": "IT Operations",

            "business_criticality": "High",
            "data_sensitivity": "Internal",

            "internet_exposed": True,

            "revenue_dependency": "Medium",
            "regulatory_impact": "Medium",

            "users_affected": 8000,

            "environment": "Production",

            "asset_value": 4000000,
            "recovery_time_hours": 4,

            "crown_jewel": False,
            "third_party_dependency": True,
            "backup_available": True,
            "technology_stack": [
                "exchange",
                "windows",
                "outlook"
            ],

            "operating_system": "Windows Server 2022",

            "cloud_provider": "Microsoft 365",

            "network_zone": "Corporate"
        },
        {
            "asset_id": "A11",
            "asset_name": "AI Workflow Platform",
            "asset_type": "LLM Platform",

            "business_function": "AI Automation",
            "business_unit": "Innovation",

            "owner": "AI Platform Team",

            "business_criticality": "High",
            "data_sensitivity": "Internal",

            "internet_exposed": True,

            "revenue_dependency": "Medium",
            "regulatory_impact": "Medium",

            "users_affected": 2000,

            "environment": "Production",

            "asset_value": 6000000,
            "recovery_time_hours": 2,

            "crown_jewel": True,
            "third_party_dependency": True,
            "backup_available": True,

            "technology_stack": [
                "flowise",
                "docker",
                "postgresql",
                "python"
            ],

            "operating_system": "Linux",

            "cloud_provider": "AWS",

            "network_zone": "DMZ"
        },
        {
            "asset_id": "A12",
            "asset_name": "Corporate Marketing Website",
            "asset_type": "Web Application",

            "business_function": "Public Website",
            "business_unit": "Marketing",

            "owner": "Web Team",

            "business_criticality": "Medium",
            "data_sensitivity": "Public",

            "internet_exposed": True,

            "revenue_dependency": "Low",
            "regulatory_impact": "Low",

            "users_affected": 100000,

            "environment": "Production",

            "asset_value": 2500000,
            "recovery_time_hours": 4,

            "crown_jewel": False,
            "third_party_dependency": True,
            "backup_available": True,

            "technology_stack": [
                "wordpress",
                "php",
                "apache",
                "mysql"
            ],

            "operating_system": "Linux",

            "cloud_provider": "AWS",

            "network_zone": "DMZ"
        },

    ]


if __name__ == "__main__":
    for asset in get_assets():
        print(asset)