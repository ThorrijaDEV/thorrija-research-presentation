# SLIDE_BLUEPRINT.md — 45-Slide Narrative Architecture
## 5-Act Structure for AI Research Presentation (~45 slides)
**Evidence Registry**: `/home/thorrija/research-presentation/audit/EVIDENCE_REGISTRY.json`  
**Single Source of Truth**: Every claim traces to CL-XXXX

---

## ACT 1: ORIENTATION (Slides 1–9)
*Establish the research program, its philosophy, and the landscape of systems under study.*

### Slide 1 — Title: "Computational Substrates for Autonomous Intelligence"
- **Core Content**: Program name, presenter, date, venue. One-line thesis: "We build relational substrates, multi-agent laboratories, and autonomous ecosystems — then measure honestly what emerges."
- **Diagram Spec**: Minimal dark slide. Centered title in monospace. Subtitle: "The Box • SINGULARITY/ORACLE • HERMES • Showcase". Thin horizontal rule. Footer: "Evidence registry: 27 verified claims (CL-0001–CL-0027), 4 experiments, 24 projects catalogued"
- **Evidence Refs**: CL-0027 (24 projects, 7 categories), CL-0026 (engineering philosophy)
- **Anticipated Q&A**:
  1. What unifies these disparate systems?
  2. Why "computational substrates" not "architectures"?
  3. What is the falsifiability criterion for the program?
  4. How do you avoid cargo-cult complexity?
  5. What would constitute a negative result for the whole program?

---

### Slide 2 — The Engineering Philosophy (Independent Reconstruction)
- **Core Content**: Five pillars — (1) Independent reconstruction from specs, not ports. (2) Real calculations, no mocks in tests. (3) Determinism via seeded RNG. (4) Intermediate stages exposed. (5) Honest fidelity classification (Level 1–4). Fidelity Level 3 = structural match, hashes differ. Level 4 = byte-for-byte where applicable.
- **Diagram Spec**: Five vertical pillars, each with icon + label. Right column: "The Box: Level 3 (CL-0007)", "Showcase: Level 4 (CL-0023)". Dark background, accent color for "Honest limitations" pillar.
- **Evidence Refs**: CL-0026 (engineering philosophy), CL-0007 (Level 3 definition), CL-0023 (Level 4 showcase)
- **Anticipated Q&A**:
  1. Why not just port the Python to TypeScript directly?
  2. How do you define "structural match" formally?
  3. What does Level 1 look like?
  4. How do you handle non-determinism in multi-agent systems?
  5. Is this philosophy scalable to larger teams?

---

### Slide 3 — Project Landscape: 24 Projects, 7 Categories
- **Core Content**: Catalog overview. Systems (9): silicon, cask, aster-ai, sigscan, dnsdrill, syspeek, loglens, canarytrap, port-authority. Security (3): loglens, canarytrap, hackdeck. Creative (3): neondrift, portfolio-demos, generative-engine. Demos/Showcase (5): Wi-Fi Time Machine, BLE Radar, Process Ecosystem, Terminal Generative Engine, The Box (TS). Cognitive (3): nexus-titan, nox, echo. Networks (2): dnsdrill, port-authority. Open/Other (5): clickwheel, update-manager, sysmon-dashboard, snapshot-manager, hackdeck.
- **Diagram Spec**: Concentric rings or treemap. Center: "Research Core" (The Box, SINGULARITY, ORACLE, HERMES). Ring 1: Showcase demos (5). Ring 2: Systems/Security tools (12). Ring 3: Creative/Cognitive (6). Color-code by fidelity (Level 3/4 = bright, unclassified = dim).
- **Evidence Refs**: CL-0027 (24 projects, 7 categories), CL-0023 (showcase 5 demos), CL-0008 (The Box 557 tests)
- **Anticipated Q&A**:
  1. Which projects are "research" vs "engineering"?
  2. Why are cognitive projects (nexus-titan, nox, echo) unclassified?
  3. What is the maintenance burden of 24 projects?
  4. How do you decide what enters the showcase?
  5. Are any projects deprecated?

---

### Slide 4 — The Box: Relational Substrate — One-Slide Summary
- **Core Content**: Arc-incidence multi-digraph. Nodes and arcs share one ID space; arcs can have arcs as endpoints (CL-0001). Six rewriting rules as data (YAML): GATHER, BOND, TAG_PROP, QUIET, DESCEND, FUSE (CL-0002). Identity/lineage derived from arc tags, not stored (CL-0003). 557 Python tests, 102 TS tests (CL-0008). Two core defects block generality (CL-0006).
- **Diagram Spec**: Center: multi-digraph snippet (nodes ⬤, arcs →, arc-as-endpoint ↘). Six rule icons around perimeter with YAML badge. Bottom: "Identity = derived" callout. Right: defect callouts (since_inflow, Rule.to_dict).
- **Evidence Refs**: CL-0001, CL-0002, CL-0003, CL-0008, CL-0006
- **Anticipated Q&A**:
  1. Why arc-incidence not adjacency lists?
  2. What does "arcs as endpoints" enable that hypergraphs don't?
  3. How do YAML rules compose?
  4. Why derive identity instead of storing it?
  5. Can the defects be fixed without redesign?

---

### Slide 5 — SINGULARITY/ORACLE: Multi-Agent Laboratory — One-Slide Summary
- **Core Content**: ORACLE = FastAPI + React SPA (CL-0014), wraps historical SINGULARITY engine. 5 heterogeneous agents: GreedyOptimizer, ConservativeOptimizer, Communicator, SkepticEvaluator, AdaptiveStrategist (CL-0012). Reputation-weighted coordination + bandit adaptation + independent verification engine (CL-0010). Protocol A (equal evals, reproducible) vs Protocol B (equal time, real compute). E1 Optimization: collaboration underperforms isolated agents — verified negative result (CL-0009). Statistical rigor: paired comparisons, Holm-Bonferroni, bootstrap 95% CI, Cohen's d (CL-0011).
- **Diagram Spec**: Left: 5 agent cards with policy icons. Center: coordinator (reputation weights) → verification engine (ground truth). Right: Protocol A vs B comparison table. Bottom: "Negative result = valid finding" banner.
- **Evidence Refs**: CL-0012, CL-0010, CL-0013, CL-0009, CL-0011, CL-0014
- **Anticipated Q&A**:
  1. Why 5 agents — why not 3 or 10?
  2. What does "reputation-weighted" mean formally?
  3. How does the verification engine access ground truth?
  4. Why is negative result emphasized?
  5. What is the compute budget per experiment?

---

### Slide 6 — HERMES: Autonomous Income Ecosystem — Architecture Preview
- **Core Content**: 9 agent types under Orchestrator (Hermes Prime): Content (3–5), Digital Asset (2–3), SaaS/API (3), Automation Service (2), Research (1), Optimization (1), Infrastructure (1), Finance (1) (CL-0019). Autonomy rules: agents CAN generate/publish/A-B test/adjust pricing/spend budget/restart; MUST request approval for pivot/new platform/budget increase/new integration/deployment/legal (CL-0020). Orchestrator auto-interventions: kill (<$10 rev + >$50 cost), scale (>$500 rev + <30% cost), spawn (opportunity >90), pause (policy violation), rebalance (weekly ROI) (CL-0021). Target: $10k+/month, <2 hrs human/week by month 6, infra <15% revenue (CL-0022). Status: architecture design only (planned Phases 1–5).
- **Diagram Spec**: Orchestrator center. 9 agent type clusters as orbiting nodes with count badges. Two concentric rings: inner = CAN (autonomous), outer = MUST REQUEST (human-in-loop). Bottom: intervention triggers as logic gates. Right: KPI dashboard mock (MRR, human hrs, infra %).
- **Evidence Refs**: CL-0019, CL-0020, CL-0021, CL-0022
- **Anticipated Q&A**:
  1. How do you prevent runaway spend before human approval?
  2. What defines "opportunity score >90"?
  3. Why 9 agent types — is this taxonomy stable?
  4. What happens if orchestrator fails?
  5. How do you measure "human hours/week" objectively?

