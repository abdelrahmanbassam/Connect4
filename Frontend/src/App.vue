<script setup>
import { ref, provide } from 'vue'
import GameMenu from './components/GameMenu.vue'
import GameBoard from './components/GameBoard.vue'

const showMenu = ref(true)
const gameSettings = ref(null)

provide('showMenu', showMenu)

const handleGameStart = (settings) => {
  gameSettings.value = settings
  showMenu.value = false
}
</script>

<template>
  <div class="app-container">
    <GameMenu v-if="showMenu" @gameStart="handleGameStart" />
    <GameBoard v-else :settings="gameSettings" />
  </div>
</template>

<style>
.app-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}
</style>