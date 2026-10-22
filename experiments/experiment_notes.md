# Resume Ranker Robustness Experiments

## Objective
Evaluate whether simple defenses reduce false skill matches in a resume-ranking system.

## Experiment 1: Valid Skills
The original matcher detects all listed skills. The boundary-aware matcher avoids incorrectly detecting the single-letter skill C when it is not present as a standalone token.

## Experiment 2: Substring Trap
The original matcher falsely identifies C in text where the letter occurs inside another word. The boundary-aware matcher rejects this false match.

## Experiment 3: Keyword Stuffing
Both matchers identify the same listed skills. The current defenses do not prevent keyword stuffing from influencing the skill-matching result.

## Experiment 4: Negated Skills
The original matcher incorrectly counts Java in "I have no experience with Java." The negation-aware matcher correctly places Java under missing skills in this test. Similar behavior was observed for C and Python in the supplied negative statements.

## Limitations
- Results are from a small, manually constructed test set.
- The tests do not establish general defense effectiveness.
- Keyword stuffing requires a separate defense and evaluation.
- These skill-matching experiments do not, by themselves, test LLM prompt injection.
- Larger and more diverse test cases are required before drawing strong conclusions.

## Next Step
Build a unified evaluation that compares the original, boundary-aware, and negation-aware matchers on the same test cases and reports quantitative results.