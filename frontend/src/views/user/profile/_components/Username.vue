<script setup lang="ts">
import { ref, watch } from 'vue';

const props = defineProps(['username'])
const newUsername = ref(props.username)

watch(() => props.username, c => {
    newUsername.value = c
}, { immediate: true })

defineExpose({
    newUsername,
})
</script>

<template>
    <fieldset class="fieldset">
        <label class="label text-base">用户名</label>
        <input v-model="newUsername" type="text" class="input w-full ">
    </fieldset>
</template>

<style scoped>

</style>
