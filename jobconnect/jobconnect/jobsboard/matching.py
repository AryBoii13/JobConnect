"""The core "AI-based recommendation" from the project proposal, scoped
to something explainable: a transparent skill-overlap score.

match_score() is deliberately simple — Jaccard overlap between a
candidate's skill set and a posting's required skills — so it is easy
to defend in a review and easy to swap for something smarter later.
"""

# A posting needs at least this much overlap with a candidate's skills
# before we bother notifying them about it.
NOTIFY_THRESHOLD = 0.3


def match_score(candidate_skills: set[str], required_skills: set[str]) -> float:
    """Return a 0.0–1.0 overlap score between two skill sets."""
    if not required_skills:
        return 0.0
    overlap = candidate_skills & required_skills
    return round(len(overlap) / len(required_skills), 2)


def rank_postings_for(candidate_skills: set[str], postings) -> list[tuple[object, float]]:
    """Sort postings by match score, highest first."""
    scored = [(p, match_score(candidate_skills, p.skill_set())) for p in postings]
    return sorted(scored, key=lambda pair: pair[1], reverse=True)
