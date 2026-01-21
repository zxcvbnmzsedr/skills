---
name: whale-admin-api-services
description: Enforce the whale-admin frontend rule that all API calls must use the generated service clients under src/api/services. Use for any task that adds, updates, or reviews API requests, service usage, or data fetching in the whale-admin project, especially when touching frontend network calls or API integrations.
---

# Whale Admin API Services

## Overview

Ensure every API call in whale-admin goes through the generated clients under src/api/services, which are produced by pnpm api.

## Guidelines

- Use functions from src/api/services for every API request.
- Avoid direct axios/fetch usage or ad-hoc request wrappers outside src/api/services.
- Check for an existing service function before adding new API usage.
- If a required endpoint is missing, regenerate services with pnpm api (after aligning the backend API spec).

## Workflow

1. Locate the required client in src/api/services.
2. Replace any direct request logic with the service function call.
3. If no service exists, coordinate the API spec update and run pnpm api, then use the new service.
4. Re-scan the modified files to confirm no direct network calls were introduced.
