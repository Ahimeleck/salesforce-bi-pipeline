from google.cloud import bigquery

OBJETOS = [
    {
        "query": "SELECT Id, Name, StageName, Amount, CloseDate, AccountId, OwnerId, LeadSource, Probability FROM Opportunity",
        "table_name": "opportunities",
        "schema": [
            bigquery.SchemaField("Id",          "STRING"),
            bigquery.SchemaField("Name",        "STRING"),
            bigquery.SchemaField("StageName",   "STRING"),
            bigquery.SchemaField("Amount",      "FLOAT"),
            bigquery.SchemaField("CloseDate",   "DATE"),
            bigquery.SchemaField("AccountId",   "STRING"),
            bigquery.SchemaField("OwnerId",     "STRING"),
            bigquery.SchemaField("LeadSource",  "STRING"),
            bigquery.SchemaField("Probability", "FLOAT"),
        ],
        "date_cols":    ["CloseDate"],
        "numeric_cols": ["Amount", "Probability"]
    },
    {
        "query": "SELECT Id, Name, Industry, Type, BillingCity, BillingCountry, AnnualRevenue, NumberOfEmployees FROM Account",
        "table_name": "accounts",
        "schema": [
            bigquery.SchemaField("Id",                "STRING"),
            bigquery.SchemaField("Name",              "STRING"),
            bigquery.SchemaField("Industry",          "STRING"),
            bigquery.SchemaField("Type",              "STRING"),
            bigquery.SchemaField("BillingCity",       "STRING"),
            bigquery.SchemaField("BillingCountry",    "STRING"),
            bigquery.SchemaField("AnnualRevenue",     "FLOAT"),
            bigquery.SchemaField("NumberOfEmployees", "INTEGER"),
        ],
        "date_cols":    [],
        "numeric_cols": ["AnnualRevenue", "NumberOfEmployees"]
    },
    {
        "query": "SELECT Id, FirstName, LastName, Email, Phone, AccountId, Title, LeadSource FROM Contact",
        "table_name": "contacts",
        "schema": [
            bigquery.SchemaField("Id",         "STRING"),
            bigquery.SchemaField("FirstName",  "STRING"),
            bigquery.SchemaField("LastName",   "STRING"),
            bigquery.SchemaField("Email",      "STRING"),
            bigquery.SchemaField("Phone",      "STRING"),
            bigquery.SchemaField("AccountId",  "STRING"),
            bigquery.SchemaField("Title",      "STRING"),
            bigquery.SchemaField("LeadSource", "STRING"),
        ],
        "date_cols":    [],
        "numeric_cols": []
    },
    {
        "query": "SELECT Id, FirstName, LastName, Email, Company, Status, LeadSource, Industry, AnnualRevenue, CreatedDate FROM Lead",
        "table_name": "leads",
        "schema": [
            bigquery.SchemaField("Id",            "STRING"),
            bigquery.SchemaField("FirstName",     "STRING"),
            bigquery.SchemaField("LastName",      "STRING"),
            bigquery.SchemaField("Email",         "STRING"),
            bigquery.SchemaField("Company",       "STRING"),
            bigquery.SchemaField("Status",        "STRING"),
            bigquery.SchemaField("LeadSource",    "STRING"),
            bigquery.SchemaField("Industry",      "STRING"),
            bigquery.SchemaField("AnnualRevenue", "FLOAT"),
            bigquery.SchemaField("CreatedDate",   "TIMESTAMP"),
        ],
        "date_cols":    ["CreatedDate"],
        "numeric_cols": ["AnnualRevenue"]
    },
    {
        "query": "SELECT Id, Name, Type, Status, StartDate, EndDate, BudgetedCost, ActualCost, ExpectedRevenue, NumberOfLeads, NumberOfOpportunities FROM Campaign",
        "table_name": "campaigns",
        "schema": [
            bigquery.SchemaField("Id",                    "STRING"),
            bigquery.SchemaField("Name",                  "STRING"),
            bigquery.SchemaField("Type",                  "STRING"),
            bigquery.SchemaField("Status",                "STRING"),
            bigquery.SchemaField("StartDate",             "DATE"),
            bigquery.SchemaField("EndDate",               "DATE"),
            bigquery.SchemaField("BudgetedCost",          "FLOAT"),
            bigquery.SchemaField("ActualCost",            "FLOAT"),
            bigquery.SchemaField("ExpectedRevenue",       "FLOAT"),
            bigquery.SchemaField("NumberOfLeads",         "INTEGER"),
            bigquery.SchemaField("NumberOfOpportunities", "INTEGER"),
        ],
        "date_cols":    ["StartDate", "EndDate"],
        "numeric_cols": ["BudgetedCost", "ActualCost", "ExpectedRevenue"]
    },
]
