I want you to upgrade the existing Shaheen-Global-Cloud project from the current Mock Provider architecture to a production-ready architecture capable of provisioning real Ubuntu VPS instances.

IMPORTANT: Before changing anything, carefully inspect the entire existing repository and read the complete "README.md". Understand the current architecture and preserve all existing working functionality.

ABSOLUTE PROJECT NAME REQUIREMENT

The project name is exactly:

Shaheen-Global-Cloud

This name is FINAL.

Never rename, abbreviate, translate, modify, or replace it.

Keep "Shaheen-Global-Cloud" exactly as it is throughout the project, including:

- UI
- titles
- metadata
- documentation
- configuration
- branding
- API/project references where applicable

ABSOLUTE UI/DESIGN REQUIREMENT

DO NOT redesign the existing frontend.

The current Shaheen-Global-Cloud visual identity and interface must remain unchanged.

Do not replace:

- existing layout
- navigation
- dashboard design
- server creation interface
- typography
- existing black/white/gray visual identity
- existing branding
- existing logo/assets

Only make the minimum frontend changes required to connect the existing UI to the real backend provisioning system.

The existing visual design has priority and must be preserved.

---

MAIN OBJECTIVE

Replace the Mock Provider with a real cloud-provider architecture while keeping the system secure, modular, and extensible.

Target architecture:

Frontend
→ FastAPI
→ PostgreSQL
→ Redis Job Queue
→ Worker
→ Dagger
→ OpenTofu
→ Cloud Provider API
→ Real Ubuntu VPS
→ Cloud-init
→ Health Check
→ READY

Do not bypass this architecture by putting provisioning directly inside an HTTP request.

The API must create a provisioning job and return immediately.

The worker must perform the actual provisioning asynchronously.

---

1. PROVIDER ABSTRACTION

Create a clean provider abstraction such as:

ProviderAdapter

with operations conceptually equivalent to:

- validate_credentials()
- list_regions()
- list_server_types()
- list_images()
- create_server()
- get_server()
- delete_server()
- reboot_server()
- power_on_server()
- power_off_server()

Do not hard-code provider-specific logic throughout the application.

The backend should select the provider through the existing provider configuration.

Keep the architecture ready for future providers.

---

2. REAL PROVIDER

Implement the first real provider according to the existing README and repository architecture.

If the README already specifies a provider, use that provider.

If no provider is specified, implement the first provider using a well-supported OpenTofu provider and make the provider configurable through environment variables.

Do NOT invent fake credentials.

Do NOT hard-code API tokens.

Do NOT commit credentials.

Do NOT make the system pretend that a real VPS was created when it was not.

If credentials are missing, the system must fail clearly with a useful error such as:

PROVIDER_CREDENTIALS_MISSING

rather than silently falling back to Mock Provider.

---

3. OPENTOFU

Upgrade the current OpenTofu infrastructure from Mock Provider to real provisioning.

Create a reusable Ubuntu VPS module with:

- server name
- region/location
- server type/size
- Ubuntu image
- SSH key
- cloud-init/user-data
- required networking configuration
- outputs for:
  - server ID
  - server name
  - public IPv4
  - public IPv6 if available
  - region
  - status

Keep infrastructure code modular.

Do not place provider secrets inside ".tf" files.

Use environment variables or secure secret injection.

Pin provider versions appropriately.

Run:

tofu fmt
tofu init
tofu validate
tofu plan

Do not execute a real "tofu apply" during development unless explicitly instructed and valid credentials are available.

---

4. CLOUD-INIT

Create production-ready cloud-init for Ubuntu.

The bootstrap process should:

- update package metadata safely
- install required base packages
- configure the required runtime
- configure SSH safely
- install/configure required monitoring or health-check components
- expose a reliable readiness signal

Do not put API tokens or private credentials directly into Git-tracked cloud-init files.

Use secure secret injection.

---

5. DAGGER

Update the Dagger module so provisioning is executed through Dagger rather than directly from the FastAPI HTTP process.

The Dagger workflow should:

1. Receive validated provisioning parameters.
2. Load required secrets securely.
3. Prepare the OpenTofu working directory.
4. Run "tofu init".
5. Run "tofu fmt".
6. Run "tofu validate".
7. Run "tofu plan".
8. Apply only when explicitly requested by the provisioning worker.
9. Capture structured output.
10. Return machine-readable results.
11. Never expose secrets in logs.

Implement destroy through the same controlled workflow.

---

6. BACKEND JOB SYSTEM

Keep provisioning asynchronous.

The API should:

1. Validate the request.
2. Create the server database record.
3. Create a provisioning job.
4. Queue the job in Redis.
5. Return the server/job ID.

The worker should:

1. Pick up the job.
2. Change server status to PROVISIONING.
3. Invoke Dagger.
4. Run OpenTofu.
5. Store outputs.
6. Detect the VPS public IP.
7. Perform health checks.
8. Change status to READY only after successful verification.
9. Change status to FAILED with a useful error if provisioning fails.

Use states such as:

PENDING
PROVISIONING
BOOTSTRAPPING
READY
FAILED
DESTROYING
DESTROYED

Make provisioning idempotent and prevent duplicate concurrent operations on the same server.

---

7. DATABASE

