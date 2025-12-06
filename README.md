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
