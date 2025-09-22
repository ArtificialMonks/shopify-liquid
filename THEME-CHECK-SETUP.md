# Theme Check Setup and Validation Guide

This repository includes two configurations for Theme Check and a helper script to validate the code library quickly in development or at production strictness.

## Configurations
- .theme-check-development.yml – fast, focused checks for day-to-day authoring
- .theme-check-production.yml – strict checks aligned with Theme Store requirements

## How to run checks

From the repo root:

- Development profile (recommended while editing):
  bash ./scripts/validate-theme.sh development

- Production profile (strict):
  bash ./scripts/validate-theme.sh production

These commands run theme-check against shopify-liquid-guides/code-library as the root. See shopify-liquid-guides/docs/validation/README.md for full validation architecture and rules.

## Troubleshooting
- Ensure Ruby and theme-check are installed (see official docs)
- If you see missing file errors, confirm you are in the repo root when running the script
- For JSON schema errors, cross-reference shopify-liquid-guides/schema-validation/schema-guidelines.md

