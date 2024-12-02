<template>
  <div class="tree-container">
    <h3 class="title">Game Tree Visualization</h3>
    <div class="visualization-area">
      <div class="demo-control-panel">
        <el-button @click="updateLayout('LR')">Left to Right</el-button>
        <el-button @click="updateLayout('TB')">Top to Bottom</el-button>
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
      <!-- Cannot use <style> directly due to restrictions of Vue. -->
      <component is="style">
        @font-face { font-family: 'Material Icons'; font-style: normal; font-weight:
        400; src:
        url(https://fonts.gstatic.com/s/materialicons/v97/flUhRq6tzZclQEJ-Vdg-IuiaDsNcIhQ8tQ.woff2)
        format('woff2'); }
      </component>
    </defs>
        <!-- Replace the node component -->
        <template #override-node="{ nodeId, scale, config, ...slotProps }">
      <circle :r="config.radius * scale" :fill="config.color" v-bind="slotProps" />
      <!-- Use v-html to interpret escape sequences for icon characters. -->
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
    <template #edge-label="{ edge, ...slotProps }">
      <v-edge-label :text="edge.label" align="center" vertical-align="above" v-bind="slotProps" />
    </template>
    </v-network-graph>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import * as vNG from "v-network-graph";
import staticData from "./data";
import { reactive, watch } from "vue";
// dagre: Directed graph layout for JavaScript
// https://github.com/dagrejs/dagre
//@ts-ignore
import dagre from "dagre/dist/dagre.min.js";

const nodeSize = 30;

const configs = vNG.defineConfigs({
  view: {
    autoPanAndZoomOnLoad: "fit-content",
    onBeforeInitialDisplay: () => layout("TB"),
  },
  node: {
    normal: { radius: nodeSize / 2 },
    label: { direction: "north", color: "#fff", lineHeight: 1.5 , fontSize: 11},
  },
  edge: {
    normal: {
      color: "#aaa",
      width: 3,
    },
    label: { color: "#aaa", fontSize: 12},
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

const graph = ref<vNG.VNetworkGraphInstance>();
// Props
const props = defineProps<{ treeData: { nodes: any; edges: any } | null }>();

// Use the initial data from `data.ts`
const data = reactive({
  nodes: staticData.nodes,
  edges: staticData.edges,
  layouts: staticData.layouts,
});

// Watch for dynamic updates to `treeData`
watch(() => props.treeData, (newTreeData) => {
  if (newTreeData) {
    data.nodes = newTreeData.nodes;
    data.edges = newTreeData.edges;
    layout("TB"); // Re-layout the graph
  }
}, { deep: true });
function layout(direction: "TB" | "LR") {
  if (Object.keys(data.nodes).length <= 1 || Object.keys(data.edges).length == 0) {
    return;
  }

  // convert graph
  // ref: https://github.com/dagrejs/dagre/wiki
  const g = new dagre.graphlib.Graph();
  // Set an object for the graph label
  g.setGraph({
    rankdir: direction,
    nodesep: nodeSize * 2,
    edgesep: nodeSize,
    ranksep: nodeSize * 2,
  });
  // Default to assigning a new object as a label for each new edge.
  // g.setDefaultEdgeLabel(() => ({}));

  // Add nodes to the graph. The first argument is the node id. The second is
  // metadata about the node. In this case we're going to add labels to each of
  // our nodes.
  Object.entries(data.nodes).forEach(([nodeId, node]) => {
    g.setNode(nodeId, { label: node.name, width: nodeSize, height: nodeSize });
  });

  // Add edges to the graph.
  Object.values(data.edges).forEach((edge) => {
    g.setEdge(edge.source, edge.target, {label: edge.label});
  });

  dagre.layout(g);

  g.nodes().forEach((nodeId: string) => {
    // update node position
    const x = g.node(nodeId).x;
    const y = g.node(nodeId).y;
    data.layouts.nodes[nodeId] = { x, y };
  });
}

function updateLayout(direction: "TB" | "LR") {
  // Animates the movement of an element.
  graph.value?.transitionWhile(() => {
    layout(direction);
  });
}
</script>

<style scoped>
.tree-container {
  height: 90%;
  width: 100%;
}

.title {
  margin-bottom: 1rem;
  margin-top: 0;
  text-align: center;
}

.visualization-area {
  height: calc(90% - 1rem);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 0.5rem;
  padding: 0.5rem;
}

.demo-control-panel {
  margin-bottom: 0.5rem;
  text-align: center;
}
/* style el-button */
el-button {
  margin: 0.5em;
  padding: 0.3rem;
  border: 1px solid #fff;
  border-radius: 0.25rem;
  cursor: pointer;
}
</style>
