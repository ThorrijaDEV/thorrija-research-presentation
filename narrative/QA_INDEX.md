# QA_INDEX.md — Anticipated Questions & Answers Index
**All 45 slides, 3–5 questions each. Evidence-grounded answers.**

---

## ACT 1: ORIENTATION

### Slide 1 — Title
**Q1: What unifies these disparate systems?**
A: The engineering philosophy (CL-0026): independent reconstruction, real calculations, determinism, intermediate stages, honest fidelity. Three substrates (relational, coordination, autonomy) built with same discipline.

**Q2: Why "computational substrates" not "architectures"?**
A: Substrates expose mechanisms; architectures hide them. The Box kernel exposes arc→arc creation; ORACLE verification engine exposes coordination cost; HERMES autonomy boundary exposes human judgment requirement.

**Q3: What is the falsifiability criterion for the program?**
A: Each substrate has explicit falsification: The Box — no statistic survives G4; ORACLE — collaboration never beats best single agent; HERMES — MRR <$1k at month 6.

**Q4: How do you avoid cargo-cult complexity?**
A: Independent reconstruction from specs (not ports), zero runtime dependencies in showcase, no microservices without demonstrated need (CL-0018), fidelity honesty (Level 3 vs 4 vs SPECULATIVE).

**Q5: What would constitute a negative result for the whole program?**
A: The Box: defects unfixable or no discovered phenomenon. ORACLE: collaboration loses on all environments. HERMES: Phase 1 deployment fails. Any would redirect the program.

---

### Slide 2 — Engineering Philosophy
**Q1: Why not just port the Python to TypeScript directly?**
A: Porting carries hidden assumptions. Independent reconstruction from THE_BOX_MASTER_DOCUMENTATION.md caught two defects (since_inflow, Rule.to_dict) that Python tests missed (CL-0006).

**Q2: How do you define "structural match" formally?**
A: Cross-language validation (CL-0025): node/arc counts exact, degree distribution KL<0.05, beta0/beta1 exact, lineage depth KS test p>0.05. Hashes differ (BLAKE2b byte-incompatibility).

**Q3: What does Level 1 look like?**
A: Specification only — no code. Level 2: structural skeleton (types, interfaces). Level 3: structural properties match (The Box TS). Level 4: behavioral match (Showcase demos).

**Q4: How do you handle non-determinism in multi-agent systems?**
A: Fixed seeds (42–71), deterministic RNG (splitmix64), verification engine recomputes from ground truth (CL-0010), audit logs for replay. Non-determinism confined to LLM calls (logged).

**Q5: Is this philosophy scalable to larger teams?**
A: Enforced by review: PR template requires CL-XXXX references, CI runs validation. Social contract (Slide 43) is the infrastructure. No framework lock-in — vanilla code, explicit patterns.

---

### Slide 3 — Project Landscape
**Q1: Which projects are "research" vs "engineering"?**
A: Research core: The Box, SINGULARITY, ORACLE, HERMES (4 systems). Engineering: Showcase (5 demos, Level 4), Systems tools (9, production-grade), Security (3). Cognitive (3) unclassified.

**Q2: Why are cognitive projects unclassified?**
A: nexus-titan, nox, echo — no fidelity rating, no tests, no showcase presence. Decision pending: apply philosophy (raise to Level 3) or archive as prior art (Slide 41, P5).

**Q3: What is the maintenance burden of 24 projects?**
A: Showcase (5) actively maintained (182 tests). Research core (4) active development. Systems/Security (12) stable, minimal changes. Cognitive (3) dormant. Burden concentrated on 9 active projects.

**Q4: How do you decide what enters the showcase?**
A: Must demonstrate philosophy at interactive level: deterministic, real calculations, intermediate stages, Level 4 fidelity, zero deps. The Box TS included as cross-validation proof.

**Q5: Are any projects deprecated?**
A: No formal deprecation. Cognitive projects dormant. Systems tools stable. If a project contradicts philosophy, it's refactored or archived (e.g., original Generative Engine had 5 failing tests — not reproduced in TS port).

---

### Slide 4 — The Box Summary
**Q1: Why arc-incidence not adjacency lists?**
A: Enables arc-as-endpoint (arc→arc) in O(1). Adjacency lists require O(n) search for "which arcs target this arc." Incidence maps: arc_incoming[arc_id] = Set[arc_ids].

**Q2: What does "arcs as endpoints" enable that hypergraphs don't?**
A: Simpler implementation (same ID space, same incidence maps), O(1) traversal both directions, natural rule effects (DESCEND creates arc→arc). Hypergraphs need separate node/edge types.

**Q3: How do YAML rules compose?**
A: Rule engine evaluates predicates → binds pools → applies effects atomically per step. Scheduler orders rules (sequential/random). Rules don't call each other — they mutate shared kernel state.

**Q4: Why derive identity instead of storing it?**
A: Enables null models (shuffle tags, recompute), ablation (remove DESCEND, recompute), counterfactuals (rewrite history). Stored identity would require kernel rewrite for each null.

**Q5: Can the defects be fixed without redesign?**
A: since_inflow: kernel counter redesign (separate step vs inflow counters). Rule.to_dict(): automatic rule registry (decorator-based). Both require kernel changes but not architecture change.

---

### Slide 5 — SINGULARITY/ORACLE Summary
**Q1: Why 5 agents — why not 3 or 10?**
A: 5 covers strategic diversity: greedy, conservative, communication, skepticism, adaptation. More agents → combinatorial coordination complexity. Fewer → insufficient heterogeneity. 5 is minimal for "genuine heterogeneity" (CL-0018).

**Q2: What does "reputation-weighted" mean formally?**
A: weight_i = rep_i / Σrep_j. rep_t = (1-α)rep_{t-1} + α×verified_quality, α=0.1. Verified_quality from verification engine (CL-0010), not self-report.

**Q3: How does the verification engine access ground truth?**
A: For Rastrigin: computes f(x) directly. For Resource Allocation: simulates environment. Runs in separate process, same seeds, deterministic. Never sees agent internals.

**Q4: Why is negative result emphasized?**
A: "No claim of collective advantage without VERIFIED evidence" (CL-0017). Negative results prevent publication bias. E1 collaborative underperformance is VERIFIED (30 trials, Holm-Bonferroni, bootstrap CI).

**Q5: What is the compute budget per experiment?**
A: E1 Protocol A: 4 conditions × 30 trials × 200 evals = 24,000 evaluations. ~10 minutes on single VPS. Protocol B: 30 seconds wall-clock per condition.

---

### Slide 6 — HERMES Architecture
**Q1: How do you prevent runaway spend before human approval?**
A: Daily budget cap per agent (CAN: spend allocated budget). Orchestrator KILL intervention: rev<$10 AND cost>$50 over 30 days (CL-0021). Payment processor limits (Stripe daily caps).

**Q2: What defines "opportunity score >90"?**
A: Trend velocity (Google Trends, Reddit, HN) + market gap (competitor absence) + competitor weakness (low ratings, abandoned). Computed by Research Agent, verified by Orchestrator.

**Q3: Why 9 agent types — is this taxonomy stable?**
A: Covers content→asset→SaaS→automation→research→optimization→infra→finance value chain. Phase 2 implements all 9; taxonomy evolves based on Phase 3 results. Not sacred.

