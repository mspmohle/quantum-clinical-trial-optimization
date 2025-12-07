
**Quantum Clinical Trial Optimization (AWS Braket + Large-Scale CT.gov Corpus)**

This repository demonstrates an end-to-end workflow for large-scale clinical trial ingestion (ClinicalTrials.gov XML at corpus scale) and portfolio-style optimization of candidate trials using:
Classical baselines (greedy / exact-when-small)
QUBO formulation
Quantum-inspired / quantum execution paths:
Local QAOA simulation (optionally with Qiskit Aer)
AWS Braket SV1 QAOA execution with results persisted to S3
The goal is to be reproducible and artifact-driven: each notebook writes versioned outputs to data/results/ and outputs/figures/ (and optionally outputs/slides/).

**Repository Structure**
```text
.
├── data/
│   ├── interim/              # large local artifacts (often gitignored)
│   ├── results/              # reproducible outputs committed when reasonable
│   └── summary/              # small rollups and profiling CSVs
├── outputs/
│   ├── figures/              # plots saved from notebooks
│   └── slides/               # generated PPTX (optional, may be gitignored)
├── docs/                     # (optional) deeper writeups
├── *.ipynb                   # numbered notebooks (pipeline + experiments)
└── README.md


Python Artifacts

00_generate_reference_tables.py — Generates small reference tables used downstream (e.g., phase cost factors, region multipliers, lookup scaffolding) so scenario notebooks can join “known” inputs consistently.

01_clinical_trials_ingestion.ipynb — Ingests the ClinicalTrials.gov XML corpus from S3, parses/normalizes trial metadata at scale, and writes intermediate parquet plus sample/summary CSV artifacts for GitHub.

01_qubo_portfolio_baseline_demo.ipynb — Toy QUBO “portfolio” demo to validate the end-to-end flow (QUBO build → decode → objective evaluation) before applying it to trials.

02_qubo_qaoa_parameter_sweep.ipynb — Runs a parameter sweep over QAOA angles (γ, β) on a small QUBO to establish baseline behavior and tuning workflow.

02_scenario_prep_and_risk_features.ipynb — Builds a scenario-ready table from trial metadata by engineering cost/risk/feasibility features and preparing joinable columns for optimization.

02b_maude_safety_reference_and_mapping.ipynb — Prepares MAUDE-derived safety signal references and maps sponsor/manufacturer names to enable safety-feature joins onto trials.

02c_benefit_scoring_and_scenarios.ipynb — Defines/derives a benefit signal and produces scored candidates suitable for scenario slicing.

02d_define_scenarios_A_B.ipynb — Carves out Scenario A and B slices (filters/IDs/candidate exports) so later notebooks consume stable scenario inputs.

03_qaoa_optimizer_refinement.ipynb — Refines QAOA evaluation/decoding utilities (objective computation, penalties, sampling) to improve reliability and debugging.

03a_scenario_selection_baseline.ipynb — Establishes a baseline selection workflow for a scenario (data checks, candidate selection logic, early outputs).

03b_qubo_construction_and_classical_baseline_scenario_B.ipynb — Constructs Scenario B’s QUBO and runs a classical baseline solver; writes best bitstring/selected trials/summary artifacts.

03b_qubo_design_for_trial_selection.ipynb — Design-focused notebook documenting the QUBO formulation choices for trial selection (objective terms + constraints).

03c_qubo_classical_solver_and_comparison.ipynb — Runs/compares classical approaches (exact/greedy/heuristic as applicable) and summarizes performance and selections.

03d_qaoa_sv1_run.ipynb — Early AWS Braket SV1 QAOA execution notebook for a scenario (submit tasks, retrieve results, decode).

03e_scenario_A_pipeline.ipynb — End-to-end Scenario A pipeline: candidate prep → QUBO build → classical baseline outputs written to data/results.

03f_qaoa_for_scenario_A_local_then_sv1.ipynb — Runs Scenario A QAOA locally first (for iteration), then on SV1 for the “AWS quantum” demo.

04_results_comparison_and_figures.ipynb — Produces cross-method comparison tables/plots (objective vs stability/overlap) and writes figures for README/slides.

04a_braket_qaoa_scenario_A.ipynb — Scenario A QAOA execution on AWS Braket (SV1), including result decoding and artifact export.

05a_robustness_sweeps_scenario_A_greedy.ipynb — Robustness sweeps for Scenario A using a greedy/classical approach across K/λ/noise; writes sweep summaries + top configs.

05b2_robustness_sweeps_scenario_A_qaoa_aer.ipynb — Scenario A robustness sweeps using QAOA with Aer (local simulator), targeting repeatability and speed.

05b_robustness_sweeps_scenario_A_qaoa.ipynb — Scenario A robustness sweeps using QAOA with fallback modes (Aer-free vs Aer), checkpointing, and summary artifacts.

05c2_compare_greedy_vs_qaoa_vs_qaoa_aer_scenario_A.ipynb — Compares Scenario A greedy vs QAOA vs QAOA(Aer): deltas, overlaps, plots, and “best by method” tables.

05c_compare_greedy_vs_qaoa_scenario_A.ipynb — A lighter-weight comparison notebook for Scenario A: greedy vs QAOA only.

06a_scenario_B_candidate_build.ipynb — Builds Scenario B candidate pool with engineered columns (benefit/cost/safety + any pool scoring) for downstream QUBO/QAOA.

07a_robustness_sweeps_scenario_B_greedy.ipynb — Scenario B greedy robustness sweeps across hyperparameters/noise, exporting sweep and top-config artifacts.

07b_robustness_sweeps_scenario_B_qaoa.ipynb — Scenario B QAOA robustness sweeps (local), with checkpointing and stability metrics (e.g., Jaccard).

07c_compare_greedy_vs_qaoa_scenario_B.ipynb — Scenario B comparison notebook producing summary tables/overlap artifacts and figures.

08a_aws_braket_qaoa_scenario_B_sv1.ipynb — AWS Braket SV1 QAOA run for Scenario B, including pool-size reduction to fit qubit limits and decoding from S3 results.

09a_scenario_C_candidate_build.ipynb — Builds Scenario C candidates (inputs + engineered scoring columns) to support a third scenario end-to-end.

09b_qubo_scenario_C_classical_baseline.ipynb — Constructs Scenario C QUBO and runs the classical baseline; writes best bitstring, selected trials, and summary CSVs.

09c_aws_braket_qaoa_scenario_C_sv1.ipynb — Runs Scenario C QAOA on SV1 (AWS), exporting task tracking and decoded best result artifacts.

09d_compare_classical_vs_sv1_scenario_C.ipynb — Compares Scenario C classical baseline vs SV1 outcome (objective/overlap and any derived plots/tables).

10a_readme_results_refresh.ipynb — Regenerates “latest results” tables/figures so README stays consistent with the current artifacts in data/results and outputs/figures.

10b_slides_deck_generator.ipynb — Builds the showcase PPTX from the project’s exported tables/figures/results for a technical presentation-ready deck.

10d_braket_resume_decode.ipynb — “Resume/repair” decoder for Braket SV1 tasks: pulls results.json from S3 prefixes, extracts measurements/counts, and writes a best-result JSON locally.

Key outputs and where to find them
Results tables (data/results/)
Classical baselines: scenario_*_classical_summary.csv, *_selected_trials.csv, *_best_bitstring*.txt
Robustness sweeps: 05a_*_sweep_summary.csv, 05b_*_sweep_summary.csv, 07a_*, 07b_*
Cross-method comparisons: 05c*, 07c*, 09d* tables (e.g., best-by-method, overlaps)
Figures (outputs/figures/)
Comparison plots (objective vs stability, overlaps)
Sweep visualizations (by K / lambdas / noise)
Slides (outputs/slides/)
quantum_clinical_trial_optimization_showcase.pptx (generated via 10b_slides_deck_generator.ipynb)
AWS Braket task outputs (S3)
Bucket: amazon-braket-us-west-2-<account-id>
Prefixes: clinical-trials-data/results/sv1_tasks/scenario_*/<task-id>/results.json
Local decoded “best” snapshots: _08a_sv1_best_scenario_B.json, _09c_sv1_best_scenario_C.json (in data/results/)

How to reproduce

1) Environment setup
  1. Clone + enter repo
    git clone https://github.com/mspmohle/quantum-clinical-trial-optimization.git
    cd quantum-clinical-trial-optimization

  2  Create/activate your Python environment
  If you have an environment.yml in the repo:
    conda env create -f environment.yml
    conda activate quantum-clinical-trial-optimization

  Otherwise, activate your existing env and confirm it’s the one Jupyter will use:
    conda activate quantum-clinical-trial-optimization
    which python
    python -V

 3 Launch Jupyter
  jupyter lab

2) AWS prerequisites (for Braket + S3-backed runs
  1. AWS credentials + region
    aws sts get-caller-identity
    aws configure get region
  This project uses us-west-2 for Braket runs.
-----
Braket results bucket rule
  Braket tasks must write to an amazon-braket-* bucket (service-managed style), not your project bucket.
  You’ll see task outputs under a prefix like: s3://amazon-braket-us-west-2-<acct>/clinical-trials-data/results/sv1_tasks/scenario_*/<task-id>/results.json
If you hit InvalidSignatureException: Signature expired refresh your AWS credentials/session (common with temporary creds), then re-run the notebook cell that calls task.result() or the decode-from-S3 step.

3) Recommended notebook run order

Option A — Fast “reviewer demo” (no re-ingestion of ~557k XMLs)
    05a_* / 05b_* / 05c* (Scenario A robustness + comparisons)
    06a_* then 07a_* / 07b_* / 07c_* (Scenario B build + sweeps + comparisons)
    09b_* then 09c_* (Scenario C classical baseline + SV1 run / decoding)
    10b_slides_deck_generator.ipynb (build PPTX)
Option B — Full pipeline (rebuild metadata from the CT.gov XML corpus in S3)
    01_clinical_trials_ingestion.ipynb (long-running; produces the full local parquet)
    Scenario build notebooks (A/B/C) → QUBO baselines → sweeps → comparisons → Braket SV1

4) Runtime expectations 
Robustness sweeps (05a/05b, 07a/07b): can be minutes to hours depending on grid size, seeds, pool size, Aer vs non-Aer mode, and checkpoint cadence.
Braket SV1 notebooks (08a, 09c): wall-clock depends on queue time + shots + parameter grid. Expect tens of minutes for even small grids, longer if expanded.

5) What “success” looks like
  New/updated tables appear under data/results/
  New figures under outputs/figures/
  SV1 tasks visible via:
    aws braket search-quantum-tasks --region us-west-2 \
    --filters name=deviceArn,operator=EQUAL,values=arn:aws:braket:::device/quantum-simulator/amazon/sv1 \
    --max-results 20

## Method: QUBO formulation (trial portfolio selection)
We model trial selection as a **binary portfolio optimization** problem.

### Decision variables
For a scenario with `n` candidate trials, define:
- `x_i ∈ {0,1}` where `x_i = 1` means trial *i* is selected.

### Objective (maximize value, penalize cost + safety risk)
Each trial has engineered components (names vary slightly by notebook/export, but conceptually):
- `benefit_i` (higher is better)
- `cost_i` (higher is worse)
- `safety_i` (higher risk is worse)
We build a scalar score to optimize (often re-expressed as a minimization energy):
- **value** term: `- benefit_i`
- **cost** term: `+ λ_cost · cost_i`
- **safety** term: `+ λ_safety · safety_i`
So the unconstrained objective can be written as:
- Minimize:  `Σ_i ( -benefit_i + λ_cost·cost_i + λ_safety·safety_i ) · x_i`

> Note: Some notebooks normalize components or store raw vs normalized columns. The key is that *benefit pushes selection on*, while *cost/safety push selection off* via their lambdas.

### Constraint: portfolio size `K`
We enforce a portfolio size target using a quadratic penalty:
- `(Σ_i x_i - K)^2`
Scaled by a penalty coefficient `A`:
- `A · (Σ_i x_i - K)^2`
This expands into linear + quadratic terms and yields a standard QUBO:
- Minimize: `x^T Q x`
Where `Q` is an `n×n` matrix (or an equivalent sparse dict) containing:
- diagonal terms: per-trial linear contributions + penalty linear terms
- off-diagonals: penalty-induced couplings between trials

### Solvers used in this repo
- **Classical baseline (greedy / heuristic)**  
  Produces deterministic selections and is used as the “fast anchor” for comparisons.
- **QAOA (local + Aer when available)**  
  Runs parameter grids over `(γ, β)` for `p=1` and decodes sampled bitstrings.
- **AWS Braket SV1 QAOA**  
  Same decoding logic, but execution happens on SV1 with results stored in the Braket results bucket.

### Decoding: bitstring → selected trials → score
Given a measured bitstring `s`:
- Convert `s` into `x ∈ {0,1}^n`
- Selected set is `{ i | x_i = 1 }`
- Evaluate:
  - QUBO energy `E = x^T Q x`
  - any “human” objective components (benefit/cost/safety sums)
  - stability/overlap vs baselines (e.g., Jaccard similarity)

### Practical constraint: SV1 qubit limits
SV1 has a fixed maximum qubit count, so SV1 notebooks apply a **pool/subset strategy**:
- rank candidates using a cheap heuristic score
- select a pool of size `n_pool` that fits on SV1
- solve the pooled QUBO on SV1
- decode pooled bitstrings back to global trial IDs

This keeps the pipeline faithful to the **large-data** setting while respecting simulator constraints.


## AWS Braket implementation notes
This repo includes **end-to-end AWS Braket SV1 runs** for QAOA, with results decoded back into trial selections and compared to classical baselines.

### Braket device + region
- Device ARN (SV1): `arn:aws:braket:::device/quantum-simulator/amazon/sv1`
- Region used in notebooks/CLI: `us-west-2`

### Output bucket rule (important)
Braket quantum tasks must write results to an **`amazon-braket-*`** bucket. If you try to use a normal project bucket (e.g., `quantum-clinical-optimization-us-west-2`) as the Braket destination, task creation will fail.

Typical task output layout:
- `s3://amazon-braket-us-west-2-<account-id>/clinical-trials-data/results/sv1_tasks/scenario_<X>/<task-id>/results.json`

