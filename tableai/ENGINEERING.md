# Table AI — Engineering Standards

## Core Principles

### DRY (Don't Repeat Yourself)
Every piece of logic lives in exactly one place.
Shared UI lives in /components. Shared logic lives in /lib.
Never copy-paste code across pages.

### YAGNI (You Aren't Gonna Need It)
Build what Casa Mariachi needs TODAY. Add complexity when there is a proven need.
No speculative features. No over-engineering.

### SOLID (Applied to our codebase)
Single Responsibility: each component does one thing.
Every page component only handles display. Logic goes in /lib hooks.
Never mix data fetching, business logic, and UI in one blob.

## Git Workflow
main branch: always deployable, always production-ready
feature branches: feature/module-name (e.g. feature/loyalty-points)
Never commit directly to main.
Every change goes through a branch and gets reviewed before merge.

## CI/CD
Vercel auto-deploys main on every push.
Goal: deployments are boring and routine, never stressful.
If a deploy breaks something, revert immediately. Fix on a branch. Re-deploy.

## Testing (to be added)
Unit tests for: loyalty point calculations, sales totals, reservation logic.
Test file lives next to the module: lib/loyalty.test.ts
Run tests before every merge to main.
Red/green/refactor: write the test first, make it pass, then clean up.

## Code Review Checklist
Before merging any feature:
- Does it work on mobile?
- Does it have loading and error states?
- Are touch targets at least 44px?
- Is any text hardcoded that should be translated?
- Are there any console errors?
- Does the build pass with 0 errors?

## File Structure
/app          Pages (display only)
/components   Shared UI components
/lib          Business logic, Supabase client, types, i18n, hooks
/public       Static assets (logo, favicon, manifest)
