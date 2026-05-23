<script setup>

</script>

<template>
    <div class="flex justify-center items-center h-[calc(100vh-64px)]">
        <fieldset class="fieldset text-base gap-y-4 bg-base-200 border-base-300 rounded-box w-xs border p-4">
            <div>
                <label class="label pb-1">邮箱 / 用户名</label>
                <input type="email" class="input" placeholder="Email / Username" />
            </div>
            
            <div>
                <label class="label pb-1">密码</label>
                <input type="password" class="input" placeholder="Password" />
            </div>

            <div>
                <label class="label pb-1">确认密码</label>
                <input type="password" class="input" placeholder="Re-Enter Password" />
            </div>
            
            <button class="btn btn-neutral mt-4">注册</button>
            <div class="flex justify-end">
                <RouterLink :to="{name: 'user_login'}" class="btn btn-xs btn-ghost text-slate-300">登录</RouterLink>
            </div>
        </fieldset>
    </div>
</template>

<style scoped>

</style>