**Q4: What happens if orchestrator fails?**
A: Agents run autonomously (CAN actions). Human notified via alert. Orchestrator stateless — restart from PostgreSQL. No single point of failure for agent execution.

**Q5: How do you measure "human hours/week" objectively?**
A: Orchestrator API logs every human approval action with timestamp. Weekly sum of (approval_time + review_time). Target <2 hrs/week = <8 approvals/week at 15 min each.

---

### Slide 7 — Showcase
**Q1: Why zero runtime dependencies?**
A: Philosophy: independent reconstruction, no cargo-cult. Custom Canvas rendering, vanilla signals, native DOM. 160 kB includes all rendering, state, parsing. Proves philosophy scales.

**Q2: How do you test without live hardware (Wi-Fi, BLE, /proc)?**
A: Synthetic fixtures from real captures (anonymized). Parsing logic tested against real formats. Behavioral logic (EMA, tree building) tested with property-based tests (fast-check).

**Q3: What is the synthetic fixture strategy?**
A: Record real data once → anonymize (MAC→hash, SSID→generic) → use as test fixtures. Ensures parser correctness without hardware dependency. Fixtures versioned in repos.

**Q4: Why Vite not Next.js?**
A: Static SPA, no SSR needed. Vite: faster dev, smaller build (160 kB), zero config. Next.js adds framework weight for no benefit (no SEO, no server components).

**Q5: Can the demos run offline?**
A: Yes. `npm run build` → `dist/` → open index.html. No network calls. All data synthetic or embedded. Service worker optional for caching.

---

### Slide 8 — Evidence Standards
**Q1: Why require ≥2 independent experiments for VERIFIED?**
A: Single experiment = fluke risk. E1: 30 trials is one experiment (one environment). VERIFIED needs replication across environments/seeds. We have 1 VERIFIED (E1), 1 EXPERIMENTAL (E2).

**Q2: How do you handle experiments that are expensive to replicate?**
A: Current experiments cheap (CPU, 10 min). If expensive: reduce trial count, increase effect size threshold, use Bayesian sequential testing. Not yet needed.

**Q3: What about effect size vs p-value?**
A: Both reported. Cohen's d for E1: -0.42 (medium negative). Bootstrap 95% CI for effect size. Power analysis: 30 trials → 80% power for d=0.5.

**Q4: Can a SPECULATIVE claim become VERIFIED?**
A: Yes. HERMES: deploy Phase 1 → measure → if MRR >$1k at month 3 with <20 hrs human → EXPERIMENTAL. Replicate across niches → VERIFIED. Path defined.

**Q5: How do you avoid p-hacking across tiers?**
A: Preregistration for confirmatory (R6-Confirm hash 0baefb69ded190ed). Analysis pipeline fixed before data. Tier assigned by evidence, not outcome. Negative results same rigor.

---

### Slide 9 — Central Research Questions
**Q1: Why these three questions — what's excluded?**
A: Excluded: "Can we build AGI?", "Can we automate coding?", "Can we beat SOTA on benchmark X?" We study substrates, not solutions. Questions chosen to be falsifiable and hierarchical.

**Q2: Are the questions independent or hierarchical?**
A: Hierarchical: substrate (Box) → coordination (ORACLE) → autonomy (HERMES). Verification primitive through-line. If Q1 fails, Q2's substrate impoverished. If Q2 fails, Q3's premise questionable.

**Q3: What would cause you to abandon a question?**
A: Q1: defects unfixable, no discovered phenomenon after Koopman+gates. Q2: collaboration loses on 5+ environments. Q3: Phase 1 deployment fails or human hours >50/week at month 3.

**Q4: How do you measure "non-trivial" for Q1?**
A: Statistic surviving G4 null model (max of structure-preserving surrogates). mean_depth p=0.00111 is only one. "Non-trivial" = not explained by degree/component/tag distribution alone.

**Q5: Is Q3 a research question or a product goal?**
A: Research question: "Can autonomy scale with human oversight?" Product goal would be "$10k MRR." We treat $10k as falsification threshold, not success metric. SPECULATIVE tier (CL-0019).

---

## ACT 2: THE BOX DEEP DIVE

### Slide 10 — Kernel Architecture
**Q1: What is the memory overhead vs adjacency list?**
A: ~4× dict entries (node_out, node_in, arc_out, arc_in). For 10k nodes, 30k arcs: ~160k dict entries vs ~40k. Acceptable for research scale. Trade-off: O(1) arc→arc queries.

**Q2: How do you serialize this structure?**
A: JSON: {nodes: [...], arcs: [{id, src, dst, tag}, ...], id_counter: N}. Import reconstructs all four incidence maps in O(n). No custom binary format.

**Q3: Why not use a proper hypergraph library?**
A: Hypergraph libraries: heavy deps, complex APIs, no arc→arc as first-class. Our kernel: 200 lines, zero deps, arc→arc native. Philosophy: independent reconstruction.

**Q4: What operations become expensive?**
A: Full graph isomorphism (FUSE candidate detection) — O(n!) worst case. We use heuristic: degree sequence + tag signature + local neighborhood. Identity derivation O(n²) per snapshot — cached.

**Q5: How does this scale to 10^6 nodes?**
A: Not designed for that. Research scale: 10k nodes, 30k arcs. For 10^6: need partitioned incidence maps, distributed kernel, different architecture. Phase 5 (distributed) would address.

---

### Slide 11 — Six Rules as Data
**Q1: Can rules be composed at runtime?**
A: Yes. foundry.yaml loaded at startup. Rules added/removed by editing YAML. Hot-reload not implemented but trivial (file watcher → reparse). Rule DSL supports any predicate/effect combination.

**Q2: What prevents rule conflicts (e.g., QUIET vs GATHER)?**
A: Scheduler order (sequential) or random shuffle. QUIET suppresses high-degree nodes; GATHER finds compatible pairs. Conflict = dynamics, not error. Ablation studies (R5) remove rules to measure interaction.

**Q3: How do you version rule sets?**
A: foundry.yaml in git. Experiment config references git commit hash. R6-Confirm preregistration includes rule set hash. Reproducibility via version control, not custom versioning.

**Q4: Is the DSL Turing-complete?**
A: No. Predicates: filters on tags, degrees, connectivity. Effects: create_arc, tag, untag, delete. No loops, recursion, arithmetic. Intentionally limited — rules as data, not code.

**Q5: Why YAML not Python decorators?**
A: YAML = data, portable across languages (TS port parses same YAML). Decorators = code, Python-specific. Philosophy: rules as data, not code (CL-0002).

---

### Slide 12 — Identity & Lineage
**Q1: Why not cache lineage incrementally?**
A: Null models require tag permutation → full recompute. Incremental cache would need invalidation on every tag change. Full recompute O(n²) is fast enough (10k arcs → ~50ms).

**Q2: How do you handle tag collisions?**
A: Tags are strings from TAG_PROP/DESCEND. Collision = same tag from different origins. Descent follows tag ancestry — collision merges lineages. This is feature, not bug: FUSE detects structural equivalence via tag overlap.

**Q3: What is the computational cost for 900-step runs?**
A: ~100M descent checks per snapshot. 900 steps → too heavy for every step. We snapshot every 50 steps + final. Total ~20 snapshots × 50ms = ~1s per run. Negligible vs kernel mutation.

