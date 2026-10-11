# Typography and script readiness

Typography is the most recognizable shared detail in the AI Bharatiyaa family.
It must support real content and remain readable when brand fonts are absent.

## Roles

- **Display:** Anek for product names and important headings. Load only the
  script subsets an application actually uses.
- **Body:** Noto Sans or an appropriate Noto Sans script family for interface
  and reading text.
- **Mono:** the platform monospace stack for code, identifiers, timestamps, and
  technical values only.

Body content starts at 16px with a line height of at least 1.5. Long-form text
should remain between roughly 45 and 75 characters per line.

## Loading policy

- Self-host production font files when licensing and deployment permit.
- Use WOFF2 and subset by script and weight.
- Prefer variable files only when their transfer size is lower than the required
  static files.
- Use `font-display: swap` or `optional`; never hide useful text while a font
  downloads.
- Preload only the font needed above the fold.
- Match fallback metrics when layout shift becomes measurable.

The preview uses Google Fonts for convenient review. That is not a requirement
or a production hosting recommendation.

## Script behavior

- Set the correct `lang` attribute when the language changes.
- Do not use an Indian script as decoration or as a translation of text that is
  not useful to the audience.
- Keep product names, person names, and user-entered content intact. Do not
  transliterate without user intent.
- Test mixed Latin and Indian-script lines for baseline, clipping, line height,
  and punctuation behavior.
- Allow headings to wrap naturally; do not force line breaks that only work in
  one language or viewport.

## Required specimens

Every application adopting multilingual content should test:

- a short product heading
- a two-line interface message
- a long Bharatiya person or organization name
- mixed-script content containing a technical identifier
- Indian Standard Time and a local date example
- 200% browser zoom and a system-font fallback

The Commons preview currently demonstrates Latin and Devanagari. Other scripts
should be added when a real product uses them, with a fluent-language review.
