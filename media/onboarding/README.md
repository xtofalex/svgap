# SV-Gap 90-second onboarding video kit

This directory contains the production source for a short public onboarding
video. Record against the final release candidate, review the rendered video,
and add its real URL to the repository only after publication.

## Intended viewer outcome

Within 90 seconds, a frontier-model researcher or applied RTL engineer should
understand that SV-Gap:

1. preserves the supplied functional result;
2. exposes a declared production question that the functional result does not
   settle;
3. identifies answered, failed, and unanswered questions; and
4. accepts any model wrapper that reads a prompt from stdin and writes RTL to
   stdout.

The video is an orientation, not an installation tutorial or research-result
claim. The screen and narration must explicitly identify the quickstart input
as a bundled known-unsafe fixture rather than a model output.

## Files

- `script.md`: narration, shots, and on-screen text.
- `terminal-session.txt`: exact commands and expected checkpoints.
- `captions.vtt`: editable WebVTT captions aligned to the shot plan.
- `recording-checklist.md`: safety, accessibility, and publication checks.
- `thumbnail.svg`: editable 16:9 source thumbnail.

## Open-source production tools

Use OBS Studio for capture and Kdenlive or Shotcut for editing. Use FFmpeg for
final encoding and media inspection. These tools are open source; no
proprietary recording service is required.

Recommended delivery:

- 1920×1080, 30 fps;
- H.264 video with AAC audio in MP4;
- clear speech around 145 words per minute;
- burned-in emphasis only for the three evidence states, with WebVTT captions
  supplied separately;
- no background music unless it remains well below the narration.

## Publication sequence

1. Record and render privately.
2. Review the full video against `recording-checklist.md`.
3. Upload it as unlisted and verify captions, thumbnail, and mobile playback.
4. Replace the unlisted state with public visibility when the matching release
   is public.
5. Add the real URL to the README and documentation in the same reviewed
   change. Do not commit a placeholder URL.
