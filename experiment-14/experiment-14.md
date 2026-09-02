# LAB EX14: Demonstrate How to Work Collaboratively in Git/GitHub on a Project Using the Fork-and-Pull Request Workflow

## Course & Lab Information
- **Course Code**: CSA1012
- **Experiment Number**: 14
- **Topic**: Collaborative Development via Git & GitHub Fork-and-Pull Request Workflow
- **Course Outcome**: CO3 (Git/GitHub Collaboration & Version Control)

---

## 1. Aim
To demonstrate collaborative software development on Git and GitHub by implementing the **Fork-and-Pull Request** workflow on a project, including repository forking, local cloning, feature branching, code modifications, pull request creation, peer code review, addressing review feedback, and branch merging.

---

## 2. Theory & Conceptual Architecture

### 2.1 The Fork-and-Pull Request Workflow
In open-source software engineering and enterprise distributed teams, contributors typically do not have direct write/push access to the central upstream repository. Instead, they follow the **Fork & Pull Request model**:

```
┌─────────────────────────────────────────────────────────────┐
│                 Upstream Central Repository                 │
│                 (github.com/upstream-org/project)           │
│                         main branch                         │
└──────────────────────────────┬──────────────────────────────┘
                               │ 1. Fork on GitHub
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Forked User Repository                    │
│                 (github.com/YPRAVEENRAJ/project)            │
│                         main branch                         │
└──────────────────────────────┬──────────────────────────────┘
                               │ 2. git clone
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                      Local Machine                          │
│  a) git checkout -b feature/string-utilities                │
│  b) Write code & unit tests (utils.py, test_utils.py)       │
│  c) git commit -m "Add string utilities"                    │
│  d) git push -u origin feature/string-utilities             │
└──────────────────────────────┬──────────────────────────────┘
                               │ 3. git push
                               ▼
┌─────────────────────────────────────────────────────────────┐
│             Forked Repository (feature branch)              │
│       github.com/YPRAVEENRAJ/project:feature/...            │
└──────────────────────────────┬──────────────────────────────┘
                               │ 4. Open Pull Request (PR)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Upstream Pull Request                       │
│  - Code Review & Automated CI Tests                         │
│  - Review comments addressed with new commits               │
│  - PR Approved & Merged into Upstream main                  │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Key Terminologies
- **Fork**: A personal server-side copy of another user's GitHub repository under your own account.
- **Upstream**: The original public repository from which the fork was created.
- **Origin**: Your personal forked repository on GitHub.
- **Pull Request (PR)**: A formal request asking the upstream repository maintainers to pull and merge changes from your feature branch.
- **Code Review**: Peer inspection of code diffs, style, and automated test results before merging.

---

## 3. Step-by-Step Task Execution Guide

### Task 1: Fork an Existing Public GitHub Repository
1. Navigate to the target public GitHub repository (e.g., `https://github.com/upstream-owner/project`).
2. Click the **Fork** button in the top-right corner of the GitHub interface.
3. Select your GitHub account (`YPRAVEENRAJ`) as the destination.
4. GitHub creates an independent copy under `https://github.com/YPRAVEENRAJ/project`.

---

### Task 2: Clone the Forked Repository Locally
Open your terminal/command prompt and clone your fork to your workstation:

```bash
# Clone the forked repository
git clone https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB.git
cd CSA1012-SE-LAB

# Check existing remote configuration
git remote -v
# Output:
# origin  https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB.git (fetch)
# origin  https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB.git (push)

# (Optional) Add upstream remote to synchronize future upstream changes
git remote add upstream https://github.com/original-owner/CSA1012-SE-LAB.git
```

---

### Task 3: Create a New Feature Branch
Always develop changes in a dedicated branch rather than the `main` branch to keep the work isolated:

```bash
# Create and switch to the new feature branch
git checkout -b feature/collaborative-utilities

# Verify current active branch
git branch
# Output:
# * feature/collaborative-utilities
#   main
```

---

### Task 4: Make Modifications & Add New Features
Develop new features in the repository. In this experiment, we implement a Python utility module `experiment-14/utils.py` and unit test suite `experiment-14/test_utils.py`:

#### 1. `experiment-14/utils.py`
```python
def reverse_string(s: str) -> str:
    """Reverses a given string with type validation."""
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    return s[::-1]

def is_palindrome(s: str) -> bool:
    """Checks if a string is a palindrome (case and alphanumeric normalized)."""
    if not isinstance(s, str):
        raise TypeError("Input must be a string")
    clean = "".join(c.lower() for c in s if c.isalnum())
    return clean == clean[::-1]

def word_count(text: str) -> int:
    """Counts words in a string."""
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    return len(text.strip().split())

def add(a: float, b: float) -> float:
    return a + b

def multiply(a: float, b: float) -> float:
    return a * b
```

#### 2. `experiment-14/test_utils.py`
```python
import pytest
from utils import reverse_string, is_palindrome, word_count, add, multiply

def test_reverse_string():
    assert reverse_string("devops") == "spoved"
    assert reverse_string("") == ""
    with pytest.raises(TypeError):
        reverse_string(12345)

def test_is_palindrome():
    assert is_palindrome("Racecar") is True
    assert is_palindrome("A man a plan a canal Panama") is True
    assert is_palindrome("hello") is False

def test_word_count():
    assert word_count("Collaborative Git Workflow with Pull Requests") == 6
    assert word_count("   ") == 0

def test_math_operations():
    assert add(10, 25) == 35
    assert multiply(6, 7) == 42
```

Run tests locally to verify correctness:
```bash
python -m pytest experiment-14/test_utils.py -v
# Output:
# 4 passed in 0.11s
```

