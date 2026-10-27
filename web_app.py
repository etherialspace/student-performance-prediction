#!/usr/bin/env python3
"""
Intelligent Student Performance Prediction System - Web Application
===================================================================
A standalone interactive web dashboard built with Python's built-in
HTTP server. Zero external web dependencies required!

Features:
- Real-time AI prediction using Machine Learning Decision Tree Classifier
- Academic parameter inputs: Attendance, Assignment Marks, Internal Marks, Study Hours
- Four performance tiers: Excellent, Good, Average, Poor
- Diagnostic Weak Areas Analysis (Advanced Feature)
- Personalized Improvement Suggestions & Step-by-Step Action Plan
- Visual Feature Importances and Decision Tree Rules
- One-click Preset Profiles & Printable Student Report Card
"""

import json
import os
import sys
from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

from student_performance_predictor import (
    StudentPerformanceSystem,
    FEATURE_NAMES,
    SKLEARN_AVAILABLE,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "student_dataset.csv")
system = StudentPerformanceSystem(csv_path=CSV_PATH)

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Intelligent Student Performance Prediction System (AI/ML)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: rgba(22, 30, 49, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --accent: #38bdf8;
      --excellent: #10b981;
      --good: #3b82f6;
      --average: #f59e0b;
      --poor: #ef4444;
      --radius: 16px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: radial-gradient(circle at 10% 10%, #1e1b4b 0%, #0b0f19 50%, #030712 100%);
      color: var(--text-main);
      min-height: 100vh;
      padding: 24px;
      line-height: 1.5;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    header {
      text-align: center;
      margin-bottom: 28px;
      padding: 16px 0;
    }

    .badge-header {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(99, 102, 241, 0.15);
      color: #a5b4fc;
      border: 1px solid rgba(99, 102, 241, 0.3);
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      margin-bottom: 12px;
    }

    h1 {
      font-size: 2.3rem;
      font-weight: 800;
      background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 8px;
    }

    .subtitle {
      color: var(--text-muted);
      font-size: 1.05rem;
      max-width: 680px;
      margin: 0 auto;
    }

    .meta-bar {
      margin-top: 14px;
      display: flex;
      justify-content: center;
      gap: 18px;
      font-size: 0.85rem;
      color: #cbd5e1;
      flex-wrap: wrap;
    }

    .meta-pill {
      background: rgba(255, 255, 255, 0.05);
      padding: 4px 12px;
      border-radius: 8px;
      border: 1px solid var(--card-border);
    }

    .grid-layout {
      display: grid;
      grid-template-columns: 1.05fr 1.35fr;
      gap: 24px;
      margin-bottom: 30px;
    }

    @media (max-width: 900px) {
      .grid-layout {
        grid-template-columns: 1fr;
      }
    }

    .card {
      background: var(--card-bg);
      backdrop-filter: blur(16px);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 24px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
      position: relative;
    }

    .card-title {
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }

    .preset-bar {
      margin-bottom: 20px;
    }

    .preset-label {
      font-size: 0.8rem;
      color: var(--text-muted);
      text-transform: uppercase;
      font-weight: 600;
      margin-bottom: 8px;
      letter-spacing: 0.5px;
    }

    .preset-buttons {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
    }

    @media (max-width: 600px) {
      .preset-buttons {
        grid-template-columns: repeat(2, 1fr);
      }
    }

    .preset-btn {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--card-border);
      color: #e2e8f0;
      padding: 8px 10px;
      border-radius: 10px;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      text-align: center;
    }

    .preset-btn:hover {
      background: rgba(99, 102, 241, 0.25);
      border-color: rgba(99, 102, 241, 0.5);
      transform: translateY(-1px);
    }

    .form-group {
      margin-bottom: 18px;
    }

    .row-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }

    label {
      display: block;
      font-size: 0.85rem;
      font-weight: 600;
      margin-bottom: 6px;
      color: #e2e8f0;
    }

    .input-text {
      width: 100%;
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 10px 14px;
      color: #fff;
      font-size: 0.95rem;
      transition: border 0.2s;
    }

    .input-text:focus {
      outline: none;
      border-color: var(--primary);
    }

    .slider-container {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    input[type=range] {
      flex: 1;
      accent-color: var(--primary);
      height: 6px;
      border-radius: 4px;
      cursor: pointer;
    }

    .slider-val-box {
      width: 72px;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 6px 8px;
      text-align: center;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
      font-size: 0.9rem;
      color: #38bdf8;
    }

    .btn-predict {
      width: 100%;
      background: linear-gradient(135deg, #6366f1, #4f46e5);
      color: white;
      border: none;
      border-radius: 12px;
      padding: 13px 20px;
      font-size: 1rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4);
      transition: all 0.2s;
      margin-top: 8px;
    }

    .btn-predict:hover {
      background: linear-gradient(135deg, #4f46e5, #4338ca);
      transform: translateY(-1px);
    }

    /* Result Panel */
    .prediction-card {
      border-radius: 14px;
      padding: 20px;
      margin-bottom: 20px;
      text-align: center;
      transition: all 0.3s;
      position: relative;
      overflow: hidden;
    }

    .tier-excellent {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.2), rgba(5, 150, 105, 0.08));
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .tier-good {
      background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(37, 99, 235, 0.08));
      border: 1px solid rgba(59, 130, 246, 0.4);
    }
    .tier-average {
      background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(217, 119, 6, 0.08));
      border: 1px solid rgba(245, 158, 11, 0.4);
    }
    .tier-poor {
      background: linear-gradient(135deg, rgba(239, 68, 68, 0.25), rgba(220, 38, 38, 0.08));
      border: 1px solid rgba(239, 68, 68, 0.45);
    }

    .student-badge-title {
      font-size: 0.85rem;
      text-transform: uppercase;
      letter-spacing: 1px;
      font-weight: 700;
      color: var(--text-muted);
      margin-bottom: 6px;
    }

    .tier-badge {
      font-size: 2.2rem;
      font-weight: 800;
      letter-spacing: 0.5px;
      margin-bottom: 4px;
    }

    .tier-summary {
      font-size: 0.95rem;
      color: #e2e8f0;
      font-weight: 500;
    }

    /* Weak Areas Diagnostic Table */
    .section-title {
      font-size: 1.05rem;
      font-weight: 700;
      margin: 18px 0 10px 0;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .diagnostic-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      margin-bottom: 16px;
      background: rgba(15, 23, 42, 0.5);
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--card-border);
    }

    .diagnostic-table th {
      background: rgba(255, 255, 255, 0.06);
      padding: 10px 12px;
      text-align: left;
      font-weight: 600;
      color: #94a3b8;
    }

    .diagnostic-table td {
      padding: 10px 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
    }

    .sev-critical {
      background: rgba(239, 68, 68, 0.2);
      color: #fca5a5;
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.75rem;
      display: inline-block;
    }
    .sev-moderate {
      background: rgba(245, 158, 11, 0.2);
      color: #fde68a;
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.75rem;
      display: inline-block;
    }
    .sev-minor {
      background: rgba(59, 130, 246, 0.2);
      color: #93c5fd;
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.75rem;
      display: inline-block;
    }

    .suggestion-item {
      background: rgba(255, 255, 255, 0.04);
      border-left: 3px solid var(--primary);
      padding: 10px 14px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 8px;
      font-size: 0.88rem;
      color: #e2e8f0;
    }

    .action-step {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.2);
      padding: 10px 14px;
      border-radius: 8px;
      margin-bottom: 8px;
      font-size: 0.88rem;
    }

    .step-num {
      background: #10b981;
      color: #042f2e;
      font-weight: 800;
      font-size: 0.75rem;
      width: 20px;
      height: 20px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      margin-top: 2px;
    }

    /* Decision Tree Rules / Code Box */
    .tree-box {
      background: #050811;
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 14px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.78rem;
      color: #38bdf8;
      overflow-x: auto;
      max-height: 240px;
      line-height: 1.4;
      white-space: pre;
    }

    .feat-bar-row {
      margin-bottom: 8px;
    }
    .feat-bar-label {
      display: flex;
      justify-content: space-between;
      font-size: 0.8rem;
      margin-bottom: 3px;
      color: #cbd5e1;
    }
    .feat-bar-bg {
      background: rgba(255, 255, 255, 0.08);
      height: 8px;
      border-radius: 4px;
      overflow: hidden;
    }
    .feat-bar-fill {
      height: 100%;
      background: linear-gradient(90deg, #6366f1, #38bdf8);
      border-radius: 4px;
      transition: width 0.4s ease;
    }

    .btn-action-row {
      display: flex;
      gap: 10px;
      margin-top: 14px;
    }

    .btn-secondary {
      background: rgba(255, 255, 255, 0.08);
      color: #fff;
      border: 1px solid var(--card-border);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      cursor: pointer;
      transition: 0.2s;
    }

    .btn-secondary:hover {
      background: rgba(255, 255, 255, 0.15);
    }

    @media print {
      body {
        background: white;
        color: black;
        padding: 0;
      }
      .preset-bar, .btn-predict, .btn-action-row, input[type=range] {
        display: none !important;
      }
      .card {
        border: 1px solid #ccc;
        box-shadow: none;
        background: white;
        color: black;
      }
      .input-text, .slider-val-box {
        border: 1px solid #bbb;
        color: black;
        background: white;
      }
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <div class="badge-header">⚡ Machine Learning Classifier (CART / scikit-learn)</div>
      <h1>Intelligent Student Performance Prediction System</h1>
      <p class="subtitle">Predicts academic performance across 4 tiers using a trained Decision Tree and diagnoses precise areas needing student improvement.</p>
      <div class="meta-bar">
        <div class="meta-pill">🧠 Algorithm: <strong>Decision Tree (Gini Impurity)</strong></div>
        <div class="meta-pill">📊 Training Records: <strong id="lbl-samples">56 students</strong></div>
        <div class="meta-pill">🎯 Validation Accuracy: <strong id="lbl-acc">85.7%</strong></div>
        <div class="meta-pill">⚙️ Engine: <strong id="lbl-engine">Active</strong></div>
      </div>
    </header>

    <div class="grid-layout">
      <!-- Input Panel -->
      <div class="card">
        <div class="card-title">
          <span>📝 Student Academic Profile</span>
        </div>

        <div class="preset-bar">
          <div class="preset-label">Quick Student Presets:</div>
          <div class="preset-buttons">
            <button class="preset-btn" onclick="applyPreset('excellent')">🌟 Aarav (Exc)</button>
            <button class="preset-btn" onclick="applyPreset('good')">📘 Priya (Good)</button>
            <button class="preset-btn" onclick="applyPreset('average')">📙 Rohan (Avg)</button>
            <button class="preset-btn" onclick="applyPreset('poor')">⚠️ Kabir (Poor)</button>
          </div>
        </div>

        <form id="prediction-form" onsubmit="event.preventDefault(); triggerPredict();">
          <div class="row-2">
            <div class="form-group">
              <label for="student_name">Student Name</label>
              <input type="text" id="student_name" class="input-text" value="Aarav Sharma" required>
            </div>
            <div class="form-group">
              <label for="student_id">Roll / Student ID</label>
              <input type="text" id="student_id" class="input-text" value="STU-101" required>
            </div>
          </div>

          <!-- Feature 1: Attendance -->
          <div class="form-group">
            <label for="attendance">1. Attendance Percentage (%)</label>
            <div class="slider-container">
              <input type="range" id="attendance" min="0" max="100" step="1" value="94" oninput="syncInput('attendance', 'attendance_val', '%')">
              <input type="text" id="attendance_val" class="slider-val-box" value="94 %" readonly>
            </div>
          </div>

          <!-- Feature 2: Assignment Marks -->
          <div class="form-group">
            <label for="assignment_marks">2. Assignment Marks (out of 100)</label>
            <div class="slider-container">
              <input type="range" id="assignment_marks" min="0" max="100" step="1" value="91" oninput="syncInput('assignment_marks', 'assignment_marks_val', '/100')">
              <input type="text" id="assignment_marks_val" class="slider-val-box" value="91 /100" readonly>
            </div>
          </div>

          <!-- Feature 3: Internal Marks -->
          <div class="form-group">
            <label for="internal_marks">3. Internal Exam Marks (out of 100)</label>
            <div class="slider-container">
              <input type="range" id="internal_marks" min="0" max="100" step="1" value="89" oninput="syncInput('internal_marks', 'internal_marks_val', '/100')">
              <input type="text" id="internal_marks_val" class="slider-val-box" value="89 /100" readonly>
            </div>
          </div>

          <!-- Feature 4: Study Hours -->
          <div class="form-group">
            <label for="study_hours">4. Daily Self-Study Hours (hrs/day)</label>
            <div class="slider-container">
              <input type="range" id="study_hours" min="0.5" max="14.0" step="0.5" value="7.5" oninput="syncInput('study_hours', 'study_hours_val', 'h')">
              <input type="text" id="study_hours_val" class="slider-val-box" value="7.5 h" readonly>
            </div>
          </div>

          <button type="submit" class="btn-predict">🔮 Predict Student Performance</button>
        </form>

        <div class="btn-action-row">
          <button class="btn-secondary" onclick="window.print()">🖨️ Print Student Report</button>
          <button class="btn-secondary" onclick="resetForm()">🔄 Reset Defaults</button>
        </div>
      </div>

      <!-- Output Panel -->
      <div class="card">
        <div class="card-title">
          <span>📊 AI Prediction & Diagnostic Report</span>
        </div>

        <div id="prediction-card" class="prediction-card tier-excellent">
          <div class="student-badge-title" id="report-student-meta">STU-101 • Aarav Sharma</div>
          <div class="tier-badge" id="report-class">EXCELLENT</div>
          <div class="tier-summary" id="report-summary">Top Tier Performance • Benchmark Exceeded</div>
        </div>

        <!-- Advanced Feature: Weak Areas Diagnostic -->
        <div class="section-title">
          <span>🔍 Areas Needing Improvement (Diagnostic Analysis)</span>
        </div>
        <div id="weak-areas-container">
          <table class="diagnostic-table">
            <thead>
              <tr>
                <th>Academic Metric</th>
                <th>Current Value</th>
                <th>Benchmark Target</th>
                <th>Priority</th>
              </tr>
            </thead>
            <tbody id="diagnostic-tbody">
              <!-- Injected dynamically -->
            </tbody>
          </table>
        </div>

        <!-- Personalized Suggestions -->
        <div class="section-title">
          <span>💡 Personalized Recommendations</span>
        </div>
        <div id="suggestions-list">
          <!-- Injected dynamically -->
        </div>

        <!-- Action Plan -->
        <div class="section-title">
          <span>📋 Step-by-Step Action Plan</span>
        </div>
        <div id="action-plan-list">
          <!-- Injected dynamically -->
        </div>
      </div>
    </div>

    <!-- Machine Learning Explainability Section -->
    <div class="card">
      <div class="card-title">
        <span>🤖 Machine Learning Explainability (Decision Tree Architecture)</span>
      </div>
      <div class="grid-layout" style="margin-bottom: 0;">
        <div>
          <div class="section-title">Feature Importances (Gini Gain Contribution)</div>
          <div id="feature-importance-bars">
            <!-- Injected dynamically -->
          </div>
        </div>
        <div>
          <div class="section-title">Trained Decision Tree Classification Rules</div>
          <pre class="tree-box" id="tree-rules-pre">Loading rules...</pre>
        </div>
      </div>
    </div>
  </div>

  <script>
    const PRESETS = {
      excellent: { name: "Aarav Sharma", id: "STU-101", att: 94, ass: 91, int: 89, std: 7.5 },
      good: { name: "Priya Nair", id: "STU-102", att: 81, ass: 78, int: 74, std: 5.0 },
      average: { name: "Rohan Verma", id: "STU-103", att: 66, ass: 61, int: 58, std: 3.2 },
      poor: { name: "Kabir Patel", id: "STU-104", att: 48, ass: 42, int: 39, std: 1.5 }
    };

    function syncInput(sliderId, boxId, unit) {
      const val = document.getElementById(sliderId).value;
      document.getElementById(boxId).value = val + " " + unit;
      triggerPredict();
    }

    function applyPreset(tier) {
      const p = PRESETS[tier];
      document.getElementById('student_name').value = p.name;
      document.getElementById('student_id').value = p.id;
      document.getElementById('attendance').value = p.att;
      document.getElementById('attendance_val').value = p.att + " %";
      document.getElementById('assignment_marks').value = p.ass;
      document.getElementById('assignment_marks_val').value = p.ass + " /100";
      document.getElementById('internal_marks').value = p.int;
      document.getElementById('internal_marks_val').value = p.int + " /100";
      document.getElementById('study_hours').value = p.std;
      document.getElementById('study_hours_val').value = p.std + " h";
      triggerPredict();
    }

    function resetForm() {
      applyPreset('excellent');
    }

    async function triggerPredict() {
      const payload = {
        student_name: document.getElementById('student_name').value || "Anonymous Student",
        student_id: document.getElementById('student_id').value || "N/A",
        attendance: parseFloat(document.getElementById('attendance').value),
        assignment_marks: parseFloat(document.getElementById('assignment_marks').value),
        internal_marks: parseFloat(document.getElementById('internal_marks').value),
        study_hours: parseFloat(document.getElementById('study_hours').value)
      };

      try {
        const resp = await fetch('/api/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await resp.json();
        renderResult(payload, data);
      } catch (err) {
        console.error('Prediction request failed:', err);
      }
    }

    function renderResult(student, res) {
      const pCard = document.getElementById('prediction-card');
      const pClass = res.predicted_class;
      const classMap = {
        'Excellent': { css: 'tier-excellent', color: '#10b981', summary: 'Top Tier Performance • Benchmark Exceeded' },
        'Good': { css: 'tier-good', color: '#3b82f6', summary: 'Above Average Performance • Consistent Academic Standard' },
        'Average': { css: 'tier-average', color: '#f59e0b', summary: 'Needs Moderate Improvement • Inconsistent Academic Standard' },
        'Poor': { css: 'tier-poor', color: '#ef4444', summary: 'Requires Immediate Academic Intervention • Below Passing Threshold' }
      };

      const info = classMap[pClass] || classMap['Average'];
      pCard.className = 'prediction-card ' + info.css;
      document.getElementById('report-student-meta').innerText = `${student.student_id} • ${student.student_name}`;
      document.getElementById('report-class').innerText = pClass.toUpperCase();
      document.getElementById('report-class').style.color = info.color;
      document.getElementById('report-summary').innerText = info.summary;

      // Diagnostic Weak Areas Table
      const tbody = document.getElementById('diagnostic-tbody');
      tbody.innerHTML = '';
      if (!res.weak_areas || res.weak_areas.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" style="text-align:center; color:#10b981; font-weight:600; padding:16px;">✨ None! All academic parameters meet or exceed top-tier benchmarks.</td></tr>`;
      } else {
        res.weak_areas.forEach(item => {
          const sevClass = item.severity === 'Critical' ? 'sev-critical' : (item.severity === 'Moderate' ? 'sev-moderate' : 'sev-minor');
          tbody.innerHTML += `
            <tr>
              <td><strong>${item.area}</strong></td>
              <td>${item.current}</td>
              <td style="color:#38bdf8;">${item.target}</td>
              <td><span class="${sevClass}">${item.severity.toUpperCase()}</span></td>
            </tr>
          `;
        });
      }

      // Suggestions List
      const sugList = document.getElementById('suggestions-list');
      sugList.innerHTML = '';
      (res.suggestions || []).forEach(s => {
        sugList.innerHTML += `<div class="suggestion-item">${s}</div>`;
      });

      // Action Plan
      const actList = document.getElementById('action-plan-list');
      actList.innerHTML = '';
      if (!res.action_plan || res.action_plan.length === 0) {
        actList.innerHTML = `<div class="action-step"><div class="step-num">✓</div><div>Continue current academic routine and maintain consistency.</div></div>`;
      } else {
        res.action_plan.forEach((step, idx) => {
          actList.innerHTML += `
            <div class="action-step">
              <div class="step-num">${idx + 1}</div>
              <div>${step}</div>
            </div>
          `;
        });
      }
    }

    async function loadModelMeta() {
      try {
        const resp = await fetch('/api/model-info');
        const data = await resp.json();
        document.getElementById('lbl-samples').innerText = data.sample_count + " students";
        document.getElementById('lbl-acc').innerText = (data.accuracy * 100).toFixed(1) + "%";
        document.getElementById('lbl-engine').innerText = data.engine;
        document.getElementById('tree-rules-pre').innerText = data.tree_rules;

        const fiContainer = document.getElementById('feature-importance-bars');
        fiContainer.innerHTML = '';
        for (const [feat, imp] of Object.entries(data.feature_importances)) {
          const pct = (imp * 100).toFixed(1);
          fiContainer.innerHTML += `
            <div class="feat-bar-row">
              <div class="feat-bar-label">
                <span>${feat}</span>
                <span style="font-family: 'JetBrains Mono', monospace;">${pct}%</span>
              </div>
              <div class="feat-bar-bg">
                <div class="feat-bar-fill" style="width: ${pct}%;"></div>
              </div>
            </div>
          `;
        }
      } catch (e) {
        console.error("Failed to load model info:", e);
      }
    }

    window.onload = function() {
      loadModelMeta();
      triggerPredict();
    };
  </script>
</body>
</html>
"""

class RequestHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Concise logging
        sys.stderr.write(f"[WebUI] {self.address_string()} - {format % args}\n")

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(HTML_PAGE.encode("utf-8"))))
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode("utf-8"))
        elif parsed.path == "/api/model-info":
            engine_str = "scikit-learn DecisionTreeClassifier" if SKLEARN_AVAILABLE else "CART DecisionTreeClassifier (Built-in)"
            data = {
                "engine": engine_str,
                "accuracy": system.accuracy,
                "sample_count": len(system.X),
                "feature_names": FEATURE_NAMES,
                "feature_importances": system.get_feature_importances(),
                "tree_rules": system.get_tree_rules(),
            }
            body = json.dumps(data).encode("utf-8")
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/predict":
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length).decode("utf-8")
            try:
                data = json.loads(raw_body)
                attendance = float(data.get("attendance", 0))
                assignment_marks = float(data.get("assignment_marks", 0))
                internal_marks = float(data.get("internal_marks", 0))
                study_hours = float(data.get("study_hours", 0))

                result = system.predict_student(
                    attendance=attendance,
                    assignment_marks=assignment_marks,
                    internal_marks=internal_marks,
                    study_hours=study_hours,
                )
                body = json.dumps(result).encode("utf-8")
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                err_body = json.dumps({"error": str(e)}).encode("utf-8")
                self.send_response(HTTPStatus.BAD_REQUEST)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(err_body)))
                self.end_headers()
                self.wfile.write(err_body)
        else:
            self.send_error(HTTPStatus.NOT_FOUND, "Not Found")


def run(port: int = 5050):
    server_address = ("127.0.0.1", port)
    try:
        httpd = HTTPServer(server_address, RequestHandler)
    except OSError:
        # Fallback to alternate port if 5050 is occupied
        port = 5051
        server_address = ("127.0.0.1", port)
        httpd = HTTPServer(server_address, RequestHandler)

    print("=" * 72)
    print("      INTELLIGENT STUDENT PERFORMANCE PREDICTION SYSTEM - WEB SERVER      ")
    print(f"      Dashboard running at: http://localhost:{port}")
    print("      Press Ctrl+C to stop.")
    print("=" * 72)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    port = 5050
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        port = int(sys.argv[1])
    run(port=port)
