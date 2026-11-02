"""
Test cases for the checker, for this week's extension.

Each case is a handoff the researcher could have sent, and the verdict a
good checker should give. Three are right. Three have an error planted
in them, each a different kind:

    case 4   a real quote, but the answer gets the number wrong
    case 5   a quote that is not in the file at all
    case 6   a real quote that does not answer this question

Given, not an exercise. Read every case before you run them, and say in
week11-OUTPUT.md if you disagree with an expected verdict.
"""

CASES = [
    {
        "question": "How much does the Growth plan cost per month?",
        "handoff": {
            "answer": "$149 a month.",
            "source": "pricing.txt",
            "quote": "Growth — $149/month",
        },
        "expected": "ok",
    },
    {
        "question": "Is SSO available on the Starter plan?",
        "handoff": {
            "answer": "No. SSO is only on the Scale plan.",
            "source": "onboarding_faq.txt",
            "quote": "No. SSO is a Scale plan feature only.",
        },
        "expected": "ok",
    },
    {
        "question": "Are duplicate charges refunded?",
        "handoff": {
            "answer": "Yes, in full, once the duplicate is confirmed.",
            "source": "refund_policy.txt",
            "quote": "Duplicate or erroneous charges (billing errors, not "
                     "cancellations) are refunded in full once confirmed, "
                     "no discretion required.",
        },
        "expected": "ok",
    },
    {
        "question": "How much does the Scale plan cost per month?",
        "handoff": {
            "answer": "$299 a month.",
            "source": "pricing.txt",
            "quote": "Scale — $499/month",
        },
        "expected": "problem",
    },
    {
        "question": "How long do email/password sessions last by default?",
        "handoff": {
            "answer": "7 days.",
            "source": "security_overview.txt",
            "quote": "Email/password sessions last 7 days.",
        },
        "expected": "problem",
    },
    {
        "question": "Can Starter customers import historical data?",
        "handoff": {
            "answer": "Yes, by CSV import.",
            "source": "onboarding_faq.txt",
            "quote": "Yes, via CSV import on Growth and Scale plans.",
        },
        "expected": "problem",
    },
]
