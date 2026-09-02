# LAB EX15: Demonstrate How to Work with Git Branches and Resolve Merge Conflicts When Collaborating with Others

## Course & Lab Information
- **Course Code**: CSA1012
- **Experiment Number**: 15
- **Topic**: Git Branching, Team Collaboration & Manual Merge Conflict Resolution
- **Course Outcome**: CO3 (Git/GitHub Version Control & Conflict Management)

---

## 1. Aim
To demonstrate how to work collaboratively in Git using isolated feature branches, simulate concurrent changes on the same file lines leading to a merge conflict, understand conflict markers, resolve the conflict manually, commit the resolution, and submit a Pull Request on GitHub.

---

## 2. Theory & Conceptual Architecture

### 2.1 Why Merge Conflicts Occur
In a collaborative team environment, multiple software engineers work on separate feature branches branched off a common base commit on `main`. A **merge conflict** occurs when:
1. Two branches modify the **exact same line(s)** of code differently.
2. One branch deletes a file that another branch modified.

Git can automatically merge changes made to different files or different lines of the same file (3-way merge). However, when two conflicting changes compete for the same lines, Git halts the merge and requests human intervention.

```
                  ┌── [Commit A] Edit Line 15 (Price Validation) ─────┐ (main)
                  │                                                    │
[Base Commit] ────┤                                                    ├──▶ CONFLICT!
                  │                                                    │    (Manual Resolution)
                  └── [Commit B] Edit Line 15 (Rate Validation) ──────┘ (feature branch)
```

### 2.2 Anatomy of Git Conflict Markers
When a conflict occurs, Git inserts special conflict markers directly into the affected file:

```python
<<<<<<< HEAD (Current Branch - feature/discount-validation)
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("Discount rate must be between 0.0 and 1.0")
    return round(price * (1 - discount_rate), 2)
=======
    if price < 0.0:
        raise ValueError("Price cannot be negative")
    return price - (price * discount_rate)
>>>>>>> main (Incoming Branch being merged)
```

- `<<<<<<< HEAD`: Marks the beginning of changes in the currently checked-out branch.
- `=======`: The separator between your changes and the incoming branch's changes.
- `>>>>>>> <branch_name>`: Marks the end of changes coming from the branch being merged.

---

## 3. Step-by-Step Task Execution

### Task 1: Clone Shared Repository to Local Machine
```bash
git clone https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB.git
cd CSA1012-SE-LAB
```

---

### Task 2: Create a New Branch and Switch to It
```bash
git checkout -b feature/discount-validation
# Output:
# Switched to a new branch 'feature/discount-validation'
```

---

### Task 3: Make Changes to a File
In `experiment-15/calculator.py`, Developer A adds discount rate validation:
```python
def calculate_discount(price: float, discount_rate: float) -> float:
    """Calculates discounted price with discount rate range validation."""
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("Discount rate must be between 0.0 and 1.0")
    return round(price * (1 - discount_rate), 2)
```

---

### Task 4: Commit Your Changes
```bash
git add experiment-15/calculator.py
git commit -m "feat: Add discount rate validation to calculate_discount"
```

---

### Task 5: Push the Changes to the Remote Repository
```bash
git push -u origin feature/discount-validation
```

---

### Task 6: Pull Latest Changes from the Main Branch
Meanwhile, a collaborator commits a competing modification on `main` to the exact same function:
```python
def calculate_discount(price: float, discount_rate: float) -> float:
    """Calculates discounted price with negative price validation."""
    if price < 0.0:
        raise ValueError("Price cannot be negative")
    return price - (price * discount_rate)
```

To integrate upstream changes before opening a PR:
```bash
git checkout main
git pull origin main
```

---

### Task 7: Switch Back to Your Feature Branch
```bash
git checkout feature/discount-validation
```

---

### Task 8: Merge the Main Branch into Your Feature Branch
```bash
git merge main
```

**Git Terminal Output (Conflict Triggered):**
```text
Auto-merging experiment-15/calculator.py
CONFLICT (content): Merge conflict in experiment-15/calculator.py
Automatic merge failed; fix conflicts and then commit the result.
```

