# ai-bharatiya-commons

Shared UI standards, design tokens, and reusable foundations for AI Bharatiyaa
applications.

This repository is intentionally small. It captures decisions that should stay
consistent across applications without forcing every application to use the
same framework or reach the same level of polish at the same time.

## Current scope

- [`docs/ui-standards.md`](docs/ui-standards.md) defines the v0.2 product and UI
  principles.
- [`design-tokens/tokens.css`](design-tokens/tokens.css) provides the first
  portable token set.
- [`design-tokens/README.md`](design-tokens/README.md) explains how applications
  should consume and extend the tokens.
- [`preview/index.html`](preview/index.html) is a living visual review of the
  standards and tokens.
- [`docs/adoption-playbook.md`](docs/adoption-playbook.md) provides the gradual
  migration path for applications.
- [`docs/v0.2-roadmap.md`](docs/v0.2-roadmap.md) records release scope and
  validation evidence.
- [`docs/platform-deployment-plan.md`](docs/platform-deployment-plan.md)
  describes the proposed shared-domain, shared-auth deployment for Task Queue
  and LinkedIn Content Agent.
- `skills/` is reserved for a future AI Bharatiyaa UI skill. It remains empty
  until the standards have been tested in more than one application.

## Adoption approach

Applications should adopt the standards incrementally:

1. Typography, color, spacing, focus, and semantic states.
2. Loading, empty, error, and responsive behavior.
3. Repeated components and shared application-shell patterns.
4. Shared packages only after the same pattern has proven useful in multiple
   applications.

Application-specific personality is welcome. Shared foundations should remain
stable; domain-specific layouts, illustrations, visualizations, and accent
treatments may vary.

## Status

Version `0.2` makes the contract testable and adoption-ready; it is still not a
component library. Changes should be driven by real application work and
recorded here when they become repeatable.

## Visual review

From the repository root, run:

```bash
python3 -m http.server 8000
```

Then open [http://localhost:8000/preview/](http://localhost:8000/preview/).
Review it at desktop width and at a narrow mobile width. The preview is a
reference surface, not a production website or component package.

## Validate

Run the dependency-free checks from the repository root:

```bash
python3 scripts/validate_ui_foundation.py
```
