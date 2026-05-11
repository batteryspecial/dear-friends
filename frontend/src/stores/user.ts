import { ref } from 'vue'
import { defineStore } from 'pinia'

export interface UserInfo {
    result: string
    access: string
    user_id: number
    username: string
    image: string
    bio: string
}

export const useUserStore = defineStore('user', () => {
    const id = ref<number>(0)
    const username = ref<string>('')
    const image = ref<string>('')
    const bio = ref<string>('')

    const accessToken = ref<string>('')

    function isLoggedIn(): boolean {
        return !!accessToken.value
    }

    function setAccessToken(token: string): void {
        accessToken.value = token
    }
    
    function setUserInfo(data: UserInfo): void {
        id.value = data.user_id
        username.value = data.username
        image.value = data.image
        bio.value = data.bio
    }

    function logout(): void {
        accessToken.value = ''
        id.value = 0
        username.value = ''
        image.value = ''
        bio.value = ''
    }

    return {
        accessToken, id, username, image, bio, isLoggedIn, setAccessToken, setUserInfo, logout
    }
})