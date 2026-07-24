# Master Plan — Rebuttal Window + Full Revision Track

## Ground rules (confirmed, NeurIPS 2026 Main Track Handbook)

- No paper or supplemental revision can be uploaded before the decision. Text only.
- One rebuttal response per official review (Mxe9, AqnD, MKod), max 10,000 characters each,
  plain text/markdown, no files, no links (except a private anonymized code link to the AC,
  only if a reviewer explicitly asks for it).
- New results can be described in text, but the *original submission* stays the basis for the
  decision — the rebuttal clarifies, it doesn't relitigate. Calibrate expectations accordingly.
- Discussion phases: you draft/post (Jul 27–Aug 3, reactive follow-ups included) → reviewer/AC-only
  discussion, you're locked out (Aug 3–10) → official notification (Sep 24).
- Given three reject-leaning reviews and an AC who already leans reject under this year's
  early-meta-review pilot, treat this cycle's realistic goal as "clean record + useful material
  for next time," not "win them over this week."

## Direct answer to "batches, or everything, or what?"

Neither. "Batches with a rebuttal after each" isn't available — you get one initial response per
review, then reactive replies to follow-up questions, all inside one ~7-day window, not repeated
independent rounds. "Fix everything, then rebut" isn't available either — most of the 19-item
ledger needs either new experiments that take weeks, or edits to the paper text itself, and paper
edits are banned this cycle regardless of how fast you work.

**What's correct:** split the ledger into (A) what's answerable as text/quick-check before Jul 27,
used in one targeted rebuttal per review, and (B) everything else, which becomes a normal-paced
revision track for a fresh future submission with no "rebuttal" step of its own until that new
venue's reviewers respond.

---

## Track A — This submission's rebuttal (now through Aug 3)

### Step 1 (Jul 24–26): do the rebuttal-eligible items first, then take whatever extra fast reruns fit

| WI | Feasible by Jul 27? | What to actually do |
|---|---|---|
| WI-1 (anonymity) | Yes | Fix the repo now. State in text it's corrected — don't link to it. |
| WI-2 (invariance proof) | Yes — pure math, no experiment needed | Write the 5-line derivation directly into the rebuttal text. |
| WI-6 (τ_T justification) | Mostly yes | Give the reasoning in text; add a quick 0.5×/1×/2× τ_T sensitivity run if time allows. |
| WI-4 (code/paper mismatches) | Partially | Can't re-run and fix Table 2 by Aug 3 — but you can state clearly, per mismatch, which is correct (paper or code), and commit to full reconciliation next revision. |
| WI-3 (normalization ablation) | Partially, if compute allows | This is the highest-value experiment to prioritize first. Run the clean Kendall + L1-normalization ablation exactly as specified below; if the full 4-point grid and 3 seeds fit, do them. If not, record the partial result honestly as preliminary and keep it clearly separated from the final claim. |
| WI-5 (saturation check) | Maybe | Only if θ/z_i were already logged during training — this would be analysis of existing logs, not new runs. Check quickly. |

Everything else (WI-7 through WI-19, minus the pieces above) is **not achievable before Aug 3** —
either the experiment takes longer than days, or it requires editing the paper, which isn't
allowed this cycle at all, on any timeline. If you discover that NYUv2 reruns are also fast in
your setup, reassess whether the WI-3 ablation and WI-6 / WI-12 / WI-13 style checks can be
completed for the rebuttal window. Do not let that decision delay starting WI-3.

### Step 2 (Jul 27): post one rebuttal per review

- Three responses total (Mxe9, AqnD, MKod), ≤10,000 characters each. The AC sees these too once
  the discussion phase opens, so no separate reply-to-AC channel is needed for content — though
  confirm on the day whether a distinct comment option appears under the meta-review itself.
- **Prioritize AqnD's response most heavily.** Lowest score, and the AC's own language
  ("insufficient intuition, motivation, or justification") echoes AqnD's critique almost exactly.
  Lead with WI-4 (correct the reproducibility record) and WI-2 / WI-3 if ready (the proof, and the
  ablation if it finished in time).
- **Mxe9's response:** most of their asks (baselines, runtime numbers, more seeds) aren't
  answerable with new data in a week. Acknowledge each directly and state it's planned for the
  next revision — don't manufacture results you don't have.
- **MKod's response:** same "incremental" critique as AqnD — reuse WI-2 / WI-3 here.
- Keep it factual, not defensive. Overclaiming in a rebuttal reads badly to reviewers and ACs.

### Step 3 (Jul 27–Aug 3): answer follow-ups reactively

If a reviewer or the AC asks something directly during this window, respond. This is the only
part of the process that resembles "another round" — and it's reactive, not something you
initiate on your own schedule.

### Step 4 (Aug 3 onward): nothing further to do here

Aug 3–10 is reviewer/AC-only, no visibility or input from you. Silence until notification on
Sep 24. Don't keep working this thread past Aug 3 — move fully to Track B.

---

## Track B — Full revision for a future submission (unhurried, starts once Track A is posted)

Work the remaining ledger in the tier order already set:
1. Finish the rest of Tier 2 properly (full WI-4 fix + rerun of affected tables, full WI-5
   writeup, WI-7 more-seeds work, WI-8 text fix).
2. Tier 3 — the expensive new-experiment items (WI-9 through WI-15: baselines, runtime, ablations,
   sensitivity studies, second benchmark).
3. Tier 4 — the paper-text rewrites (WI-16 through WI-18), which literally could not happen any
   earlier than this, since no revision upload was allowed during Track A regardless of readiness.
4. Tier 5 — WI-19, the final consistency pass, done last.

This track has no "rebuttal" step of its own until you submit to a new venue and *that* venue's
reviewers respond — at which point you'll run a smaller version of this same Step 1→4 process
under whatever that venue's specific rules turn out to be.

Target venue and timing depend on how much of Tier 3 is realistically finishable. Since you have
time now, use this window to complete as much of Track A as possible and to pre-stage the highest-
value Track B items that do not require a paper upload. Tier 3 alone is plausibly several weeks of
work, so the next ICML deadline should still be checked closer to the time.
