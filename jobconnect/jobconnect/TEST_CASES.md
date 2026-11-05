# JobConnect test cases

Four manual scenarios that show how the match score and alerts behave. The score is
`shared skills ÷ required skills`, rounded to two decimals. A seeker is alerted when a new
job scores **0.30 or more**.

## Setup

Four job seekers sign up and upload a resume. Four recruiters then each post one job.

| Seeker | Skills found in the resume |
| --- | --- |
| priya_k | python, django, sql, git |
| arjun_m | sql, excel, communication |
| kiran_s | docker, python |
| lena_d | excel, tableau |

## Cases

| # | Scenario | Seeker | Job (recruiter) | Job needs | Score | Alert |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Full match | priya_k | Python Developer Intern (hr_asha) | python, django, sql | 3/3 = 100% | Yes |
| 2 | Partial match | arjun_m | Data Analyst Trainee (hr_ravi) | sql, excel, pandas, tableau | 2/4 = 50% | Yes |
| 3 | Just below the line | kiran_s | Cloud Support Engineer (hr_meera) | aws, docker, kubernetes, linux | 1/4 = 25% | No |
| 4 | No match | lena_d | Frontend Developer (hr_dev) | react, html, css, javascript | 0/4 = 0% | No |

## How to run them

1. Start the server with `python manage.py runserver` and open http://127.0.0.1:8000/.
2. Sign up the four seekers at `/accounts/signup/` (role: Job Seeker) and upload a resume
   containing the skills listed above.
3. Sign up the four recruiters (role: Employer) and post the jobs from the table.
4. Sign in as each seeker. The Jobs page shows the ranked score and Notifications shows
   the alert, where the table says one is expected.
