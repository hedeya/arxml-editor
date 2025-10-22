# Release 1.2.0 (Release_1.2.0)

Release date: 2025-10-22

Summary
-------
This release adds a dependency-injection cleanup, decouples UI event emission from the domain, and introduces a pure-domain dataclasses migration path. It also provides v2 application-service APIs that operate on pure-domain objects so UI/tooling can interact with domain logic without Qt dependencies.

Highlights
----------
- Dependency Injection container improvements and safer repository resolution.
- Added `UIEventBus` and `UIEventAdapter` to decouple domain -> UI signaling.
- Introduced pure-domain dataclasses under `src/core/domain/models.py`:
  - `SwComponentType`, `Composition`, `PortInterface`, `DataElement` (dataclasses)
- Added v2 application-service methods that accept/return dataclasses:
  - `SwComponentTypeApplicationService.create_component_type_v2/update_component_type_v2/get_component_type_details_v2/search_component_types_v2`
  - `PortInterfaceApplicationService.create_port_interface_v2/update_port_interface_v2/search_port_interfaces_v2`
- Updated in-memory repositories to be tolerant of dataclass fields (string-based categories/types) so they can persist pure-domain objects.
- Backward compatible: existing v1 APIs and Qt-based models continue to work.

Files/Areas changed
-------------------
- `src/core/container.py` — DI improvements + UIEventBus registration
- `src/core/events/ui_event_bus.py` — new UI event bus
- `src/ui/adapters/ui_event_adapter.py` — adapter bridging bus to Qt signals
- `src/core/domain/models.py` — new pure-domain dataclasses and converters
- `src/core/repositories/memory_repositories.py` — in-memory repos made tolerant to dataclasses
- `src/core/application_services/*.py` — new v2 methods in services
- Tests: new lightweight tests under `tests/` validating invariants and DI/repo wiring

Compatibility & Migration notes
------------------------------
- No immediate breaking changes: existing public v1 APIs remain available and tested.
- Recommended migration path:
  1. Start using v2 service methods from application/service boundaries.
  2. Migrate UI and tooling to construct and consume pure-domain dataclasses.
  3. Once application services and repositories uniformly use dataclasses, you can remove Qt coupling from domain models and simplify tests.

Known limitations / follow-ups
----------------------------
- Persistence: In-memory repositories accept dataclasses for now. For durable storage, implement repository adapters that map dataclasses to DB rows (e.g., `SqliteRepository`).
- CI: Add GitHub Actions to run tests and type checks on push (recommended).

Tests run locally
-----------------
- Ran internal DI tests and lightweight domain tests: all passed locally (100% on the DI test harness used in this repo)

How to create this release on GitHub
----------------------------------
You can create a draft release from the tag `Release_1.2.0` using the GitHub web UI, or run the provided script `tools/create_release.sh` (see repository root) — it expects an environment variable `GITHUB_TOKEN` with repo write permissions.

Example (local):

```bash
# Create a draft release using the release notes file
GITHUB_TOKEN="<your-token>" ./tools/create_release.sh Release_1.2.0 Release_1.2.0 "RELEASE_NOTES/Release_1.2.0.md"
```

Make sure the token has the `repo` scope for private repos or `public_repo` for public repos.

---
If you'd like, I can create the GitHub Release entry via the GitHub API now — supply a personal access token (or allow me to guide you through using the script). Otherwise this file is ready and included in the repo.
