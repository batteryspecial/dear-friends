<script setup lang="ts">
import CreateCharacter from './character/CreateCharacter.vue';

export interface Author {
  user_id: number;
  username: string;
  image: string;
}

export interface Character {
  id: number;
  name: string;
  desc: string;
  image: string;
  bg_image: string;
  author: Author;
}

export interface Friend {
    id: string;
    character: Character;
}
</script>

<template>
    <CreateCharacter />
</template>

<style scoped>

</style>