Ensure the database stores enough information to track a real VPS safely, including where appropriate:

- server ID
- provider
- provider server ID
- name
- region
- image
- size
- status
- public IPv4
- public IPv6
- hostname if configured
- created_at
- updated_at
- error information
- provisioning job ID

Never store raw provider API tokens in the database.

---

8. API

Keep the existing API contract where possible.

Ensure these operations work correctly:

POST /api/v1/servers
GET /api/v1/servers
GET /api/v1/servers/{id}
POST /api/v1/servers/{id}/destroy
GET /api/v1/jobs/{id}
GET /api/v1/servers/{id}/logs

Return proper HTTP status codes and structured errors.

---

9. FRONTEND

Do NOT redesign the frontend.

Keep the existing Shaheen-Global-Cloud interface exactly as it currently looks.

Only update the API integration so the existing UI can:

- create a real provisioning job
- display provisioning progress
- display server status
- display public IP
- display provider
- display region
- display Ubuntu version
- display server size
- display errors
- refresh server status
- destroy a server

Remove any assumption that successful provisioning means a Mock Provider response.

Do not hard-code "http://localhost:8000" for production.

Use environment-based API configuration, for example:

VITE_API_BASE_URL

with a safe development default.

---

10. SECURITY

This is critical.

Implement:

- environment-based secrets
- secure secret injection
- input validation
- provider credential validation
- authorization checks where already supported
- safe subprocess handling
- no arbitrary shell execution from user input
- no arbitrary OpenTofu/HCL supplied by users
- no secrets in logs
- no credentials in Git
- no ".env" files committed
- no OpenTofu state committed
- no provider tokens committed
- no private keys committed

Never allow a frontend user to submit arbitrary Terraform/OpenTofu code for execution.

The backend must map validated server specifications to trusted infrastructure modules.

---

11. MOCK PROVIDER

Do not simply delete the Mock Provider if it is useful for tests.

Keep it isolated as a testing provider.

Production mode must NOT silently use Mock Provider.

Clearly separate:

development/test provider

from:

real cloud provider.

Tests should continue to work without real cloud credentials.

---

12. TESTING

Add/update tests for:

- provider abstraction
- provider credential validation
- server creation API
- job creation
- worker processing
- provisioning failures
- duplicate operations
- server status transitions
- OpenTofu configuration
- Dagger pipeline
- Mock Provider
- real-provider configuration validation

Real cloud provisioning tests must be optional and must never run automatically in CI without explicit credentials.

---

13. DOCKER

Update Docker configuration so the complete local stack remains reproducible:

- frontend
- backend
- worker
- PostgreSQL
- Redis

Do not assume Docker Compose can be used by a production hosting platform.

Document local development separately from production deployment.

---

14. PRODUCTION CONFIGURATION

Create a clear ".env.example" containing placeholders only.

Document all required environment variables.

For example, use placeholders such as:

PROVIDER_API_TOKEN=
PROVIDER_PROJECT_ID=
DATABASE_URL=
REDIS_URL=
SECRET_KEY=
VITE_API_BASE_URL=

Do not put real credentials into the repository.

---

15. CLOUDFLARE

Do NOT add Cloudflare Tunnel yet unless it is already required by the existing README architecture.

First make sure the actual VPS provisioning pipeline works correctly.

The priority is:

Real Cloud Provider
→ Ubuntu VPS
→ Public IP
→ Health Check
→ READY

Cloudflare integration can be added afterward.

---

16. DO NOT BREAK THE EXISTING PROJECT

Before modifying files:

- inspect existing files
- read README.md
- inspect package.json
- inspect backend
- inspect dagger
- inspect infrastructure
- inspect Docker Compose
- inspect GitHub Actions
- inspect current frontend services

Do not create duplicate files.

Do not replace working files unnecessarily.

Do not randomly restructure the repository.

Do not create placeholder implementations.

Every new file must have a real purpose and must integrate into the existing architecture.

---

17. VERIFICATION

After implementation, run:

- frontend build
- TypeScript typecheck
- backend tests
- OpenTofu fmt
- OpenTofu validate
- Dagger validation
- Docker Compose configuration validation
- security/configuration checks

Fix all errors you encounter.

Do NOT execute a real VPS creation merely to prove the code works unless valid credentials are explicitly configured.

Instead, verify that the real-provider path reaches the point where it is ready for a legitimate "tofu apply".

---

FINAL REPORT

When finished, give me:

1. Complete final file tree.
2. Files created.
3. Files modified.
4. Files removed, if any, with justification.
5. Provider implemented.
6. OpenTofu changes.
7. Dagger changes.
8. Backend changes.
9. Frontend integration changes.
10. Environment variables required.
11. Tests executed and results.
12. Build results.
13. Security checks performed.
14. Exact commands to run locally.
15. Exact steps required to configure a real provider.
16. Exact command/workflow that would provision a real Ubuntu VPS once credentials are supplied.
17. Any remaining limitations.

Most importantly:

DO NOT claim that a real VPS was created unless a real cloud API was actually called successfully.

Do not change the project name.

Do not change the existing visual design.

Do not randomly create files.

Read "README.md" and inspect the existing project FIRST.

Then implement the migration carefully and systematically.