### Task submission pattern
SV1 notebooks submit a parameter grid over `(γ, β)` (and sometimes multiple seeds/configs):
- build QAOA circuit (p=1)
- submit to SV1 with `shots = N`
- track task ARNs (CSV “task table” artifacts)
- optionally resume/repair decoding later from S3

### Results decoding (results.json schemas)
SV1 `results.json` may contain **either**:
- `measurement_counts` (counts keyed by bitstring), or
- `measurements` (raw sample arrays), or
- `resultTypes` entries (when requested)
This repo includes “resume/decoder” logic that:
- lists `results.json` under a scenario prefix
- extracts either counts or samples
- reconstructs bitstrings (with a documented bit-order convention)
- evaluates QUBO energy and writes a local “best” JSON snapshot

### Common failure modes + fixes
- **Wrong destination bucket**
  - Symptom: validation error saying bucket must start with `amazon-braket-`
  - Fix: write to the Braket results bucket and keep your project bucket for the CT.gov corpus.

- **Qubit limit exceeded**
  - Symptom: “Used N qubits, more than device qubit count…”
  - Fix: reduce `n_pool` via the pool/subset strategy (rank candidates → choose top `n_pool`).

- **Credential expiry**
  - Symptom: `InvalidSignatureException: Signature expired`
  - Fix: refresh AWS credentials/session and re-run the cell that calls `task.result()` or run the decode-from-S3 notebook to resume.

