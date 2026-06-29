/**
 * Appends access token on every request.
 * -> If return code is 401, access is expired
 * -> Refresh access using the refresh token
 * -> If successful, retry the request
 * @returns result data
 */

import { fetchEventSource, type EventSourceMessage } from '@microsoft/fetch-event-source';
import { useUserStore } from "@/stores/user.js";
import api from "./api.js";

const BASE_URL = 'http://127.0.0.1:8000'

export type StreamMessagePayload = {
    content?: string;
    [key: string]: any;
}

export type StreamOptions = {
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
    headers?: Record<string, string>;
    body?: Record<string, any>;
    onmessage?: (data: StreamMessagePayload | string, isDone: boolean) => void;
    onerror?: (err: Error) => void;
    onclose?: () => void;
}

/**
 * Streaming request boilerplate
 * @param {string} url request address
 * @param {object} options settings (method, body, onmessage, onerror等)
 */
export default async function stream(url: string, options: StreamOptions = {}): Promise<void> {
    const user = useUserStore();

    const startFetch = async (): Promise<void> => {
        return await fetchEventSource(BASE_URL + url, {
            method: options?.method ?? "POST",
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${user.accessToken}`,
                ...options.headers,
            },
            body: JSON.stringify(options.body || {}),
            openWhenHidden: true, // allow background execution
            async onopen(response: Response): Promise<void> {
                if (response.status === 401) {
                    try {
                        // Use Axios's interceptor to refresh access
                        await api.post("api/user/account/refresh_token/", {});
                        throw new Error("TOKEN_REFRESHED");
                    } catch (err) {
                        throw err;
                    }
                }
                if (!response.ok || !response.headers.get('content-type')?.includes('text/event-stream')) {
                    const errorData = await response.json().catch(() => ({ detail: undefined }));
                    throw new Error(errorData.detail || `请求失败: ${response.status}`);
                }
            },
            onmessage(msg: EventSourceMessage): void {
                if (msg.data === "[DONE]") {
                    if (options.onmessage) options.onmessage('', true)
                    return;
                }
                try {
                    const json: StreamMessagePayload = JSON.parse(msg.data);
                    if (options.onmessage) options.onmessage(json, false);
                } catch (err) {
                    console.error("流解析失败:", err);
                }
            },
            onerror(err: any): number | void {
                if (err instanceof Error && err.message === "TOKEN_REFRESHED") {
                    startFetch()
                    return;
                }

                // Deal with other errors according to user options
                if (options.onerror) {
                    options.onerror(err instanceof Error ? err : new Error(String(err)))
                }
                throw err;
            },
            onclose: options.onclose,
        })
    }

    return await startFetch();
}
