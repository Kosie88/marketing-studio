# Optional upstream video engine

The skill's campaign/copy workflow does not require the engine. For an actual
engine render, locate the checkout supplied by the user/configuration, inspect its
README and `docs/PLAYBOOK.md`, then only the relevant `docs/playbook/` recipe.
Run `python launch.py --check` there to diagnose prerequisites before proposing
installation. Read-only checks may fail when Blender, Remotion, browser capture or
audio credentials are unavailable; document the missing components and use
available image/video tools if that meets the requested deliverable.

The portable campaign manifest is not the engine's Zod brief or render manifest.
Translate the approved brief into `studio/src/lib/brief.ts` fields and the current
recipe's props through its builder. Retain audience, customerLanguage, objections,
proofPoints, hook categories, CTA, direction and shots where relevant. Do not feed
the portable JSON directly to engine scripts or bypass their schemas.

Use `--project <campaign-project>` on project-aware builders/renderers and the
recipe's explicit public media directory. Brand configuration supplies palette,
type and motion; source footage/photos remain traceable to the campaign brief.
Do not use the upstream Claude skill installer for Codex.

For a hero film, approve a style frame and rough animatic before finishing. Review
start/middle/end frames for each shot and inspect the complete final cut with sound
where playback is available. Make short channel cuts intentional: show the payoff
early, preserve the actual offer, respect crop/safe areas, and communicate with
sound off. Narration and music are creative choices, not mandatory for every food
ad. If an upstream template enforces audio, either satisfy that specific recipe or
choose a suitable template; do not declare its checks passed without running them.

Record renderer, props, output paths, duration/aspect, review and deviations in the
campaign. Render serially when tools/CPU require it. Skip intact approved outputs
on resume; rerender only changed/missing assets. Do not automatically bootstrap,
upload, call paid providers or invoke the `launch/` live distribution commands.