- **Jupyter async/event-loop issues**
  - Symptom: asyncio/nest_asyncio runtime errors during `task.result()`
  - Fix: avoid long synchronous waits inside the notebook. Prefer:
    - submit tasks → write task table → decode later from S3 (resume notebook)

### Operational tip: monitor tasks via CLI

bash
aws braket search-quantum-tasks --region us-west-2 \
  --filters name=deviceArn,operator=EQUAL,values=arn:aws:braket:::device/quantum-simulator/amazon/sv1 \
  --max-results 20 \
  --query "quantumTasks[].{arn:quantumTaskArn,status:status,created:createdAt,ended:endedAt}" \
  --output table

  --query "quantumTasks[].{arn:quantumTaskArn,status:status,created:createdAt,ended:endedAt}" \
  --output table

This lets you confirm task completion even if a notebook kernel disconnects.
  ::contentReference[oaicite:0]{index=0}

## Results overview (Scenarios A / B / C)

This repo implements three scenario tracks (A/B/C) and evaluates multiple solvers:

- **Classical baselines** (greedy / heuristic)
- **QAOA local** (Aer when available)
- **QAOA on AWS Braket SV1** (subset/pool strategy to fit qubit limits)

### Where to look first

- `data/results/` — primary tables and “best run” JSONs
- `outputs/figures/` — exported plots used in comparisons
- `outputs/slides/quantum_clinical_trial_optimization_showcase.pptx` — generated slide deck

