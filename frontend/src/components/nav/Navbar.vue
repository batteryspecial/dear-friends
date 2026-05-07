<script setup>
import MenuIcon from '@/components/icons/menu.vue'

import HomeIcon from '@/components/icons/home.vue'
import UserIcon from '@/components/icons/user.vue'
import CreateIcon from '@/components/icons/create.vue'

import SearchIcon from '@/components/icons/search.vue'
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
                    <div class="px-4 font-bold text-lg">Dear Friends</div>
                </div>
                <div class="md:navbar-center md:w-1/3">
                    <div class="join w-full">
                        <input class="input outline-none border-none rounded-l-xl w-4/5 join-item" placeholder="搜索你感兴趣的内容" />
                        <button class="btn bg-amber-700/80 hover:bg-amber-600 transition-colors duration-300 rounded-r-xl join-item ">
                            <SearchIcon />
                            搜索
                        </button>
                    </div>
                </div>
                <div class="navbar-end">
                    <button class="btn btn-ghost text-lg">登录</button>
                </div>
            </nav>
            <!-- Page content here -->
            <div class="p-4">
                <slot></slot>
            </div>
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
                        <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right flex justify-center items-center" data-tip="Homepage">
                            <!-- Home icon -->
                            <HomeIcon />
                            <span class="is-drawer-close:hidden is-drawer-open:animate-[fadeIn_0.5s_ease_0.2s_both]">主页</span>
                        </button>
                    </li>
                    <li>
                        <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right flex justify-center items-center" data-tip="Homepage">
                            <!-- User icon -->
                            <UserIcon />
                            <span class="is-drawer-close:hidden is-drawer-open:animate-[fadeIn_0.5s_ease_0.2s_both]">好友</span>
                        </button>
                    </li>
                    <li>
                        <button class="is-drawer-close:tooltip is-drawer-close:tooltip-right flex justify-center items-center" data-tip="Homepage">
                            <!-- Create icon -->
                            <CreateIcon />
                            <span class="is-drawer-close:hidden is-drawer-open:animate-[fadeIn_0.5s_ease_0.2s_both]">创造</span>
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<style scoped>
</style>

<style>
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>

