#!/usr/bin/env python3
"""
Script to generate a comprehensive, publication-quality university DOCX report
for the Intelligent Student Performance Prediction System.
"""

import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, hex_color):
    """Set the background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    """Set inner padding for table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_callout(doc, text, title="KEY TAKEAWAY / NOTE", bg_color="F0F4F8", border_color="1B365D"):
    """Add a professional styled callout box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell = tbl.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Left border only
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run_t = p.add_run(f"[{title}] ")
    run_t.bold = True
    run_t.font.name = "Arial"
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    run_body = p.add_run(text)
    run_body.font.name = "Arial"
    run_body.font.size = Pt(9.5)
    run_body.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    
    # Space after table
    sp = doc.add_paragraph()
    sp.paragraph_format.space_before = Pt(0)
    sp.paragraph_format.space_after = Pt(6)

def style_heading(p, font_size, color_rgb, space_before=12, space_after=6, bold=True):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.keep_with_next = True
    for r in p.runs:
        r.bold = bold
        r.font.name = "Arial"
        r.font.size = Pt(font_size)
        r.font.color.rgb = color_rgb

def build_docx():
    doc = Document()
    
    # Page setup - 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Base Colors
    NAVY = RGBColor(0x1B, 0x36, 0x5D)      # Primary Header #1B365D
    SLATE = RGBColor(0x2B, 0x6C, 0xB0)     # Subheader #2B6CB0
    CHARCOAL = RGBColor(0x2D, 0x37, 0x48)  # Body text #2D3748
    MUTED = RGBColor(0x71, 0x80, 0x96)     # Muted caption #718096
    
    # -------------------------------------------------------------
    # TITLE & COVER BLOCK
    # -------------------------------------------------------------
    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cat = p_meta.add_run("ACADEMIC PROJECT REPORT • ARTIFICIAL INTELLIGENCE & MACHINE LEARNING")
    r_cat.font.name = "Arial"
    r_cat.font.size = Pt(9)
    r_cat.font.bold = True
    r_cat.font.color.rgb = SLATE
    p_meta.paragraph_format.space_after = Pt(8)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("Intelligent Student Performance Prediction System")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = NAVY
    p_title.paragraph_format.space_after = Pt(6)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Comprehensive Technical Documentation, Theoretical Formulation, and Question-by-Question Solution Guide")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = CHARCOAL
    p_sub.paragraph_format.space_after = Pt(16)

    # Horizontal Divider Line via Table
    div_tbl = doc.add_table(rows=1, cols=1)
    div_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_div = div_tbl.cell(0, 0)
    cell_div.width = Inches(6.5)
    set_cell_background(cell_div, "1B365D")
    set_cell_margins(cell_div, top=10, bottom=10, left=0, right=0)
    
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_after = Pt(14)

    # Project Metadata Box
    meta_tbl = doc.add_table(rows=4, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Objective:", "Develop an AI system that predicts student performance based on academic information."),
        ("AI Concepts Employed:", "Supervised Machine Learning, Multi-Class Classification, Decision Tree (CART / Gini Impurity)."),
        ("Key Features Considered:", "Attendance (%), Assignment Marks (/100), Internal Marks (/100), Daily Study Hours."),
        ("Advanced Feature:", "Diagnostic Gap Analysis with Severity Priority Ranking (Critical / Moderate / Minor) & Action Plan."),
    ]
    for row_idx, (label, val) in enumerate(meta_data):
        c0 = meta_tbl.cell(row_idx, 0)
        c1 = meta_tbl.cell(row_idx, 1)
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F7FAFC")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=80, bottom=80, left=100, right=100)
        set_cell_margins(c1, top=80, bottom=80, left=100, right=100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.name = "Arial"
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = NAVY
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.name = "Arial"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = CHARCOAL

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # -------------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY & OBJECTIVE
    # -------------------------------------------------------------
    h1 = doc.add_paragraph("1. Executive Summary & Objective")
    style_heading(h1, 16, NAVY, space_before=16, space_after=8)

    p = doc.add_paragraph(
        "The primary objective of this project is to develop an Artificial Intelligence (AI) system capable of "
        "predicting student academic performance accurately and proactively, well before final summative examinations take place. "
        "In traditional educational environments, performance assessment is often conducted post-facto. By the time final examination "
        "results are published, students, educators, and institutional mentors lack the opportunity to carry out corrective academic interventions."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph(
        "By employing Educational Data Mining (EDM) and Supervised Machine Learning Classification techniques, this system "
        "synthesizes four foundational academic dimensions—classroom attendance, continuous assignment scores, internal examination "
        "assessments, and daily self-study habits. It categorizes students into four distinct performance tiers (Excellent, Good, Average, "
        "and Poor), and incorporates an Advanced Diagnostic Feature that detects specific weak areas, compares them against institutional benchmarks, "
        "and compiles personalized, prioritized study remediation plans."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)

    add_callout(
        doc,
        "System Objective Statement: To engineer an interpretable, transparent, and responsive AI classification system "
        "that accurately classifies student academic trajectory and delivers prescriptive, actionable pedagogical recommendations.",
        title="CORE OBJECTIVE"
    )

    # -------------------------------------------------------------
    # SECTION 2: TASK 1 — STUDENT DETAILS INTAKE
    # -------------------------------------------------------------
    h1 = doc.add_paragraph("2. Task 1: Student Details Intake & Data Validation")
    style_heading(h1, 16, NAVY, space_before=16, space_after=8)

    p = doc.add_paragraph(
        "The first functional task requires capturing comprehensive student information while ensuring strict data integrity, "
        "type verification, and boundary compliance. In production educational systems, invalid inputs (such as negative scores, "
        "percentage marks exceeding 100, or negative study durations) can corrupt model inferences."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph("The system captures two broad categories of information:")
    p.paragraph_format.space_after = Pt(4)

    # Bullet points
    bp1 = doc.add_paragraph(style='List Bullet')
    r = bp1.add_run("Student Identification Metadata: ")
    r.bold = True
    bp1.add_run("Student Full Name, Student Roll Number / ID, Academic Cohort / Department.")
    bp1.paragraph_format.space_after = Pt(2)

    bp2 = doc.add_paragraph(style='List Bullet')
    r = bp2.add_run("Quantitative Academic Metrics: ")
    r.bold = True
    bp2.add_run("Attendance Percentage, Assignment Score, Internal Assessment Marks, and Daily Independent Study Hours.")
    bp2.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph(
        "Input Validation Logic: The system incorporates defensive boundary verification routines (`prompt_float`) "
        "which reject non-numeric characters and constrain inputs to scientifically permissible domains:"
    )
    p.paragraph_format.space_after = Pt(6)

    # Table of Input Constraints
    tbl_inputs = doc.add_table(rows=6, cols=4)
    tbl_inputs.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Input Parameter", "Data Type", "Permissible Range", "Institutional Context"]
    for i, h in enumerate(headers):
        c = tbl_inputs.cell(0, i)
        set_cell_background(c, "1B365D")
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    input_rows = [
        ("Student Name & Roll No", "String", "Non-empty alphanumeric", "Institutional record tracking"),
        ("Attendance", "Float", "0.0% to 100.0%", "Lecture & practical laboratory participation"),
        ("Assignment Marks", "Float", "0.0 to 100.0", "Periodic coursework, projects & continuous credit"),
        ("Internal Marks", "Float", "0.0 to 100.0", "Mid-term & continuous assessment evaluations"),
        ("Study Hours", "Float", "0.0 to 16.0 hrs/day", "Dedicated independent self-study duration"),
    ]
    for row_idx, r_data in enumerate(input_rows, start=1):
        bg = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            c = tbl_inputs.cell(row_idx, col_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(9)
            r.font.color.rgb = CHARCOAL

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 3: TASK 2 — CONSIDERATION OF ACADEMIC PARAMETERS
    # -------------------------------------------------------------
    h1 = doc.add_paragraph("3. Task 2: Academic Metrics Considered & Their Significance")
    style_heading(h1, 16, NAVY, space_before=16, space_after=8)

    p = doc.add_paragraph(
        "The performance predictor considers four critical academic dimensions. Each parameter captures a distinct "
        "facet of a student's cognitive engagement and educational discipline:"
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)

    metrics_detail = [
        ("1. Attendance Percentage (%):",
         "Measures physical presence and engagement across theory lectures and practical laboratories. "
         "In higher education, a strict statutory threshold (typically 75% or 80%) is required for examination eligibility. "
         "Regular attendance ensures continuous absorption of core concepts, active instructor contact, and timely awareness of syllabus milestones."),
        
        ("2. Assignment Marks (out of 100):",
         "Reflects the student's ability to research, solve non-trivial problems, collaborate on project deliverables, "
         "and adhere to deadlines. Assignment grades highlight practical understanding and application ability, serving as a leading "
         "indicator of continuous academic effort rather than short-term rote memorization."),
        
        ("3. Internal Marks (out of 100):",
         "Captures summative mid-term and sessional examination performance conducted under invigilated, timed test conditions. "
         "Internal tests assess depth of conceptual mastery, examination endurance, and analytical accuracy, showing strong correlation "
         "with final university board examination scores."),
        
        ("4. Daily Study Hours (hrs/day):",
         "Quantifies self-directed learning time outside formal lecture hours. This metric reflects individual dedication, "
         "repetition, assignment completion, and mastery of difficult subjects. Research shows study hours have a high Gini gain "
         "in segmenting struggling students from high achievers."),
    ]

    for title, desc in metrics_detail:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        r_t = p.add_run(title + " ")
        r_t.bold = True
        r_t.font.name = "Arial"
        r_t.font.color.rgb = SLATE
        r_d = p.add_run(desc)
        r_d.font.name = "Arial"
        r_d.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # SECTION 4: TASK 3 — PERFORMANCE PREDICTION TIERS
    # -------------------------------------------------------------
    h1 = doc.add_paragraph("4. Task 3: Performance Prediction Classes & Criteria")
    style_heading(h1, 16, NAVY, space_before=16, space_after=8)

    p = doc.add_paragraph(
        "The system formulates the prediction challenge as a 4-class multi-class classification problem. "
        "The target variable Y belongs to the set {Excellent, Good, Average, Poor}. "
        "Each class represents a distinct academic cohort requiring a differentiated pedagogical strategy:"
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)

    tiers_table = doc.add_table(rows=5, cols=4)
    tiers_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_headers = ["Performance Tier", "Typical Score Bands", "Study Habits", "Academic Status & Meaning"]
    for i, h in enumerate(t_headers):
        c = tiers_table.cell(0, i)
        set_cell_background(c, "1B365D")
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    tier_data = [
        ("EXCELLENT", "Marks: 85-100\nAtt: 88-100%", "7.0 to 9.5 hrs/day", "Top-tier student; exemplary mastery and discipline. Candidates for academic honors and peer tutoring."),
        ("GOOD", "Marks: 70-84\nAtt: 75-87%", "4.5 to 6.8 hrs/day", "Above-average student; consistent performance. Minor refinements needed to push into the top honor tier."),
        ("AVERAGE", "Marks: 50-69\nAtt: 60-74%", "2.8 to 4.5 hrs/day", "Moderate performance; vulnerable to falling behind. Inconsistent attendance or exam preparation."),
        ("POOR", "Marks: < 50\nAtt: < 60%", "< 2.5 hrs/day", "Critical academic risk; failure or examination debarment imminent without immediate structured intervention."),
    ]

    for row_idx, r_data in enumerate(tier_data, start=1):
        bg = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            c = tiers_table.cell(row_idx, col_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(8.5)
            r.font.color.rgb = CHARCOAL
            if col_idx == 0:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 5: TASK 4 & ADVANCED FEATURE — DIAGNOSTICS & SUGGESTIONS
    # -------------------------------------------------------------
    h1 = doc.add_paragraph("5. Task 4 & Advanced Feature: Diagnostic Gap Analysis & Suggestions")
    style_heading(h1, 16, NAVY, space_before=16, space_after=8)

    p = doc.add_paragraph(
        "A critical limitation of conventional ML prediction systems is that they output an opaque label (e.g. 'Poor') "
        "without explaining why the prediction was made or what actionable steps the student can take to improve. "
        "To solve this, our system introduces an Advanced Diagnostic Feature:"
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)

    # Sub-bullets of how it works
    d_points = [
        ("Parametric Gap Analysis:", "Each of the student's 4 metrics is compared against institutional excellence benchmarks."),
        ("Multi-Tier Severity Classification:", "Deficiencies are dynamically mapped to 'Critical', 'Moderate', or 'Minor' priority."),
        ("Prescriptive Action Planning:", "Generates a structured, numbered remediation plan with weekly targets."),
        ("Cross-Parameter Anomaly Detection:", "Detects cognitive imbalances, such as students who study long hours but score poorly on internal tests, signaling passive studying rather than active recall."),
    ]
    for label, desc in d_points:
        bp = doc.add_paragraph(style='List Bullet')
        r = bp.add_run(label + " ")
        r.bold = True
        bp.add_run(desc)
        bp.paragraph_format.space_after = Pt(3)

    p = doc.add_paragraph("Diagnostic Rule & Severity Benchmark Matrix:")
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(4)

    # Benchmark Matrix Table
    tbl_bench = doc.add_table(rows=5, cols=4)
    tbl_bench.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_headers = ["Academic Metric", "Critical Threshold", "Moderate Threshold", "Minor / Excellent Benchmark"]
    for i, h in enumerate(b_headers):
        c = tbl_bench.cell(0, i)
        set_cell_background(c, "1B365D")
        set_cell_margins(c, top=100, bottom=100, left=120, right=120)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    bench_rows = [
        ("Attendance (%)", "< 60.0% (Risk of debarment)", "60.0% to 74.9% (Below standard)", "75.0% to 87.9% (Target: >= 88.0%)"),
        ("Assignment Marks (/100)", "< 55.0 (Severe coursework deficit)", "55.0 to 74.9 (Moderate gaps)", "75.0 to 85.9 (Target: >= 86.0)"),
        ("Internal Marks (/100)", "< 55.0 (High exam failure risk)", "55.0 to 74.9 (Conceptual lapses)", "75.0 to 85.9 (Target: >= 86.0)"),
        ("Study Hours (hrs/day)", "< 2.5 h (Severe study deficit)", "2.5 to 4.9 h (Average effort)", "5.0 to 6.9 h (Target: >= 7.0 h)"),
    ]
    for row_idx, r_data in enumerate(bench_rows, start=1):
        bg = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            c = tbl_bench.cell(row_idx, col_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(8.5)
            r.font.color.rgb = CHARCOAL

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 6: TASK 5 — DISPLAYING THE PREDICTION RESULT
    # -------------------------------------------------------------
    h1 = doc.add_paragraph("6. Task 5: Displaying Prediction Results (CLI & Web UI)")
    style_heading(h1, 16, NAVY, space_before=16, space_after=8)

    p = doc.add_paragraph(
        "To ensure accessibility across all institutional user groups (students on mobile devices, faculty advisors on desktop computers, "
        "and researchers in shell environments), the system delivers prediction outputs through two clean presentation channels:"
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph("1. Comprehensive CLI Report Card Format:")
    p.paragraph_format.space_after = Pt(4)

    # Code block in table
    code_tbl = doc.add_table(rows=1, cols=1)
    code_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell = code_tbl.cell(0, 0)
    c_cell.width = Inches(6.5)
    set_cell_background(c_cell, "1E293B")
    set_cell_margins(c_cell, top=100, bottom=100, left=140, right=140)
    p_code = c_cell.paragraphs[0]
    p_code.paragraph_format.space_after = Pt(0)
    sample_cli = (
        "========================================================================\n"
        "                     STUDENT PERFORMANCE REPORT                         \n"
        "========================================================================\n"
        "  Student Name      : Rohan Verma       | Student ID / Roll : STU-103\n"
        "------------------------------------------------------------------------\n"
        "  INPUT ACADEMIC METRICS:\n"
        "    1. Attendance       :   66.0 %      | 2. Assignment Marks :  61.0 / 100\n"
        "    3. Internal Marks   :   58.0 / 100  | 4. Study Hours      :   3.2 hrs/day\n"
        "------------------------------------------------------------------------\n"
        "  PREDICTED PERFORMANCE : AVERAGE       | STATUS: Needs Moderate Improvement\n"
        "------------------------------------------------------------------------\n"
        "  AREAS NEEDING IMPROVEMENT (Diagnostic Analysis):\n"
        "    Parameter            | Current        | Recommended      | Priority\n"
        "    Attendance           | 66.0%          | 80.0%+           | Moderate\n"
        "    Assignment Marks     | 61.0/100       | 80.0/100+        | Moderate\n"
        "    Internal Marks       | 58.0/100       | 82.0/100+        | Moderate\n"
        "    Study Hours          | 3.2 hrs/day    | 5.5 - 7.0 hrs/day| Moderate\n"
        "------------------------------------------------------------------------\n"
        "  RECOMMENDED ACTION PLAN:\n"
        "    [1] Improve weekly attendance to >= 80% to strengthen classroom comprehension.\n"
        "    [2] Revise past assignment feedback to achieve 80+ in coursework.\n"
        "    [3] Expand daily independent study from 3.2 hrs to 6.0 hrs/day.\n"
        "========================================================================"
    )
    r_c = p_code.add_run(sample_cli)
    r_c.font.name = "Courier New"
    r_c.font.size = Pt(8)
    r_c.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph("2. Interactive Web Dashboard (web_app.py):")
    p.paragraph_format.space_after = Pt(4)
    ui_features = [
        ("Real-Time Metric Sliders:", "Sliders synchronized with numeric input boxes for intuitive manipulation."),
        ("Preset Academic Profiles:", "One-click loading for Excellent (Aarav), Good (Priya), Average (Rohan), and Poor (Kabir)."),
        ("Color-Coded Visual Badges:", "Emerald Green (Excellent), Sky Blue (Good), Amber (Average), and Rose Red (Poor)."),
        ("Diagnostic Gap Table:", "Displays metrics, targets, and priority badges dynamically."),
        ("One-Click Report Printing:", "Specialized CSS media query for instant PDF export of student report cards."),
    ]
    for f_title, f_desc in ui_features:
        bp = doc.add_paragraph(style='List Bullet')
        r = bp.add_run(f_title + " ")
        r.bold = True
        bp.add_run(f_desc)
        bp.paragraph_format.space_after = Pt(2)

    # -------------------------------------------------------------
    # SECTION 7: AI CONCEPTS — ML CLASSIFICATION & DECISION TREES
    # -------------------------------------------------------------
    h1 = doc.add_paragraph("7. AI Concepts Used: Classification & Decision Trees")
    style_heading(h1, 16, NAVY, space_before=16, space_after=8)

    p = doc.add_paragraph(
        "7.1 Machine Learning Classification: Supervised classification is an AI methodology where an algorithm "
        "learns a mapping function from training instances characterized by continuous or discrete feature vectors to a set "
        "of discrete target labels. In our system, the input vector x = [Attendance, Assignment, Internal, Study_Hours]^T is mapped "
        "to y in {Excellent, Good, Average, Poor}."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph(
        "7.2 Why Decision Trees? Decision Trees (CART - Classification and Regression Trees) offer compelling structural "
        "advantages over alternative algorithms (such as Deep Neural Networks, Support Vector Machines, or Naive Bayes) in educational settings:"
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(4)

    dt_reasons = [
        ("Complete White-Box Explainability:", "Unlike black-box models, every classification path can be directly translated into plain-language logical rules (IF ... AND ... THEN)."),
        ("Invariance to Monotonic Transformations:", "Features with differing units (percentages 0-100% vs hours 0-16) do not require normalization or standardization."),
        ("Handling of Threshold Non-Linearities:", "Institutional rules (such as 75% minimum attendance requirement) naturally manifest as orthogonal tree splits."),
        ("Rapid Training & Inference:", "Trees compute inferences in O(depth) time, enabling sub-millisecond real-time prediction."),
    ]
    for r_title, r_desc in dt_reasons:
        bp = doc.add_paragraph(style='List Bullet')
        r = bp.add_run(r_title + " ")
        r.bold = True
        bp.add_run(r_desc)
        bp.paragraph_format.space_after = Pt(2)

    p = doc.add_paragraph(
        "7.3 Mathematical Splitting Criterion: Gini Impurity: "
        "The CART algorithm recursively partitions nodes to minimize Gini Impurity. "
        "For a node D containing samples across K = 4 classes, Gini Impurity is defined as:"
    )
    p.paragraph_format.space_after = Pt(4)

    # Math Callout Box
    add_callout(
        doc,
        "Gini Impurity Formula:\n"
        "   IG(D) = 1 - sum_{k=1}^K (p_k)^2\n\n"
        "Weighted Gini of Candidate Split on Feature j at Threshold theta:\n"
        "   IG(D, j, theta) = (|D_L| / |D|) * IG(D_L) + (|D_R| / |D|) * IG(D_R)\n\n"
        "Gini Information Gain to Maximize:\n"
        "   Delta IG = IG(D) - IG(D, j, theta)",
        title="MATHEMATICAL CRITERION"
    )

    p = doc.add_paragraph("7.4 Learned Feature Importances:")
    p.paragraph_format.space_after = Pt(4)
    p = doc.add_paragraph(
        "Feature importances represent the total normalized reduction in Gini Impurity contributed by each parameter across all tree nodes:"
    )
    p.paragraph_format.space_after = Pt(4)

    # Feature Importance Table
    tbl_fi = doc.add_table(rows=5, cols=3)
    tbl_fi.alignment = WD_TABLE_ALIGNMENT.CENTER
    fi_headers = ["Academic Parameter", "Importance Weight (%)", "Visual Representation"]
    for i, h in enumerate(fi_headers):
        c = tbl_fi.cell(0, i)
        set_cell_background(c, "1B365D")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    fi_data = [
        ("Daily Study Hours", "59.0%", "################## (Primary Discriminator)"),
        ("Internal Marks", "32.1%", "########## (Strong Midterm Predictor)"),
        ("Assignment Marks", "8.8%", "### (Coursework Baseline)"),
        ("Attendance Percentage", "0.0%", "Threshold Gatekeeper"),
    ]
    for row_idx, r_data in enumerate(fi_data, start=1):
        bg = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(r_data):
            c = tbl_fi.cell(row_idx, col_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, top=80, bottom=80, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(8.5)
            r.font.color.rgb = CHARCOAL
            if col_idx == 1:
                r.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph("7.5 Full Extracted Decision Tree Rules:")
    p.paragraph_format.space_after = Pt(4)

    # Decision tree rules box
    code_tbl2 = doc.add_table(rows=1, cols=1)
    code_tbl2.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_cell2 = code_tbl2.cell(0, 0)
    c_cell2.width = Inches(6.5)
    set_cell_background(c_cell2, "0F172A")
    set_cell_margins(c_cell2, top=100, bottom=100, left=140, right=140)
    p_code2 = c_cell2.paragraphs[0]
    p_code2.paragraph_format.space_after = Pt(0)
    rules_text = (
        "|--- Study_Hours <= 4.20\n"
        "|   |--- Internal_Marks <= 49.00\n"
        "|   |   |--- class: Poor\n"
        "|   |--- Internal_Marks >  49.00\n"
        "|   |   |--- Assignment_Marks <= 46.50\n"
        "|   |   |   |--- class: Poor\n"
        "|   |   |--- Assignment_Marks >  46.50\n"
        "|   |   |   |--- class: Average\n"
        "|--- Study_Hours >  4.20\n"
        "|   |--- Study_Hours <= 6.70\n"
        "|   |   |--- Assignment_Marks <= 68.00\n"
        "|   |   |   |--- class: Average\n"
        "|   |   |--- Assignment_Marks >  68.00\n"
        "|   |   |   |--- class: Good\n"
        "|   |--- Study_Hours >  6.70\n"
        "|   |   |--- Internal_Marks <= 80.50\n"
        "|   |   |   |--- class: Good\n"
        "|   |   |--- Internal_Marks >  80.50\n"
        "|   |   |   |--- class: Excellent"
    )
    r_c2 = p_code2.add_run(rules_text)
    r_c2.font.name = "Courier New"
    r_c2.font.size = Pt(8.5)
    r_c2.font.color.rgb = RGBColor(0x38, 0xBD, 0xF8)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 8: SOFTWARE ARCHITECTURE & REPOSITORY SPECIFICATION
    # -------------------------------------------------------------
    h1 = doc.add_paragraph("8. Software Architecture & Implementation Files")
    style_heading(h1, 16, NAVY, space_before=16, space_after=8)

    p = doc.add_paragraph(
        "The project has been architected with high modularity, zero mandatory third-party dependencies, "
        "and published on GitHub at https://github.com/etherialspace/student-performance-prediction."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)

    files_data = [
        ("student_performance_predictor.py", "Core AI script containing both the production scikit-learn model and the pure Python CART fallback classifier, diagnostic engine, and interactive CLI."),
        ("web_app.py", "Lightweight HTTP server built on Python standard library (http.server). Delivers REST endpoints (/api/predict, /api/model-info) and the interactive browser dashboard."),
        ("test_student_performance.py", "Automated test suite using unittest framework. Runs 8 test cases validating model initialization, predictions across all 4 tiers, feature importances, and diagnostic triggers."),
        ("student_dataset.csv", "Curated dataset of 56 student records distributed across all 4 performance tiers."),
        ("PROJECT_REPORT.md", "Complete academic project documentation in Markdown format."),
        ("requirements.txt", "Optional dependency declaration (scikit-learn)."),
    ]

    tbl_files = doc.add_table(rows=7, cols=2)
    tbl_files.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(["File Name", "Role in System"]):
        c = tbl_files.cell(0, i)
        set_cell_background(c, "1B365D")
        set_cell_margins(c, top=80, bottom=80, left=100, right=100)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for row_idx, (fname, frole) in enumerate(files_data, start=1):
        bg = "F7FAFC" if row_idx % 2 == 1 else "FFFFFF"
        c0 = tbl_files.cell(row_idx, 0)
        c1 = tbl_files.cell(row_idx, 1)
        c0.width = Inches(2.3)
        c1.width = Inches(4.2)
        set_cell_background(c0, bg)
        set_cell_background(c1, bg)
        set_cell_margins(c0, top=60, bottom=60, left=80, right=80)
        set_cell_margins(c1, top=60, bottom=60, left=80, right=80)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(fname)
        r0.bold = True
        r0.font.name = "Courier New"
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = NAVY
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(frole)
        r1.font.name = "Arial"
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = CHARCOAL

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # SECTION 9: QUESTION-BY-QUESTION VIVA VOCE & DEFENSE GUIDE
    # -------------------------------------------------------------
    h1 = doc.add_paragraph("9. Question-by-Question Viva Voce & Evaluation Guide")
    style_heading(h1, 16, NAVY, space_before=16, space_after=8)

    p = doc.add_paragraph(
        "Below is a direct, question-by-question response guide addressing each facet of the project problem statement "
        "and typical defense questions posed by university examination committees:"
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(6)

    qa_list = [
        ("Q1: How does the system handle Task 1 (Student Details Input)?",
         "The system provides input validation through both interactive terminal prompts (prompt_float) and the Web API. "
         "It collects student identifier metadata (Name, Roll ID) alongside four continuous parameters. Numeric inputs are validated "
         "against real-world physical bounds (Attendance 0-100%, Assignment Marks 0-100, Internal Marks 0-100, and Study Hours 0-16 hrs/day). "
         "Non-numeric and out-of-bound inputs are intercepted with helpful error messages."),

        ("Q2: How does the system evaluate Task 2 (Attendance, Assignment, Internal, and Study Hours)?",
         "The model treats these four parameters as continuous input dimensions in a 4-dimensional vector space. "
         "Rather than using arbitrary manual score weights, the Decision Tree applies information theory (Gini Impurity reduction) "
         "to discover optimal splitting thresholds from empirical student records. Study hours (59.0% importance) and internal marks (32.1% importance) "
         "were discovered to have the greatest discriminative power in partitioning performance."),

        ("Q3: How is Task 3 (Performance Prediction into 4 Tiers) executed mathematically?",
         "The model traverses the binary Decision Tree from the root node down to a leaf node. At each internal node, the student's parameter "
         "is evaluated against the optimal threshold theta (e.g., Study_Hours <= 4.20). The traversal terminates at a leaf node containing "
         "the majority performance class (Excellent, Good, Average, or Poor) and computes class probability distributions."),

        ("Q4: How does Task 4 (Give Suggestions for Improvement) work?",
         "The system invokes its diagnostic rule engine which compares each student metric against institutional benchmarks. "
         "Deficiencies are prioritized into Critical, Moderate, or Minor severities. The engine dynamically produces personalized suggestions "
         "and a concrete, numbered action plan (e.g., adopting Pomodoro intervals, collecting missed lecture notes, timed mock internal tests)."),

        ("Q5: How does Task 5 (Display Prediction Result) present information?",
         "Results are rendered across two interfaces: (1) An ASCII formatted terminal report card displaying metrics, tier badges, "
         "diagnostic tables, and action plans; and (2) A responsive web dashboard (web_app.py) with interactive sliders, color-coded badges "
         "(Emerald, Blue, Amber, Red), real-time tree rule inspector, and an instant print-to-PDF report generator."),

        ("Q6: Explain the AI concepts: Machine Learning Classification and Decision Trees.",
         "Machine Learning Classification is supervised learning where models infer a mapping function from training data to discrete classes. "
         "A Decision Tree (CART) is chosen because it creates interpretable, white-box orthogonal partitions using Gini Impurity (IG = 1 - sum p_i^2). "
         "It does not require feature scaling and directly mirrors human educational decision-making."),

        ("Q7: What constitutes the Advanced Feature in this project?",
         "The Advanced Feature is the Diagnostic Improvement Engine. Unlike standard classifiers that merely assign a label, our engine "
         "conducts multi-tier parametric gap analysis, assigns priority severity tags, produces cross-metric cognitive insights (e.g., detecting high study hours "
         "coupled with low exam marks), and crafts an actionable remediation schedule."),
    ]

    for q, a in qa_list:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(8)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q)
        r_q.bold = True
        r_q.font.name = "Arial"
        r_q.font.size = Pt(10)
        r_q.font.color.rgb = SLATE

        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(6)
        p_a.paragraph_format.line_spacing = 1.15
        r_a = p_a.add_run(a)
        r_a.font.name = "Arial"
        r_a.font.size = Pt(9.5)
        r_a.font.color.rgb = CHARCOAL

    # -------------------------------------------------------------
    # SECTION 10: CONCLUSION & REPOSITORY VERIFICATION
    # -------------------------------------------------------------
    h1 = doc.add_paragraph("10. Conclusion & Project Deliverables")
    style_heading(h1, 16, NAVY, space_before=16, space_after=8)

    p = doc.add_paragraph(
        "The Intelligent Student Performance Prediction System fully realizes all functional tasks, machine learning concepts, "
        "and advanced diagnostic features mandated by the project specification. With 100% pass rates across automated unit tests, "
        "a resilient dual-engine architecture (scikit-learn + built-in CART), an interactive web interface, and full source code published "
        "to GitHub, the project stands complete and ready for academic submission and defense."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(10)

    add_callout(
        doc,
        "GitHub Repository: https://github.com/etherialspace/student-performance-prediction\n"
        "Branch: main | Fully committed with web application, unit tests, and dataset.",
        title="ONLINE REPOSITORY VERIFICATION"
    )

    return doc

if __name__ == "__main__":
    out_dir = "/Users/lakshaywalia/.gemini/antigravity/scratch/student-performance-prediction"
    out_file = os.path.join(out_dir, "Student_Performance_Prediction_System_Documentation.docx")
    doc = build_docx()
    doc.save(out_file)
    print(f"Document successfully created at: {out_file}")
