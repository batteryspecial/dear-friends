<script setup>
import UserSpaceIcon from '@/components/icons/space.vue'
import UserProfileIcon from '@/components/icons/user.vue'
import UserLogoutIcon from '@/components/icons/leave.vue'

import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';
import api from '@/js/http/api';

const user = useUserStore()
const router = useRouter()

const menuActionItems = [
    { icon: UserSpaceIcon,   label: '个人空间', to: () => ({ name: 'user_space', params: { user_id: user.id } }) },
    { icon: UserProfileIcon, label: '个人资料', to: () => ({ name: 'user_profile' }) },
]

function closeMenu() {
    const element = document.activeElement
    if (element && element instanceof HTMLElement)
        element.blur()
}

async function handleLogout() {
    try {
        const r = await api.post('/api/user/account/logout/')
        if (r.data.result === 'success') {
            user.logout()
            await router.push({
                name: 'homepage_index'
            })
        }
    } catch (err) {
        console.log(err)
    }
}
</script>

<template>
    <div class="px-4 dropdown dropdown-end">
        <div tabindex="0" role="button" class="avatar btn btn-circle w-8 h-8 mr-5">
            <div class="w-8 rounded-full shadow-md hover:shadow-lg">
                <img :src="user.image" alt="profile" referrerpolicy="origin"/>
            </div>
        </div>
        <ul tabindex="-1" class="dropdown-content menu bg-base-100 rounded-box z-1 w-52 p-2 gap-y-3 shadow-md">
            <li>
                <RouterLink @click="closeMenu" :to="{name: 'user_space', params: {user_id: user.id}}">
                    <div class="avatar">
                        <div class="w-5 border rounded-full">
                            <img :src="user.image" alt="username" referrerpolicy="origin"/>
                        </div>
                    </div>
                    <span class="text-base font-semibold line-clamp-1">{{ user.username }}</span>
                </RouterLink>
            </li>

            <!-- regular menu icons -->
            <li v-for="item in menuActionItems" :key="item.label">
                <RouterLink @click="closeMenu" :to="item.to()">
                    <component :is="item.icon" class="w-5 h-auto" />
                    <span class="text-base font-semibold">{{ item.label }}</span>
                </RouterLink>
            </li>

            <li></li>
            
            <li>
                <a @click="handleLogout" class="text-base font-semibold">
                    <UserLogoutIcon class="w-5 h-auto" />
                    <span class="text-base font-semibold">退出登录</span>
                </a>
            </li>
        </ul>
    </div>
</template>

<style scoped>

</style>
