# Design tokens

`tokens.css` is the v0.2 source of truth for shared visual values. It uses plain
CSS custom properties so current applications can adopt it without choosing a
shared frontend framework.

## Usage

Copy or package the file through the consuming application's normal asset
pipeline, then import it before application styles:

```css
@import url("./path/to/tokens.css");
```

Components should use semantic tokens:

```css
.button-primary {
  min-height: var(--control-height-md);
  padding-inline: var(--space-4);
  color: var(--color-text-on-action);
  background: var(--color-action);
  border-radius: var(--radius-sm);
  transition: background-color var(--duration-fast) var(--ease-standard);
}

.button-primary:hover {
  background: var(--color-action-hover);
}

.button-primary:focus-visible {
  outline: var(--focus-ring-width) solid var(--color-focus);
  outline-offset: var(--focus-ring-offset);
}
```

Do not use primitive palette values directly in application components. The
primitives exist to define semantic roles and may change as the system matures.

## Application accent

Applications may override `--color-app-accent` and
`--color-text-on-app-accent` at `:root`. The pair must meet WCAG 2.2 AA contrast
and must not be used for success, warning, danger, or informational states.

## Density

Comfortable density is the default. Place `data-density="compact"` on a bounded
application region when repeated operational data benefits from tighter controls:

```html
<section data-density="compact">
  <!-- Controls use --control-height-current and related density aliases. -->
</section>
```

Density must not reduce necessary touch targets in a touch-first context. Do
not place the attribute on the document root merely to make an entire interface
feel smaller.

## Layout and layering

The content-width and gutter tokens define shared rhythm without prescribing an
application shell. Layer tokens provide a small, predictable order for sticky
UI, menus, overlays, and toasts. Applications should not invent arbitrarily high
z-index values to escape this order.

## Validation

Run the dependency-free validation before publishing a token change:

```bash
python3 scripts/validate_ui_foundation.py
```

It checks duplicate root declarations, undefined token references, and critical
WCAG contrast pairs. Visual and keyboard review remain required.

## Fonts

The tokens name font families but do not download fonts. Each application owns
font loading and should load only the scripts and weights it actually uses.
System fallbacks keep the tokens functional before hosted or self-hosted fonts
are introduced.

## What is intentionally missing

- Dark-theme tokens
- Framework-specific exports
- Generated JSON, TypeScript, Tailwind, or native-platform formats
- Component code

Add these only when a real consumer requires them. When multiple output formats
are needed, introduce one machine-readable source and generate the platform
files rather than maintaining duplicates by hand.