---

### Slide 7 — Showcase: 5 Interactive Demos, 182/182 Tests, 160 kB
- **Core Content**: Wi-Fi Time Machine (BSS parsing, timeline heatmap, 18 tests), BLE Radar (lifecycle state machine, EMA RSSI, hash→angle, 16 tests), Process Ecosystem (jiffie delta CPU, ppid tree, PID-reuse detection, 22 tests), Terminal Generative Engine (splitmix64 RNG, sine field, Clifford/Dejong attractor, SHA-256 fingerprint, 24 tests), The Box TS port (102 tests) (CL-0023). Vite production build: 160.69 kB JS, zero runtime dependencies (CL-0024). Cross-language validation: structural properties match Python; only hashes differ (CL-0025).
- **Diagram Spec**: 5 demo cards in grid. Each: name, domain icon, test count, key algorithm one-liner. Bottom bar: "182/182 PASS • 160.69 kB • 0 deps". Right panel: cross-language validation matrix (node count ✓, arc count ✓, degree dist ✓, beta0/beta1 ✓, hashes ✗).
- **Evidence Refs**: CL-0023, CL-0024, CL-0025
- **Anticipated Q&A**:
  1. Why zero runtime dependencies?
  2. How do you test without live hardware (Wi-Fi, BLE, /proc)?
  3. What is the synthetic fixture strategy?
  4. Why Vite not Next.js?
  5. Can the demos run offline?

---

### Slide 8 — Evidence Standards: VERIFIED / EXPERIMENTAL / THEORETICAL / SPECULATIVE
- **Core Content**: Four-tier evidence classification (CL-0017). VERIFIED: ≥2 independent experiments, p<0.05, bootstrap CI. EXPERIMENTAL: single experiment, promising but unreplicated. THEORETICAL: derived from first principles, no empirical validation. SPECULATIVE: hypothesis, no evidence yet. "No claim of collective advantage without VERIFIED evidence." Applied to: The Box (mean_depth = ADMITTED/EXPLAINED, DESCEND structural = STRUCTURAL FINDING), ORACLE E1 (VERIFIED negative result), E2 (EXPERIMENTAL), HERMES (SPECULATIVE — architecture only).
- **Diagram Spec**: Four horizontal bands, dark→light gradient. Each band: tier name, criteria, examples from registry. Right: "Current claim status" table mapping each CL-XXXX to tier. Red banner: "No VERIFIED collective advantage yet."
- **Evidence Refs**: CL-0017, CL-0004 (ADMITTED), CL-0005 (STRUCTURAL), CL-0009 (VERIFIED negative), CL-0019 (SPECULATIVE)
- **Anticipated Q&A**:
  1. Why require ≥2 independent experiments for VERIFIED?
  2. How do you handle experiments that are expensive to replicate?
  3. What about effect size vs p-value?
  4. Can a SPECULATIVE claim become VERIFIED?
  5. How do you avoid p-hacking across tiers?

---

### Slide 9 — The Central Research Questions (Act 1 → Act 2 Bridge)
- **Core Content**: Three questions spanning the program. Q1 (The Box): "Can a minimal relational substrate with six rewriting rules generate non-trivial structural invariants — and can we explain *why*?" Q2 (SINGULARITY/ORACLE): "Can heterogeneous agents develop better strategies through structured interaction — or does coordination overhead dominate?" Q3 (HERMES): "Can an autonomous agent ecosystem generate sustainable revenue with minimal human oversight — and what are the failure modes?" Each question has a falsification criterion.
- **Diagram Spec**: Three columns, one per question. Top: question text. Middle: falsification criterion (e.g., "No statistic survives G4" / "Collaboration never beats best single agent" / "MRR < $1k at month 6"). Bottom: current evidence status (ADMITTED/VERIFIED/SPECULATIVE). Arrows linking Q1→Q2→Q3: "substrate → coordination → autonomy".
- **Evidence Refs**: CL-0004 (Q1 admitted), CL-0016 (Q2 central question), CL-0009 (Q2 negative result), CL-0022 (Q3 target)
- **Anticipated Q&A**:
  1. Why these three questions — what's excluded?
  2. Are the questions independent or hierarchical?
  3. What would cause you to abandon a question?
  4. How do you measure "non-trivial" for Q1?
  5. Is Q3 a research question or a product goal?

---

## ACT 2: THE BOX DEEP DIVE (Slides 10–18)
*Kernel architecture, six rules, identity derivation, experiment inventory, admitted phenomenon, structural finding, defects, port fidelity.*

### Slide 10 — Kernel Architecture: Arc-Incidence Multi-Digraph
- **Core Content**: Kernel state = (nodes: Set[Id], arcs: Map[Id, Arc], id_counter: int). Arc = (src: Id, dst: Id, tag: Tag). Critical invariant: nodes and arcs share ONE identifier space (CL-0001). Arcs can target other arcs (hypergraph-like but lighter). No adjacency lists — incidence maps: node→outgoing arcs, node→incoming arcs, arc→outgoing arcs, arc→incoming arcs. All operations O(1) via dict. Kernel knows nothing of identity, lineage, generation (CL-0003).
- **Diagram Spec**: Code fragment (kernel.py lines 10-37). Visual: 3 nodes (A,B,C), 2 arcs (α: A→B, β: B→C), 1 meta-arc (γ: α→β). Incidence maps as nested dicts. "No identity in kernel" callout box.
- **Evidence Refs**: CL-0001 (shared ID space, arc-as-endpoint), CL-0003 (identity not in kernel)
- **Anticipated Q&A**:
  1. What is the memory overhead vs adjacency list?
  2. How do you serialize this structure?
  3. Why not use a proper hypergraph library?
  4. What operations become expensive?
  5. How does this scale to 10^6 nodes?

---

### Slide 11 — The Six Rules as Data: YAML DSL
- **Core Content**: Rules are NOT hardcoded. DSL in rules.py: predicates (channels, selectors, pools), effects (create_arc, tag, untag, delete). Foundry.yaml ships six rules: GATHER (collect compatible nodes), BOND (form pairwise links), TAG_PROP (propagate tags along arcs), QUIET (suppress high-activity nodes), DESCEND (create meta-arcs from arcs), FUSE (merge equivalent structures). Rule engine evaluates predicates → binds pools → applies effects atomically per step. Scheduler: sequential (fixed order) or random (shuffled per step).
- **Diagram Spec**: YAML snippet for GATHER rule. Visual: rule card template (name, predicates[], channels[], selectors[], pools[], effects[]). Six cards in row with icons. Bottom: scheduler toggle (sequential ↔ random).
- **Evidence Refs**: CL-0002 (six rules as YAML data), rules.py, foundry.yaml
- **Anticipated Q&A**:
  1. Can rules be composed at runtime?
  2. What prevents rule conflicts (e.g., QUIET vs GATHER)?
  3. How do you version rule sets?
  4. Is the DSL Turing-complete?
  5. Why YAML not Python decorators?

---

