---
id: 6
title: Fix Register Password Validation
stage: green
date: 2026-02-26
surface: agent
model: claude-sonnet-4-6
feature: todo-web-app
branch: main
user: user
command: chat
labels: ["auth","validation","bugfix","register","password"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/utils/validation.py
  - frontend/src/app/register/page.tsx
tests:
  - manual: POST /auth/register with special-character password returns 200
  - manual: POST /auth/register with password < 6 chars returns 400
  - manual: POST /auth/register with password > 71 bytes returns 400
---

## Prompt

This project is deployed on Vercel, but I'm facing issues in the authentication Register option. These restrictions appear:

"Password cannot be longer than 72 bytes, truncate manually if necessary (e.g. my_password[:72])"

"Password must be at least 6 characters long"

And in the console, this error appears:

Failed to load resource: the server responded with a status of 400 ()

POST https://ovais123-todo-full-stack-app.hf.space/auth/register 400 (Bad Request)

I need help understanding and fixing these errors.

## Response snapshot

Two root causes identified and fixed:

1. **Overly restrictive password regex** (`validation.py:24`): `re.fullmatch(r"[a-zA-Z0-9]+", password)` rejected any password with special characters (@, !, $, etc.), causing 400 for most real-world passwords. The check was removed entirely — letters, numbers, and symbols are all permitted.

2. **72-byte limit too close to passlib's internal limit**: Changed from `> 72` to `> 71` bytes to avoid passlib/bcrypt raising its own "truncate manually" error for borderline-length passwords (bcrypt counts the null terminator).

Frontend (`register/page.tsx`) updated with matching client-side validation and a hint label so users know special characters are allowed.

## Outcome

- ✅ Impact: Registration now works for passwords with special characters; 400 errors resolved
- 🧪 Tests: Manual test cases for special chars, too-short, and too-long passwords
- 📁 Files: backend/src/utils/validation.py, frontend/src/app/register/page.tsx
- 🔁 Next prompts: Add password confirmation field; consider stronger password requirements (uppercase + digit)
- 🧠 Reflection: The alphanumeric-only regex was the hidden primary cause; the 72-byte passlib message was a secondary symptom from borderline-length inputs

## Evaluation notes (flywheel)

- Failure modes observed: Alphanumeric-only regex silently blocked common passwords without a clear user-facing message explaining the restriction
- Graders run and results (PASS/FAIL): n/a
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): Add a confirm-password field to the register form
