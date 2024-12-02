<template>
  <div class="game-container">
    <!-- <h1 class="title">Connect Four</h1> -->
    
    <div class="game-layout">
      <div class="scores-container">
        <ScoreBoard 
          :playerScore="playerScore"
          :aiScore="aiScore"
          :expandedNodes="expandedNodes"
        />
        
        <div class="status-container">
          <h2 class="status">{{ gameStatus }}</h2>
          <div class="button-container">
            <button class="game-btn" @click="newGame">New Game</button>
            <button class="game-btn show-tree-btn" @click="updateTree">Show Tree</button>
          </div>
        </div>
      </div>

      <div class="board-container">
        <div 
          v-if="currentPlayer === playerTurn && hoveredColumn !== -1 && !isProcessing" 
          class="hover-disc player-disc"
          :style="{ left: `${hoveredColumn * 110 + 22}px` }"
        ></div>
        
        <div class="board">
          <div 
            v-for="(row, rowIndex) in board" 
            :key="rowIndex" 
            class="board-row"
          >
            <div 
              v-for="(cell, colIndex) in row" 
              :key="colIndex" 
              class="cell"
              @click="makeMove(colIndex)"
              @mousemove="handleMouseMove(colIndex)"
              @mouseleave="handleMouseLeave"
            >
              <div 
                class="disc" 
                :class="{
                  'player-disc': cell === playerTurn,
                  'ai-disc': cell === aiTurn
                }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <TreeVisualization 
      :show="showTreeModal"
      :treeData="treeFromBack"
      @close="showTreeModal = false"
    />
    
  </div>
</template>

<script>
import { ref, onMounted, inject } from 'vue'
import ScoreBoard from './ScoreBoard.vue'
import TreeVisualization from './TreeVisualization.vue'
//treex
// import TreeModal from './TreeModal.vue'
import { gameService } from '../services/gameService'

export default {
  name: 'GameBoard',
  components: {
    ScoreBoard,
    TreeVisualization
    // TreeModal
  },
  props: {
    settings: {
      type: Object,
      required: true
    }
  },
  setup(props) {
    const showMenu = inject('showMenu')
    const board = ref(Array(6).fill().map(() => Array(7).fill(0)))
    const playerTurn = ref(props.settings.playerTurn);
    const aiTurn = ref(props.settings.aiTurn);
    const currentPlayer = ref(1) // 1 for player, 2 for AI
    const playerScore = ref(0)
    const aiScore = ref(0)
    const expandedNodes = ref(0)
    const gameStatus = ref('Your Turn')
    const hoveredColumn = ref(-1)
    const isProcessing = ref(false)
    const currentTree = ref(null)
    const treeFromBack = ref(null); // Ref to hold dynamic game tree data
    // treex
    const showTreeModal = ref(false)

    // Initialize game with settings
    onMounted(() => {
      // console.log('GameBoard mounted')
      // console.log(JSON.stringify(props.settings, null, 2))
      // console.log(playerTurn.value)
      if(playerTurn.value === 2) {
        aiAgentTurn()
      }
    })
    

    const newGame = () => {
      showMenu.value = true
    }

    //this method needs some work and edits
    const makeMove = async (col) => {
      if (!isValidMove(col) || isProcessing.value || currentPlayer.value !== playerTurn.value) return
      
      const row = getLowestEmptyRow(col)
      if (row === -1) return


      board.value[row][col] = playerTurn.value

      // console.log("after player move")
      aiAgentTurn()
    }
    
    const aiAgentTurn = async () => {
      isProcessing.value = true
      gameStatus.value = 'AI is thinking...'
      currentPlayer.value =  aiTurn.value

      await updateValues();

      isProcessing.value = false
      gameStatus.value = 'Your Turn'
      currentPlayer.value = playerTurn.value
      // console.log(currentPlayer.value, playerTurn.value, isProcessing.value)
    }
    const updateValues = async () => {
      const response = await gameService.sendGameInfoToBackend(board.value,props.settings)
      console.log("response arrived")
      if (response) {
        board.value = response.board
        playerScore.value = response.playerScore
        aiScore.value = response.aiScore
        expandedNodes.value = response.expandedNodes
        currentTree.value = response.gameTree
        // console.log(treeFromBack.value)
      }
    }
    const updateTree = () => {
      showTreeModal.value = true;
      treeFromBack.value = currentTree.value;
      // Additional logic to update the tree can be added here
    }
    const isValidMove = (col) => {
      return col >= 0 && col < 7 && board.value[0][col] === 0
    }

    const getLowestEmptyRow = (col) => {
      for (let row = 5; row >= 0; row--) {
        if (board.value[row][col] === 0) return row
      }
      return -1
    }

    const handleMouseMove = (colIndex) => {
      // console.log(isProcessing.value)
      if (!isProcessing.value && currentPlayer.value === playerTurn.value) {
        hoveredColumn.value = colIndex
      }
      // console.log( hoveredColumn.value)
    }

    const handleMouseLeave = () => {
      hoveredColumn.value = -1
    }

    return {
      board,
      currentTree,
      aiTurn,
      playerTurn,
      currentPlayer,
      playerScore,
      aiScore,
      expandedNodes,
      gameStatus,
      newGame,
      makeMove,
      hoveredColumn,
      handleMouseMove,
      handleMouseLeave,
      isProcessing,
      treeFromBack,
      showTreeModal,
      updateTree 
    }
  }
}
</script>

<style scoped>
.game-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.title {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 2rem;
}

.game-layout {
  
  display: grid;
  grid-template-columns: 1fr 2fr 2fr;
  gap: 2rem;
  align-items: center;
}

.scores-container {
  
  background: white;
  border-radius: 1rem;
  padding: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.status-container {
  
  text-align: center;
  margin-top: 1rem;
}

.status {
  color: #2c3e50;
  margin-bottom: 1rem;
}

/* .new-game-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
} */
.button-container {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.game-btn {
  background: #4CAF50;
  font-size: 20px;
  color: rgb(240, 240, 240);
  border: none;
  padding: 1rem 0.9rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.show-tree-btn {
  background: #2196F3;
}
.new-game-btn:hover {
  background: #45a049;
}

.board-container {
  position: relative;
  padding-top: 100px;
}

.hover-disc {
  position: absolute;
  top: 0px;
  /* bottom: 10px; */
  width: 95px;
  height: 95px;
  border-radius: 50%;
  transition: left 0.1s ease;
}

.board {
  position: relative;
  background: #1a237e;
  padding: 1rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.board-row {
  display: flex;
  justify-content: center;
}

.cell {
  width: 100px;
  height: 100px;
  padding: 5px;
  cursor: pointer;
}

.disc {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: white;
  transition: background-color 0.3s ease;
}

.player-disc {
  background: #eded3b;
}

.ai-disc {
  background: #f44336;
}

.tree-viz {
  background: #333;
  border-radius: 1rem;
  padding: 1rem;
  color: white;
  min-height: 400px;
}
</style>