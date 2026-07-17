# WasmBox – Secure Multi-Tenant Plugin Sandbox

WasmBox is an advanced, security-first platform for hosting and validating multi-tenant WebAssembly plugins. The project combines a policy-driven backend, a modern React dashboard, and deployment-ready container support to demonstrate a strong foundation for a production sandbox product.

## Highlights

- Tenant-specific sandbox policies
- Plugin validation with import, memory, network, signing, execution-time, and host checks
- Audit trail for plugin approvals and rejections
- React-based control center for policy review and validation
- Docker and CI support for GitHub-based delivery

## Project structure

- apps/api: Express API with policy engine and audit logging
- apps/web: React dashboard for tenant and plugin management
- .github/workflows: GitHub Actions CI pipeline

## Quick start

1. Install dependencies
   ```bash
   npm install
   ```
2. Copy environment settings
   ```bash
   cp .env.example .env
   ```
3. Start both services
   ```bash
   npm run dev
   ```
4. Open the app at http://localhost:3000
5. Check the API at http://localhost:4000/health

## Docker

```bash
docker compose up --build
```

## Advanced roadmap

The next phase can include:

- real WebAssembly module execution in an isolated runtime
- cryptographic plugin signing and attestation
- database-backed tenant policy storage
- RBAC, quotas, and observability
- Kubernetes deployment and autoscaling

## GitHub upload

```bash
git init
git add .
git commit -m "Advanced WasmBox implementation"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```
