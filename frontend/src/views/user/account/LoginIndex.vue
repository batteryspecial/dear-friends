<script setup lang="ts">
import { ref } from 'vue';

import api from '@/js/http/api';
import { useUserStore } from '@/stores/user';

import type { UserInfo } from '@/stores/user';
import { useRouter } from 'vue-router';

const username = ref('')
const password = ref('')

const errMsg = ref('')

const user = useUserStore()
const router = useRouter()

async function handleLogin() {
    errMsg.value = ''

    if (!username.value.trim()) {
        errMsg.value = '用户名为空'
    } else if (!password.value) {
        errMsg.value = '密码为空'
    } else {
        try {
            const r = await api.post<UserInfo>('/api/user/account/login/', {
                username: username.value,
                password: password.value,
            })

            const data = r.data
            if (data.result === 'success') {
                user.setAccessToken(data.access)
                user.setUserInfo(data)

                router.push({
                    name: 'homepage_index'
                })
            } else {
                errMsg.value = data.result
            }
        }
        catch (e) {
            console.log(e)
        }
    }
}
</script>

<template>
    <div class="flex justify-center items-center h-[calc(100vh-64px)]">
        <form @submit.prevent="handleLogin" class="fieldset text-base gap-y-4 bg-base-200 border-base-300 rounded-box w-xs border p-4">
            <div>
                <label class="label pb-1">邮箱/用户名</label>
                <input v-model="username" type="text" class="input" placeholder="Email" />
            </div>
            
            <div>
                <label class="label pb-1">密码</label>
                <input v-model="password" type="password" class="input" placeholder="Password" />
            </div>

            <p v-if="errMsg" class="text-sm text-red-500 mt-2">出错了 {{ errMsg }}</p>
            
            <button class="btn btn-neutral mt-4">登录</button>
            <div class="flex justify-end">
                <RouterLink :to="{name: 'user_register'}" class="btn btn-xs btn-ghost text-slate-300">注册</RouterLink>
            </div>
        </form>
    </div>
</template>

<style scoped>

</style>
