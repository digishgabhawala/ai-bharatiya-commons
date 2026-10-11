# Adoption playbook

Use this playbook when a product is ready to adopt the commons foundation. It
supports small, reversible increments and does not require a visual rewrite.

## Before starting

- Pin a Commons release tag or commit.
- Capture screenshots of the target screen at its important viewport sizes.
- Choose one usability or consistency problem for the increment.
- Record application-specific values that should remain local.
- Confirm that concurrent functional work will not change the same markup.

## Recommended adoption order

### 1. Foundation

- Import or copy the pinned `tokens.css`.
- Apply body, display, and mono typography roles.
- Replace repeated raw color and spacing values with semantic tokens.
- Add the shared focus indicator.
- Do not restructure the page in this step.

### 2. Shell

- Apply adaptive page gutters and content widths.
- Clarify product identity, current location, and the primary page action.
- Check sticky regions against keyboard focus and anchored navigation.

### 3. States

- Add loading, empty, successful, stale, recoverable-error, and permission
  implications for the target surface.
- Preserve layout during loading where practical.
- Announce dynamic status changes without moving focus unexpectedly.

### 4. Screen refinement

- Improve one workflow or screen at a time.
- Use real content, long identifiers, and realistic failure messages.
- Extract a pattern into Commons only after a second application validates it.

## Application override boundary

Applications may override:

- `--color-app-accent` and `--color-text-on-app-accent`
- information density within the documented modes
- domain-specific illustration, visualization, and imagery
- application shell details required by the product's navigation

Applications should not redefine shared semantic status colors or change the
meaning of typography, focus, spacing, and action tokens.

## Migration worksheet

Copy this section into the consuming application's issue or pull request.

```markdown
## Commons adoption increment

- Commons version:
- Target screen or workflow:
- Problem being solved:
- Files expected to change:
- Existing screenshots captured:
- Viewports to review:
- States affected:
- Accessibility checks:
- Deferred follow-ups:
- Rollback: revert this isolated increment and restore the prior stylesheet.
```

## Pull-request checklist

- The change addresses one stated problem.
- No unrelated functional behavior was changed.
- New values use semantic tokens or have a documented local role.
- Keyboard focus is visible and not obscured.
- Loading, empty, success, and error implications were reviewed.
- Long names and identifiers do not break the layout.
- A before-and-after comparison is attached.
- Deferred improvements are listed instead of added to the current scope.
