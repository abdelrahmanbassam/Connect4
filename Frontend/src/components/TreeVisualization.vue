<template>
  <div v-if="show" class="modal-overlay">
    <div class="modal-content">
      <div class="modal-header">
        <h2>Game Tree Visualization</h2>
        <button class="close-btn" @click="$emit('close')">×</button>
      </div>
      <div class="tree-container">
        <div class="visualization-area">
          <div class="demo-control-panel">
            <button class="control-btn" @click="updateLayout('LR')">Left to Right</button>
            <button class="control-btn" @click="updateLayout('TB')">Top to Bottom</button>
          </div>
          <v-network-graph
            ref="graph"
            class="graph"
            :nodes="data.nodes"
            :edges="data.edges"
            :layouts="data.layouts"
            :configs="configs"
          >
            <defs>
              <component is="style">
                @font-face { 
                  font-family: 'Material Icons'; 
                  font-style: normal; 
                  font-weight: 400; 
                  src: url(https://fonts.gstatic.com/s/materialicons/v97/flUhRq6tzZclQEJ-Vdg-IuiaDsNcIhQ8tQ.woff2) format('woff2'); 
                }
              </component>
            </defs>
            <template #override-node="{ nodeId, scale, config, ...slotProps }">
              <circle :r="config.radius * scale" :fill="config.color" v-bind="slotProps" />
              <text
                font-family="Material Icons"
                :font-size="40 * scale"
                fill="#ffffff"
                text-anchor="middle"
                dominant-baseline="central"
                style="pointer-events: none"
                v-html="data.nodes[nodeId].icon"
              />
            </template>
          </v-network-graph>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import * as vNG from "v-network-graph";
import staticData from "./data";
import { reactive, watch } from "vue";
import dagre from "dagre/dist/dagre.min.js";

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  treeData: {
    type: Object,
    default: null
  }
});

defineEmits(['close']);

const nodeSize = 30;
const graph = ref();

const configs = vNG.defineConfigs({
  view: {
    autoPanAndZoomOnLoad: "fit-content",
    onBeforeInitialDisplay: () => layout("TB"),
  },
  node: {
    normal: { radius: nodeSize / 2 },
    label: { direction: "north", color: "#fff", lineHeight: 1.5 },
  },
  edge: {
    normal: {
      color: "#aaa",
      width: 3,
    },
    margin: 2,
    marker: {
      target: {
        type: "arrow",
        width: 3,
        height: 3,
      },
    },
  },
});

const data = reactive({
  nodes: staticData.nodes,
  edges: staticData.edges,
  layouts: staticData.layouts,
});

watch(() => props.treeData, (newTreeData) => {
  if (newTreeData) {
    data.nodes = newTreeData.nodes;
    data.edges = newTreeData.edges;
    layout("TB");
  }
}, { deep: true });

function layout(direction) {
  if (Object.keys(data.nodes).length <= 1 || Object.keys(data.edges).length == 0) {
    return;
  }

  const g = new dagre.graphlib.Graph();
  g.setGraph({
    rankdir: direction,
    nodesep: nodeSize * 2,
    edgesep: nodeSize,
    ranksep: nodeSize * 2,
  });
  g.setDefaultEdgeLabel(() => ({}));

  Object.entries(data.nodes).forEach(([nodeId, node]) => {
    g.setNode(nodeId, { label: node.name, width: nodeSize, height: nodeSize });
  });

  Object.values(data.edges).forEach((edge) => {
    g.setEdge(edge.source, edge.target);
  });

  dagre.layout(g);

  g.nodes().forEach((nodeId) => {
    const x = g.node(nodeId).x;
    const y = g.node(nodeId).y;
    data.layouts.nodes[nodeId] = { x, y };
  });
}

function updateLayout(direction) {
  graph.value?.transitionWhile(() => {
    layout(direction);
  });
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: #333;
  width: 90%;
  height: 90%;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.modal-header h2 {
  color: white;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  padding: 0;
  line-height: 1;
}

.close-btn:hover {
  color: #ff4444;
}

.tree-container {
  flex: 1;
  padding: 1rem;
  overflow: hidden;
}

.visualization-area {
  height: 100%;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  padding: 0.5rem;
}

.demo-control-panel {
  margin-bottom: 0.5rem;
  text-align: center;
}

.control-btn {
  margin: 0.5em;
  padding: 0.5rem 1rem;
  border: 1px solid #fff;
  border-radius: 0.25rem;
  background: transparent;
  color: #fff;
  cursor: pointer;
  transition: background-color 0.2s;
}

.control-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.graph {
  height: calc(100% - 50px);
  width: 100%;
}
</style>