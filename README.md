Work in Progress

This repository is actively under development as part of a large-scale applied research project integrating real-world clinical trial data, scalable AWS cloud data engineering, and hybrid quantum–classical optimization workflows using Amazon Braket.

Current Status

Large-scale raw CTGov XML dataset (~557K files) fully uploaded to S3
(s3://quantum-clinical-optimization-us-west-2/clinical-trials-data/raw/)

High-performance S3 synchronization scripts built to ensure reliable, resumable ingestion (including fast-dedupe logic and scalable batching)

AWS Braket environment validated (SV1 connected and QAOA test circuits executed)

Local development environment fully configured (Ubuntu VM, Python virtual environment, boto3, AWS CLI, Braket SDK)

Initial QAOA benchmarking and optimizer-refinement notebooks completed (parameter sweeps, convergence analysis, classical vs. quantum comparisons)

In Progress

Phase 1: Data Engineering Pipeline

Parsing raw CTGov XML into structured tables

Converting metadata into Parquet format

Creating scalable partitioned storage layouts (S3 → local notebook environment)

Implementing validation checks and schema normalization

Phase 2: Feature Engineering

Extracting outcome measures, interventions, conditions, and timeline fields

Generating text embeddings (BioClinicalBERT, TF-IDF)

Building cost, reward, and penalty features for QUBO modeling

Phase 3: Problem Formulation

Defining optimization objectives for trial portfolio selection

Translating clinical and operational constraints into QUBO-compatible structures

Coming Soon

Classical baseline optimization models (linear programming, mixed-integer programming, greedy heuristics)

Quantum optimization workflows (QAOA on Amazon Braket simulators and hardware backends)

End-to-end hybrid pipeline: S3 ingestion → feature extraction → baseline models → QUBO → QAOA → evaluation

Final project report and visualizations:

Clinical trial trend dashboards

Portfolio comparison charts

Quantum vs. classical performance summaries

Architecture diagrams and methodology documentation

Project Goal

To develop a scalable, end-to-end framework for clinical trial portfolio optimization using hybrid quantum-classical methods, leveraging AWS Braket and real-world biomedical datasets.
