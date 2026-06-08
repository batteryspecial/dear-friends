<script setup>
import MenuIcon from '@/components/icons/menu.vue'
import HomeIcon from '@/components/icons/home.vue'
import UserIcon from '@/components/icons/user.vue'
import CreateIcon from '@/components/icons/create.vue'
import SearchIcon from '@/components/icons/search.vue'

import { useUserStore } from '@/stores/user'

import UserMenu from './UserMenu.vue'

const user = useUserStore()
</script>

<template>
    <div class="drawer lg:drawer-open">
        <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />
        <div class="drawer-content">
            <!-- Navbar -->
            <nav class="navbar w-full bg-base-300">
                <div class="navbar-start">
                    <label for="my-drawer-4" aria-label="open sidebar" class="btn btn-square btn-ghost">
                        <!-- Sidebar toggle icon -->
                        <MenuIcon />
                    </label>
                    <div class="px-4 font-bold md:text-lg text-sm">Dear Friend</div>
                </div>
                <div class="navbar-center md:justify-center justify-end lg:w-4/5 max-w-150">
                    <div class="join w-4/5 flex justify-center">
                        <input class="input outline-none border-none rounded-l-xl w-4/5 join-item" placeholder="搜索你感兴趣的内容" />
                        <button class="btn btn-vue rounded-r-xl join-item">
                            <SearchIcon />
                            <span class="hidden lg:block">搜索</span>
                        </button>
                    </div>
                </div>
                <div class="navbar-end">
                    <RouterLink v-if="user.hasPulledUserInfo && user.isLoggedIn()" :to="{name: 'create_index'}" active-class="btn-active" class="btn btn-ghost text-base mr-5">
                        <CreateIcon />
                        <span>创作</span>
                    </RouterLink>
                    <RouterLink v-if="user.hasPulledUserInfo && !user.isLoggedIn()" :to="{name: 'user_login'}" active-class="btn-active" class="btn btn-ghost text-lg">
                        登录
                    </RouterLink>
                    <UserMenu v-else-if="user.hasPulledUserInfo && user.isLoggedIn()" />
                </div>
            </nav>
            <!-- Page content here -->
            <slot></slot>
        </div>

        <div class="drawer-side is-drawer-close:overflow-visible">
            <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay"></label>
            <div class="flex min-h-full flex-col items-start bg-base-200 is-drawer-close:w-15 is-drawer-open:w-64">
                <!-- Spacer matching navbar height; border shown when sidebar is open -->
                <div class="h-1.5 w-full shrink-0 is-drawer-open:border-b is-drawer-open:border-base-100"></div>
                <!-- Sidebar content here -->
                <ul class="menu w-full grow gap-y-2">
                    <!-- List item -->
                    <li>
                        <RouterLink :to="{name: 'homepage_index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right flex justify-center items-center" data-tip="主页">
                            <!-- Home icon -->
                            <HomeIcon />
                            <span class="is-drawer-close:hidden is-drawer-open:animate-[fadeIn_0.5s_ease_0.2s_both]">主页</span>
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink :to="{name: 'friend_index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right flex justify-center items-center" data-tip="好友">
                            <!-- User icon -->
                            <UserIcon />
                            <span class="is-drawer-close:hidden is-drawer-open:animate-[fadeIn_0.5s_ease_0.2s_both]">好友</span>
                        </RouterLink>
                    </li>
                    <li>
                        <RouterLink :to="{name: 'create_index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right flex justify-center items-center" data-tip="创造">
                            <!-- Create icon -->
                            <CreateIcon />
                            <span class="is-drawer-close:hidden is-drawer-open:animate-[fadeIn_0.5s_ease_0.2s_both]">创造</span>
                        </RouterLink>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>
