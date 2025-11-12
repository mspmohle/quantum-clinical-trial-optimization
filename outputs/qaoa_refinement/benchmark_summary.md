### QAOA Benchmark Summary (p = 1)
| Method | γ | β | Expected Cost ⟨C⟩ | Comment |
|:--|--:|--:|--:|:--|
| Classical (Baseline) | – | – | 0.0460 | Mean–risk objective |
| QAOA (Sweep) | 0.0000 | 0.0000 | -0.0603 | Initial grid search |
| QAOA (Refined) | 0.0000 | 0.0000 | -0.0558 | Local refinement |

**Observations:**  
- The classical baseline serves as a deterministic benchmark.  
- The QAOA sweep identified a valid minimum around γ≈0.000, β≈0.000.  
- Refinement confirmed stability with ⟨C⟩† = -0.0558.