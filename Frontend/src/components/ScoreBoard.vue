<template>
  <div class="score-container">
    <div class="score-card">
      <h3 class="score-label">Player Score</h3>
      <div class="score-value player">{{ playerScore }}</div>
    </div>
    
    <div class="score-card">
      <h3 class="score-label">AI Score</h3>
      <div class="score-value ai">{{ aiScore }}</div>
    </div>

    <div class="expanded-nodes">
      <h3 class="nodes-label">Expanded Nodes</h3>
      <div class="nodes-value">{{ expandedNodes }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ScoreBoard',
  props: {
    playerScore: {
      type: Number,
      default: 0
    },
    aiScore: {
      type: Number,
      default: 0
    },
    expandedNodes: {
      type: Number,
      default: 0
    }
  }
}
</script>

<style scoped>
.score-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.score-card {
  text-align: center;
  padding: 0.5rem;
  background: #f5f5f5;
  border-radius: 0.5rem;
}

.score-label, .nodes-label {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.score-value {
  font-size: 2rem;
  font-weight: bold;
}

.score-value.player {
  color: #eded3b;
}

.score-value.ai {
  color: #f44336;
}

.expanded-nodes {
  text-align: center;
  padding: 0.5rem;
  background: #f5f5f5;
  border-radius: 0.5rem;
}

.nodes-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2c3e50;
}
</style>