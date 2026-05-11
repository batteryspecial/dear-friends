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

import axios from "axios";
import { useUserStore } from "@/stores/user";

const BASE_URL = 'http://127.0.0.1:8000'

const api = axios.create({
    baseURL: BASE_URL,
    withCredentials: true,
})

api.interceptors.request.use(config => {
    const user = useUserStore()
    if (user.accessToken) {
        config.headers.Authorization = `Bearer ${user.accessToken}`
    }
    return config
})

let isRefreshing: boolean = true
let refreshSubscribers: any[] = []

function subscribeTokenRefresh(callback: any): void {
    refreshSubscribers.push(callback);
}

function onRefreshed(token: string): void {
    refreshSubscribers.forEach((cb) => cb(token));
    refreshSubscribers = [];
}

function onRefreshFailed(err: any): void {
    refreshSubscribers.forEach(cb => cb(null, err))
    refreshSubscribers = []
}

// if the request succeeds, just return the response
api.interceptors.response.use(response => response, async error => {
    console.log(error)

    const user = useUserStore()
    const originalRequest = error?.config

    if (!originalRequest) {
        // no config data 🪫 give it up son 😢
        return Promise.reject(error)
    }

    if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true

        return new Promise((resolve, reject) => {
            // store the request first
            subscribeTokenRefresh((token: string, error: any) => {
                if (error) {
                    reject(error)
                } else {
                    originalRequest.headers.Authorization = `Bearer ${token}`
                    resolve(api(originalRequest))
                }
            })

            if (!isRefreshing) {
                isRefreshing = true // enter refresh state
                axios.post(
                    // try refreshing access
                    `${BASE_URL}/api/user/account/refresh_token/`, {},
                    { 
                        withCredentials: true,
                        timeout: 5000,
                    }
                ).then(r => {
                    const newToken = r.data.access
                    user.setAccessToken(newToken)
                    onRefreshed(newToken)
                }).catch(err => {
                    user.logout()
                    onRefreshFailed(err)
                }).finally((): void => {
                    isRefreshing = false
                })
            }
        })
    }

    return Promise.reject(error)
})

export default api