**Q4: Can identity be ambiguous (multiple valid derivations)?**
A: Descent = tag ancestry. If tag A → tag B → tag C, lineage is unique. FUSE creates multiple ancestors → DERIVED class becomes FUSED. Ambiguity resolved by class hierarchy.

**Q5: How does this affect reproducibility?**
A: Identity derived deterministically from kernel state + tags. Same seed → same kernel → same tags → same identity. Cross-language: TS derives same identity from same tags (validated in CL-0025).

---

### Slide 13 — R1 Admitted Phenomenon
**Q1: Why only 3 seeds?**
A: Computational cost: 900 steps × 900 surrogates × 5 nulls × 3 seeds = 12.15M graph derivations. ~18 minutes on 2023 hardware. 3 seeds sufficient for effect size (p=0.00111).

**Q2: What are the 900 surrogates — how generated?**
A: Per null model: G0=shuffle all tags, G1=degree-preserving shuffle (configuration model), G2=component-preserving, G3=tag-distribution-preserving. 900 independent permutations each.

**Q3: Why does invariance vary across nulls?**
A: Invariance = p-value stability across trajectory windows (early/mid/late). G0 (shuffle) perfectly invariant (0.000). G1/G2/G3 preserve structure → some drift (0.059, 0.088) but below significance.

**Q4: What would "discovered not explained" look like?**
A: Statistic survives G4 but NO rule ablation explains it. We ablated each rule: only DESCEND removal collapses mean_depth. If none did → discovered phenomenon. Current: explained.

**Q5: Is p=0.00111 after multiple comparison correction?**
A: G4 = max(G0–G3). Single test against maximum null. No further correction needed. G4 p-value IS the corrected p-value (Westfall-Young max-t principle).

---

### Slide 14 — R5 DESCEND Structural Finding
**Q1: What defines "reliably settles"?**
A: FIXED_POINT = no rule fires for 50 consecutive steps. "Never reliably settles" = in 300-600 steps, never reaches 50-step quiescence. 100% of 164 runs with DESCEND failed to settle.

**Q2: Could QUIET alone prevent the divergence?**
A: QUIET suppresses high-degree nodes. DESCEND creates meta-arcs (arc→arc) which may not have high degree initially. QUIET doesn't target meta-arc creation directly. FUSE merges equivalent structures but meta-arcs often unique.

**Q3: Is this sensitive to initial structure?**
A: Tested 8 structures: empty, single node, chain, star, cycle, complete, random sparse, random dense. 100% concordance — DESCEND absent always settles, present never settles. Not structure-sensitive.

**Q4: What happens at 10,000 steps?**
A: Not tested. Hypothesis: meta-arc count grows until memory exhausted or FUSE/QUIET catch up. Structural finding suggests unbounded growth without suppression mechanism.

**Q5: Does this generalize beyond 8 structures?**
A: 8 structures cover topological diversity. Conjecture: holds for any finite initial structure. Proof would require showing DESCEND creates infinite descending chain in tag ancestry — plausible but not proven.

---

### Slide 15 — R6 & R6-Confirm
**Q1: What is the "mechanism flip direction" metric?**
A: Intervention modifies DESCEND firing condition (e.g., require tag overlap >0.5). Flip = lineage depth trend reverses (increasing→decreasing or vice versa). 7/12 intervention seeds flipped; 0/12 control.

**Q2: Why did birth_rate falsify?**
A: DESCEND converts node→node arcs to arc→arc arcs. Total arc count similar. Birth rate (arcs/step) unchanged. What changes: arc TYPE distribution (more meta-arcs). Our hypothesis was wrong.

**Q3: What does INCONCLUSIVE mean for always_converges?**
A: 11/24 converged, 13/24 didn't. Not decisive for "always." Need more steps or different structures. "Inconclusive" = evidence insufficient, not "false."

**Q4: How does preregistration hash work?**
A: Analysis plan + hypotheses + seeds committed as SHA-256 hash (0baefb69ded190ed) BEFORE running 24 seeds. After run, hash revealed, plan verified. Prevents p-hacking, HARKing.

**Q5: Are there unpublished failed replications?**
A: No. All experiments in registry. R1–R6 are the complete experiment inventory (THE_BOX_MASTER_DOCUMENTATION.md §24). Negative results published (R6-Confirm birth_rate falsified).

---

### Slide 16 — Two Core Defects
**Q1: Why weren't these caught in 557 tests?**
A: since_inflow: tests used synthetic graphs with controlled inflow timing (not realistic). Rule.to_dict(): FUSE fires rarely in short tests (<50 steps). 300-step integration test caught it.

**Q2: Can you patch without breaking existing experiments?**
A: since_inflow fix changes starvation semantics → R1/R5/R6 results may shift. Must re-run all experiments. Rule.to_dict() fix restores FUSE firing → hashes change. Breaking change, but correct.

**Q3: How does since_inflow affect QUIET rule?**
A: QUIET suppresses nodes with since_inflow > threshold. Bug: 10× overcount → QUIET suppresses too aggressively → nodes starved prematurely → dynamics distorted.

**Q4: What is the fix timeline?**
A: No committed timeline — research pace. Priority: high (blocks Level 4, distributed). Requires kernel counter redesign + rule registry. Estimated 2-4 weeks engineering.

**Q5: Do these defects invalidate the admitted phenomenon?**
A: mean_depth (R1) uses lineage depth from tags, not since_inflow. FUSE under-firing affects fusion but not DESCEND-driven depth increase. Phenomenon likely robust, but must re-verify post-fix.

---

### Slide 17 — TypeScript Port Fidelity
**Q1: Why not use a WASM build of Python hashlib?**
A: Philosophy: independent reconstruction, not binding. WASM adds binary dependency, build complexity. Pure TS BLAKE2b is functionally correct; byte-compatibility not required for structural validation.

**Q2: What is the KL divergence threshold for "match"?**
A: <0.05 for degree distribution. Empirically: 0.023. Chosen because: visible difference in plots at ~0.1, indistinguishable at ~0.01. 0.05 = conservative.

**Q3: Does hash divergence matter for the admitted phenomenon?**
A: No. mean_depth depends on lineage depth distribution (KS test p>0.05 ✓). Hashes used for exact reproducibility; structural validation uses statistical properties.

**Q4: Will you implement Koopman in TS?**
A: Only if Python implements first. Koopman requires numpy LA. Options: port numpy LA to TS (heavy), bind via WASM (complex), or accept Python-only for Koopman. Decision pending.

**Q5: How do you test cross-language without shared fixtures?**
A: Python runs experiment → exports JSON (nodes, arcs, tags) → TS imports → computes properties → compares. Fixtures generated by Python, consumed by TS. No shared fixture repo needed.

---

### Slide 18 — Limitations & Path Forward
**Q1: Why no SQLite yet?**
A: JSON export/import sufficient for current scale (10k nodes). SQLite adds dependency, migration complexity. Priority: defects → Koopman → gates → persistence. Persistence not blocking current experiments.

**Q2: Is Koopman the right tool for this substrate?**
A: Koopman analyzes dynamical systems via linear eigenfunctions. The Box is discrete, graph-based. Koopman on graph embeddings (node2vec, spectral) is established. Alternative: graph neural nets. Koopman chosen for interpretability.

