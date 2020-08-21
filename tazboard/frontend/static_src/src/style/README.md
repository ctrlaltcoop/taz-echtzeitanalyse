# Styling

This folder contains styles that should be globally available to the application including styles by vendors (bootstrap).
This file should document should document styling conventions in this codebase.

## Global styles in src/styles

Any style that affect more than one specific component including scss-mixins and functions should be placed in an scss file in this folder.
All css non-vendor classes should be prefixed with `tazboard-` to avoid potential collisions. Try to come up with a name that describes the
purpose. No BEM convention or similar is enforced.

## Specific classes may remain in a _scoped_ style block of components

Any styling that is specific to _one_ component should be in a `<style scoped>`-block of the component. No non-scoped `<style>`-block should be used.
All unscoped styles belong here (see above). In a `scoped` style block no prefix is needed. Mixins, variables and functions may be imported in scoped
`<style>`-block.

## Avoid !important whenever possible

To override vendor styles in some cases it's unavoidable to use `!important`. However be sure you tried overriding scss variables
and use specific class denominators first. 


