# JobConnect — starter project

Django skeleton for the "JobConnect: A Resume-Matched Job Portal" First Review proposal.
Two roles (job seeker / employer), resume upload with automatic skill extraction,
a transparent skill-overlap match score, and in-app notifications when a new
posting matches a seeker's profile.

## What's already built

| App | Purpose |
|---|---|
| `accounts` | Signup/login, `Profile` model (role: seeker/employer, skills, optional GitHub username) |
| `resumes` | Resume upload, text extraction (`resumes/utils.py`), keyword-based skill parsing |
| `jobsboard` | Job postings, `matching.py` (the match-score logic), `signals.py` (fires a notification when a new posting matches a seeker) |

The matching logic is a simple, explainable skill-overlap score (see
`jobsboard/matching.py`) — not a black-box ML model — so it's easy to
describe in a review and easy to extend later.

## 1. Open it in VS Code

1. Unzip the project folder and open it in VS Code (`File → Open Folder…`).
2. Install the **Python** extension (Microsoft) if you don't already have it.

## 2. Set up the environment

Open a terminal in VS Code (`` Ctrl+` ``/`` Cmd+` ``) in the project root and run:

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then point VS Code at this interpreter: `Ctrl+Shift+P` → **Python: Select Interpreter** →
choose the one inside `venv/`.

## 3. Set up the database

```bash
python manage.py migrate
python manage.py createsuperuser   # follow the prompts — this is your admin login
```

## 4. Run the test server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser. Leave this terminal running while
you work — Django auto-reloads when you save a file.

- `/` — home page
- `/accounts/signup/` — create a seeker or employer account
- `/jobs/` — browse postings (ranked by match score if you're logged in as a seeker)
- `/resumes/upload/` — upload a resume (PDF or .txt) as a seeker
- `/admin/` — Django admin, log in with the superuser you created above

## 5. Try the whole flow

1. Sign up as an **employer**, post a job with `required_skills` like `python, django, sql`.
2. Sign up as a **seeker** (different browser or incognito window, since only one
   login is active per browser session), upload a resume that mentions some of
   those skills as plain text, and check `/jobs/` — you should see a match
   percentage and, under **Notifications**, an alert about the new posting.

## Where to extend things

- **More skills**: add words/phrases to `SKILLS_VOCAB` in `resumes/utils.py`.
- **Smarter matching**: `jobsboard/matching.py` has one function, `match_score()` —
  swap its internals for something fancier without touching any view.
- **GitHub integration**: `Profile.github_username` is already there; add a call to
  `https://api.github.com/users/<username>/repos` (via the `requests` library,
  already installed) to pull languages into `profile.skills`.
- **Styling**: everything currently uses inline CSS in `templates/base.html` —
  swap in Bootstrap/Tailwind if you want a quicker visual upgrade.

## Notes

- `DEBUG = True` and the `SECRET_KEY` in `jobconnect/settings.py` are fine for local
  development/demo purposes only — never deploy this as-is.
- SQLite (`db.sqlite3`) is used for local development; it's created the first time
  you run `migrate` and is git-ignored.