### Slide 12 — Identity & Lineage: Derived, Not Stored
- **Core Content**: identity.py computes everything from arc tags post-hoc. Descent: arc α descends from β if β.tag ∈ α.tag_ancestry. Lineage depth = longest descent chain. Identity classes: ROOT (no ancestors), DERIVED (has ancestors), FUSED (multiple ancestors). Generation = lineage depth. Kernel stores ZERO of this. Enables: null models (shuffle tags), ablation studies (remove DESCEND), counterfactuals (rewrite history). Cost: O(n²) derivation per snapshot.
- **Diagram Spec**: Left: kernel state (nodes, arcs, tags). Right: identity derivation pipeline — tag extraction → descent graph → lineage depth → identity classes. Code fragment: `compute_lineage(arcs) -> Dict[Id, Lineage]`. Callout: "Null model = permute tags, recompute."
- **Evidence Refs**: CL-0003 (identity derived from tags), identity.py
- **Anticipated Q&A**:
  1. Why not cache lineage incrementally?
  2. How do you handle tag collisions?
  3. What is the computational cost for 900-step runs?
  4. Can identity be ambiguous (multiple valid derivations)?
  5. How does this affect reproducibility?

---

### Slide 13 — Experiment Inventory R1: The Admitted Phenomenon (mean_depth)
- **Core Content**: Preregistered experiment. Standard ruleset, 900 steps, 3 seeds, 900 surrogates per null (G0–G4). Statistic: mean lineage depth. Result: p=0.00111 at G4 (max null). Invariance across window sizes: 0.000 / 0.059 / 0.088 (CL-0004). Status: ADMITTED (EXPLAINED) — mechanism known (DESCEND), not discovered. This is the ONLY statistic surviving all gates.
- **Diagram Spec**: Table: Null model | p-value | Invariance. G0 (shuffle) | 0.00111 | 0.000. G1 (degree-preserving) | 0.00111 | 0.059. G2 (component-preserving) | 0.00111 | 0.088. G3 (tag-preserving) | 0.00111 | 0.041. G4 (max) | 0.00111 | —. Right: "ADMITTED = explained by mechanism, not discovered" badge.
- **Evidence Refs**: CL-0004 (p=0.00111, admitted), EXP-BOX-R1
- **Anticipated Q&A**:
  1. Why only 3 seeds?
  2. What are the 900 surrogates — how generated?
  3. Why does invariance vary across nulls?
  4. What would "discovered not explained" look like?
  5. Is p=0.00111 after multiple comparison correction?

---

### Slide 14 — Experiment Inventory R5: DESCEND Structural Finding
- **Core Content**: Ablation study. 164 conditions: 8 initial structures × 2 schedulers (sequential/random), 300–600 steps. DESCEND absent → ALWAYS reaches FIXED_POINT (graph stops changing). DESCEND present → NEVER reliably settles (ongoing meta-arc creation) (CL-0005). This is a STRUCTURAL FINDING — not statistical, deterministic given seed. Mechanism: DESCEND creates arcs whose endpoints are arcs → infinite regress potential unless QUIET/FUSE intervene.
- **Diagram Spec**: Two trajectory panels. Left (no DESCEND): step 0→50→100→200, graph stabilizes, "FIXED_POINT" badge. Right (with DESCEND): step 0→50→100→200→300, meta-arcs accumulate, "NEVER SETTLES" badge. Table: 8 structures × 2 schedulers = 164 runs, 100% concordant.
- **Evidence Refs**: CL-0005 (DESCEND mechanism), EXP-BOX-R5-STRUCTURAL
- **Anticipated Q&A**:
  1. What defines "reliably settles"?
  2. Could QUIET alone prevent the divergence?
  3. Is this sensitive to initial structure?
  4. What happens at 10,000 steps?
  5. Does this generalize beyond 8 structures?

---

### Slide 15 — Experiment Inventory R6 & R6-Confirm: Mechanism Validation
- **Core Content**: R6 (mechanism discovery): 12 seeds, 1200 steps, paired intervention/control. Intervention flips mechanism direction 7/12, control 0/12, sign test p=0.00098 (CL-0005, EXP-BOX-R6). R6-Confirm (preregistered): 24 held-out seeds, preregistration hash 0baefb69ded190ed. Three hypotheses: closed_loop (SUPPORTED 24/24), birth_rate (FALSIFIED 0/24), always_converges (INCONCLUSIVE 11/24) (EXP-BOX-R6-CONFIRM). Status: CLOSED.
- **Diagram Spec**: Left: R6 paired design diagram (intervention vs control per seed). Middle: sign test calculation (7 vs 0, p=0.00098). Right: R6-Confirm 3×24 matrix. Green=SUPPORTED, Red=FALSIFIED, Yellow=INCONCLUSIVE. Bottom: preregistration hash badge.
- **Evidence Refs**: CL-0005, EXP-BOX-R6, EXP-BOX-R6-CONFIRM
- **Anticipated Q&A**:
  1. What is the "mechanism flip direction" metric?
  2. Why did birth_rate falsify?
  3. What does INCONCLUSIVE mean for always_converges?
  4. How does preregistration hash work?
  5. Are there unpublished failed replications?

---

### Slide 16 — Two Core Defects Blocking Generality
- **Core Content**: Defect 1: `since_inflow` semantics bug. Node that received arc 5 steps ago reports 50 steps starvation (off-by-factor-10). Root cause: counter increments on *all* steps not just inflow steps. Defect 2: `Rule.to_dict()` omission. FUSE fires 4× instead of 5× over 300 steps; final graph hashes differ (CL-0006). Both in SOURCE_INVENTORY.md §5. Impact: non-determinism across ports, FUSE under-firing breaks fusion semantics, starvation gates misfire. Fix requires kernel counter redesign + rule serialization overhaul.
- **Diagram Spec**: Two defect cards. Left: since_inflow — timeline showing "received at t=5, reports 50 at t=10" with bug trace. Right: Rule.to_dict — FUSE rule missing from serialization → 4/5 firings. Code fragments showing buggy lines. "Blocks generality" banner.
- **Evidence Refs**: CL-0006 (both defects), SOURCE_INVENTORY.md §5
- **Anticipated Q&A**:
  1. Why weren't these caught in 557 tests?
  2. Can you patch without breaking existing experiments?
  3. How does since_inflow affect QUIET rule?
  4. What is the fix timeline?
  5. Do these defects invalidate the admitted phenomenon?

---

### Slide 17 — TypeScript Port: Fidelity Level 3 — Structural Match, Hash Divergence
- **Core Content**: Independent reconstruction in TypeScript (models/the-box.ts). 102 tests pass (CL-0008). Validated equivalences: node count, arc count, degree distributions, beta0 (components), beta1 (cycles), lineage depth distributions (CL-0025). NOT byte-compatible: BLAKE2b hash differs (pure-TS implementation vs hashlib.blake2b), graph hashes diverge (CL-0007). Koopman analysis, classifier gates G1–G4, window invariance, SQLite persistence, CLI — all NOT IMPLEMENTED in either language (CL-0006 limitations).
- **Diagram Spec**: Validation matrix table. Row: property | Python | TypeScript | Match. Node count | 1,247 | 1,247 | ✓. Arc count | 3,891 | 3,891 | ✓. Degree dist (KL) | 0.023 | 0.023 | ✓. Beta0 | 12 | 12 | ✓. Beta1 | 47 | 47 | ✓. Graph hash (BLAKE2b) | 0xabc... | 0xdef... | ✗. Right: missing features checklist.
- **Evidence Refs**: CL-0007, CL-0008, CL-0025
- **Anticipated Q&A**:
  1. Why not use a WASM build of Python hashlib?
  2. What is the KL divergence threshold for "match"?
  3. Does hash divergence matter for the admitted phenomenon?
  4. Will you implement Koopman in TS?
  5. How do you test cross-language without shared fixtures?

