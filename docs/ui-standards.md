# AI Bharatiyaa UI standards

Status: v0.2 adoption-ready foundation
Applies to: AI Bharatiyaa applications and portfolio surfaces

## Purpose

AI Bharatiyaa products should feel related without feeling cloned. A user moving
between Task Queue, LinkedIn Content Generator, Demo Reel, AI Mentor, Chess
Vision, or a future application should recognize the same care in typography,
spacing, interaction, and feedback.

These standards define a minimum quality floor. They are not a requirement to
finish every possible improvement before shipping useful work.

## Audience and promise

The initial audience is software developers, beginning with the developer who
builds and dogfoods these products. The interfaces should therefore reward
technical fluency without requiring a person to decipher the implementation.

The portfolio-level promise is:

> AI-native tools made by a Bharatiya builder, with Bharatiya users and
> workflows treated as first-class rather than an afterthought.

“Bharatiyaa” is a point of view, not a decorative theme. Products may serve a
global audience, but the suite should be comfortable with Indian names,
languages, time zones, formats, networks, and working contexts from the start.

## Product character

The shared visual language is:

- **Clear:** operational information and the next useful action are easy to
  find.
- **Calm:** color and motion communicate meaning instead of competing for
  attention.
- **Capable:** interfaces can be dense when the work requires it, while keeping
  hierarchy and spacing disciplined.
- **Human:** language is direct and helpful; empty and error states explain what
  a person can do next.
- **Rooted, not ornamental:** Indian identity may emerge through language,
  content, illustration, and typography. Do not default to flag colors or
  decorative cultural motifs.

The memorable shared detail is typography. Headings and product marks use the
Anek family where practical, connecting the suite to a multiscript type system.
Interfaces remain quiet around it.

### Design signature

Three recurring details make the suite recognizable:

- **Multiscript-aware typography:** Anek gives product names and major headings
  a specific voice. Indian-language text appears only when it communicates real
  meaning, never as surface decoration.
- **Builder structure:** grids, rules, aligned metadata, terminal-like prompts,
  and monospaced identifiers may expose how work moves through a system. These
  devices organize information; they do not imitate a hacker aesthetic.
- **AI as visible assistance:** show inputs, transformations, provenance, and
  status. Avoid unexplained sparkle icons or vague “magic” language.

The suite does not use tricolor palettes, mandala patterns, monuments, or script
samples as shorthand for Indian identity. Cultural specificity should come from
real language, real use cases, and the people the software is built for.

## Foundation

### Typography

- Use `--font-family-display` for product names and important page headings.
- Use `--font-family-body` for interface and reading text.
- Use `--font-family-mono` only for identifiers, code, timestamps, and technical
  values.
- Default body text is 16px with a line height of at least 1.5.
- Keep long-form text below 75 characters per line.
- Use sentence case. Avoid all-caps labels and excessive letter spacing.
- Use tabular numerals for metrics that update or align in columns.
- Applications load only the script-specific font files they need. Until those
  files are available, the token stacks fall back to system and Noto fonts.

### Color

- Neutral ink and surface colors carry most of the interface.
- Indigo is the common action and focus color.
- Green, amber, red, and blue are reserved for semantic status.
- Never use color as the only signal. Pair it with text, an icon, or both.
- Applications may override `--color-app-accent`, but the override must preserve
  accessible foreground contrast and must not replace semantic status colors.
- Meet WCAG 2.2 AA contrast: at least 4.5:1 for normal text and 3:1 for large
  text and meaningful interface boundaries.

Dark mode remains deliberately outside v0.2. Add it when an application has a real
use case and both themes can be tested together.

### Spacing and layout

- Use the shared 4px-based spacing tokens. Do not introduce one-off spacing
  values without a component-specific reason.
- Align related content to a common edge.
- Prefer visible grouping and whitespace over putting every section in a card.
- Use borders for persistent structure, shadows for temporary elevation, and
  neither when spacing already communicates the relationship.
- Default page content should remain readable between 320px and 1440px.
- Data-heavy screens may be dense, but interactive targets remain at least
  44px high or wide where practical.

### Shape and elevation

- Small controls use `--radius-sm`; containers use `--radius-md` or
  `--radius-lg`; status pills alone use `--radius-pill`.
- Do not apply the same large radius and shadow to every surface.
- Use `--shadow-raised` sparingly for elevated menus or selected focal
  surfaces. Use `--shadow-overlay` for dialogs and overlays.

### Icons

