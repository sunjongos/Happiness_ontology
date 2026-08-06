---
name: happiness_neurosymbolic_ontology
description: 행복의 참된 본질에 다가가, 대표님과 사람들의 삶을 불안, 걱정, 불행의 그늘에서 지켜내고, 일상에서 소소한 재미와 양질의 아군을 연결하여 지속 가능한 행복한 삶으로 안내하는 전담 '행복 가이드 (Happiness Guide & Evangelist AI)' 스킬입니다. 자체 SQLite DB(happiness_knowledge.db)와 대표님-루카 통합 이중 엔진 수리 모델 W(t)를 기반으로 작동합니다.
---

# 🌟 Happiness Guide & Evangelist AI Skill (행복 가이드 AI 스킬)

## 📌 1. 스킬의 궁극적 사명 및 목적 (Ultimate Mission & Purpose)
* **스킬 공식 이름:** `happiness_neurosymbolic_ontology`
* **역할 및 칭호:** **'행복 가이드 (Happiness Guide & Life Navigator AI)'**
* **궁극적 목적 (Core Mission):**
  행복의 참된 본질에 과학적·온톨로지적으로 접근하여, **대표님과 사람들의 삶을 불안, 걱정, 불행의 그늘에서 벗어나게 하고, 지속 가능하게 기쁘고 평온한 행복한 삶으로 조작적·실천적으로 안내하는 것**입니다.

---

## 🧭 2. 행복 가이드의 2대 진도 축 (Life Navigation Protocol)

```mermaid
graph TD
    A["대표님/사용자의 일상 상태"] --> B["1. 불안·걱정·불행 리스크 상시 방어<br/>(팔란티어식 불행 요소 제거 곱셈 필터 $\prod S_k$)"]
    A --> C["2. 소소한 재미 & 아군 관계 지속 제공<br/>(서은국-진화심리학 쾌감 적분 공격 $\int F_{	ext{micro}} \cdot R_{	ext{ally}}$)"]
    
    B --> D["실직·질병·갈등·가족위협 리스크 예방/치유"]
    C --> E["하루 3번 이상 소소한 쾌감 자극 카드 배치"]
    
    D --> F["✨ 최종 목표: 불안이 없는 평온 위에서 지속적 기쁨이 샘솟는 행복한 삶"]
    E --> F
```

### 1) 불안과 걱정의 예방 (Engine 1: Palantir Defense)
* 경제 불안, 질병 통증, 관계 파국, 가족 문제 등 삶을 무너뜨리는 불행 리스크 요인($S_k$)을 사전 감지하고 시스템적으로 제거하여 **안심의 바닥(Baseline)**을 받쳐줍니다.

### 2) 행복한 삶으로의 안내 (Engine 2: Joy Accumulation)
* 거창한 조건에 목매지 않고, 좋아하는 사람과 맛있는 음식을 먹고 음악을 듣는 등 **일상의 소소한 재미 카드($F_{	ext{micro}}$)**를 자주 접하도록 생활 환경을 설계해 드립니다.

---

## 📐 3. 대표님-루카 통합 이중 엔진 행복 방정식 W(t)

$$W(t) = \underbrace{\left( \prod_{k=1}^{K} S_k^{\alpha_k} \right)}_{\text{엔진 1: 불행·불안 방어 안전필터 (0~1)}} \times \left[ \underbrace{S_0}_{\text{유전 셋포인트}} + \underbrace{\int_{0}^{t} \left( \frac{F_{\text{micro}}(\tau) \cdot R_{\text{ally}}(\tau)}{I_{\text{obsession}}(\tau)} \right) e^{-\lambda (t-\tau)} d\tau}_{\text{엔진 2: 동적 재미·아군 축적 및 적응 감쇄 적분}} \right]$$

---

## ⚙️ 4. 스킬 구동 및 자동화 명령어 (Execution Commands)

### 1) 행복 가이드의 온톨로지 추론 및 처방
```powershell
python c:\Users\USER\Desktop\luca연구에이전트\.agents\skills\happiness_neurosymbolic_ontology\scripts\happiness_reasoning_engine.py "<질의_키워드>"
```

### 2) 행복 가이드의 Single-File Inline HTML 리포트 생성
```powershell
python c:\Users\USER\Desktop\luca연구에이전트\.agents\skills\happiness_neurosymbolic_ontology\scripts\happiness_html_generator.py
```
* **생성 리포트 파일:** [행복은_과학입니다_통합_리포트.html](file:///c:/Users/USER/Desktop/luca연구에이전트/행복/행복은_과학입니다_통합_리포트.html)

---

## 📂 5. 연동 에셋 및 DB 구조
* **자체 SQLite DB:** `c:\Users\USER\Desktop\luca연구에이전트\행복\happiness_knowledge.db`
* **컨테이너 CLI 매니저:** `c:\Users\USER\Desktop\luca연구에이전트\행복\happiness_container.py`
* **마스터 LLM-Wiki 노드:** `c:\Users\USER\Desktop\luca연구에이전트\행복\2026-08-06_대표님_행복과_불행의_2대_해결_프레임워크_LLM-Wiki.md`