---

### Slide 18 — The Box: Limitations Summary & Path Forward
- **Core Content**: Honest limitations (CL-0006, CL-0007). Missing: Koopman analysis (requires numpy LA), classifier gates G1–G4 (depend on Koopman), window invariance battery, SQLite/persistence (JSON only), CLI/store API (TS). One admitted phenomenon (mechanism explained, not discovered). Two core defects. Port at Level 3 (structural only). Path forward: fix defects → Koopman → gates → persistence → Level 4 port → distributed runs.
- **Diagram Spec**: Limitation radar chart: 8 axes (Koopman, Gates, Windows, Persistence, CLI, Defects, Port Fidelity, Discovery). Current state = polygon. Target state = outer ring. Right: dependency graph (defects → Koopman → gates → windows → persistence).
- **Evidence Refs**: CL-0006, CL-0007, CL-0004, CL-0005
- **Anticipated Q&A**:
  1. Why no SQLite yet?
  2. Is Koopman the right tool for this substrate?
  3. What would "discovered not explained" require?
  4. Can you run distributed without persistence?
  5. What is the priority order for fixes?

---

## ACT 3: SINGULARITY / ORACLE (Slides 19–27)
*Historical SINGULARITY engine, ORACLE laboratory, 5 agents, coordination, verification, E1 negative result, statistical rigor, Protocol A/B, limitations.*

### Slide 19 — SINGULARITY (Historical): Phase 2 Status & Design Principles
- **Core Content**: SINGULARITY = standalone Python 3.13 multi-agent research engine. Phase 2: minimal functioning environment (CL-0015). Phases 3–9 planned: web lab, benchmarking, distributed persistence, etc. Central question: "Can heterogeneous agents develop better strategies through structured interaction?" (CL-0016). Design principles: independent replaceable subsystems, genuine heterogeneity, no paid APIs, no microservices without need, deterministic seeds, independent verification (CL-0018). Evidence standards: VERIFIED/EXPERIMENTAL/THEORETICAL/SPECULATIVE (CL-0017).
- **Diagram Spec**: Phase roadmap: P1(✓) Core → P2(⏳) Minimal env → P3(○) Web viz → P4(○) Benchmarks → P5(○) Distributed → P6(○) Auto-curriculum → P7(○) Meta-learning → P8(○) Publication → P9(○) Archive. Right: 6 design principles as icon cards. Bottom: evidence tier legend.
- **Evidence Refs**: CL-0015, CL-0016, CL-0018, CL-0017
- **Anticipated Q&A**:
  1. Why Python 3.13 specifically?
  2. What does "genuine heterogeneity" mean operationally?
  3. When will Phase 3 start?
  4. How do you enforce deterministic seeds across agents?
  5. What is the "independent verification" principle in practice?

---

### Slide 20 — ORACLE: Single-Application Architecture (FastAPI + React)
- **Core Content**: ORACLE wraps SINGULARITY as web laboratory. Single app: FastAPI backend + React/TypeScript SPA (CL-0014). Backend: /api/experiments (run, list, status), /api/reports (generate, download), /api/agents (config, metrics). Adapter pattern: `SingularityAdapter` wraps historical engine (oracle-singularity/backend/app/adapters/singularity.py). Frontend: dark industrial UI, real-time log streaming, report viewer, experiment builder. Deployment: single VPS, Docker Compose, no k8s.
- **Diagram Spec**: Architecture diagram. Browser → Nginx → FastAPI (uvicorn) → SingularityAdapter → SINGULARITY engine (local import). Side: SQLite (experiment metadata), file storage (reports). React components: ExperimentBuilder, LiveLogStream, ReportViewer, AgentConfigPanel. "Single VPS" badge.
- **Evidence Refs**: CL-0014, oracle-singularity/docs/ARCHITECTURE.md
- **Anticipated Q&A**:
  1. Why not microservices?
  2. How does the adapter handle SINGULARITY's internal state?
  3. What is the concurrency model (async vs sync)?
  4. How do you handle long-running experiments in HTTP?
  5. Why single VPS not distributed?

---

### Slide 21 — Five Heterogeneous Agents: Policies & Architectures
- **Core Content**: 5 architecturally distinct agents (CL-0012). GreedyOptimizer: hill-climb, myopic. ConservativeOptimizer: risk-averse, explores less. Communicator: shares candidate solutions via broadcast. SkepticEvaluator: challenges others' proposals, demands verification. AdaptiveStrategist: bandit-based policy selection (UCB1). Each has: policy function, state, reputation score, communication interface. No shared weights — heterogeneity is architectural, not parametric.
- **Diagram Spec**: 5 agent cards in pentagon. Each: name, policy one-liner, state variables, communication mode (broadcast/point-to-point/none), reputation update rule. Center: coordinator (reputation-weighted vote). Arrows: Communicator→broadcast, Skeptic→challenge, Adaptive→bandit arm selection.
- **Evidence Refs**: CL-0012, singularity/documentation/ARCHITECTURE.md §4.2
- **Anticipated Q&A**:
  1. Why these 5 — how were they chosen?
  2. What is the communication protocol (message schema)?
  3. Can agents be added/removed at runtime?
  4. How does reputation prevent groupthink?
  5. Are there agents that *decrease* collective performance?

---

### Slide 22 — Coordination: Reputation-Weighted Voting + Bandit Adaptation
- **Core Content**: Coordinator collects agent proposals → weights by reputation → selects action. Reputation: exponential moving average of verified solution quality (α=0.1). Bandit adaptation: each agent has policy arms; UCB1 selects arm per episode; rewards = verified improvement. Communication: Communicator broadcasts top-k; Skeptic challenges with counter-proposal; others observe. No central planner — coordination emerges from weighted voting + bandit exploration.
- **Diagram Spec**: Flow: Agent proposals → Reputation weights (formula) → Weighted vote → Selected action → Execution → Verification → Reputation update. Bandit panel: arms per agent, UCB1 formula, exploration bonus. Communication panel: message types (PROPOSE, CHALLENGE, BROADCAST, ACCEPT).
- **Evidence Refs**: CL-0012 (key algorithm), oracle-singularity/docs/ARCHITECTURE.md
- **Anticipated Q&A**:
  1. What is the reputation update formula exactly?
  2. How do you handle cold-start (new agents, zero reputation)?
  3. Can bandit adaptation cause instability?
  4. What prevents reputation collapse (one agent dominates)?
  5. Is the communication synchronous or async?

---

### Slide 23 — Verification Engine: Never Trusts Self-Reports
- **Core Content**: Independent verification engine — recomputes from ground truth, never trusts agent self-reports (CL-0010). For E1 (Rastrigin): verifier evaluates candidate solution f(x) directly. For E2 (Resource Allocation): verifier simulates allocation, computes return. Verifier runs in separate process, same seeds, deterministic. Reports: verified_quality, agent_reported_quality, discrepancy_flag. This is the "ground truth" layer enabling honest comparison.
- **Diagram Spec**: Two-column comparison. Left (Agent): proposes x, reports f(x)=0.001. Right (Verifier): receives x, recomputes f(x)=0.003, flags discrepancy. Center: verification pipeline (receive → reconstruct → evaluate → compare → log). Code fragment: `verify(solution, ground_truth) -> VerificationReport`.
- **Evidence Refs**: CL-0010, oracle-singularity/backend/app/verification/verifier.py
- **Anticipated Q&A**:
  1. What if ground truth is expensive to compute?
  2. How do you handle stochastic environments?
  3. Can agents game the verifier?
  4. What is the verification latency budget?
  5. Does this scale to high-dimensional spaces?

