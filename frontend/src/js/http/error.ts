/**
 * Global "something broke" hint.
 *
 * Most catch blocks in this app only console.log the error, so a failed request
 * left the UI silent. Rather than edit every call site, the axios interceptor
 * sets this ref and App.vue renders it — one choke point, every request covered.
 */
import { ref } from 'vue'

export const apiErrMsg = ref('')

let clearTimer: ReturnType<typeof setTimeout> | undefined

export function showApiError(msg: string = '出错了，请稍后重试'): void {
    apiErrMsg.value = msg
    // Restart the countdown on every error so rapid failures don't cut it short.
    clearTimeout(clearTimer)
    clearTimer = setTimeout(() => { apiErrMsg.value = '' }, 5000)
}

export function clearApiError(): void {
    clearTimeout(clearTimer)
    apiErrMsg.value = ''
}