### Scenario A

Includes:
- Classical baseline artifacts (`scenario_A_classical_*`)
- QAOA robustness sweeps (local/Aer-free + Aer variants)
- Comparisons:
  - Greedy vs QAOA
  - Greedy vs QAOA vs QAOA(Aer)

Look for:
- robustness summaries: `05a_*_summary.csv`, `05b_*_summary.csv`
- top-config tables: `*_top_config_table.csv`
- overlap/comparison tables: `05c*` outputs (best-by-method, overlaps, plots)

### Scenario B

Includes:
- Candidate build + classical baseline (`scenario_B_classical_*`)
- Greedy/QAOA robustness sweeps (`07a`, `07b`)
- Comparison notebook (`07c`)
- Braket SV1 run notebook (`08a`) with decoded “best” payload

Look for:
- SV1 decoded best: `_08a_sv1_best_scenario_B.json`
- task tables and selections: `08a` / `07b` / `07c` outputs under `data/results/`

### Scenario C

Includes:
- Candidate build (`09a`)
- Classical baseline (`09b`)
- Braket SV1 execution (`09c`)
- Comparison (`09d`)
- Resume/repair decoding from S3 (`10d`) for robustness against disconnects/credential expiry

Look for:
- SV1 decoded best: `_09c_sv1_best_scenario_C.json`
- classical baseline outputs: `09b_scenario_C_classical_*`
- SV1 selections/summary: `09c_sv1_*_scenario_C.csv`