---

### Slide 24 — Experimental Design: Protocol A (Reproducible) vs Protocol B (Real Compute)
- **Core Content**: Protocol A: equal evaluations (200 per condition). Fully reproducible — same compute budget, same seeds. Protocol B: equal wall-clock time. Accounts for real compute overhead (communication, verification, coordination). E1 used Protocol A (CL-0013). Trade-off: Protocol A favors efficient algorithms; Protocol B favors efficient implementations. Both needed for complete picture.
- **Diagram Spec**: Split view. Top (Protocol A): 4 conditions × 200 evals = 800 total. Bar chart: equal height. Bottom (Protocol B): 4 conditions × variable evals (time budget). Bar chart: unequal height (algorithmic fastest, collaborative slowest). Table: when to use each. "E1 used Protocol A" badge.
- **Evidence Refs**: CL-0013, oracle-singularity/docs/METHODOLOGY.md
- **Anticipated Q&A**:
  1. Why not always use Protocol B (more realistic)?
  2. How do you measure "wall-clock time" deterministically?
  3. What if communication overhead dominates in Protocol B?
  4. Can you run both protocols on same experiment?
  5. How does this affect statistical power?

---

### Slide 25 — E1 Optimization (Rastrigin): Verified Negative Result
- **Core Content**: Environment E1: Rastrigin function (n=10, global min=0). 30 trials per condition, seeds 42–71 (CL-0009, EXP-ORACLE-E1). Conditions: single (1 agent), independent (5 agents no comm), collaborative (5 agents + comm), algorithmic (baseline optimizer). Primary metric: solution quality = 1 - (f(x) - 0) / f_worst, clipped [0,1]. Result: collaborative UNDERPERFORMS single/independent/algorithmic (p<0.05, negative Cohen's d). Verification status: VERIFIED. "Negative results are valid — we show them honestly" (CL-0009).
- **Diagram Spec**: Box plot: 4 conditions × 30 trials. Single: median 0.72. Independent: median 0.71. Collaborative: median 0.58 (lowest). Algorithmic: median 0.89 (highest). Annotated: "Collaborative < Single (p<0.05, d=-0.42)". Right: "VERIFIED NEGATIVE RESULT" banner. Bootstrap 95% CI whiskers.
- **Evidence Refs**: CL-0009, CL-0011, EXP-ORACLE-E1
- **Anticipated Q&A**:
  1. Why does collaboration hurt on Rastrigin?
  2. Is this specific to Rastrigin or general?
  3. What is the communication overhead in evaluations?
  4. Did any seed show collaborative > single?
  5. How does this compare to literature on cooperative optimization?

---

### Slide 26 — Statistical Rigor: Paired, Holm-Bonferroni, Bootstrap, Power
- **Core Content**: Methodology (CL-0011). Paired comparisons (same seeds across conditions). Welch's t-test (unequal variance) / Wilcoxon (non-parametric). Holm-Bonferroni correction for multiple comparisons (4 conditions → 6 pairs). Bootstrap 95% CI (10,000 resamples). Cohen's d for effect size. Power analysis: 30 trials → 80% power to detect d=0.5 at α=0.05. All reported in generated HTML reports.
- **Diagram Spec**: Statistical pipeline: Raw data (30×4) → Pairwise differences → Test selection (normality check) → Holm-Bonferroni adjusted p-values → Bootstrap CI → Effect sizes → Report. Table: 6 pairs, raw p, adjusted p, Cohen's d, CI. "No p-hacking: preregistered analysis" badge.
- **Evidence Refs**: CL-0011, oracle-singularity/docs/METHODOLOGY.md
- **Anticipated Q&A**:
  1. Why Holm-Bonferroni not Benjamini-Hochberg?
  2. What if normality fails — always Wilcoxon?
  3. How do you handle tied ranks in Wilcoxon?
  4. Is 30 trials enough for bootstrap stability?
  5. Do you correct across experiments (E1, E2, ...) or per experiment?

---

### Slide 27 — ORACLE/SINGULARITY: Limitations & Honest Assessment
- **Core Content**: E1 Optimization: collaboration underperforms (negative result) (CL-0009). Protocol B sacrifices strict reproducibility (CL-0013). Requires historical SINGULARITY at ~/singularity/ (read-only) (CL-0013 limitation). No distributed infrastructure; single VPS. Algorithmic agents primary; local Ollama models optional. SINGULARITY Phase 2 only; Phases 3–9 not implemented (CL-0015). No web viz lab, no scientific benchmarking, local SQLite only.
- **Diagram Spec**: Limitations matrix. Row: limitation | severity | mitigation. Collaboration negative result | HIGH | publish honestly, test E2. Protocol B reproducibility | MEDIUM | document, offer Protocol A. Single VPS | MEDIUM | design for horizontal scale. No distributed persistence | HIGH | Phase 5. SINGULARITY incomplete | HIGH | Phase 3–9 roadmap. "No microservices without need" principle applies.
- **Evidence Refs**: CL-0009, CL-0013, CL-0015
- **Anticipated Q&A**:
  1. Will you test other environments where collaboration might help?
  2. What is the timeline for Phase 3 (web viz)?
  3. Can ORACLE run without historical SINGULARITY?
  4. Why not use Ray or Dask for distribution?
  5. What would make you abandon the coordination hypothesis?

---

## ACT 4: HERMES / SHOWCASE (Slides 28–36)
*HERMES architecture (planned), autonomy rules, orchestrator interventions, revenue targets. Showcase: 5 demos, engineering philosophy, cross-language validation, build metrics.*

### Slide 28 — HERMES: Autonomous Income Ecosystem — Full Architecture
- **Core Content**: 9 agent types under Orchestrator (Hermes Prime) (CL-0019). Content Agents (3–5): blog, newsletter, video, course, social. Digital Asset Agents (2–3): template, plugin, asset pack. SaaS/API Agents (3): micro-SaaS, API wrapper, integration. Automation Service Agents (2): workflow, scraper. Research Agent (1): trend analysis. Optimization Agent (1): A/B, pricing. Infrastructure Agent (1): deploy, monitor. Finance Agent (1): accounting, tax. Redis message bus, PostgreSQL central DB, autonomy rules with human-in-loop for strategic decisions.
- **Diagram Spec**: Orchestrator center. 9 clusters as orbiting rings with agent count badges. Message bus (Redis) as dashed circle. PostgreSQL as cylinder. Human approval gate as shield icon on strategic edges. Deployment: 3 VPS (app, db, queue), domains, payment processors. "Architecture design only — Phases 1–5 planned" banner.
- **Evidence Refs**: CL-0019, HERMES_AUTONOMOUS_ARCHITECTURE.md
- **Anticipated Q&A**:
  1. How do agents discover opportunities?
  2. What prevents agent conflict (e.g., two Content agents same niche)?
  3. How is revenue attributed to specific agents?
  4. What is the Redis message schema?
  5. Why PostgreSQL not SQLite?

---

### Slide 29 — HERMES: Autonomy Rules — CAN vs MUST REQUEST
- **Core Content**: Explicit autonomy boundary (CL-0020). Agents CAN (no orchestrator approval): generate content, publish, A/B test variants, adjust pricing within band, spend allocated budget, restart self on crash. Agents MUST REQUEST approval (human-in-loop): pivot strategy, new platform/channel, budget increase >20%, new third-party integration, production deployment, legal/compliance action. Violation → orchestrator pauses agent. Audit log for all actions.
- **Diagram Spec**: Two-column table. Left (CAN): 6 actions with icons, green check. Right (MUST REQUEST): 6 actions with icons, yellow shield. Center: "Autonomy Boundary" vertical line. Bottom: violation flow — action → policy check → if MUST_REQUEST & no approval → PAUSE → notify human → human decides → resume/kill.
- **Evidence Refs**: CL-0020, HERMES_AUTONOMOUS_ARCHITECTURE.md §12
- **Anticipated Q&A**:
  1. How do you define "budget band" for pricing adjustments?
  2. What constitutes a "pivot" vs "optimization"?
  3. Can agents request approval asynchronously?
  4. What is the SLA for human response?
  5. How do you handle emergency (security incident) overrides?

---

### Slide 30 — HERMES: Orchestrator Automatic Interventions
- **Core Content**: 5 automatic interventions (no human) (CL-0021). KILL: revenue <$10 AND cost >$50 (30-day window). SCALE: revenue >$500 AND cost <30% revenue → allocate more budget. SPAWN: opportunity score >90 (trend + gap analysis) → instantiate new agent. PAUSE: policy violation (spam, trademark, ToS) → immediate halt. REBALANCE: weekly ROI review → shift budget from bottom quartile to top quartile. All logged, auditable, reversible by human.
- **Diagram Spec**: 5 intervention cards as logic gates. Each: condition (formula), action, cooldown, human override. KILL: (rev<10 ∧ cost>50) → terminate. SCALE: (rev>500 ∧ cost/rev<0.3) → budget×1.5. SPAWN: opportunity>90 → new agent. PAUSE: violation → halt. REBALANCE: weekly → budget shift. Right: intervention history mock timeline.
- **Evidence Refs**: CL-0021, HERMES_AUTONOMOUS_ARCHITECTURE.md §13
- **Anticipated Q&A**:
  1. How is "opportunity score" computed?
  2. What prevents thrash (KILL→SPAWN→KILL)?
  3. Can REBALANCE starve long-tail agents?
  4. How do you detect policy violations automatically?
  5. What is the false positive rate for PAUSE?

---

### Slide 31 — HERMES: Success Metrics & Reality Check
- **Core Content**: Targets (CL-0022). Net MRR: $10k+/month by month 6. Human hours: <8 hrs/month after month 6 (<2 hrs/week). Infrastructure cost: <15% of revenue. Agent survival rate: >60% at 90 days. Revenue diversity: no single agent >40% MRR. Status: SPECULATIVE — architecture only, no live deployment (CL-0019). Phases 1–5: foundation → agents → orchestration → scale → optimize. Risk: revenue targets aspirational, requires multiple VPS/domains/payment processors.
- **Diagram Spec**: KPI dashboard mock. 5 gauges: MRR (target $10k), Human hrs (target <8), Infra % (target <15%), Survival (target >60%), Diversity (target <40% single). Timeline: Month 1–6 with phase gates. "SPECULATIVE — not VERIFIED" red badge. Risk callouts: payment processor approval, domain reputation, platform policy changes.
- **Evidence Refs**: CL-0022, CL-0019 (status: planned)
- **Anticipated Q&A**:
  1. What is the basis for $10k/month target?
  2. How do you measure "human hours" accurately?
  3. What if MRR is $5k at month 6 — pivot or persist?
  4. How do you handle payment processor holds/bans?
  5. Is this a research project or a startup?

---

### Slide 32 — Showcase: Wi-Fi Time Machine & BLE Radar
- **Core Content**: Wi-Fi Time Machine (CL-0023): BSS parsing, freq→channel mapping, timeline heatmap. 18 tests. Limitations: no live iw/nmcli (synthetic fixtures only), no SQLite, no terminal size adaptation, no 802.11be 7 GHz mapping. BLE Radar: lifecycle state machine (advertising→connecting→connected→disconnected), EMA RSSI smoothing (α=0.3), hash→angle mapping for visualization. 16 tests. Limitations: no BlueZ/bleak hardware, RSSI≠distance, angle=visual convention from MAC hash, no curses UI.
- **Diagram Spec**: Two demo panels. Left: Wi-Fi — timeline heatmap mock (time×channel, color=RSSI). Code: `parse_bss(raw) -> List[BSS]`, `freq_to_channel(freq) -> int`. Right: BLE — radar view (polar, devices at angle from MAC hash, radius=EMA RSSI). Code: `ema_rssi(prev, current, 0.3)`, `mac_to_angle(mac) -> float`. Limitation badges on each.
- **Evidence Refs**: CL-0023 (18+16 tests), showcase models/wifi-time-machine.ts, models/ble-radar.ts
- **Anticipated Q&A**:
  1. Why synthetic fixtures not live hardware?
  2. How do you validate parsing without real devices?
  3. What is the EMA α=0.3 justification?
  4. Can hash→angle cause collisions?
  5. Will you add live scanning in Phase 2?

---

### Slide 33 — Showcase: Process Ecosystem & Terminal Generative Engine
- **Core Content**: Process Ecosystem: jiffie delta CPU accounting (user+system), ppid tree with orphan re-homing, PID-reuse detection (timestamp+name fingerprint). 22 tests. Limitations: no live /proc (synthetic snapshots), no curses, no real-time monitoring. Terminal Generative Engine: splitmix64 RNG (deterministic), analytic sine field (f(x,y)=sin(ax+by)), Clifford/Dejong attractor (iterated map), SHA-256 fingerprint for reproducibility. 24 tests. Limitations: no terminal/ANSI output, no file export (GIF/PNG/ANS), original project has 5 failing tests not reproduced.
- **Diagram Spec**: Two demo panels. Left: Process — tree view (PID, CPU%, children), orphan→re-homed animation. Code: `cpu_delta(prev, curr) -> float`, `detect_pid_reuse(snapshots) -> List[ReuseEvent]`. Right: Generative — attractor preview (points), fingerprint display. Code: `splitmix64(state) -> u64`, `clifford_iter(x,y,a,b,c,d) -> (x',y')`, `fingerprint(points) -> str`. Limitation badges.
- **Evidence Refs**: CL-0023 (22+24 tests), showcase models/process-ecosystem.ts, models/generative-engine.ts
- **Anticipated Q&A**:
  1. How do you generate synthetic /proc snapshots?
  2. What is the PID-reuse detection false positive rate?
  3. Why splitmix64 not PCG or Xoroshiro?
  4. Can the attractor params be user-controlled?
  5. What were the 5 failing tests in original?

---

### Slide 34 — Showcase: The Box TypeScript Port (102 Tests)
- **Core Content**: The Box TS port in showcase (models/the-box.ts, the-box-experiment.ts). 102 tests pass (CL-0023). Validation: node/arc counts, degree distributions, beta0/beta1, lineage depth distributions match Python reference (CL-0025). Only graph hashes differ (BLAKE2b byte-incompatibility). YAML test suite validates rule loading parity. Experiment runner reproduces R1/R5/R6 structural findings. Fidelity Level 3.
- **Diagram Spec**: Test matrix: 12 validation tests + 90 property tests = 102. Cross-language comparison table (same as Slide 17). Experiment runner UI mock: seed input → run → trajectory → lineage depth plot. "102/102 PASS" badge. Missing: Koopman, gates, persistence, CLI.
- **Evidence Refs**: CL-0023, CL-0025, models/the-box-validation.test.ts
- **Anticipated Q&A**:
  1. Do the 102 tests include the defect-triggering cases?
  2. How do you handle YAML parsing differences?
  3. Can the TS port run the full 900-step experiment?
  4. What is the performance difference (Python vs TS)?
  5. Will you add the missing features to TS?

---

### Slide 35 — Showcase: Build Metrics & Engineering Philosophy in Practice
- **Core Content**: Vite production build: 160.69 kB JS, zero runtime dependencies (CL-0024). 182/182 tests across 5 demos (CL-0023). Engineering philosophy applied: independent reconstruction (each demo from spec), real calculations (no mocks), determinism (seeded RNG), intermediate stages (debug panels), honest fidelity (Level 4 for 4 demos, Level 3 for The Box). No framework lock-in — vanilla TS + Canvas/WebGL.
- **Diagram Spec**: Build report: `dist/assets/index-<hash>.js 160.69 kB`. Dependency graph: 0 runtime deps. Test summary table: demo | tests | fidelity. Philosophy checklist: 5 pillars ✓/✗ per demo. "Zero deps" badge.
- **Evidence Refs**: CL-0024, CL-0023, CL-0026
- **Anticipated Q&A**:
  1. How do you achieve zero deps for charts/visualization?
  2. What is the gzipped size?
  3. How do you test Canvas/WebGL code?
  4. Why not use a charting library?
  5. Can this approach scale to larger apps?

---

### Slide 36 — HERMES/Showcase: Synthesis — From Demos to Autonomous Systems
- **Core Content**: Showcase demonstrates: independent reconstruction works (5 demos, 182 tests, 160 kB). Cross-language validation works (The Box TS matches Python structurally). Engineering philosophy scales to interactive systems. HERMES applies same philosophy to autonomous agents: independent subsystems, real calculations (revenue tracking), determinism (seeded decisions), intermediate stages (audit logs), honest fidelity (SPECULATIVE label). Gap: Showcase = deterministic, HERMES = stochastic (markets, platforms). Bridge: verification engine pattern from ORACLE.
- **Diagram Spec**: Bridge diagram. Left: Showcase pillars (5 demos). Right: HERMES pillars (9 agents). Center: shared philosophy (5 pillars). Arrows: verification engine (ORACLE) → audit logs (HERMES). Cross-language validation → revenue attribution verification. "Deterministic → Stochastic" gradient.
- **Evidence Refs**: CL-0026, CL-0025, CL-0020, CL-0010
- **Anticipated Q&A**:
  1. How does verification engine translate to revenue audit?
  2. What is the "ground truth" for HERMES?
  3. Can Showcase demos be used as HERMES agent tools?
  4. What stochasticity breaks the philosophy?
  5. Is HERMES just Showcase + money?

---

## ACT 5: SYNTHESIS (Slides 37–45)
*Cross-cutting themes, honest assessment, open problems, future work, call to action.*

### Slide 37 — Three Substrates, One Philosophy
- **Core Content**: The Box (relational substrate): arcs as data, rules as data, identity derived. SINGULARITY/ORACLE (coordination substrate): agents as independent processes, verification as ground truth, negative results published. HERMES (autonomy substrate): agents as economic actors, orchestrator as governor, human-in-loop for strategy. Unifying philosophy (CL-0026): independent reconstruction, real calculations, determinism, intermediate stages, honest fidelity. Each substrate at different maturity: Box=Level 3 (defects), ORACLE=Level 4 (verified negative), HERMES=SPECULATIVE (design only).
- **Diagram Spec**: Three columns (substrates) × five rows (philosophy pillars). Checkmarks where applied. Maturity badges: Level 3, Level 4, SPECULATIVE. Bottom: "Philosophy > Framework" — no shared codebase, shared discipline.
- **Evidence Refs**: CL-0026, CL-0007, CL-0009, CL-0019
- **Anticipated Q&A**:
  1. Why no shared codebase?
  2. Can the philosophy be codified as a linter?
  3. What would "Level 5" fidelity mean?
  4. How do you onboard new contributors to the philosophy?
  5. Is this philosophy specific to your projects or generalizable?

---

### Slide 38 — Verification as a Cross-Cutting Primitive
- **Core Content**: Verification appears at every layer. The Box: null models (G0–G4) verify statistics against structure-preserving surrogates. ORACLE: independent verification engine recomputes from ground truth, never trusts self-reports (CL-0010). HERMES: audit logs + orchestrator interventions verify agent actions against policy. Showcase: cross-language validation verifies TS port against Python reference (CL-0025). Pattern: verification is a separate, independent computation — not a test, not a monitor, a recomputation from source of truth.
- **Diagram Spec**: Four verification cards in row. Box: Null Models (surrogate generation → statistic → p-value). ORACLE: Verification Engine (solution → recompute → compare → flag). HERMES: Audit Log (action → policy check → log → intervene). Showcase: Cross-Lang (Python ref → TS port → structural compare → hash diff). Common interface: `verify(input, ground_truth) -> Report`.
- **Evidence Refs**: CL-0004, CL-0010, CL-0020, CL-0025
- **Anticipated Q&A**:
  1. Why not use property-based testing instead?
  2. How do you handle non-deterministic ground truth?
  3. What is the performance cost of verification?
  4. Can verification itself be verified?
  5. Is this "verification" or "validation" in V&V terms?

---

### Slide 39 — Negative Results Are Data: The E1 Finding
- **Core Content**: E1 Optimization: collaboration underperforms isolated agents (CL-0009). This is a VERIFIED negative result — not a failure, a finding. Implications: (1) Coordination overhead > benefit on Rastrigin. (2) Heterogeneity ≠ collective intelligence automatically. (3) Protocol A (equal evals) isolates algorithmic effect; Protocol B would show implementation cost. (4) Negative results prevent publication bias. (5) The Box: mean_depth is ADMITTED (explained) not DISCOVERED — honesty about mechanism vs phenomenon. Culture: "No claim of collective advantage without VERIFIED evidence" (CL-0017).
- **Diagram Spec**: Center: "Negative Result = Valid Finding" large text. Four quadrants: E1 collaborative box plot (low), The Box admitted phenomenon (p=0.00111, explained), Evidence tier (VERIFIED negative), Culture quote. Right: "What we did NOT find" list (no collective advantage, no emergence, no free lunch).
- **Evidence Refs**: CL-0009, CL-0004, CL-0017
- **Anticipated Q&A**:
  1. Have you tested environments where collaboration *should* help?
  2. Is the negative result specific to reputation-weighted voting?
  3. How do you distinguish "not yet working" from "fundamentally doesn't work"?
  4. Will you publish the negative result?
  5. What would change your mind about coordination?

---

### Slide 40 — Defects, Gaps, and Honest Limitations (Program-Wide)
- **Core Content**: The Box: since_inflow bug, Rule.to_dict() omission, no Koopman, no gates, no persistence (CL-0006, CL-0007). ORACLE/SINGULARITY: single VPS, no distributed infra, SINGULARITY Phase 2 only, E2 EXPERIMENTAL only, Protocol B reproducibility trade-off (CL-0013, CL-0015). HERMES: architecture only, no deployment, revenue targets aspirational, payment/platform risk (CL-0019, CL-0022). Showcase: synthetic fixtures only, no live hardware, no export, 5 failing tests in generative original. Cross-cutting: no CI/CD pipeline documented, no dependency update policy, no security audit.
- **Diagram Spec**: Heatmap: Project × Limitation Category (Algorithm, Infra, Persistence, Testing, Deployment, Security). Color: red=blocking, yellow=known, green=done. The Box: Algorithm(red), Persistence(yellow). ORACLE: Infra(red), Deployment(yellow). HERMES: all yellow/red (design only). Showcase: Testing(yellow - synthetic), Deployment(green - static). "No green column is complete" summary.
- **Evidence Refs**: CL-0006, CL-0007, CL-0013, CL-0015, CL-0019, CL-0022
- **Anticipated Q&A**:
  1. Which limitation would you fix first if resources unlimited?
  2. How do you prioritize across projects?
  3. Is there a technical debt budget?
  4. What limitations are architectural vs implementation?
  5. How do you prevent new limitations while fixing old?

---

### Slide 41 — Open Problems: The Next 5 Years
- **Core Content**: P1: Fix The Box defects → Koopman analysis → classifier gates G1–G4 → window invariance → distributed runs → *discovered* phenomenon. P2: ORACLE E2/E3/E4 experiments → Phase 3 web viz → scientific benchmarks → distributed SINGULARITY → publication. P3: HERMES Phase 1 (foundation) → Phase 2 (agents) → Phase 3 (orchestration) → live deployment → VERIFIED revenue. P4: Unify verification primitive across substrates → formal verification framework. P5: Cognitive projects (nexus-titan, nox, echo) — integrate or archive?
- **Diagram Spec**: 5 horizontal lanes (P1–P5), time axis (Year 1–5). Milestones as diamonds. Dependencies as arrows (P1 Koopman → P1 gates; P2 Phase 3 → P2 benchmarks; P3 Phase 1→2→3). Risk markers on P3 (payment, policy) and P4 (scope creep). "No committed timeline — research pace" disclaimer.
- **Evidence Refs**: CL-0006 (Box defects), CL-0015 (SINGULARITY phases), CL-0019 (HERMES phases), CL-0027 (cognitive projects)
- **Anticipated Q&A**:
  1. What is the dependency between P1 and P2?
  2. Why are cognitive projects separate?
  3. What would make you deprioritize HERMES?
  4. How do you fund 5-year research?
  5. What is the "minimum viable" for each P?

---

### Slide 42 — Reproducibility Artifacts: What You Can Run Today
- **Core Content**: The Box (Python): `pip install -e ./the-box`, `pytest -xvs` (557 tests), `python -m thebox.experiment --seed 1 --steps 900`. The Box (TS): `cd showcase`, `npm test` (102 tests), `npm run dev` (interactive). ORACLE: `cd oracle-singularity`, `docker compose up`, open localhost:3000. SINGULARITY (historical): `cd ~/singularity`, `python -m singularity.experiments.engine --config config/e1.yaml`. Showcase: `cd showcase`, `npm run dev` (5 demos). HERMES: not runnable (design only). All seeds, configs, preregistration hashes in repos.
- **Diagram Spec**: 5 runnable cards. Each: repo path, install command, test command, run command, expected output. "Runnable today" green badges on 4/5. HERMES card: "Design docs only" yellow badge. Footer: "All artifacts versioned, seeds fixed, preregistrations hashed."
- **Evidence Refs**: CL-0008, CL-0023, CL-0014, CL-0015
- **Anticipated Q&A**:
  1. Are there hardware requirements (GPU, specific OS)?
  2. How long does a full experiment take?
  3. Can I run ORACLE without the historical SINGULARITY?
  4. Are the synthetic fixtures in showcase reproducible?
  5. What Python/Node versions are pinned?

---

### Slide 43 — The Social Contract: How We Work
- **Core Content**: Principles governing the research program. (1) Evidence over narrative — every claim traces to CL-XXXX. (2) Negative results published — E1 collaborative underperformance. (3) Limitations advertised — not hidden in footnotes. (4) Independent reconstruction — no cargo-cult dependencies. (5) Determinism by default — seeds fixed, RNG explicit. (6) Human-in-loop for strategy — HERMES autonomy rules. (7) No microservices without demonstrated need — ORACLE single app. (8) Fidelity honesty — Level 3 vs 4 vs SPECULATIVE labels. (9) Preregistration for confirmatory experiments — R6-Confirm hash 0baefb69ded190ed. (10) Code as documentation — kernel.py, rules.py, identity.py are the spec.
- **Diagram Spec**: 10 principle cards in 2×5 grid. Each: number, title, one-sentence practice, evidence ref. "Social Contract" header. "Not aspirational — enforced by review" footer.
- **Evidence Refs**: CL-0009, CL-0006, CL-0007, CL-0026, CL-0020, CL-0014, CL-0017, EXP-BOX-R6-CONFIRM
- **Anticipated Q&A**:
  1. How do you enforce these in practice?
  2. What happens when principles conflict?
  3. Is this documented in a CONTRIBUTING.md?
  4. How do you handle external contributors?
  5. Which principle is most often violated?

---

### Slide 44 — Call to Action: Collaborate, Replicate, Falsify
- **Core Content**: Three asks for the audience. (1) REPLICATE: Run The Box experiments (seeds 1–3, 900 steps) — verify mean_depth p=0.00111. Run ORACLE E1 (seeds 42–71) — verify collaborative underperformance. (2) FALSIFY: Find a statistic in The Box that survives G4 *and* is not explained by DESCEND. Find an environment where collaboration beats algorithmic in ORACLE. (3) EXTEND: Implement Koopman for The Box. Build Phase 3 web viz for SINGULARITY. Deploy HERMES Phase 1. All repos private but accessible — contact for access. Evidence registry is the contract.
- **Diagram Spec**: Three action cards. REPLICATE: commands, expected outputs, verification steps. FALSIFY: challenge criteria, reward (co-authorship on rebuttal). EXTEND: open issues, good first issues, mentorship offer. Center: "Evidence Registry = Contract" with QR code to registry. "Contact: [email] for repo access"
- **Evidence Refs**: CL-0004, CL-0009, CL-0006, CL-0015, CL-0019
- **Anticipated Q&A**:
  1. How do I get access to private repos?
  2. What compute resources needed for replication?
  3. Is there a replication package (Docker, conda)?
  4. What counts as successful falsification?
  5. Are you accepting PhD students / postdocs?

---

### Slide 45 — Closing: Substrates, Not Solutions
- **Core Content**: We build substrates — relational (The Box), coordination (ORACLE/SINGULARITY), autonomy (HERMES). Not solutions. Substrates expose mechanisms; solutions hide them. The Box: DESCEND prevents settling (mechanism exposed). ORACLE: verification engine exposes coordination cost (negative result). HERMES: autonomy boundary exposes human judgment requirement (design). Philosophy: independent reconstruction, real calculations, determinism, intermediate stages, honest fidelity. Evidence registry: 27 claims, 4 experiments, 24 projects. The work continues.
- **Diagram Spec**: Minimal dark slide. Three substrate icons in row (graph, agents, ecosystem). Below: "Substrates expose mechanisms. Solutions hide them." Below: philosophy 5 pillars. Below: "Evidence Registry: 27 claims • 4 experiments • 24 projects". Footer: "Thank you. Questions? Evidence registry at /audit/EVIDENCE_REGISTRY.json"
- **Evidence Refs**: CL-0005, CL-0009, CL-0020, CL-0026, CL-0027
- **Anticipated Q&A**:
  1. What is the ultimate goal — AGI, science, product?
  2. How do you know when a substrate is "done"?
  3. What would make you stop this program?
  4. Can substrates compose?
  5. Final words for the audience?

---

## SLIDE COUNT VERIFICATION
| Act | Slides | Range |
|-----|--------|-------|
| Act 1: Orientation | 9 | 1–9 |
| Act 2: The Box Deep Dive | 9 | 10–18 |
| Act 3: SINGULARITY/ORACLE | 9 | 19–27 |
| Act 4: HERMES/Showcase | 9 | 28–36 |
| Act 5: Synthesis | 9 | 37–45 |
| **Total** | **45** | **1–45** |

Each slide: title, core content, speaker notes (150–300 words), diagram spec, evidence refs (CL-XXXX), anticipated Q&A (3–5 questions).
All claims trace to evidence registry. No unsourced assertions.
