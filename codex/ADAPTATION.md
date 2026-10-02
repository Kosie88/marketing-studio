# Codex port

Source: [ucsandman/marketing-studio](https://github.com/ucsandman/marketing-studio),
forked into [Kosie88/marketing-studio](https://github.com/Kosie88/marketing-studio).
Upstream code and skill material are MIT licensed, copyright 2026 Wes Sander.
Retain the root LICENSE when redistributing this port. This is Marketing Studio;
it is not LangChain Studio.

Port baseline: upstream commit `66cd1c30919f1144c60aed3692a915bb0b2c6238`.
Relevant source contracts are the [marketing workflow](https://github.com/ucsandman/marketing-studio/blob/66cd1c30919f1144c60aed3692a915bb0b2c6238/skills/marketing/SKILL.md),
[shared studio skill](https://github.com/ucsandman/marketing-studio/blob/66cd1c30919f1144c60aed3692a915bb0b2c6238/skills/marketing-studio/SKILL.md),
[announcement workflow](https://github.com/ucsandman/marketing-studio/blob/66cd1c30919f1144c60aed3692a915bb0b2c6238/skills/announce/SKILL.md),
[social clip workflow](https://github.com/ucsandman/marketing-studio/blob/66cd1c30919f1144c60aed3692a915bb0b2c6238/skills/social-clip/SKILL.md)
and [engine brief schema](https://github.com/ucsandman/marketing-studio/blob/66cd1c30919f1144c60aed3692a915bb0b2c6238/studio/src/lib/brief.ts).

## Supported entrypoint

`codex/skills/marketing-studio-codex/SKILL.md` supports brief development, factual
copy, channel adaptation, coordinated static/video planning, actual product-photo
selection, review and a resumable posting kit. Automatic discovery remains enabled
(the default); explicit invocation is `$marketing-studio-codex`.

The port preserves upstream grounding/proofPoints, distinct hook angles,
storyboard/style-frame/animatic gates, brand/source ownership and render review.
It removes Claude path variables, Claude tool names, fixed model tiers, mandatory
agent orchestration, global installer assumptions and unverified reach statistics.
Brand enthusiasm follows the brand's guide rather than a universal ban on hype or
punctuation. The iBuddies overlay preserves order-link, actual-photo and festival
rules without applying them to other clients.

## Install

Copy the complete folder `codex/skills/marketing-studio-codex` into the user's
configured Codex skill directory (`$CODEX_HOME/skills`, or `~/.codex/skills` when
unset). Preserve an existing installation before replacing it. The copied folder
is self-contained for copy/static planning and validation. New skills become
available to discovery after Codex refreshes its skill inventory; an already
running session may require a new turn/session. This document does not imply that
installation has occurred.

To validate the folder with Codex's bundled creator:

```sh
python /path/to/skill-creator/scripts/quick_validate.py /path/to/marketing-studio-codex
python -m unittest discover -s codex/tests -v
```

## Engine limits

Upstream `skills/` remain unchanged for upstream compatibility. They are not the
Codex entrypoint. Remotion/Blender/Playwright/ComfyUI/audio integrations retain their
own dependencies, schemas and credentials. The portable manifest is a campaign
readiness record, not a replacement for engine render props or its checks. No
engine dependencies, credentials or live publishing routines are installed by
this port. The portable validator checks structural/file invariants; a reviewer
must still judge semantics, product identity, quantities in images, offer accuracy
and visual realism.

## Pilot

Use one approved physical-product offer, a small set of distinct hook angles,
Facebook/Instagram/WhatsApp copy, an ordered real-photo/hero carousel and a review
record. Keep the existing approved commercial terms. Test copy clarity and factual
consistency before extending to optional motion production. Distribution metrics
should come from the client's actual channel results, not imported universal
platform multipliers.