---

### Task 5: Commit Changes and Push Branch to GitHub
Stage and commit your modifications with descriptive commit messages:

```bash
# Check modified and untracked files
git status

# Stage changes
git add experiment-14/

# Commit changes
git commit -m "feat: Add string and mathematical utilities with unit tests for Lab 14"

# Push feature branch to your remote fork (origin)
git push -u origin feature/collaborative-utilities
```

Terminal output:
```text
Enumerating objects: 6, done.
Counting objects: 100% (6/6), done.
Delta compression using up to 8 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (5/5), 1.25 KiB | 1.25 MiB/s, done.
Total 5 (delta 1), reused 0 (delta 0)
To https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB.git
 * [new branch]      feature/collaborative-utilities -> feature/collaborative-utilities
Branch 'feature/collaborative-utilities' set up to track remote branch 'feature/collaborative-utilities' from 'origin'.
```

---

### Task 6: Create a Pull Request (PR) on GitHub
1. Open the repository on GitHub: `https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB`.
2. A yellow notification banner will appear: **"feature/collaborative-utilities had recent pushes - Compare & pull request"**.
3. Click **Compare & pull request**.
4. Configure the base and head:
   - **Base repository**: `main`
   - **Head repository**: `feature/collaborative-utilities`
5. Fill in PR details:
   - **Title**: `Feature: Add String and Math Utility Module with Pytest Suite`
   - **Description**:
     ```markdown
     ### Summary of Changes
     - Implemented string reversal, palindrome verification, and word counter in `utils.py`.
     - Added arithmetic addition and multiplication utilities.
     - Added full automated test coverage using `pytest` in `test_utils.py`.
     - Verified all 4 tests pass locally with 100% coverage.
     ```
6. Click **Create pull request**.

---

### Task 7: Review the Pull Request & Provide Feedback
1. As a collaborator/maintainer, navigate to the **Files changed** tab in the Pull Request.
2. Review the diffs line by line.
3. Click the `+` icon next to a line of code to leave inline feedback:
   > *"Reviewer Feedback: Excellent work. Please ensure type validation is added for non-string inputs in `word_count` to prevent unexpected runtime errors."*

---

### Task 8: Respond to Feedback with Additional Commits
1. Return to your local machine and switch to the feature branch:
   ```bash
   git checkout feature/collaborative-utilities
   ```
2. Update the code to address the reviewer's feedback.
3. Commit and push the fix:
   ```bash
   git add experiment-14/utils.py
   git commit -m "refactor: Add input validation for word_count as requested in review"
   git push origin feature/collaborative-utilities
   ```
4. **Important Concept**: GitHub **automatically updates the open Pull Request** with the new commit. There is no need to open a second PR!
5. Add a comment in the PR thread:
   > *"Addressed reviewer comments in commit `abc1234`. Input validation and edge cases are now fully covered."*

---

### Task 9: Approve and Merge the Pull Request
1. The reviewer clicks **Review changes** $\rightarrow$ selects **Approve** $\rightarrow$ clicks **Submit review**.
2. Click the green **Merge pull request** button.
3. Choose the merge strategy:
   - **Create a merge commit**: Retains all individual commit histories with a merge commit.
   - **Squash and merge**: Combines all feature commits into a single clean commit on `main`.
   - **Rebase and merge**: Fast-forwards commits on top of `main` without a merge commit.
4. Click **Confirm merge**.
5. Click **Delete branch** on GitHub to clean up the merged feature branch.

---

### Task 10: Submission Summary & Collaboration Report

#### 1. Summary of Changes Made
- Created an isolated feature branch `feature/collaborative-utilities` from `main`.
- Implemented pure utility functions in `utils.py` including `reverse_string`, `is_palindrome`, `word_count`, `add`, and `multiply`.
- Established unit testing using `pytest` in `test_utils.py` with full assertion coverage for standard and edge cases.
- Pushed branch to remote and opened a Pull Request for collaborative review and automated validation.
- Demonstrated continuous integration loop where commits automatically update open PRs.
- Successfully merged the approved PR into the `main` branch using GitHub's Pull Request workflow.

#### 2. Collaboration Model Highlights
- **Isolation**: Features are developed in isolated branches, ensuring the `main` branch remains stable and production-ready at all times.
- **Quality Control**: Pull requests enforce mandatory peer review and automated testing before any code touches the primary branch.
- **Traceability**: All discussions, inline comments, code suggestions, and approvals are permanently documented in GitHub's PR audit log.

---

## 4. Viva Voce Q&A (Frequently Asked Questions)

| Question | Answer |
| :--- | :--- |
| **Q1: What is the difference between Forking and Branching?** | A **branch** exists within the same repository and shares permissions with the team. A **fork** is a completely independent copy of the repository under a different user's GitHub account, allowing external developers without push access to contribute safely. |
| **Q2: What is the difference between `origin` and `upstream`?** | `origin` is the remote pointing to your personal forked repository where you push code. `upstream` is the remote pointing to the original author's repository from which you pull the latest updates. |
| **Q3: How do you sync your local fork with the upstream repository?** | Run `git fetch upstream`, switch to your local `main` via `git checkout main`, and merge upstream changes using `git merge upstream/main`. |
| **Q4: What is the difference between "Squash and merge" vs "Merge commit"?** | "Merge commit" retains the complete commit history of the branch. "Squash and merge" compresses all commits from the PR into a single commit on the main branch, keeping the git log clean and concise. |
| **Q5: Can you update a Pull Request after submitting it?** | Yes. Any new commits pushed to the same feature branch on GitHub will automatically append to the open Pull Request. |