### Stability and overlap metrics

Robustness and cross-method comparisons use stability-style metrics, including:

- **Jaccard similarity** between selected sets  
  `J(A,B) = |A ∩ B| / |A ∪ B|`
- sweep summaries report:
  - mean/STD of objective proxies across seeds/noise
  - mean/STD of Jaccard overlap vs a baseline selection

Interpretation:
- Higher objective is “better” under the chosen scoring convention
- Higher Jaccard indicates more stable selection under perturbations/hyperparameter changes
- SV1 runs are compared primarily on:
  - decoded best QUBO energy / objective proxy
  - overlap with classical selections
  - reproducibility via stored task outputs in S3

## Reproducibility and repo hygiene

### What is (and is not) committed

To keep the repository usable on GitHub, large intermediate artifacts are not committed.

- **Committed**
  - notebook sources (`*.ipynb`)
  - small samples and summary tables
  - scenario results tables (`data/results/*.csv`, `data/results/*.json`)
  - figures and slides (when explicitly generated and added)

- **Not committed (typically)**
  - full-scale ingestion outputs (e.g., full parquet metadata for ~557k trials)
  - large raw extracts that can be regenerated from S3

### Determinism and experiment control

Most experiment notebooks support:
- explicit `seed` control (for perturbations / sampling)
- consistent scenario candidate pools (saved candidates + stable ordering)
- checkpointing for long sweeps (partial CSV checkpoints)

