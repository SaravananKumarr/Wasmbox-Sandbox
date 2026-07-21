# API Reference

## Health
- `GET /` - Welcome
- `GET /api/health` - Health check

## Auth
- `POST /auth/register` - Register user
- `POST /auth/login` - Login and get JWT

## Plugins
- `GET /api/plugins` - List plugins
- `GET /api/plugin/{id}` - Get plugin
- `POST /api/plugin` - Create plugin
- `PUT /api/plugin/{id}` - Update plugin
- `DELETE /api/plugin/{id}` - Delete plugin

## Execution
- `POST /api/run` - Run plugin from source
- `POST /api/trigger/{id}` - Trigger plugin by ID

## Webhooks
- `POST /api/webhook/test` - Webhook test endpoint

## WebSocket
- `WS /ws/execution/{id}` - Execution stream