**Q3: What would "discovered not explained" require?**
A: Exploratory search on larger parameter spaces (rulesets, schedulers, initial structures) → find statistic surviving G4 → ablate ALL rules → none explains it → run preregistered confirmation → DISCOVERED.

**Q4: Can you run distributed without persistence?**
A: Current: single process. Distributed needs: shared state (persistence), work distribution (queue), result aggregation. JSON files on NFS possible but fragile. SQLite → PostgreSQL → distributed queue is path.

**Q5: What is the priority order for fixes?**
A: 1) since_inflow (blocks QUIET semantics), 2) Rule.to_dict() (blocks reproducibility), 3) Koopman (enables gates), 4) Gates G1–G4 (enables windows), 5) Windows (statistical rigor), 6) Persistence (enables distributed), 7) Distributed (scale).

---

## ACT 3: SINGULARITY / ORACLE

### Slide 19 — SINGULARITY Phase 2
**Q1: Why Python 3.13 specifically?**
A: Pattern matching (match/case) for agent message handling, improved typing (Self, TypeGuard), performance gains. No 3.13-specific features that block backport to 3.11+.

**Q2: What does "genuine heterogeneity" mean operationally?**
A: Agents differ in: state representation (Greedy: current best; Adaptive: UCB1 arms), policy function (hill-climb vs bandit), communication interface (Communicator broadcasts, Skeptic challenges). Not same algorithm + different params.

**Q3: When will Phase 3 start?**
A: After P1 defects fixed and Koopman baseline established. Phase 3 (web viz) enables human-in-loop experiments which are next research step. No date — research pace.

**Q4: How do you enforce deterministic seeds across agents?**
A: Experiment engine assigns seed per trial. All agents, coordinator, verifier, environment receive same seed. RNG: Python random (global) + per-agent SplitMix64 (for internal stochasticity).

**Q5: What is the "independent verification" principle in practice?**
A: Verifier module (singularity/verification/verifier.py) imports environment ground truth, never agent code. Receives agent proposal → computes true value → returns verified_quality. Coordinator uses verified_quality for reputation.

---

### Slide 20 — ORACLE Architecture
**Q1: Why not microservices?**
A: "No microservices without demonstrated need" (CL-0018). Current scale: 24k evals/experiment, 10 min runtime. Single VPS handles. Microservices add: network latency, deployment complexity, debugging difficulty, partition bugs.

**Q2: How does the adapter handle SINGULARITY's internal state?**
A: Adapter creates fresh SINGULARITY engine per experiment run. No shared state across runs. Engine is pure function: (config, seed) → results. State isolated per trial.

**Q3: What is the concurrency model (async vs sync)?**
A: FastAPI async for HTTP. SINGULARITY engine sync (CPU-bound). Adapter runs engine in thread pool (run_in_executor) to not block event loop. SSE for log streaming.

**Q4: How do you handle long-running experiments in HTTP?**
A: POST /api/experiments returns run_id immediately. SSE /api/experiments/{id}/logs streams progress. GET /api/experiments/{id}/status polls. No long-held HTTP connections.

**Q5: Why single VPS not distributed?**
A: Research question: agent coordination, not infrastructure. Single VPS eliminates network variables. Phase 5 (distributed persistence) when evidence demands. Current bottleneck: not compute.

---

### Slide 21 — Five Heterogeneous Agents
**Q1: Why these 5 — how were they chosen?**
A: Cover strategic archetypes: exploitation (Greedy), risk-aversion (Conservative), information sharing (Communicator), quality control (Skeptic), meta-learning (Adaptive). Minimal set for "genuine heterogeneity."

**Q2: What is the communication protocol (message schema)?**
A: {type: PROPOSE|CHALLENGE|BROADCAST|ACCEPT, payload: {...}, agent_id, timestamp, seed}. JSON over in-process queue (SINGULARITY) or Redis (ORACLE). Versioned in singularity/coordination/protocol.py.

**Q3: Can agents be added/removed at runtime?**
A: Coordinator supports dynamic registration. Experiment config defines agent roster per trial. Not tested mid-trial. Phase 3 (web viz) may enable live agent injection.

**Q4: How does reputation prevent groupthink?**
A: Reputation = EMA of VERIFIED quality. If all agents converge to same wrong solution, verified quality drops → reputation drops → weight drops → exploration increases (bandit). Skeptic challenges accelerate correction.

**Q5: Are there agents that *decrease* collective performance?**
A: E1 shows collaborative (all 5) < single. But which agent? Ablation not run. Hypothesis: Communicator broadcasts noise; Skeptic challenges good solutions. Phase 4 (agent ablation studies) planned.

---

### Slide 22 — Coordination Mechanism
**Q1: What is the reputation update formula exactly?**
A: rep_t = 0.9×rep_{t-1} + 0.1×verified_quality. verified_quality ∈ [0,1] (normalized). New agents: rep_0 = 1.0. Minimum weight floor: 0.05. Decay for inactivity: -0.01/step no proposal.

**Q2: How do you handle cold-start (new agents, zero reputation)?**
A: New agents start at 1.0 (neutral). Bandit exploration ensures they propose. If proposals verified good → reputation rises. If bad → decays to floor. No special cold-start logic needed.

**Q3: Can bandit adaptation cause instability?**
A: UCB1 has logarithmic regret bound. Exploration bonus decays as arms pulled. Instability risk: non-stationary rewards (environment changes). Current environments static → stable. Dynamic environments → need sliding window UCB.

**Q4: What prevents reputation collapse (one agent dominates)?**
A: Minimum weight floor (0.05). Reputation decay for inactivity. Verified quality based on GROUND TRUTH — if dominant agent stops improving, its verified quality drops, reputation decays.

**Q5: Is the communication synchronous or async?**
A: Async. Communicator broadcasts every N steps (fire-and-forget). Skeptic challenges on receipt (event-driven). Coordinator collects proposals with timeout (default 5s). No synchronous rounds.

---

### Slide 23 — Verification Engine
**Q1: What if ground truth is expensive to compute?**
A: Current environments cheap (Rastrigin: ~1μs/eval). If expensive: cache verified results (LRU), approximate verification (surrogate model), or accept probabilistic verification (Monte Carlo). Not yet needed.

**Q2: How do you handle stochastic environments?**
A: Verifier runs same seed → same stochastic trajectory. For inherently stochastic (no seed control): run N replicates, report mean ± CI. Verified_quality = mean. Discrepancy threshold widened.

**Q3: Can agents game the verifier?**
A: Agents never see verifier code or ground truth function. Only receive verified_quality scalar. Gaming = finding x that looks good to verifier but isn't — impossible because verifier IS ground truth.

**Q4: What is the verification latency budget?**
A: <50ms per verification (Rastrigin). For E2 (Resource Allocation): ~5ms (simple simulation). Total per trial: 200 evals × 50ms = 10s verification overhead. Acceptable.

**Q5: Does this scale to high-dimensional spaces?**
A: Verification cost = ground truth eval cost. Rastrigin n=100: still ~1μs. Neural net loss landscape: ~1ms. Verification scales with ground truth, not dimension. Bottleneck is ground truth, not verifier.

---

