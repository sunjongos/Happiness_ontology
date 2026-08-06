#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
🧠 Happiness Neurosymbolic Ontology Reasoning Engine
===============================================================================
행복 컨테이너 DB(happiness_knowledge.db)와 연동하여
사용자의 행복 관련 질문을 팩트 온톨로지(좌뇌)와 수리 방정식, 뇌과학/진화심리학
메커니즘으로 다차원 추론하여 심층 답변을 생성하는 모듈입니다.
"""

import sys
import os
import sqlite3
import json
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = r"c:\Users\USER\Desktop\luca연구에이전트\행복\happiness_knowledge.db"

def search_ontology(query):
    if not os.path.exists(DB_PATH):
        return {"error": f"Database not found at {DB_PATH}"}
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Split query into keywords
    keywords = query.split()
    
    matched_concepts = []
    matched_formulas = []
    matched_slides = []
    
    # Fetch all concepts and score them
    cur.execute("SELECT concept_name, category, description, key_insight FROM concepts")
    for r in cur.fetchall():
        score = sum(1 for kw in keywords if kw.lower() in (r[0] + r[2] + r[3]).lower())
        if score > 0 or len(keywords) == 0:
            matched_concepts.append({
                "concept_name": r[0],
                "category": r[1],
                "description": r[2],
                "key_insight": r[3],
                "score": score
            })
            
    # Fetch all formulas
    cur.execute("SELECT formula_name, latex_expression, variables_description, implication FROM formulas")
    for r in cur.fetchall():
        score = sum(1 for kw in keywords if kw.lower() in (r[0] + r[1] + r[2] + r[3]).lower())
        if score > 0 or len(keywords) == 0:
            matched_formulas.append({
                "formula_name": r[0],
                "latex": r[1],
                "variables": r[2],
                "implication": r[3],
                "score": score
            })
            
    # Fetch matching slides
    cur.execute("SELECT presentation_name, slide_number, title, content FROM slides")
    for r in cur.fetchall():
        score = sum(1 for kw in keywords if kw.lower() in (r[2] + r[3]).lower())
        if score > 0:
            matched_slides.append({
                "presentation": r[0],
                "slide_num": r[1],
                "title": r[2],
                "content_snippet": r[3][:150]
            })
            
    # Sort matches by score
    matched_concepts.sort(key=lambda x: x['score'], reverse=True)
    matched_formulas.sort(key=lambda x: x['score'], reverse=True)
    
    # If no specific matches, return all core concepts
    if not matched_concepts:
        cur.execute("SELECT concept_name, category, description, key_insight FROM concepts")
        matched_concepts = [{"concept_name": r[0], "category": r[1], "description": r[2], "key_insight": r[3]} for r in cur.fetchall()]
    if not matched_formulas:
        cur.execute("SELECT formula_name, latex_expression, variables_description, implication FROM formulas")
        matched_formulas = [{"formula_name": r[0], "latex": r[1], "variables": r[2], "implication": r[3]} for r in cur.fetchall()]
        
    conn.close()
    
    return {
        "query": query,
        "ontology_fact_graph": {
            "concepts": matched_concepts[:4],
            "formulas": matched_formulas[:2],
            "slides_count": len(matched_slides)
        }
    }

def format_reasoning_output(res):
    output = []
    output.append(f"### 🧠 [Neurosymbolic Ontology Reasoning Context: '{res['query']}']\n")
    
    output.append("#### 1. 좌뇌 팩트 온톨로지 노드 (Fact Ontology Nodes)")
    for c in res['ontology_fact_graph']['concepts']:
        output.append(f"* **[{c['category']}] {c['concept_name']}**")
        output.append(f"  - 메커니즘: {c['description']}")
        output.append(f"  - 핵심 통찰: {c['key_insight']}")
    output.append("")
    
    output.append("#### 2. 수리적 연관 방정식 (Mathematical Models)")
    for f in res['ontology_fact_graph']['formulas']:
        output.append(f"* **{f['formula_name']}**")
        output.append(f"  - 수식: `{f['latex']}`")
        output.append(f"  - 함의: {f['implication']}")
    output.append("")
    
    return "\n".join(output)

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "행복의 본질과 유전"
    res = search_ontology(q)
    print(format_reasoning_output(res))
