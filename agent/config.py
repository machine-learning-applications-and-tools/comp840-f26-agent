"""Course-wide settings. Change model names HERE, not in individual labs."""

# Verified working 26 August 2026. A 404 means the model was withdrawn.
# To see what is available to you:
#   python -c "from google import genai; c=genai.Client(); [print(m.name) for m in c.models.list()]"
MODEL = "gemini-3.5-flash-lite"

# Alternates, for the benchmarking lab later in the term.
# Check quotas at https://ai.dev/rate-limit before using either.
MODEL_SMALL = "gemini-3.5-flash-lite"
MODEL_LARGE = "gemini-3.5-flash"

# Free-tier quota is per project, PER MODEL. We space our own calls out
# to stay under it rather than getting rejected.
REQUESTS_PER_MINUTE = 15