### Slide 24 — Protocol A vs B
**Q1: Why not always use Protocol B (more realistic)?**
A: Protocol B confounds algorithm quality with implementation speed. Protocol A isolates algorithmic contribution. Science needs Protocol A; engineering needs Protocol B. We provide both.

**Q2: How do you measure "wall-clock time" deterministically?**
A: time.perf_counter() in single process. No network, no GC pauses (Python GC deterministic-ish). For distributed: not applicable (single VPS). Protocol B for single-machine comparison only.

**Q3: What if communication overhead dominates in Protocol B?**
A: Then collaborative loses — which is the FINDING. Protocol B reveals real-world cost. If comm overhead > algorithmic benefit, collaboration fails in practice. That's valid data.

**Q4: Can you run both protocols on same experiment?**
A: Yes. Experiment config: budget_type: "evals" | "time", budget: 200 | 30. Engine handles both. Reports labeled with protocol. E1 used Protocol A; E2 can run both.

**Q5: How does this affect statistical power?**
A: Protocol A: fixed evals → fixed variance → power calculable. Protocol B: variable evals → heteroscedastic → power depends on time budget. We power for Protocol A (30 trials, d=0.5).

---

### Slide 25 — E1 Negative Result
**Q1: Why does collaboration hurt on Rastrigin?**
A: Rastrigin: many local minima, global at origin. Agents explore different basins. Sharing basin locations doesn't help escape — each must find global independently. Communication wastes evals on verification/broadcast.

**Q2: Is this specific to Rastrigin or general?**
A: Specific to Rastrigin + this coordination + these agents. E2 (Resource Allocation) may differ. General claim: "coordination overhead can exceed benefit on symmetric multimodal landscapes."

**Q3: What is the communication overhead in evaluations?**
A: Collaborative: ~40% evals on broadcast/challenge/verify. Single/Independent: 100% on search. Algorithmic (DE): 100% on search + gradient-free optimization.

**Q4: Did any seed show collaborative > single?**
A: 30 seeds. Collaborative median 0.58, Single median 0.72. Some seeds: collaborative > single (variance). But paired test: 30 differences, median negative, p<0.05.

**Q5: How does this compare to literature on cooperative optimization?**
A: Literature mixed: CMA-ES with population helps; particle swarm helps; but "island models" with migration often show diminishing returns. Our finding: reputation-weighted voting + bandit + verification overhead hurts on Rastrigin.

---

### Slide 26 — Statistical Rigor
**Q1: Why Holm-Bonferroni not Benjamini-Hochberg?**
A: FWER (family-wise error rate) control: probability of ANY false positive among 6 pairs. BH controls FDR (expected proportion). We want NO false positives for VERIFIED claims. Holm-Bonferroni is conservative but appropriate.

**Q2: What if normality fails — always Wilcoxon?**
A: Shapiro-Wilk on paired differences. If p<0.05 → Wilcoxon. In E1: most pairs normal → Welch's t-test. Collaborative vs Algorithmic: non-normal → Wilcoxon. Both reported.

**Q3: How do you handle tied ranks in Wilcoxon?**
A: Standard mid-rank assignment (average rank for ties). scipy.stats.wilcoxon handles automatically. Ties rare in continuous quality metric.

**Q4: Is 30 trials enough for bootstrap stability?**
A: 10,000 resamples of 30 → stable percentile CI. Bootstrap theory: n=30 sufficient for percentile CI if distribution not pathological. Verified by running bootstrap 100× — CI variation <1%.

**Q5: Do you correct across experiments (E1, E2, ...) or per experiment?**
A: Per experiment. Each experiment has its own hypothesis, pairs, correction. Cross-experiment correction would be meta-analysis — not yet needed (only E1 VERIFIED).

---

### Slide 27 — Limitations
**Q1: Will you test other environments where collaboration might help?**
A: E2 (Resource Allocation) — different structure (combinatorial, not continuous). E3/E4 planned: multi-modal with shared structure, adversarial. Collaboration may help where information sharing reduces search space.

**Q2: What is the timeline for Phase 3 (web viz)?**
A: After P1 (The Box defects) and P2 (E2 verification). Phase 3 enables human-in-loop experiments. No date — depends on defect fix velocity. Estimated 3-6 months from go-ahead.

**Q3: Can ORACLE run without historical SINGULARITY?**
A: No. Adapter imports singularity modules directly. SINGULARITY at ~/singularity/ (read-only). Could vendor-copy but violates "independent subsystem" principle. Phase 5 may extract interface.

**Q4: Why not use Ray or Dask for distribution?**
A: "No microservices without demonstrated need." Current scale: 10 min/experiment. Ray/Dask add: cluster management, serialization, debugging complexity. When Phase 5 needs >1000 trials parallel → evaluate.

**Q5: What would make you abandon the coordination hypothesis?**
A: Collaboration loses on 5+ diverse environments (E1–E5) with VERIFIED evidence. Or: coordination overhead proven theoretically necessary (no free lunch for this coordination class). Not yet.

---

## ACT 4: HERMES / SHOWCASE

### Slide 28 — HERMES Architecture
**Q1: How do agents discover opportunities?**
A: Research Agent: trend analysis (Google Trends API, Reddit Pushshift, HN Algolia). Optimization Agent: A/B test results, pricing experiments. Communicator: cross-agent insight sharing. Opportunity score = f(trend_velocity, market_gap, competitor_weakness).

**Q2: What prevents agent conflict (e.g., two Content agents same niche)?**
A: Orchestrator assigns niches via REBALANCE (weekly). Opportunity score includes niche saturation. Content agents register topic → orchestrator enforces diversification. Conflict → PAUSE → human resolves.

**Q3: How is revenue attributed to specific agents?**
A: Each agent has unique tracking IDs (UTMs, Stripe metadata, affiliate codes). Finance Agent aggregates. Verification: Orchestrator audits attribution monthly. Discrepancy → PAUSE → investigation.

**Q4: What is the Redis message schema?**
A: {type: PROPOSE|ACT|QUERY|RESPONSE|EVENT, from_agent, to_agent, payload, timestamp, seed}. Pub/sub for broadcasts, streams for agent↔orchestrator. Defined in hermes/protocol.py (planned).

**Q5: Why PostgreSQL not SQLite?**
A: Concurrent agents (9+) writing revenue, metrics, audit logs. PostgreSQL: connection pooling, row-level locking, JSONB for flexible payloads, replication for backup. SQLite: single writer, no horizontal scale.

---

### Slide 29 — Autonomy Rules
**Q1: How do you define "budget band" for pricing adjustments?**
A: ±20% of current price. Calibrated: enough for optimization (A/B test $29 vs $35), not enough for catastrophic loss (price $29 → $290). Band adjustable per agent type via orchestrator config.

**Q2: What constitutes a "pivot" vs "optimization"?**
A: Pivot: change agent type (Content→SaaS), platform (Twitter→LinkedIn), business model (free→paid). Optimization: A/B test headline, adjust price ±20%, change posting schedule. Orchestrator classifies via action schema.

**Q3: Can agents request approval asynchronously?**
A: Yes. MUST_REQUEST actions → Redis stream → human approval queue (web UI + email/Slack). Agent pauses that action, continues others. Human SLA: 24h for PAUSE review, 72h for strategic approval.

