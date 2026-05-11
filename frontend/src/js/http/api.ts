/**
 * api.ts
 * 
 * - add access token (as bearer) in every auth header
 *     -> if failure (access expired), try updating with refresh
 *     -> if failure (refresh expired), log out the user
 * 
 * - if success (renewed access)
 *     -> @returns original request
 */

import axios, { AxiosError } from "axios";
import type { AxiosResponse, InternalAxiosRequestConfig } from "axios";

import { useUserStore } from "@/stores/user";

interface RetryableRequest extends InternalAxiosRequestConfig {
    _retry?: boolean
}

interface RefreshTokenResponse {
    access: string
}

type TokenRefreshCallback = (token: string | null, error?: unknown) => void

const BASE_URL = 'http://127.0.0.1:8000'

const api = axios.create({
    baseURL: BASE_URL,
    withCredentials: true,
})

api.interceptors.request.use((config: InternalAxiosRequestConfig): InternalAxiosRequestConfig => {
    const user = useUserStore()
    if (user.accessToken) {
        config.headers.Authorization = `Bearer ${user.accessToken}`
    }
    return config
})

let isRefreshing: boolean = false
let refreshSubscribers: TokenRefreshCallback[] = []

function subscribeTokenRefresh(callback: TokenRefreshCallback): void {
    refreshSubscribers.push(callback);
}

function onRefreshed(token: string): void {
    refreshSubscribers.forEach((cb) => cb(token));
    refreshSubscribers = [];
}

function onRefreshFailed(err: unknown): void {
    refreshSubscribers.forEach(cb => cb(null, err))
    refreshSubscribers = []
}

// if the request succeeds, just return the response
api.interceptors.response.use(
    (response: AxiosResponse) => response,
    async (error: AxiosError) => {
        console.log(error)

        const user = useUserStore()
        const originalRequest = error?.config as RetryableRequest | undefined

        if (!originalRequest) {
            // no config data 🪫 give it up son 😢
            return Promise.reject(error)
        }

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true

            return new Promise((resolve, reject) => {
                // store the request first
                subscribeTokenRefresh((token: string | null, error?: unknown) => {
                    if (error) {
                        reject(error)
                    } else {
                        originalRequest.headers.Authorization = `Bearer ${token}`
                        resolve(api(originalRequest))
                    }
                })

                if (!isRefreshing) {
                    isRefreshing = true // enter refresh state
                    axios.post<RefreshTokenResponse>(
                        // try refreshing access
                        `${BASE_URL}/api/user/account/refresh_token/`, {},
                        {
                            withCredentials: true,
                            timeout: 5000,
                        }
                    ).then((r: AxiosResponse<RefreshTokenResponse>) => {
                        const newToken: string = r.data.access
                        user.setAccessToken(newToken)
                        onRefreshed(newToken)
                    }).catch((err: unknown) => {
                        user.logout()
                        onRefreshFailed(err)
                    }).finally((): void => {
                        isRefreshing = false
                    })
                }
            })
        }

        return Promise.reject(error)
    }
)

export default api

