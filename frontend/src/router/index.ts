import { createRouter, createWebHistory } from 'vue-router'

import FriendIndex from '@/views/friends/FriendIndex.vue'
import CreateIndex from '@/views/create/CreateIndex.vue'
import ErrorIndex from '@/views/error/ErrorIndex.vue'
import LoginIndex from '@/views/user/account/LoginIndex.vue'
import RegisterIndex from '@/views/user/account/RegisterIndex.vue'
import SpaceIndex from '@/views/user/space/SpaceIndex.vue'
import ProfileIndex from '@/views/user/profile/ProfileIndex.vue'
import HomepageIndex from '@/views/homepage/HomepageIndex.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'homepage_index',
      component: HomepageIndex,
    },
    {
      path: '/friend',
      name: 'friend_index',
      component: FriendIndex,
    },
    {
      path: '/create',
      name: 'create_index',
      component: CreateIndex,
    },
    {
      path: '/404',
      name: 'not_found',
      component: ErrorIndex,
    },
    {
      path: '/user/account/login',
      name: 'user_login',
      component: LoginIndex,
    },
    {
      path: '/user/account/register',
      name: 'user_register',
      component: RegisterIndex,
    },
    {
      path: '/user/space/:user_id',
      name: 'user_space',
      component: SpaceIndex,
    },
    {
      path: '/user/profile',
      name: 'user_profile',
      component: ProfileIndex,
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'path_not_found',
      component: ErrorIndex,
    },
  ],
})

export default router
