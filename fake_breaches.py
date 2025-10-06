# fake_breaches.py
# Mock breach data for testing the Personal Cybersecurity Dashboard.
# This is used so the app can run without needing an API key.
# Each email maps to a list of breach objects with a Name and BreachDate.
# You can add more emails or breaches here for testing purposes.

fake_breaches = {
    "m.karthigan31@gmail.com": [
        {"Name": "ExampleBreach1", "BreachDate": "2025-01-01"},
        {"Name": "ExampleBreach2", "BreachDate": "2025-03-15"}
    ],
    "demo@example.com": [
        {"Name": "ExampleBreach1", "BreachDate": "2025-01-01"},
        {"Name": "ExampleBreach2", "BreachDate": "2025-03-15"}
    ],
    "testuser@example.com": [
        {"Name": "DemoLeak", "BreachDate": "2025-06-10"}
    ],
    "alice@example.com": [
        {"Name": "SocialAppLeak", "BreachDate": "2024-11-09"},
        {"Name": "OldForumDump", "BreachDate": "2022-05-22"}
    ],
    "bob123@mailinator.com": [
        {"Name": "RetailStoreDB", "BreachDate": "2023-08-30"}
    ],
    "multi_leaks@example.com": [
        {"Name": "LeakOne", "BreachDate": "2021-03-11"},
        {"Name": "LeakTwo", "BreachDate": "2022-04-22"},
        {"Name": "LeakThree", "BreachDate": "2023-05-05"}
    ],
    "cleanuser@nowhere.test": []  # no breaches for this email, useful for testing "no new breaches" case
}
