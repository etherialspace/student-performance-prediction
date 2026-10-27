# Intelligent Student Performance Prediction System (AI/ML)

## 📌 Project Objective
Develop an Artificial Intelligence system that predicts student academic performance based on historical and continuous assessment metrics using **Machine Learning Classification** (**Decision Tree Classifier**), and provides intelligent, personalized diagnostic recommendations identifying specific areas where the student needs improvement.

---

## 🎯 Tasks Implemented

1. **Student Details as Input**:
   - Student Name & Roll / Student ID
   - **Attendance (%)** (Range: `0` to `100%`)
   - **Assignment Marks** (Range: `0` to `100`)
   - **Internal Marks** (Range: `0` to `100`)
   - **Study Hours** (Daily self-study hours, Range: `0` to `16 hrs/day`)

2. **Performance Classification Tiers**:
   - 🌟 **Excellent**: High academic performance, consistent attendance, top internal and assignment scores.
   - 📘 **Good**: Above-average performance, meeting standard benchmarks with minor areas for refinement.
   - 📙 **Average**: Moderate performance, inconsistent scores or study duration; needs guided improvement.
   - ⚠️ **Poor**: Critical performance, falling below passing or eligibility thresholds; requires immediate intervention.

3. **Advanced Diagnostic Feature (Areas for Improvement)**:
   - Evaluates each of the 4 academic metrics against institutional benchmarks.
   - Assigns priority severity: `Critical`, `Moderate`, or `Minor`.
   - Displays a diagnostic comparison table (`Current Value` vs `Recommended Target`).
   - Generates actionable, step-by-step improvement recommendations and a customized study schedule.

4. **Prediction Result Display**:
   - Formatted comprehensive performance report card in CLI.
   - Real-time interactive web dashboard with color-coded tier cards, metric sliders, Decision Tree rule visualization, and report printing.

---

## 🧠 AI / ML Concepts Used

- **Supervised Learning**: Classification task mapping continuous input features to discrete academic performance tiers.
- **Decision Tree Classifier**:
  - Employs **Gini Impurity** to discover optimal splits across academic parameters.
  - Generates clear, explainable decision paths (white-box model).
  - Works with standard **scikit-learn** (`sklearn.tree.DecisionTreeClassifier`) and includes a pure Python CART fallback implementation so it runs out-of-the-box with **zero external dependencies**.
- **Feature Importance Analysis**: Measures the Gini gain contribution of Attendance, Assignment Marks, Internal Marks, and Study Hours.
- **Rule Extraction**: Translates trained tree nodes into human-readable logical rules (`IF attendance > 75 AND study_hours > 6.0 THEN Good`).

---

## 📂 Project Structure

```text
student-performance-prediction/
├── student_performance_predictor.py   # Core AI engine: CART & scikit-learn Decision Tree, diagnostic logic, CLI & Demo modes
├── web_app.py                         # Interactive Web Dashboard (Standard library HTTP server, zero dependencies)
├── test_student_performance.py        # Automated test suite (unittest) covering all 4 tiers, edge cases & diagnostics
├── student_dataset.csv                # Representative dataset of 56 student records across all performance tiers
├── requirements.txt                   # Optional dependencies (scikit-learn)
└── README.md                          # Comprehensive project documentation
```

---

## 🚀 How to Run

### 1. Interactive Command Line Interface (CLI)
Run the predictor interactively in your terminal:
```bash
python3 student_performance_predictor.py
```
*Prompted inputs: Student Name, Roll No, Attendance %, Assignment Marks, Internal Marks, and Study Hours.*

### 2. Demo Mode (All 4 Performance Tiers)
Execute automated sample predictions for Excellent, Good, Average, and Poor students:
```bash
python3 student_performance_predictor.py --demo
```

### 3. Interactive Web Dashboard (Recommended)
Launch the responsive browser UI:
```bash
python3 web_app.py
```
Open your browser at: **[http://localhost:5050](http://localhost:5050)**

**Web Dashboard Features:**
- Interactive real-time sliders for all 4 parameters.
- Instant preset buttons (`🌟 Aarav - Excellent`, `📘 Priya - Good`, `📙 Rohan - Average`, `⚠️ Kabir - Poor`).
- Color-coded tier badges with real-time feedback.
- Diagnostic weak areas table with severity tags (`CRITICAL`, `MODERATE`, `MINOR`).
- Step-by-step personalized action plan.
- Feature importance visualization and Decision Tree rules inspector.
- One-click print/PDF student report generator (`🖨️ Print Student Report`).

### 4. Running Unit Tests
Validate model predictions, tree rules, and diagnostic recommendations:
```bash
python3 test_student_performance.py
```

---

## 📊 Sample Output (Poor Tier Example)

```text
========================================================================
                     STUDENT PERFORMANCE REPORT                         
========================================================================
  Student Name      : Kabir Patel
  Student ID / Roll : STU-104
------------------------------------------------------------------------
  INPUT ACADEMIC METRICS:
    1. Attendance       :   48.0 %
    2. Assignment Marks :   42.0 / 100
    3. Internal Marks   :   39.0 / 100
    4. Study Hours      :    1.5 hrs/day
------------------------------------------------------------------------
  PREDICTED PERFORMANCE : POOR
  ASSESSMENT SUMMARY    : POOR (Requires Immediate Academic Intervention)
------------------------------------------------------------------------
  AREAS NEEDING IMPROVEMENT (Diagnostic Analysis):
    Parameter            | Current        | Recommended      | Priority
    ----------------------------------------------------------------
    Attendance           | 48.0%          | 75.0% - 88.0%    | Critical
    Assignment Marks     | 42.0/100       | 70.0/100+        | Critical
    Internal Marks       | 39.0/100       | 70.0/100+        | Critical
    Study Hours          | 1.5 hrs/day    | 4.5 - 6.0 hrs/day | Critical
------------------------------------------------------------------------
  PERSONALIZED SUGGESTIONS FOR IMPROVEMENT:
    1. [CRITICAL] Attendance is very low (48.0%). You risk missing core lecture concepts and falling below minimum exam eligibility (75%).
    2. [CRITICAL] Assignment score (42.0/100) indicates gaps in practical application and timely submission.
    3. [CRITICAL] Internal exam score (39.0/100) is critically low and heavily impacts final performance.
    4. [CRITICAL] Daily self-study time (1.5 hrs/day) is insufficient for mastering coursework.

  RECOMMENDED ACTION PLAN:
    [1] Attend all upcoming lectures consistently and collect missed class notes from peers/faculty.
    [2] Start assignments early, review grading rubrics carefully, and consult teaching assistants before submission.
    [3] Solve past internal test papers under timed conditions and focus on high-weightage syllabus units.
    [4] Increase daily focused study time from 1.5 hrs to at least 4.5 hrs/day using structured Pomodoro blocks (50m study / 10m break).
========================================================================
```
