Work in Progress


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
