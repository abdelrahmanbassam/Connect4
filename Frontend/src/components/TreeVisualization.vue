<template>
  <div class="tree-container">
    <h3 class="title">Game Tree Visualization</h3>
    <div class="visualization-area">
      <!-- Tree visualization will be implemented later -->
    </div>
  </div>
</template>

<script>
export default {
  name: 'TreeVisualization'
}
</script>


<style scoped>
.tree-container {
  height: 100%;
}

.title {
  margin-bottom: 1rem;
  text-align: center;
}

.visualization-area {
  height: calc(100% - 2rem);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
}
</style>