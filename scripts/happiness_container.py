#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
📦 행복(Happiness) Neurosymbolic Container CLI & Local Database Manager
===============================================================================
연세대학교 심리학과 서은국 교수의 《행복의 기원》 진화심리학·뇌과학 연구,
NotebookLM MCP 딥리서치 인사이트, 수리 모델링($H = S + F/I \times R/C - A$) 
데이터베이스 통합 독립 컨테이너 모듈입니다.
"""

import sys
import os
import sqlite3
import json
import argparse
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

CONTAINER_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(CONTAINER_DIR, "happiness_knowledge.db")

def get_connection():
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: Database file not found at {DB_PATH}")
        sys.exit(1)
    return sqlite3.connect(DB_PATH)

def cmd_status():
    conn = get_connection()
    cur = conn.cursor()
    
    print("=" * 60)
    print("📦 [행복 Neurosymbolic & NotebookLM MCP Knowledge Container Status]")
    print(f"📍 Container Location: {CONTAINER_DIR}")
    print(f"💾 Database File: {DB_PATH} ({os.path.getsize(DB_PATH) / 1024:.1f} KB)")
    print("-" * 60)
    
    tables = ["slides", "concepts", "formulas", "llm_wiki_nodes", "sources",
              "notebooklm_notebooks", "notebooklm_insights", "notebooklm_sources"]
    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM {t}")
            cnt = cur.fetchone()[0]
            print(f"  • Table '{t}': {cnt} records")
        except Exception:
            pass
        
    print("\n📁 Container Files:")
    for f in os.listdir(CONTAINER_DIR):
        fpath = os.path.join(CONTAINER_DIR, f)
        size_kb = os.path.getsize(fpath) / 1024
        print(f"  - [{f}] ({size_kb:.1f} KB)")
    print("=" * 60)
    conn.close()

def cmd_query(keyword):
    conn = get_connection()
    cur = conn.cursor()
    print(f"\n🔍 Searching container database for: '{keyword}'\n")
    
    # 1. Search Concepts
    print("--- [Concepts] ---")
    cur.execute("SELECT concept_name, category, description, key_insight FROM concepts WHERE concept_name LIKE ? OR description LIKE ? OR key_insight LIKE ?",
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    rows = cur.fetchall()
    if rows:
        for r in rows:
            print(f"📌 [{r[1]}] {r[0]}\n   설명: {r[2]}\n   통찰: {r[3]}\n")
    else:
        print("  (No matching concepts)")

    # 2. Search Formulas
    print("--- [Formulas] ---")
    cur.execute("SELECT formula_name, latex_expression, implication FROM formulas WHERE formula_name LIKE ? OR latex_expression LIKE ? OR implication LIKE ?",
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    rows = cur.fetchall()
    if rows:
        for r in rows:
            print(f"📐 {r[0]}\n   공식: {r[1]}\n   의미: {r[2]}\n")
    else:
        print("  (No matching formulas)")

    # 3. Search NotebookLM Insights
    print("--- [NotebookLM MCP RAG Insights] ---")
    try:
        cur.execute("SELECT topic, insight_content, citation_source FROM notebooklm_insights WHERE topic LIKE ? OR insight_content LIKE ? OR keywords LIKE ?",
                    (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        rows = cur.fetchall()
        if rows:
            for r in rows:
                print(f"💡 [NotebookLM RAG] {r[0]}\n   인사이트: {r[1]}\n   출처: {r[2]}\n")
        else:
            print("  (No matching NotebookLM insights)")
    except Exception:
        print("  (NotebookLM insights table pending)")

    conn.close()

def cmd_notebooklm():
    conn = get_connection()
    cur = conn.cursor()
    print("\n📚 [NotebookLM MCP Notebooks & Deep Research Insights]\n")
    try:
        cur.execute("SELECT notebook_title, notebook_url, description FROM notebooklm_notebooks")
        for r in cur.fetchall():
            print(f"📓 노트북: {r[0]}")
            print(f"   URL: {r[1]}")
            print(f"   설명: {r[2]}\n")
            
        print("--- [NotebookLM Deep RAG Insights] ---")
        cur.execute("SELECT topic, insight_content, citation_source FROM notebooklm_insights")
        for r in cur.fetchall():
            print(f"💡 [{r[0]}]")
            print(f"   내용: {r[1]}")
            print(f"   출처: {r[2]}\n")
    except Exception as e:
        print("Error fetching NotebookLM data:", e)
    conn.close()

def cmd_formulas():
    conn = get_connection()
    cur = conn.cursor()
    print("\n📐 [행복 및 유전 수리 모델 전체 목록]\n")
    cur.execute("SELECT formula_name, latex_expression, variables_description, implication FROM formulas")
    for r in cur.fetchall():
        print(f"🔹 이름: {r[0]}")
        print(f"   수식: {r[1]}")
        print(f"   변수: {r[2]}")
        print(f"   의미: {r[3]}\n")
    conn.close()

def cmd_export_json():
    conn = get_connection()
    cur = conn.cursor()
    data = {}
    tables = ["slides", "concepts", "formulas", "llm_wiki_nodes", "sources",
              "notebooklm_notebooks", "notebooklm_insights", "notebooklm_sources"]
    for table in tables:
        try:
            cur.execute(f"SELECT * FROM {table}")
            cols = [description[0] for description in cur.description]
            data[table] = [dict(zip(cols, row)) for row in cur.fetchall()]
        except Exception:
            pass
    
    out_file = os.path.join(CONTAINER_DIR, "happiness_export.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ Exported full container database to JSON: {out_file}")
    conn.close()

def main():
    parser = argparse.ArgumentParser(description="행복 Neurosymbolic Knowledge Container CLI")
    parser.add_argument("--status", action="store_true", help="Check container status and table statistics")
    parser.add_argument("--query", type=str, help="Search database for a keyword")
    parser.add_argument("--formulas", action="store_true", help="Print all mathematical formulas")
    parser.add_argument("--notebooklm", action="store_true", help="Print NotebookLM MCP RAG insights")
    parser.add_argument("--export-json", action="store_true", help="Export container DB to JSON file")
    
    args = parser.parse_args()
    
    if args.status:
        cmd_status()
    elif args.query:
        cmd_query(args.query)
    elif args.formulas:
        cmd_formulas()
    elif args.notebooklm:
        cmd_notebooklm()
    elif args.export_json:
        cmd_export_json()
    else:
        cmd_status()

if __name__ == "__main__":
    main()
