# LAB EX20: Create a GitHub Repository and Implement Version Control

## Course & Lab Information
- **Course Code**: CSA1012
- **Experiment Number**: 20
- **Topic**: Create a GitHub Repository and Implement Team Version Control
- **Course Outcome**: CO3 (Version Control, Branching, Pull Requests & Conflict Resolution)

---

## 1. Aim
To create a team repository on GitHub, establish professional Git version control workflows, develop individual system modules on isolated branches, conduct code reviews and merge branches via Pull Requests, resolve merge conflicts during branch integration, document the workflow, and submit the repository.

---

## 2. Team Architecture & Modular Design

The application is structured into three discrete services integrated by an orchestrator:

```
                               ┌────────────────────────────────┐
                               │       Main Branch (main)       │
                               │   Stable, Production-Ready     │
                               └───────────────┬────────────────┘
                                               │
               ┌───────────────────────────────┼───────────────────────────────┐
               ▼                               ▼                               ▼
┌──────────────────────────────┐┌──────────────────────────────┐┌──────────────────────────────┐
│  Branch: module/auth         ││ Branch: module/order-proc    ││ Branch: module/notifications │
│  user_auth.py                ││ order_processor.py           ││ notification_service.py      │
│  - User Registration         ││ - Cart Subtotal Calculation  ││ - Multi-channel Dispatch     │
│  - SHA-256 Hash Auth         ││ - Tax Computation            ││ - Audit Logging              │
│  - Session Verification      ││ - Order Confirmation         ││ - Delivery Status Tracking   │
└──────────────┬───────────────┘└──────────────┬───────────────┘└──────────────┬───────────────┘
               │                               │                               │
               └───────────────────────┬───────┴───────────────────────────────┘
                                       ▼
                       Pull Request & Code Review Gate
                                       ▼
                         Merged into 'main' branch
                                       ▼
                              Integrated in main.py
```

---

## 3. Step-by-Step Task Execution Guide

### Task 1: Set Up a Repository for a Team Project
1. Initialized local Git repository and connected to remote origin on GitHub:
   ```bash
   git init
   git branch -M main
   git remote add origin https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB.git
   ```
2. Configured `.gitignore` to prevent caching artifacts (`__pycache__`, `.pytest_cache`, logs) from entering the repository.
3. Published initial baseline commit to GitHub.

---

### Task 2: Create Branches for Individual Modules
In enterprise collaborative development, each developer or sub-team creates an isolated feature branch matching their assigned module:

```bash
# Branch 1: User Authentication Module
git checkout -b module/user-auth

# Branch 2: Order Processing Module
git checkout -b module/order-processing

# Branch 3: Notifications Service Module
git checkout -b module/notifications
```

---

### Task 3: Merge Branches with Pull Requests after Code Reviews
1. Develop module code on the dedicated branch (e.g. `module/order-processing`).
2. Verify code quality using automated tests (`pytest test_project.py -v`).
3. Commit and push the module branch to GitHub:
   ```bash
   git add experiment-20/order_processor.py
   git commit -m "feat(orders): Implement OrderProcessor with tax computation and cart checkout"
   git push -u origin module/order-processing
   ```
4. **Open Pull Request**:
   - Go to `https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB/pull/new/module/order-processing`.
   - Set **Base branch**: `main` $\leftarrow$ **Compare branch**: `module/order-processing`.
   - Add description outlining newly introduced methods and test validation.
5. **Code Review Gate**:
   - Peer reviewer inspects the diff under the **Files changed** tab.
   - Verifies edge cases (e.g., handling zero-item carts).
   - Upon approval, the PR is merged into `main`.

---

### Task 4: Resolve Conflicts During Branch Merging
When two module branches concurrently update the same integration file or shared interface (e.g., modifying `main.py` or configuration headers):

1. **Conflict Trigger**:
   - Branch A (`module/order-processing`) updates integration lines in `main.py`.
   - Branch B (`module/notifications`) concurrently updates the same lines in `main.py`.
2. **Git Conflict Alert**:
   ```text
   Auto-merging experiment-20/main.py
   CONFLICT (content): Merge conflict in experiment-20/main.py
   Automatic merge failed; fix conflicts and then commit the result.
   ```
3. **Inspect Conflict Markers**:
   ```python
   <<<<<<< HEAD (Current Branch)
       # Order processor integration
       order = processor.place_order("ORD-1", "student_dev", cart)
   =======
       # Notification service integration
       notif = notifier.send_notification("student_dev@univ.edu", "Order Placed")
   >>>>>>> main (Incoming Branch)
   ```
4. **Manual Resolution**:
   - Open file in editor.
   - Delete markers `<<<<<<<`, `=======`, `>>>>>>>`.
   - Combine both operations in proper sequence:
     ```python
     order = processor.place_order("ORD-1", "student_dev", cart)
     notif = notifier.send_notification("student_dev@univ.edu", f"Order {order['order_id']} placed")
     ```
5. **Finalize Merge**:
   ```bash
   git add experiment-20/main.py
   git commit -m "Merge branch 'main' into module/notifications: Resolve main.py integration conflict"
   git push origin module/notifications
   ```

---

### Task 5: Document the Workflow in README
Created comprehensive documentation in both:
- [experiment-20/README.md](file:///c:/Users/yprav/OneDrive/Desktop/CSA1012/experiment-20/README.md): Documents the project architecture, module descriptions, execution instructions, and Git workflow rules.
- [experiment-20/experiment-20.md](file:///c:/Users/yprav/OneDrive/Desktop/CSA1012/experiment-20/experiment-20.md): Complete laboratory manual record with step-by-step evidence, diagrams, and theoretical background.

---

### Task 6: Submit Repository Link

> **Lab Submission Details**
> - **Student Name**: YPRAVEENRAJ
> - **Course**: CSA1012 (Software Engineering Lab)
> - **Experiment**: LAB EX20 – Create a GitHub Repository and Implement Version Control
> - **Course Outcome**: CO3
> - **Repository URL**: [https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB](https://github.com/YPRAVEENRAJ/CSA1012-SE-LAB)

---

## 4. Key Takeaways & Best Practices

1. **Trunk-Based Development**: Keep feature branches short-lived and merge frequently into `main` to minimize merge conflicts.
2. **Protected Main Branch**: Enforce branch protection rules on GitHub so no code can be pushed directly to `main` without passing code reviews and automated tests.
3. **Atomic Commits**: Write small, focused commits with clear imperative messages (`feat: ...`, `fix: ...`, `docs: ...`).
4. **Clean Merge Strategy**: Use "Squash and merge" for feature branches to maintain a clean, linear git commit history on `main`.
