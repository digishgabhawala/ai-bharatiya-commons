# Accessibility quality gate

This is the minimum manual review for a UI increment. It complements automated
tools; it does not claim complete WCAG conformance.

## Keyboard

- Start at the address bar and use only Tab, Shift+Tab, Enter, Space, Escape,
  and arrow keys where appropriate.
- A skip link reaches the primary content.
- Focus order follows the visual and task order.
- Every interactive control receives a visible focus indicator.
- Sticky headers, footers, banners, and overlays do not fully obscure focus.
- Dialogs contain focus while open, close with Escape, and restore focus to the
  control that opened them.
- Horizontally scrollable regions can be reached and identified.

## Forms

- Every field has a persistent visible label.
- Instructions and errors are connected with `aria-describedby`.
- Invalid state is communicated with text and semantics, not color alone.
- Multi-error forms present a focusable summary that links to each invalid
  field while retaining inline errors.
- Validation normally occurs on blur or submit, not on every keystroke.
- Disabled controls use native semantics and explain the unmet requirement when
  it is not apparent.

## Dynamic content

- Loading containers expose `aria-busy="true"` when appropriate.
- Important background status changes use a polite live region.
- Blocking errors use an alert only when immediate interruption is warranted.
- Progress includes a name and a current value when it is determinate.
- Focus does not move for routine background updates.

## Visual and responsive behavior

- Normal text reaches at least 4.5:1 contrast.
- Large text and meaningful interface boundaries reach at least 3:1.
- Color is never the only status signal.
- Content reflows at 320 CSS pixels without page-level horizontal scrolling.
- Long names, URLs, and identifiers wrap or remain in a labelled scroll region.
- Controls are at least 44 by 44 CSS pixels where practical.
- Text remains usable at 200% browser zoom.

## Motion and media

- `prefers-reduced-motion` removes non-essential movement and renders final
  states immediately.
- No content flashes more than three times per second.
- Informative images have useful alternatives; decorative images and icons are
  hidden from assistive technology.

## Suggested evidence

Record the browser, viewport, input method, automated tool, failures, and any
accepted limitations. A short, honest record is more useful than an unchecked
claim of compliance.