**Q4: What is the SLA for human response?**
A: PAUSE (policy violation): 24h mandatory review. Strategic approval (pivot, budget): 72h. Auto-escalation: no response → conservative default (deny pivot, maintain budget).

**Q5: How do you handle emergency (security incident) overrides?**
A: Orchestrator has EMERGENCY_STOP: kills ALL agents, freezes budgets, alerts human. Trigger: security webhook (Stripe fraud, domain abuse, DMCA). Human must manually resume each agent after audit.

---

### Slide 30 — Orchestrator Interventions
**Q1: How is "opportunity score" computed?**
A: trend_velocity (derivative of search volume) × market_gap (1 - competitor_density) × competitor_weakness (1 - avg_rating). Normalized 0–100. Threshold 90 = top 10% of observed opportunities.

**Q2: What prevents thrash (KILL→SPAWN→KILL)?**
A: KILL cooldown 7d, SPAWN cooldown 30d, minimum agent lifetime 14d before KILL eligible. REBALANCE max 20% budget shift/week. Thrash simulated in Phase 1 before live.

**Q3: Can REBALANCE starve long-tail agents?**
A: Bottom quartile loses budget, but minimum allocation floor (5% of initial). Long-tail = new agents (<14d) exempt from REBALANCE. Survival rate target >60% at 90 days monitors this.

**Q4: How do you detect policy violations automatically?**
A: Spam: content classifier (self-hosted) >0.8 threshold. Trademark: USPTO API + common law DB. ToS: platform-specific rules (Twitter automation, LinkedIn scraping). Finance Agent monitors.

**Q5: What is the false positive rate for PAUSE?**
A: Unknown — not deployed. Phase 1: run classifier on historical content, measure precision/recall. Target: precision >0.95 (few false pauses). False pause cost: human review time. False negative cost: platform ban.

---

### Slide 31 — HERMES Metrics & Reality
**Q1: What is the basis for $10k/month target?**
A: 5 content × $500 + 2 digital asset × $1000 + 1 SaaS × $2000 = $9500. Conservative: assumes each hits target, no bans, no holds. Reality: most fail. Target = falsification threshold (if <$1k at month 6 → abandon).

**Q2: How do you measure "human hours" accurately?**
A: Orchestrator API logs every human action: approval_time (decision), review_time (reading context). Automated timer starts on approval request, ends on submit. Weekly sum. No self-reporting.

**Q3: What if MRR is $5k at month 6 — pivot or persist?**
A: Pre-committed: if MRR <$1k at month 6 → abandon HERMES (falsification). $1k–$10k → extend Phase 5 (optimize), add niches, reduce human hours target. >$10k → scale.

**Q4: How do you handle payment processor holds/bans?**
A: Multiple processors (Stripe, Paddle, Lemon Squeezy). Finance Agent monitors account health. Hold → auto-switch to backup. Ban → KILL affected agents, human notified. Diversification is risk mitigation.

**Q5: Is this a research project or a startup?**
A: Research project: "Can autonomy scale with human oversight?" (Q3, Slide 9). Startup would optimize for revenue. We optimize for evidence. SPECULATIVE tier (CL-0019) — not a business plan.

---

### Slide 32 — Wi-Fi Time Machine & BLE Radar
**Q1: Why synthetic fixtures not live hardware?**
A: Philosophy: determinism, reproducibility, no hardware dependency. Live hardware: non-deterministic, requires specific OS/drivers, not portable. Synthetic fixtures from real captures = best of both.

**Q2: How do you validate parsing without real devices?**
A: Fixtures FROM real devices (captured once, anonymized). Parser tested against real frame formats. Behavioral logic (EMA, heatmap) tested with property-based tests on synthetic streams.

**Q3: What is the EMA α=0.3 justification?**
A: Half-life ≈ 3 seconds (ln(0.5)/ln(0.7) ≈ 2.5). BLE advertising interval ~100ms–1s. 3s half-life smooths noise without lagging behind movement. Tuned on synthetic random walk.

**Q4: Can hash→angle cause collisions?**
A: Yes. MAC → hash → angle. 360° resolution. 2^32 MAC space → collisions inevitable. But: visualization convention only. Angle ≠ physical direction. Collisions = overlapping dots on radar — acceptable.

**Q5: Will you add live scanning in Phase 2?**
A: Not planned. Philosophy: deterministic substrates. Live scanning → non-determinism → breaks reproducibility. If needed: separate "live adapter" package, not core demo.

---

### Slide 33 — Process Ecosystem & Generative Engine
**Q1: How do you generate synthetic /proc snapshots?**
A: Recorded real /proc sequences on Linux 6.x. Anonymized PIDs, cmd names. Inject PID reuse events, orphan re-homing, CPU spikes. Fixtures versioned in tests/fixtures/.

**Q2: What is the PID-reuse detection false positive rate?**
A: Fingerprint = (start_time, cmd_hash). Collision if same PID reused within same second with same cmd. Probability: negligible (PID space 32768, 1s granularity). Tested: 0 false positives in 10k synthetic sequences.

**Q3: Why splitmix64 not PCG or Xoroshiro?**
A: splitmix64: 64-bit state, single function, no BigInt issues in JS (uses number + bitwise), good statistical quality (passes BigCrush), deterministic across languages. PCG needs 128-bit state. Xoroshiro needs BigInt.

**Q4: Can the attractor params be user-controlled?**
A: Demo has parameter sliders (a,b,c,d for Clifford/Dejong). Seed fixed per session. User can explore parameter space deterministically. No random mutation — philosophy: determinism.

**Q5: What were the 5 failing tests in original?**
A: Original Python project (not our port) had 5 failing tests. Likely: RNG differences, floating-point precision, attractor divergence. Our TS port: 24/24 pass. We didn't replicate failures — not our codebase.

---

### Slide 34 — The Box TS Port
**Q1: Do the 102 tests include the defect-triggering cases?**
A: Yes. Since_inflow: test creates node, waits 5 steps, checks starvation=5 (not 50). Rule.to_dict(): test serializes rules, checks FUSE present, runs 300 steps, checks fire count=5. TS passes; Python fails.

**Q2: How do you handle YAML parsing differences?**
A: Python: PyYAML. TS: js-yaml. Both load same foundry.yaml. Validation test: load in both → compare rule objects (name, predicates, effects) → deep equality. 100% match.

**Q3: Can the TS port run the full 900-step experiment?**
A: Yes. `npm run experiment -- --seed 1 --steps 900`. Runs in ~30s (vs Python ~18min for full validation suite). Produces same trajectory (structural properties). Used for R1/R5/R6 replication.

**Q4: What is the performance difference (Python vs TS)?**
A: TS ~2× slower for 900 steps (V8 JIT warmup, GC pressure). Python: 18min for 557 tests (includes 900 surrogates × 5 nulls). TS: 30s for 102 tests (no surrogates). Different workloads.

**Q5: Will you add the missing features to TS?**
A: Only if Python adds first. Koopman, gates, persistence, CLI — Python leads, TS follows. Philosophy: independent reconstruction from same spec. TS port tracks Python fidelity.

---

### Slide 35 — Build Metrics & Philosophy
**Q1: How do you achieve zero deps for charts/visualization?**
A: Custom Canvas 2D API. Heatmap: ctx.fillRect per cell. Radar: ctx.arc + ctx.lineTo per point. Tree: recursive layout + ctx.strokeText. Attractor: ctx.fillRect per point. No D3, no Chart.js, no Three.js.

