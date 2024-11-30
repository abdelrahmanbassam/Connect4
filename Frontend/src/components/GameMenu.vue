<script>
export default {
  name: 'GameMenu',
  data() {
    return {
      selectedAlgorithm: 1,
      firstPlayer: 1,
      searchDepth: 0
    }
  },
  methods: {
    startGame() {
      this.$emit('gameStart', {
        algorithm: this.selectedAlgorithm,
        firstPlayer: this.firstPlayer,
        depth: this.searchDepth
      })
    },
    updateDepth(event) {
      const value = parseInt(event.target.value)
      if (value >= 0 && value <= 42) {
        this.searchDepth = value
      }
    }
  }
}
</script>

<template>
  <div class="menu-container">
    <h1 class="title">Connect Four</h1>
    <div class="settings-card">
      <h2 class="settings-title">Game Settings</h2>
      
      <div class="section">
        <h3 class="section-title">Algorithm</h3>
        <div class="button-group">
          <button 
            :class="['algorithm-btn', selectedAlgorithm === 1 ? 'active' : '']"
            @click="selectedAlgorithm = 1"
          >
            Minimax
          </button>
          <button 
            :class="['algorithm-btn', selectedAlgorithm === 2 ? 'active' : '']"
            @click="selectedAlgorithm = 2"
          >
            Minimax with Pruning
          </button>
          <button 
            :class="['algorithm-btn', selectedAlgorithm === 3 ? 'active' : '']"
            @click="selectedAlgorithm = 3"
          >
            Expected Minimax
          </button>
        </div>
      </div>

      <div class="section">
        <h3 class="section-title">Search Depth</h3>
        <div class="depth-selector">
          <input 
            type="number" 
            :value="searchDepth"
            @input="updateDepth"
            min="0"
            max="42"
            class="depth-input"
          />
          <span class="depth-hint">Choose between 0-42</span>
        </div>
      </div>

      <div class="section">
        <h3 class="section-title">Who starts?</h3>
        <div class="button-group">
          <button 
            :class="['start-btn', firstPlayer === 1 ? 'active' : '']"
            @click="firstPlayer = 1"
          >
            Player Starts
          </button>
          <button 
            :class="['start-btn', firstPlayer === 2 ? 'active' : '']"
            @click="firstPlayer = 2"
          >
            AI Starts
          </button>
        </div>
      </div>

      <button class="start-game-btn" @click="startGame">
        START GAME
      </button>
    </div>
  </div>
</template>

<style scoped>
.menu-container {
  text-align: center;
  padding: 2rem;
}

.title {
  color: #2c3e50;
  font-size: 2.5rem;
  margin-bottom: 2rem;
}

.settings-card {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 0 auto;
}

.settings-title {
  color: #2c3e50;
  font-size: 1.8rem;
  margin-bottom: 2rem;
}

.section {
  margin-bottom: 2rem;
}

.section-title {
  color: #2c3e50;
  font-size: 1.4rem;
  margin-bottom: 1rem;
}

.button-group {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;
}

.algorithm-btn, .start-btn {
  padding: 0.8rem;
  border: 2px solid #4CAF50;
  border-radius: 0.5rem;
  background: white;
  color: #4CAF50;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.algorithm-btn.active, .start-btn.active {
  background: #4CAF50;
  color: white;
}

.depth-selector {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.depth-input {
  width: 100px;
  padding: 0.5rem;
  font-size: 1.2rem;
  border: 2px solid #4CAF50;
  border-radius: 0.5rem;
  text-align: center;
}

.depth-hint {
  color: #666;
  font-size: 0.9rem;
}

.start-game-btn {
  width: 100%;
  padding: 1rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
}

.start-game-btn:hover {
  background: #45a049;
}
</style>