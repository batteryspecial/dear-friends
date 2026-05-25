import { createRouter, createWebHistory } from 'vue-router'

import FriendIndex from '@/views/friends/FriendIndex.vue'
import CreateIndex from '@/views/create/CreateIndex.vue'
import ErrorIndex from '@/views/error/ErrorIndex.vue'
import LoginIndex from '@/views/user/account/LoginIndex.vue'
import RegisterIndex from '@/views/user/account/RegisterIndex.vue'
import SpaceIndex from '@/views/user/space/SpaceIndex.vue'
import ProfileIndex from '@/views/user/profile/ProfileIndex.vue'
import HomepageIndex from '@/views/homepage/HomepageIndex.vue'
import { useUserStore } from '@/stores/user'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'homepage_index',
      component: HomepageIndex,
      meta: {
        needLogin: false,
      },
    },
    {
      path: '/friend',
      name: 'friend_index',
      component: FriendIndex,
      meta: {
        needLogin: true,
      },
    },
    {
      path: '/create',
      name: 'create_index',
      component: CreateIndex,
      meta: {
        needLogin: true,
      },
    },
    {
      path: '/404',
      name: 'not_found',
      component: ErrorIndex,
      meta: {
        needLogin: false,
      },
    },
    {
      path: '/user/account/login',
      name: 'user_login',
      component: LoginIndex,
      meta: {
        needLogin: false,
      },
    },
    {
      path: '/user/account/register',
      name: 'user_register',
      component: RegisterIndex,
      meta: {
        needLogin: false,
      },
    },
    {
      path: '/user/space/:user_id',
      name: 'user_space',
      component: SpaceIndex,
      meta: {
        needLogin: false,
      },
    },
    {
      path: '/user/profile',
      name: 'user_profile',
      component: ProfileIndex,
      meta: {
        needLogin: true,
      },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'path_not_found',
      component: ErrorIndex,
      meta: {
        needLogin: false,
      },
    },
  ],
})

// router guard
router.beforeEach((to, from) => {
  const user = useUserStore()
  if (to.meta.needLogin && !user.isLoggedIn()) {
    return {
      name: 'user_login',

    }
  }
  return true
})

export default router