- Prefer Lucide SVG icons across web applications.
- Use one icon style and consistent optical size within a surface.
- Decorative icons are hidden from assistive technology.
- Icon-only controls require an accessible name and a visible tooltip where the
  meaning is not universally understood.
- Do not use emoji as interface icons.

## Interaction standards

### Actions

- Give each region one clear primary action.
- Button labels describe the result: “Save changes,” “Retry,” or “Create task.”
- Primary, secondary, tertiary, and destructive actions must look different.
- Hover is enhancement, not the only way to reveal necessary information.
- Every keyboard-focusable control has a visible focus indicator.
- Disabled controls should explain the unmet requirement when it is not
  obvious.

### Feedback and states

Every data-driven surface must account for:

1. Initial loading
2. Empty data
3. Successful content
4. Partial or stale data
5. Recoverable failure
6. Permission failure, when authentication is introduced

Loading indicators reserve the final layout where possible. Empty states explain
what the surface normally contains and provide a relevant next action. Errors
state what failed and how to recover; they do not rely on “Something went
wrong.”

Dynamic status changes that do not move focus must be exposed to assistive
technology through an appropriate live region or status role.

### Motion

- Motion explains a state change or responds to an action.
- Use the shared fast and standard durations for most interface transitions.
- Avoid staggered page-load animation as a default treatment.
- Animate opacity and transforms rather than layout properties where possible.
- Respect `prefers-reduced-motion` and render the final state immediately.

## Reusable interface patterns

The following rules apply before shared components exist:

- **Navigation:** the current product and current location are always clear.
- **Page headers:** state the page purpose; actions sit near the title only when
  they apply to the whole page.
- **Cards:** use cards for independently meaningful groups, not as default page
  decoration.
- **Tables:** provide meaningful headers, predictable alignment, horizontal
  containment on small screens, and sorting/filtering only when genuinely
  useful.
- **Status labels:** use adjective or state language such as “Queued,” “Running,”
  and “Failed.” Status labels are not buttons.
- **Forms:** use visible labels, field-level help, inline validation, and an error
  summary for longer forms.
- **Metrics:** show units and time ranges. Avoid charts when a number or small
  table communicates the information more honestly.

## Application individuality

Shared across the suite:

- Typography roles
- Neutral palette and semantic colors
- Spacing and shape scales
- Focus, loading, empty, error, and responsive behavior
- Action hierarchy and interface language

Allowed to vary by application:

- `--color-app-accent`
- Information density
- Illustration and imagery
- Domain-specific visualizations and components
- Marketing-page composition

Variation should reflect the product’s subject matter, not a different design
trend for each repository.

## Incremental adoption

### Foundation pass

- Import the shared tokens.
- Replace raw colors and repeated spacing with semantic tokens.
- Apply typography, focus, and status rules.
- Add intentional loading, empty, and error states.
- Verify the primary screen at 375px, 768px, 1024px, and 1440px.

### Product pass

- Improve hierarchy and navigation.
- Add only the filters, details, and interactions supported by real user needs.
- Record useful application-specific patterns before extracting them.

### Commons pass

Promote a pattern into this repository only when:

- It has been used successfully by at least two applications.
- Its API and visual states are understood.
- It can remain framework-neutral or has a clearly identified framework owner.
- It includes accessibility and responsive behavior.

## Definition of done for a UI increment

A small UI improvement is ready when:

- It solves one stated usability or consistency problem.
- It uses shared tokens rather than adding accidental new values.
- Loading, empty, success, and error implications have been considered.
- Keyboard focus and text contrast remain visible.
- The affected viewport sizes have been checked.
- Any deferred improvements are recorded as backlog rather than silently
  expanding the current task.

## Governance

- Prefer small pull requests that change one category of decision.
- Document why a token or rule changes, including affected applications.
- Add a new token only when its semantic role differs from existing tokens.
- Avoid breaking token renames until consumers can migrate deliberately.
- Revisit this document after the standards are used in two applications; that
  is the earliest point for creating the shared AI Bharatiyaa UI skill.

## Supporting guides

- [`typography.md`](typography.md) defines font loading and mixed-script review.
- [`accessibility-checklist.md`](accessibility-checklist.md) is the manual quality
  gate for each increment.
- [`adoption-playbook.md`](adoption-playbook.md) describes the migration order
  for consuming applications.
- [`application-identity.md`](application-identity.md) separates family traits
  from product-specific expression.
- [`v0.2-roadmap.md`](v0.2-roadmap.md) records scope and release evidence.
