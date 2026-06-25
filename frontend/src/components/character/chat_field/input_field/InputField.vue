<script setup lang="ts">
import MicIcon from '@/components/icons/mic.vue';
import SendIcon from '@/components/icons/send.vue';

const { color } = defineProps(["color"])
console.log(color)
</script>

<template>
    <div class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
        <input
            class="input w-full pr-17 rounded-2xl bg-black/30 backdrop-blur-sm border !border-[color:var(--avg-color)] text-white text-base"
            :style="{ '--avg-color': color }"
            type="text"
            placeholder="文本输入..."
        >
        <div class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
            <SendIcon class="hover:stroke-[color-mix(in_srgb,var(--avg-color)_90%,#42d392)] transition-colors duration-300" :style="{ '--avg-color': color }" />
        </div>
        <div class="absolute right-9 w-8 h-8 flex justify-center items-center cursor-pointer">
            <MicIcon class="dark:stroke-white hover:stroke-[color-mix(in_srgb,var(--avg-color)_90%,#42d392)] transition-colors duration-300" :style="{ '--avg-color': color }" />
        </div>
    </div>
</template>

<style scoped>

</style>
