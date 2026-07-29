/**
 * Single source of truth for the backend origin.
 *
 * Set VITE_API_BASE_URL in .env.development / .env.production.
 * Empty string = same origin, which is what production wants: nginx serves the
 * built app and proxies everything else to gunicorn, so a relative /api/... hits
 * the right box. An absolute 127.0.0.1 would resolve to the *visitor's* machine.
 */
export const BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? ''
