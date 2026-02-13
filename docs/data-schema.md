# Data Schema

Each sample is a single message or message segment.

## Required Fields
- `id`: string
- `text`: string
- `label`: int (1=phishing, 0=benign)
- `language`: string (ISO 639-1 or custom for code-mix)
- `script`: string (e.g., Devanagari, Latin, Bengali)
- `source`: string (sms, email, chat, user_report)
- `timestamp`: string (ISO 8601)

## Optional Fields
- `intent`: string (credential, payment, kyc, delivery, other)
- `url_count`: int
- `phone_count`: int
- `has_otp_request`: bool
- `brand_mention`: string
- `region`: string

## Example (JSONL)
{"id":"msg_0001","text":"aapka KYC update karo","label":1,"language":"hi-mix","script":"Latin","source":"sms","timestamp":"2026-01-12T10:21:00Z"}