If you re-run sweeps with different machine/AWS timing:
- results should remain comparable because artifacts include the config grid values and run counts.

### Artifact naming conventions

Artifacts are written under `data/results/` with prefixes that match notebooks:

- `05a_*` / `05b_*` / `05c*` → Scenario A sweeps + comparisons
- `07a_*` / `07b_*` / `07c_*` → Scenario B sweeps + comparisons
- `08a_*` → Scenario B Braket SV1 run + decoded best JSON
- `09b_*` / `09c_*` / `09d_*` → Scenario C classical + SV1 + comparison
- `10b_*` → slide deck generator outputs (`outputs/slides/`)
- `10d_*` → Braket resume/decoder diagnostics and best JSON snapshots

### “If you only read three files…”

1. **Slide deck**  
   `outputs/slides/quantum_clinical_trial_optimization_showcase.pptx`

2. **Best decoded SV1 payloads (proof of AWS quantum execution)**
   - `data/results/_08a_sv1_best_scenario_B.json`
   - `data/results/_09c_sv1_best_scenario_C.json`

3. **Cross-method comparison tables**
   - Scenario A: `05c*` outputs
   - Scenario B: `07c*` outputs
   - Scenario C: `09d*` outputs

These provide the fastest path to understanding the pipeline, the QUBO formulation, and the measured outcomes across classical vs quantum executions.


## Limitations and next steps

### Current limitations

- **SV1 qubit limit drives pooling/subsetting**
  - Full scenarios can exceed SV1’s qubit capacity.
  - SV1 notebooks use a pool strategy (rank candidates → select a smaller subset) to keep QAOA feasible.

- **Large-data ingestion is expensive to reproduce locally**
  - The CT.gov XML corpus is large (~557k trials).
  - The repo is structured so reviewers can run “demo paths” without re-ingesting everything.

- **QAOA is sensitive to hyperparameters**
  - Results can vary with `(γ, β)`, penalty strength `A`, and scaling/normalization choices.
  - Robustness sweeps are included to characterize this sensitivity.

- **AWS credential expiry can interrupt long waits**
  - Long `task.result()` waits can fail if temporary credentials expire.
  - Resume/decoder notebooks mitigate this by decoding from S3 after completion.

### Next steps (engineering and research)

- **Scale pooling strategy**
  - Explore systematic pool selection: stratified by sponsor/phase/region, not only “top score”.
  - Compare pooled SV1 selections to full classical selections for bias/coverage.

- **Add alternative classical baselines**
  - Local search / simulated annealing (classical) as a stronger baseline for medium `n`.
  - Report runtime vs quality tradeoffs.

- **Improve QAOA tuning**
  - Add smarter parameter selection (coarse-to-fine grid, Bayesian search, or warm starts).
  - Evaluate `p>1` on smaller pools as a controlled experiment.

- **Add cost tracking**
  - Log Braket task counts, shots, and estimated cost per experiment bundle.

- **Extend to additional scenarios**
  - More scenario definitions beyond A/B/C (e.g., by condition area, geography, sponsor tier).
  - Evaluate robustness of “best-by-method” conclusions across scenario families.

## License and citation

### License

This project is intended as a portfolio-quality technical demonstration. See `LICENSE` for details.

### Citation

If you reference or adapt this work, please cite the repository:

- **Repository**: `quantum-clinical-trial-optimization`
- **Author**: Michael S. Mohle
- **Tag/Release**: `v0.5.0` (Scenario A robustness sweeps: greedy (05a) + QAOA (05b))

### Data sources

- **ClinicalTrials.gov** (public, non-HIPAA): trial registry metadata derived from the CT.gov XML corpus stored in S3
- **FDA MAUDE** (public, non-HIPAA): safety signal features derived from MAUDE-based summaries/mappings

> Note: The large raw corpus and full intermediate builds are intentionally not committed to GitHub; the repo includes representative samples and downstream results artifacts for reproducibility of the analysis flow.
