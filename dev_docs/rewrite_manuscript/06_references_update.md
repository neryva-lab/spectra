# 06 — References Update

## 1. New entries to add to `working/paper/references.bib`

```bibtex
@inproceedings{navon2022nash,
  title={Multi-Task Learning as a Bargaining Game},
  author={Navon, Aviv and Shamsian, Aviv and Achituve, Idan and Maron, Haggai
          and Kawaguchi, Kenji and Chechik, Gal and Fetaya, Ethan},
  booktitle={Proceedings of the 39th International Conference on Machine Learning},
  series={Proceedings of Machine Learning Research},
  volume={162},
  pages={16428--16446},
  year={2022}
}

@inproceedings{liu2021imtl,
  title={Independent Component Alignment for Multi-Task Learning},
  author={Liu, Liyang and Li, Yanqi and Davison, Andrew J. and Johns, Edward},
  booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
  pages={2008--2017},
  year={2021}
}

@inproceedings{liu2023famo,
  title={{FAMO}: Fast Adaptive Multitask Optimization},
  author={Liu, Bo and Feng, Yihua and Fernando, Chrisantha and Rodr{\'i}guez-Opazo,
          Cesar and Reid, Ian and Gould, Stephen},
  booktitle={Advances in Neural Information Processing Systems},
  year={2023}
}

@article{liu2022autolambda,
  title={Auto-Lambda: Disentangling Dynamic Task Relationships},
  author={Liu, Shikun and James, Stephen and Davison, Andrew J. and Johns, Edward},
  journal={Transactions on Machine Learning Research},
  year={2022}
}
```

**Notes on the entries:**
- `navon2022nash` — used in Related Work (§2), Experimental Setup (§4.2), Results (§5.2),
  Appendix A. **This is the only one that must be cited** (Nash-MTL is evaluated).
- `liu2021imtl`, `liu2023famo` — cited once in Related Work (one sentence, see
  `02_section_by_section_rewrite_plan.md` §2). Also referenced in the Discussion future-work
  sentence if worded as "IMTL-G, FAMO, CAGrad, Auto-Lambda".
- `liu2022autolambda` — cite only if actually discussed (either the Related-Work sentence or
  the Discussion future-work list). Do not add a dangling bibliography entry that is never
  cited — bibtex will warn and reviewers notice.
- Page numbers for `liu2021imtl` and `liu2023famo` should be verified against the official
  versions during implementation (web search if needed; do not guess).

## 2. Citation integrity checks after editing

1. `grep` the manuscript for `\cite{navon2022nash}`, `\cite{liu2021imtl}`, `\cite{liu2023famo}`,
   `\cite{liu2022autolambda}` — each must appear at least once.
2. Run `bibtex`; check `build/main.blg` for `Warning--I didn't find a database entry` and
   `Warning--citation ... undefined`.
3. Check `build/main.log` for `LaTeX Warning: Citation ... undefined` and
   `Reference ... undefined`.
4. The reference list will grow by 3–4 entries (from 11 to 14–15) — references don't count
   against the 9-page limit, so no page impact.

## 3. Related-work paragraph wording (citation context)

Insert into the Pareto/gradient-surgery paragraph of Related Work (after the Sener–Koltun
sentence):

> More recent methods solve a per-step multi-objective subproblem: Nash-MTL frames the shared
> update as a bargaining game over task gradients \cite{navon2022nash}, while IMTL-G
> \cite{liu2021imtl} and FAMO \cite{liu2023famo} propose alternative gradient-level or
> objective-level rules. These methods are not the closest conceptual predecessors to BPGS ---
> they do not target loss-scale invariance of scalar weights --- but Nash-MTL provides a recent
> comparison point in our NYUv2 experiments, and the others remain future work
> (Section~\ref{sec:limitations}).

Wording discipline: this paragraph only *positions* these methods; it must not imply they were
evaluated (only Nash-MTL was).