**Q2: What is the gzipped size?**
A: ~45 kB gzipped (160.69 kB raw). Measured: `gzip -c dist/assets/index-*.js | wc -c`. Acceptable for static hosting.

**Q3: How do you test Canvas/WebGL code?**
A: Property-based: generate random inputs → render to OffscreenCanvas → read pixels → assert invariants (color ranges, point counts, bounds). Snapshot: render reference → compare pixel hashes (CI).

**Q4: Why not use a charting library?**
A: Philosophy: independent reconstruction, zero deps, determinism. Chart.js: 50 kB, non-deterministic animations, theme assumptions. Custom: 5 kB, fully controlled, testable.

**Q5: Can this approach scale to larger apps?**
A: For research demos: yes. For product apps: maybe not (accessibility, i18n, complex state). We use this for substrates + demos. Products would use framework — but substrate stays zero-dep.

---

### Slide 36 — HERMES/Showcase Synthesis
**Q1: How does verification engine translate to revenue audit?**
A: ORACLE verifier: recompute f(x) from x. HERMES audit: recompute revenue attribution from (agent_action, platform_event, payment_event). Ground truth: Stripe webhook + platform API + agent log. Same pattern: independent recomputation.

**Q2: What is the "ground truth" for HERMES?**
A: Payment processor (Stripe) = ground truth for revenue. Platform API (Twitter, LinkedIn) = ground truth for reach. Agent log = ground truth for action. Finance Agent reconciles all three. Discrepancy → investigation.

**Q3: Can Showcase demos be used as HERMES agent tools?**
A: Yes. Process Ecosystem → Infrastructure Agent (monitoring). Generative Engine → Content Agent (visual assets). Wi-Fi/BLE → Research Agent (environment sensing). The Box → Optimization Agent (structure search).

**Q4: What stochasticity breaks the philosophy?**
A: LLM output (non-deterministic), platform algorithm changes (non-stationary), market demand (uncontrollable). Philosophy handles: log everything, seed where possible, verify against ground truth, human-in-loop for strategy.

**Q5: Is HERMES just Showcase + money?**
A: No. Showcase = deterministic substrates (physics, math, parsing). HERMES = stochastic autonomy (markets, platforms, LLMs). Bridge: verification primitive. Showcase proves we build correct deterministic systems. HERMES asks: can we verify stochastic ones?

---

## ACT 5: SYNTHESIS

### Slide 37 — Three Substrates, One Philosophy
**Q1: Why no shared codebase?**
A: Substrates have different domains (graph kernel, agent coordination, economic autonomy). Shared codebase creates coupling, forces premature abstraction. Philosophy = discipline, not library. Each substrate reimplements patterns independently.

**Q2: Can the philosophy be codified as a linter?**
A: Partially: deterministic seeds (check for random.seed), no mocks (check for unittest.mock), fidelity labels (check for comment). But "independent reconstruction" and "honest limitations" require human review. Social contract > tooling.

**Q3: What would "Level 5" fidelity mean?**
A: Formal verification (Coq/Lean proofs of kernel properties), cross-language byte-compatibility (WASM BLAKE2b), distributed consensus on state. Not on roadmap — research substrates, not certified systems.

**Q4: How do you onboard new contributors to the philosophy?**
A: CONTRIBUTING.md (planned) with: read THE_BOX_MASTER_DOCUMENTATION.md, run 557 tests, fix one defect, add CL-XXXX to PR. Mentorship: pair on first PR. Philosophy transmitted by practice, not document.

**Q5: Is this philosophy specific to your projects or generalizable?**
A: Generalizable: any research software benefits from: independent reconstruction (catches assumptions), real calculations (catches mocks), determinism (enables reproducibility), intermediate stages (enables debugging), honest fidelity (prevents hype). We're not unique — just explicit.

---

### Slide 38 — Verification Primitive
**Q1: Why not use property-based testing instead?**
A: PBT checks code properties (∀input: property(output)). Verification checks TRUTH: recompute from ground truth. PBT: "sort output is sorted." Verification: "sort output equals reference sort." Different epistemic level.

**Q2: How do you handle non-deterministic ground truth?**
A: Run N replicates with same seed → mean ± CI. Verified_quality = mean. Discrepancy threshold = CI width. If ground truth inherently non-seedable: accept probabilistic verification, label EXPERIMENTAL.

**Q3: What is the performance cost of verification?**
A: ORACLE: ~50ms/eval (Rastrigin). The Box null models: 900 surrogates × 5 nulls = 4500 derivations per experiment. HERMES: audit log append-only (O(1)). Cost budgeted per experiment design.

**Q4: Can verification itself be verified?**
A: Verifier code is pure function: (input, ground_truth) → report. Tested with property-based tests (known inputs → known outputs). Verifier has no internal state. Trust base: ground truth implementation (Rastrigin, Stripe API).

**Q5: Is this "verification" or "validation" in V&V terms?**
A: Verification: "did we build the system right?" (code matches spec). Validation: "did we build the right system?" (system meets needs). Our primitive: "does the output match ground truth?" = output validation. Closer to validation.

---

### Slide 39 — Negative Results Are Data
**Q1: Have you tested environments where collaboration *should* help?**
A: E2 (Resource Allocation) — combinatorial, information sharing may reduce search. E3/E4 planned: shared structure, adversarial. Not yet run. E1 negative is specific, not general.

**Q2: Is the negative result specific to reputation-weighted voting?**
A: Yes. Tested: 5 agents + reputation-weighted voting + bandit + verification. Other coordination: consensus, auction, gradient-sharing — not tested. Finding: THIS coordination hurts on Rastrigin.

**Q3: How do you distinguish "not yet working" from "fundamentally doesn't work"?**
A: VERIFIED negative = 30 trials, Holm-Bonferroni, bootstrap CI, power analysis. "Not yet working" = EXPERIMENTAL (E2) or SPECULATIVE (HERMES). Tier tells you evidence strength.

**Q4: Will you publish the negative result?**
A: Yes. ORACLE E1 negative result is VERIFIED. We treat it as a finding. Publication venue: ML systems workshop or arXiv. Evidence registry is the pre-publication record.

**Q5: What would change your mind about coordination?**
A: VERIFIED positive on E2, E3, or E4 (collaboration beats algorithmic). Or: theoretical proof that reputation-weighted voting is suboptimal for this class. Or: new coordination mechanism that VERIFIED helps.

---

### Slide 40 — Defects, Gaps, Limitations
**Q1: Which limitation would you fix first if resources unlimited?**
A: The Box since_inflow defect (blocks QUIET semantics, distorts all dynamics). Then Rule.to_dict() (blocks reproducibility). Then Koopman (enables gates). These three unblock The Box Level 4.

**Q2: How do you prioritize across projects?**
A: Dependency graph: The Box defects → Koopman → gates → ORACLE benchmarks → HERMES Phase 1. HERMES blocked by The Box maturity (substrate for Optimization Agent). ORACLE blocked by SINGULARITY Phase 3.

**Q3: Is there a technical debt budget?**
A: No formal budget. 20% rule: 1 day/week on defects, 4 days on research. Currently: The Box defects are research blockers (not just debt). HERMES has no debt — not built yet.

