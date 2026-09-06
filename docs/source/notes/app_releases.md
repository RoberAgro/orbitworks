# Testing and releasing the OrbitWorks app

## Run all tests locally

From the repository root, after `poetry install`:

```powershell
poetry run python scripts/run_tests.py
```

The script discovers the complete `tests/` directory and preserves pytest's
exit code. It uses its own location to find the repository, so an IDE or an
absolute-path invocation from another directory works too. Use the project's
Python environment; the runner does not install dependencies. These tests
include physics, Dash callbacks/assets, version consistency and the local
launcher, but do not constitute a complete visual/browser test suite.

## What triggers testing and deployment

| Event | Tests | Render deployment request |
| --- | --- | --- |
| Push to `main` | Ubuntu and Windows | No |
| Pull request into `main` | Ubuntu and Windows | No |
| Push `app-vMAJOR.MINOR.PATCH` | Ubuntu and Windows | Only after both test jobs succeed |
| Manual Actions run | Ubuntu and Windows | No, even if a tag is selected |

`.github/workflows/test_and_deploy_app.yaml` uses Python 3.13 and Poetry 2.1.2.
Both platforms install `poetry.lock` dependencies and call the same test script.
The Render job depends on the whole test matrix. It then verifies that the tag
matches the package version and the tagged commit is an ancestor of `main`.
It sends the checked-out commit SHA explicitly, preventing a later unrelated
push from changing which code Render is asked to deploy.

Deployment requests are serialized. GitHub does not guarantee chronological
execution of queued releases: avoid pushing several release tags at once.
An older tagged commit on main is allowed; deploying it intentionally is a
rollback. A successful deployment-request job means Render accepted the request,
not that the app build or rollout finished. Check Render's dashboard for that
result. A network timeout can happen after acceptance, so inspect Render before
retrying a failed request.

Documentation publishing remains a separate, unchanged workflow. Its success
is not a prerequisite for this app deployment job. Nothing publishes to PyPI.

## One-time setup before pushing these changes

1. In the Render service's **Settings**, set **Auto-Deploy to Off**. The repository
   now also specifies `autoDeployTrigger: 'off'` in `render.yaml`, but editing a
   local file does not update an existing service's settings by itself.
2. If the service belongs to a Render Blueprint, check its **Auto Sync** setting.
   Blueprint changes can themselves trigger updates/deploys; use manual Blueprint
   syncing if you want release tags to be the only automatic app deployment path.
   Disable existing commit-driven deployment before pushing this configuration.
3. Copy the service's secret **Deploy Hook URL** from Render Settings.
4. In GitHub, open **Settings → Secrets and variables → Actions → New repository
   secret**. Name it `RENDER_DEPLOY_HOOK_URL` and paste the URL there. Never commit
   it to a file, print it in logs, or share it in an issue/chat.
5. Confirm that the Render build uses the intended Python runtime (the CI matrix
   uses 3.13). The Blueprint pins Poetry 2.1.2; a service not managed by that
   Blueprint needs its build command updated in the dashboard if necessary.

Consider protecting `main` and restricting creation/update/deletion of `app-v*`
tags to release maintainers through GitHub rulesets. A workflow is not protection
against someone authorized to modify it or manually deploy from Render. The
deploy-hook secret is supplied only to the tag deployment step, never to PR tests.

No dashboard setting, repository secret, push, tag or deployment is created by
merely adding these files to the local repository.

## Version ownership

The initial configured version is **0.1.0**. `.bumpversion.cfg` updates these
values together:

- Its own `current_version`.
- `[tool.poetry].version` in `pyproject.toml`.
- `__version__` in `src/orbitworks/__init__.py`.

`docs/conf.py` imports `orbitworks.__version__` for its Sphinx `release`, so the
documentation does not have a separate hardcoded version. Tests detect drift
between the version sources. Bumpversion creates a release commit and an
annotated tag named `app-v{new_version}`. The version number itself does not
include the `app-v` prefix.

## Release procedure

Start on `main`, up to date with the remote, with all intended work committed
and a clean working tree. Do not use `--allow-dirty` for an actual release.

```powershell
poetry run python scripts/run_tests.py

# 0.1.0 → 0.1.1, including the release commit and app-v0.1.1 tag:
poetry run bumpversion patch

# Check the resulting versioned state:
poetry run python scripts/run_tests.py

# Substitute the exact tag generated above for future releases:
git push --atomic origin main app-v0.1.1
```

Use `minor` or `major` instead of `patch` when appropriate. Inspect the result
before pushing. The explicit tag avoids accidentally releasing every unpublished
local tag, as `git push --tags` would. The atomic push publishes main and that
tag together; GitHub still runs separate push workflows for the branch and tag,
but only the tag workflow can request an app deployment.

The bump command already creates the commit and tag: do not create them a
second time manually. A local tag does not deploy anything until pushed. If
checks fail, do not force-move a published release tag; fix the problem and
create a new patch release. A dry run previews the version change without a
commit or tag:

```powershell
poetry run bumpversion --dry-run --verbose patch
```

After a version bump, `poetry install` can refresh the installed distribution
metadata in the local environment. The source `orbitworks.__version__` and docs
already reflect the new version without reinstalling.

## External references

- [Render deploy hooks](https://render.com/docs/deploy-hooks): secret URL and exact-commit `ref` parameter.
- [Render deployment settings](https://render.com/docs/deploys): disabling commit-driven deployment.
- [Render Blueprints](https://render.com/docs/infrastructure-as-code): Blueprint Auto Sync is separate from service Auto-Deploy.
- [bump2version](https://github.com/c4urself/bump2version): file replacement, release commits and tags.