---

### Task 9: Resolve Conflicts Manually & Mark as Resolved
Open `experiment-15/calculator.py`. Locate the conflict markers and combine both business rules into a unified, clean function:

**Resolved Code (`experiment-15/calculator.py`):**
```python
def calculate_discount(price: float, discount_rate: float) -> float:
    """
    Calculates discounted price with comprehensive validation.
    Resolved Merge Conflict: Retains both price positivity and discount rate bounds.
    """
    if price < 0.0:
        raise ValueError("Price cannot be negative")
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("Discount rate must be between 0.0 and 1.0")
    return round(price * (1 - discount_rate), 2)
```

Run tests to verify functionality:
```bash
python -m pytest experiment-15/test_calculator.py -v
# Output: 3 passed in 0.12s
```

Mark the conflict as resolved using `git add`:
```bash
git add experiment-15/calculator.py
git status
```
*Status: `All conflicts fixed but you are still merging.`*

---

### Task 10: Commit the Resolved Merge
```bash
git commit -m "Merge branch 'main' into feature/discount-validation: Resolved calculate_discount validation conflict"
# Output:
# [feature/discount-validation 60d6204] Merge branch 'main' into feature/discount-validation: Resolved calculate_discount validation conflict
```

---

### Task 11: Push Feature Branch to GitHub & Create Pull Request
```bash
git push origin feature/discount-validation
```

🔗 **Pull Request URL**:  
`https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB/pull/new/feature/discount-validation`

---

### Task 12: Summary of Steps, Conflicts Encountered, and Resolution

#### 1. Summary of Steps Performed:
1. Created an isolated branch `feature/discount-validation` from `main`.
2. Implemented discount rate bounds checking (`0.0 <= rate <= 1.0`) on `feature/discount-validation` and committed.
3. Simultaneously on `main`, a competing commit added price negativity checking (`price < 0.0`) on the exact same lines of `calculator.py`.
4. Merged `main` into `feature/discount-validation` to synchronize branch with production code before PR creation.
5. Detected content conflict in `calculator.py` as both branches touched the same function body.
6. Examined conflict markers (`<<<<<<< HEAD`, `=======`, `>>>>>>> main`), removed markers, and combined both validation features cleanly.
7. Verified code correctness with `pytest` unit tests.
8. Marked resolved with `git add` and finalized merge with a descriptive merge commit.
9. Pushed clean branch to GitHub and opened Pull Request for final review and merge.

#### 2. Conflict Encountered:
- **File**: `experiment-15/calculator.py`
- **Function**: `calculate_discount(price, discount_rate)`
- **Conflict Cause**: Competing validation logic on the same lines of code between the feature branch (rate validation) and the main branch (price validation).

#### 3. Resolution Method:
- Rather than discarding either change (`ours` vs `theirs`), a **collaborative union** was implemented where both validations were kept in sequence:
  1. Guard clause 1: Reject negative price (`price < 0.0`).
  2. Guard clause 2: Reject invalid rate bounds (`not 0.0 <= discount_rate <= 1.0`).
  3. Formula: Applied round calculation to 2 decimal places.
- Removed all conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).

---

## 4. Viva Voce Q&A (Frequently Asked Questions)

| Question | Answer |
| :--- | :--- |
| **Q1: Why does Git not automatically resolve conflicts on the same lines?** | Git does not make assumptions about business logic or developer intent. If two developers write different code on the same lines, only a human can decide whether to keep branch A, keep branch B, or combine them. |
| **Q2: What command aborts an active merge if you get stuck?** | `git merge --abort`. This restores the working directory to the exact state before `git merge` was initiated. |
| **Q3: What does `git status` show during an active merge conflict?** | It lists the conflicting files under **"Unmerged paths:"** with the label `both modified: <filename>`. |
| **Q4: How do you mark a conflict as resolved in Git?** | After manually editing the file and removing conflict markers, run `git add <filename>`. |
| **Q5: What is the benefit of merging `main` into your feature branch before creating a PR?** | It allows the developer to resolve conflicts locally on their machine and test their code against the latest production baseline before submitting the Pull Request. |