**Q4: What limitations are architectural vs implementation?**
A: Architectural: The Box arc-incidence (fixed), SINGULARITY single-process (Phase 5), HERMES human-in-loop (by design). Implementation: since_inflow bug, Rule.to_dict(), no SQLite, no CI/CD. Architectural = choice; implementation = fixable.

**Q5: How do you prevent new limitations while fixing old?**
A: Philosophy enforcement: new code must pass validation (cross-lang, determinism, intermediate stages). PR review checks for CL-XXXX, fidelity label, limitation section. Defects caught by independent reconstruction (TS port caught Python defects).

---

### Slide 41 — Open Problems
**Q1: What is the dependency between P1 and P2?**
A: P1 (The Box Koopman) → Optimization Agent in HERMES uses Koopman for structure search. P2 (ORACLE benchmarks) independent. P3 (HERMES) uses The Box as substrate. Loose coupling — lanes can parallelize.

**Q2: Why are cognitive projects separate?**
A: nexus-titan, nox, echo: different paradigm (cognitive architectures vs substrates). No fidelity, no tests, no philosophy applied. Decision: apply philosophy (P5) or archive. Not integrated yet.

**Q3: What would make you deprioritize HERMES?**
A: Phase 1 deployment fails (payment processor rejection, platform ban, human hours >50/week). Or: The Box/ORACLE produce VERIFIED findings that redirect resources. HERMES is SPECULATIVE — lowest evidence tier.

**Q4: How do you fund 5-year research?**
A: Self-funded (consulting, grants, stipends). No VC (misaligned incentives). HERMES revenue target is research hypothesis, not funding plan. If HERMES VERIFIED → self-sustaining research.

**Q5: What is the "minimum viable" for each P?**
A: P1: defects fixed + Koopman prototype. P2: E2 VERIFIED + Phase 3 demo. P3: Phase 1 live + 1 agent earning $100/mo. P4: verify() interface spec + 2 implementations. P5: decision (integrate/archive) + 1 project at Level 3.

---

### Slide 42 — Reproducibility Artifacts
**Q1: Are there hardware requirements (GPU, specific OS)?**
A: No GPU. All CPU. OS: Linux (primary), macOS (tested), Windows (WSL2). Python 3.13, Node 20, Docker. The Box Python: numpy optional (Koopman only). ORACLE: Ollama optional (local LLMs).

**Q2: How long does a full experiment take?**
A: The Box R1: ~18 min (557 tests including 900 surrogates). ORACLE E1: ~10 min (24k evals). Showcase: ~30s (182 tests). SINGULARITY E1: ~8 min (direct, no HTTP).

**Q3: Can I run ORACLE without the historical SINGULARITY?**
A: No. Adapter imports singularity modules. SINGULARITY at ~/singularity/ required. Could vendor-copy but violates principle. Contact for SINGULARITY repo access.

**Q4: Are the synthetic fixtures in showcase reproducible?**
A: Yes. Fixtures generated by deterministic scripts (seeded). Stored in tests/fixtures/. `npm test` loads fixtures → deterministic results. No network, no hardware.

**Q5: What Python/Node versions are pinned?**
A: Python 3.13 (pyproject.toml), Node 20 (package.json engines), Docker base: python:3.13-slim, node:20-alpine. Exact versions in lockfiles (poetry.lock, package-lock.json).

---

### Slide 43 — Social Contract
**Q1: How do you enforce these in practice?**
A: PR template: requires CL-XXXX references, evidence tier, limitation section. CI: runs tests, validation, cross-lang check. Review: checks for fidelity label, negative result honesty, independent reconstruction. No merge without passing.

**Q2: What happens when principles conflict?**
A: Hierarchy: Evidence > Narrative (1), Negative results > Positive spin (2), Limitations > Hype (3). Example: if independent reconstruction (4) conflicts with code reuse → reconstruct. If determinism (5) conflicts with LLM call → log seed, verify output.

**Q3: Is this documented in a CONTRIBUTING.md?**
A: Planned. Current: implicit in PR reviews, explicit in this deck (Slide 43). Writing CONTRIBUTING.md is "good first issue" for contributors.

**Q4: How do you handle external contributors?**
A: Same standards. First PR: reproduce one experiment (R1 or E1), add CL-XXXX, fix one defect. Mentorship provided. No exceptions to evidence tier or fidelity honesty.

**Q5: Which principle is most often violated?**
A: "Limitations advertised" — temptation to hide defects in footnotes. Slide 18, 27, 31, 40 exist because we caught ourselves. "Negative results published" — temptation to re-run until positive. E1 negative survived because VERIFIED.

---

### Slide 44 — Call to Action
**Q1: How do I get access to private repos?**
A: Email [contact] with: GitHub handle, research interest, which repo(s). Access granted for replication/falsification/extension. No NDAs — evidence registry is public contract.

**Q2: What compute resources needed for replication?**
A: The Box R1: 2 CPU cores, 4 GB RAM, 18 min. ORACLE E1: 2 CPU cores, 4 GB RAM, Docker, 10 min. Showcase: any modern browser. No GPU, no cluster.

**Q3: Is there a replication package (Docker, conda)?**
A: The Box: `docker build -t the-box .` (Dockerfile in repo). ORACLE: `docker compose up`. Showcase: `npm run dev` (no container needed). Conda env in repo (environment.yml).

**Q4: What counts as successful falsification?**
A: The Box: statistic surviving G4, not explained by DESCEND (ablation shows no rule removal collapses it). ORACLE: collaboration beats algorithmic on any environment (VERIFIED: 30 trials, p<0.05, Holm-Bonferroni). Co-authorship on rebuttal.

**Q5: Are you accepting PhD students / postdocs?**
A: Yes. Research areas: The Box (Koopman, defects), ORACLE (E2–E4, Phase 3), HERMES (Phase 1–2), Verification framework. Self-funded or grant-supported. Contact for discussion.

---

### Slide 45 — Closing
**Q1: What is the ultimate goal — AGI, science, product?**
A: Science: understanding substrates. What minimal rules generate open-endedness? Does coordination help or hurt? Can autonomy scale with oversight? Not AGI, not product. Substrates are the contribution.

**Q2: How do you know when a substrate is "done"?**
A: The Box: Level 4 fidelity + DISCOVERED phenomenon. ORACLE: VERIFIED results on 5+ environments. HERMES: VERIFIED revenue + <8 hrs human. "Done" = evidence tier VERIFIED for core claims.

**Q3: What would make you stop this program?**
A: The Box: defects unfixable, no discovered phenomenon after Koopman. ORACLE: collaboration loses on 5+ environments VERIFIED. HERMES: Phase 1 fails falsification. Program stops when substrates falsified.

**Q4: Can substrates compose?**
A: The Box (relational) → Optimization Agent in HERMES. ORACLE (coordination) → HERMES orchestrator. HERMES (autonomy) → future substrate for meta-autonomy. Composition = research question (P4 verification unification).

**Q5: Final words for the audience?**
A: We build substrates, not solutions. Substrates expose mechanisms; solutions hide them. The evidence registry is the contract: 27 claims, 4 experiments, 24 projects. Every claim traces to CL-XXXX. Replicate, falsify, extend. The work continues. Thank you.
