<script setup lang="ts">
import { ref } from 'vue';

import api from '@/js/http/api';
import { useUserStore } from '@/stores/user';

import { useRouter } from 'vue-router';
import type { UserInfo } from '@/stores/user';

const username = ref('')
const password = ref('')
const repeatPassword = ref('')
const errMsg = ref('')

const user = useUserStore()
const router = useRouter()

async function handleRegister() {
    errMsg.value = ''
    if (!username.value.trim()) {
        errMsg.value = '用户名不能为空'
    } else if (!password.value.trim()) {
        errMsg.value = '密码不能为空'
    } else if (password.value.trim() !== repeatPassword.value.trim()) {
        errMsg.value = '密码不一致'
    } else {
        try {
            const r = await api.post<UserInfo>('/api/user/account/register/', {
                username: username.value,
                password: password.value,
            })

            const data = r.data
            if (data.result === "success") {
                user.setAccessToken(data.access)
                user.setUserInfo(data)

                await router.push({
                    name: 'homepage_index',
                })
            } else {
                errMsg.value = data.result
            }
        } catch (err) {
            console.log(err)
            
        }
        console.log(errMsg.value)
    }
}
</script>

<template>
    <div class="flex justify-center items-center h-[calc(100vh-64px)]">
        <form @submit.prevent="handleRegister" class="fieldset text-base gap-y-4 bg-base-200 border-base-300 rounded-box w-xs border p-4">
            <div>
                <label class="label pb-1">邮箱 / 用户名</label>
                <input v-model="username" type="text" class="input" placeholder="Email / Username" />
            </div>
            
            <div>
                <label class="label pb-1">密码</label>
                <input v-model="password" type="password" class="input" placeholder="Password" />
            </div>

            <div>
                <label class="label pb-1">确认密码</label>
                <input v-model="repeatPassword" type="password" class="input" placeholder="Re-Enter Password" />
            </div>

            <p v-if="errMsg" class="text-sm text-red-500 mt-1">{{ errMsg }}</p>
            
            <button type="submit" class="btn btn-neutral mt-4">注册</button>
            <div class="flex justify-end">
                <RouterLink :to="{name: 'user_login'}" class="btn btn-xs btn-ghost text-slate-300">登录</RouterLink>
            </div>
        </form>
    </div>
</template>

<style scoped>

</style>
