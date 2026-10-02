---
name: marketing-studio-codex
description: Develop grounded marketing campaign copy and coordinated ad assets from a product brief, including channel variants, real product imagery, storyboards and a reviewed posting kit. Use for campaign creative or a marketing asset suite, with optional video production.
---

# Marketing Studio for Codex

Adapted from Wes Sander's MIT-licensed Marketing Studio. The upstream production
engine remains optional; this entrypoint works with available Codex tools.

## Campaign workflow

1. **Ground the brief.** Read the project's current brand and channel writing guides,
   product facts, approved offer and earlier effective copy. Establish audience,
   occasion/job, customer language, objections, offer, variants, CTA and proofPoints.
   Tag unresolved facts. Client confirmation can support an offer; inventory and
   checkout behaviour require current operational evidence if claimed. Preserve
   supplied corrections and distinguish a client-approved promise from a tested
   implementation.
2. **Choose useful angles.** Develop distinct hooks such as an occasion story,
   practical cooking payoff and concrete value. Select enough variants to learn
   something without generating a full suite the user did not request. Each hook
   must deliver its promise. Enthusiasm comes from specifics and sensory language;
   avoid fabricated testimonials, product qualities, urgency and performance stats.
3. **Write for each requested channel.** Use its reading behaviour, voice and CTA.
   Adapt the opening, amount of detail and rhythm where the channels differ;
   changing only hashtags or the closing CTA is insufficient channel adaptation.
   Lead with the chosen hook; connect the product to a use or outcome; make prices,
   quantities, choices, gifts and restrictions legible. Use emojis when consistent
   with the brand. Keep ordering links wherever the project's rules require them.
   Do not import upstream claims about algorithm reach or hide links by default.
4. **Plan the visual evidence.** Select actual product reference photos and record
   their product/variant identities. Pair them with campaign creative when useful.
   Check depicted quantities, anatomy, preparation, packaging and flavour against
   the brief. Generated images illustrate a scene; they do not prove the product's
   actual appearance. For a video or multi-card story, make a short storyboard with
   hook, proof/payoff and CTA. Review a representative style frame before expensive
   generation or rendering. Read [video-engine.md](references/video-engine.md) only
   when producing video with the upstream engine.
5. **Review through three lenses.** Check positioning clarity, emotional relevance
   and evidence honesty. Then inspect the actual deliverables for offer accuracy,
   legibility, visual realism and channel fit. Use a human or independent reviewer
   when available and warranted; no fixed model or agent count is required. Record
   material objections and resolve them. Mechanical validation cannot approve copy
   meaning or image realism.
6. **Deliver and resume reliably.** Keep each campaign's brief, copy, media,
   storyboard and review record in its project workspace. Maintain the small campaign
   manifest described in [campaign-contract.md](references/campaign-contract.md).
   Confirm files still exist before trusting a saved rendered/approved status.
   Provide pasteable channel copy, an ordered asset list and outstanding operational
   checks. Scheduling/publishing needs authorization covering the actual channels
   and timing; previous authorization remains valid within its scope.

## Tool and asset ownership

- Discover current tools/connectors/skills before selecting a renderer or publisher.
  Use an existing project's deterministic tools before building duplicates.
- Resolve skill resources relative to this SKILL.md. Configure the optional engine
  path explicitly; do not use Claude variables or assume a global installation.
- Reusable engine/template changes belong in the engine checkout; campaign outputs
  belong in the campaign project (for example `marketing/assets/<brand>/<campaign>`).
  Check shared edits and respect file ownership without interrupting unrelated work.
- Keep credentials in their tool's supported credential store; never in manifests,
  skill files, prompts or copied assets. Do not run dependency installers, paid
  generation or live publishing scripts merely because upstream recipes name them.
  Execute only work authorized by the user and respect the environment's limits.

For iBuddies work, also read [ibuddies.md](references/ibuddies.md). Those local rules
do not apply to unrelated brands.
