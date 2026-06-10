<script setup lang="ts">
import Background from './_components/Background.vue';
import Description from './_components/Description.vue';
import Image from './_components/Image.vue';
import Name from './_components/Name.vue';

</script>

<template>
    <div class="flex justify-center">
        <div class="card w-120 bg-base200 shadow-md mt-[16vh]">
            <div class="card-body">
                <h3 class="card-title font-semibold!">创建角色</h3>
                <Image />
                <Name />
                <Description />
                <Background />
                <div class="justify-end card-actions">
                    <button class="btn btn-vue">更新</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
