#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
🌌 Obsidian-Style Interactive Knowledge Graph Generator
===============================================================================
행복 컨테이너 DB(happiness_knowledge.db)의 모든 노드와 엣지를 
옵시디언(Obsidian) 그래프 뷰와 동일한 암전 다크 모드, 물리 포스 렌더링, 
클릭 시 측면 노드 상세 패널이 뜨는 HTML 지식 그래프로 생성합니다.
"""

import os
import sys
import sqlite3
import json
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

DB_PATH = r"c:\Users\USER\Desktop\luca연구에이전트\행복\happiness_knowledge.db"
OUTPUT_HTML = r"c:\Users\USER\Desktop\luca연구에이전트\행복\행복_옵시디언_지식그래프.html"

def generate_obsidian_graph():
    if not os.path.exists(DB_PATH):
        print(f"Error: DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    nodes = []
    edges = []

    # 1. Master Hub Node
    nodes.append({
        "id": "hub-master",
        "label": "🧠 서은국 교수의 《행복의 기원》",
        "group": "master",
        "type": "Master Hub Node",
        "color": "#a855f7",
        "size": 35,
        "details": "연세대 심리학과 서은국 교수의 진화심리학·뇌과학 기반 행복론 통합 지식 허브 노드"
    })

    # 2. Concepts
    cur.execute("SELECT id, concept_name, category, description, key_insight FROM concepts")
    for r in cur.fetchall():
        nid = f"concept-{r[0]}"
        label = f"💡 {r[1]}"
        details = f"<b>분류:</b> {r[2]}<br><b>설명:</b> {r[3]}<br><b>핵심 통찰:</b> {r[4]}"
        nodes.append({
            "id": nid,
            "label": label,
            "group": "concept",
            "type": "개념 온톨로지",
            "color": "#06b6d4",
            "size": 22,
            "details": details
        })
        edges.append({"from": "hub-master", "to": nid, "label": "개념 결합"})

    # 3. Formulas
    cur.execute("SELECT id, formula_name, latex_expression, implication FROM formulas")
    for r in cur.fetchall():
        nid = f"formula-{r[0]}"
        label = f"📐 {r[0]}"
        details = f"<b>수식:</b> <code>{r[1]}</code><br><b>의미:</b> {r[2]}"
        nodes.append({
            "id": nid,
            "label": label,
            "group": "formula",
            "type": "수리 방정식",
            "color": "#3b82f6",
            "size": 26,
            "details": details
        })
        edges.append({"from": "hub-master", "to": nid, "label": "수리 모델링"})

    # 4. NotebookLM Insights
    try:
        cur.execute("SELECT id, topic, insight_content, citation_source FROM notebooklm_insights")
        for r in cur.fetchall():
            nid = f"rag-{r[0]}"
            label = f"🧪 {r[1]}"
            details = f"<b>주제:</b> {r[1]}<br><b>인사이트:</b> {r[2]}<br><b>출처:</b> {r[3]}"
            nodes.append({
                "id": nid,
                "label": label,
                "group": "rag",
                "type": "NotebookLM RAG",
                "color": "#10b981",
                "size": 20,
                "details": details
            })
            edges.append({"from": "hub-master", "to": nid, "label": "딥리서치 RAG"})
    except Exception:
        pass

    # 5. Sources
    cur.execute("SELECT id, source_type, title, url_or_path FROM sources")
    for r in cur.fetchall():
        nid = f"source-{r[0]}"
        label = f"🌐 [{r[1]}] {r[2][:15]}"
        details = f"<b>종류:</b> {r[1]}<br><b>제목:</b> {r[2]}<br><b>경로/URL:</b> {r[3]}"
        nodes.append({
            "id": nid,
            "label": label,
            "group": "source",
            "type": "원천 데이터 출처",
            "color": "#f43f5e",
            "size": 18,
            "details": details
        })
        edges.append({"from": "hub-master", "to": nid, "label": "원천 데이터"})

    conn.close()

    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)
    node_count = len(nodes)
    edge_count = len(edges)

    html_str = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>행복 지식 그래프 (Obsidian Style Graph View)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Noto+Sans+KR:wght@400;500;700&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>

    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            background-color: #111111;
            color: #dcddde;
            font-family: 'Noto Sans KR', 'Inter', sans-serif;
            height: 100vh;
            overflow: hidden;
            display: flex;
        }

        #graph-container {
            flex: 1;
            height: 100vh;
            position: relative;
            background: radial-gradient(circle at center, #1e1e24 0%, #0d0d11 100%);
        }

        #side-panel {
            width: 380px;
            background-color: #16161a;
            border-left: 1px solid #2b2b36;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
            box-shadow: -5px 0 25px rgba(0,0,0,0.5);
            overflow-y: auto;
        }

        .obsidian-title {
            font-size: 1.2rem;
            font-weight: 700;
            color: #a855f7;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            border-bottom: 1px solid #2b2b36;
            padding-bottom: 0.8rem;
        }

        .search-box {
            width: 100%;
            padding: 0.7rem 1rem;
            background-color: #24242e;
            border: 1px solid #3b3b4f;
            border-radius: 8px;
            color: #ffffff;
            font-size: 0.9rem;
            outline: none;
        }

        .search-box:focus { border-color: #a855f7; }

        .node-detail-card {
            background-color: #202029;
            border: 1px solid #323242;
            border-radius: 12px;
            padding: 1.2rem;
            font-size: 0.9rem;
            line-height: 1.6;
        }

        .node-type-tag {
            display: inline-block;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 0.8rem;
            text-transform: uppercase;
        }

        .stats-box {
            background: #1a1a22;
            border-radius: 8px;
            padding: 0.8rem;
            font-size: 0.82rem;
            color: #94a3b8;
        }

        .legend { display: flex; flex-wrap: wrap; gap: 0.5rem; font-size: 0.8rem; }
        .legend-item { display: flex; align-items: center; gap: 0.4rem; background: #22222d; padding: 0.3rem 0.6rem; border-radius: 6px; }
        .legend-dot { width: 10px; height: 10px; border-radius: 50%; }
    </style>
</head>
<body>

<div id="graph-container"></div>

<div id="side-panel">
    <div class="obsidian-title">
        <span>🔮 Obsidian Graph View</span>
    </div>

    <input type="text" id="search" class="search-box" placeholder="노드 및 키워드 검색...">

    <div class="legend">
        <div class="legend-item"><div class="legend-dot" style="background:#a855f7;"></div> 마스터 허브</div>
        <div class="legend-item"><div class="legend-dot" style="background:#06b6d4;"></div> 개념 온톨로지</div>
        <div class="legend-item"><div class="legend-dot" style="background:#3b82f6;"></div> 수리 방정식</div>
        <div class="legend-item"><div class="legend-dot" style="background:#10b981;"></div> NotebookLM RAG</div>
        <div class="legend-item"><div class="legend-dot" style="background:#f43f5e;"></div> 원천 출처</div>
    </div>

    <div class="stats-box">
        📊 총 노드: <strong>__NODE_COUNT__개</strong> | 연결 엣지: <strong>__EDGE_COUNT__개</strong><br>
        💾 DB 위치: <code>happiness_knowledge.db</code>
    </div>

    <div id="node-info" class="node-detail-card">
        <span class="node-type-tag" style="background: rgba(168,85,247,0.2); color: #a855f7;">GUIDE</span>
        <h3 style="color: #ffffff; margin-bottom: 0.5rem;">노드를 클릭하세요</h3>
        <p style="color: #94a3b8;">그래프 상의 노드를 선택하면 해당 데이터베이스의 상세 팩트와 수리적 인과관계가 이곳에 표시됩니다.</p>
    </div>
</div>

<script>
    const rawNodes = __NODES_JSON__;
    const rawEdges = __EDGES_JSON__;

    const nodesData = new vis.DataSet(rawNodes.map(n => ({
        id: n.id,
        label: n.label,
        color: { background: n.color, border: '#ffffff', highlight: { background: '#ffffff', border: n.color } },
        shape: 'dot',
        size: n.size,
        font: { color: '#dcddde', size: 13, face: 'Noto Sans KR' },
        details: n.details,
        type: n.type
    })));

    const edgesData = new vis.DataSet(rawEdges.map(e => ({
        from: e.from,
        to: e.to,
        label: e.label,
        color: { color: 'rgba(255,255,255,0.15)', highlight: '#a855f7' },
        font: { color: '#64748b', size: 10 },
        arrows: { to: { enabled: true, scaleFactor: 0.6 } }
    })));

    const container = document.getElementById('graph-container');
    const data = { nodes: nodesData, edges: edgesData };
    const options = {
        physics: {
            solver: 'forceAtlas2Based',
            forceAtlas2Based: {
                gravitationalConstant: -50,
                centralGravity: 0.01,
                springLength: 100,
                springConstant: 0.08
            },
            maxVelocity: 50,
            timestep: 0.5,
            stabilization: { iterations: 150 }
        },
        interaction: {
            hover: true,
            tooltipDelay: 200,
            zoomView: true
        }
    };

    const network = new vis.Network(container, data, options);

    network.on("click", function (params) {
        if (params.nodes.length > 0) {
            const nodeId = params.nodes[0];
            const node = nodesData.get(nodeId);
            document.getElementById('node-info').innerHTML = `
                <span class="node-type-tag" style="background: rgba(168,85,247,0.2); color: #a855f7;">${node.type}</span>
                <h3 style="color: #ffffff; margin-bottom: 0.8rem;">${node.label}</h3>
                <div>${node.details}</div>
            `;
        }
    });

    document.getElementById('search').addEventListener('input', function(e) {
        const val = e.target.value.toLowerCase();
        if (!val) {
            nodesData.forEach(n => nodesData.update({ id: n.id, hidden: false }));
            return;
        }
        nodesData.forEach(n => {
            const match = n.label.toLowerCase().includes(val) || (n.details && n.details.toLowerCase().includes(val));
            nodesData.update({ id: n.id, hidden: !match });
        });
    });
</script>
</body>
</html>
"""

    html_str = html_str.replace("__NODES_JSON__", nodes_json)\
                       .replace("__EDGES_JSON__", edges_json)\
                       .replace("__NODE_COUNT__", str(node_count))\
                       .replace("__EDGE_COUNT__", str(edge_count))

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_str)

    print(f"Successfully generated Obsidian-style Knowledge Graph HTML: {OUTPUT_HTML}")

if __name__ == "__main__":
    generate_obsidian_graph()
