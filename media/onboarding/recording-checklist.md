# Onboarding video recording checklist

## Before recording

- [ ] Record against the exact reviewed release-candidate wheel.
- [ ] Run the full test suite and strict documentation build at the same commit.
- [ ] Confirm `svgap doctor` passes in the recording environment.
- [ ] Create a fresh `/tmp/svgap-video` directory and neutral terminal prompt.
- [ ] Disable notifications, password managers, autocomplete history, and
      account avatars.
- [ ] Close internal repositories, proprietary RTL, email, chat, and employer
      applications.
- [ ] Confirm no API keys or provider identifiers will appear.
- [ ] Confirm the browser uses only public repository and documentation pages.

## Content accuracy

- [ ] Say that quickstart uses a bundled known-unsafe fixture.
- [ ] Say that the fixture is not a model result.
- [ ] State that open RTL prerequisites are already installed.
- [ ] Keep the result conditional on supplied evidence and configured rules.
- [ ] Keep “not silicon signoff” visible or spoken.
- [ ] Do not claim a defect rate, comprehensive coverage, certification, or a
      general model ranking.
- [ ] Do not show or describe unavailable perturbation instrumentation.
- [ ] Do not show the cold container pull as the time-to-value path.

## Visual and accessibility review

- [ ] All commands and evidence questions are readable at mobile playback size.
- [ ] The terminal font is at least 20 px and contrast passes WCAG AA.
- [ ] Captions match the final narration rather than the draft timing.
- [ ] Captions identify technical acronyms accurately, including RTL and RDC.
- [ ] Meaning does not depend on color alone.
- [ ] No rapid zoom, cursor movement, or transitions create distraction.
- [ ] The thumbnail remains legible at 320 px width.

## Artifact and metadata review

- [ ] Run `ffprobe` and record duration, dimensions, frame rate, and codecs.
- [ ] Export a separate WebVTT caption file.
- [ ] Use the repository SVG as the thumbnail source and export a 1280×720 PNG.
- [ ] Title: `From Functional Pass to Production Question | SV-Gap in 90 Seconds`.
- [ ] Description includes the repository URL, scope boundary, and fixture
      disclosure.
- [ ] Disable automatic chapter text unless it has been manually verified.
- [ ] Upload unlisted first and test desktop, mobile, captions, and outbound
      links.

## Before adding repository links

- [ ] The final video URL resolves without authentication.
- [ ] The video demonstrates commands available in the matching public release.
- [ ] The public release, documentation, and video use the same terminology.
- [ ] Add a linked thumbnail to the README; do not embed autoplay media.
- [ ] Add a text link beside the thumbnail for screen-reader and low-bandwidth
      access.
- [ ] Link the transcript and captions from the documentation page.
