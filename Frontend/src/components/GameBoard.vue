<template>
  <div class="game-container">
    <h1 class="title">Connect Four</h1>
    
    <div class="game-layout">
      <div class="scores-container">
        <ScoreBoard 
          :playerScore="playerScore"
          :aiScore="aiScore"
          :expandedNodes="expandedNodes"
        />
        
        <div class="status-container">
          <h2 class="status">{{ gameStatus }}</h2>
          <button class="new-game-btn" @click="newGame">New Game</button>
        </div>
      </div>

      <div class="board-container">
        <div 
          v-if="currentPlayer === 1 && hoveredColumn !== -1 && !isProcessing" 
          class="hover-disc player-disc"
          :style="{ left: `${hoveredColumn * 80 + 22  }px` }"
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
                  'player-disc': cell === 1,
                  'ai-disc': cell === 2
                }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <TreeVisualization class="tree-viz" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, inject } from 'vue'
import ScoreBoard from './ScoreBoard.vue'
import TreeVisualization from './TreeVisualization.vue'
import { gameService } from '../services/gameService'

export default {
  name: 'GameBoard',
  components: {
    ScoreBoard,
    TreeVisualization
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
    const currentPlayer = ref(1) // 1 for player, 2 for AI
    const playerScore = ref(0)
    const aiScore = ref(0)
    const expandedNodes = ref(0)
    const gameStatus = ref('Your Turn')
    const hoveredColumn = ref(-1)
    const isProcessing = ref(false)
   
    // Initialize game with settings
    onMounted(() => {
      console.log('GameBoard mounted')
      // console.log(JSON.stringify(board.value, null, 2))
      // console.log(JSON.stringify(props.settings.value, null, 2))

      gameService.sendGameInfoToBackend(board.value, props.settings)
      // initGame()
    })
    // const initGame = async () => {
    //   console.log("Initializing game with settings:", props.settings)
    //   isProcessing.value = true
    //   const response = await gameService.initializeGame(props.settings)
      
    //   if (response) {
    //     board.value = response.board
    //     currentPlayer.value = response.currentPlayer
    //     playerScore.value = response.playerScore
    //     aiScore.value = response.aiScore
    //     gameStatus.value = currentPlayer.value === 1 ? 'Your Turn' : 'AI Turn'
        
    //     if (currentPlayer.value === 2) {
    //       // If AI starts, make the first move
    //       await makeMove()
    //     }
    //   }
      
    //   isProcessing.value = false
    // }

    const newGame = () => {
      showMenu.value = true
    }

    const makeMove = async (col) => {
      if (!isValidMove(col) || isProcessing.value || currentPlayer.value !== 1) return
      
      const row = getLowestEmptyRow(col)
      if (row === -1) return

      isProcessing.value = true
      board.value[row][col] = 1 // Player move
      
      // Send move to backend and wait for AI response
          console.log(JSON.stringify(props.settings, null, 2))
          console.log(JSON.stringify(props.settings, null, 2))

      const response = await gameService.sendGameInfoToBackend(board.value, currentPlayer.value)
      
      if (response) {
        board.value = response.board
        playerScore.value = response.playerScore
        aiScore.value = response.aiScore
        expandedNodes.value = response.expandedNodes
        // Update tree visualization here when implemented
      }
      
      isProcessing.value = false
      gameStatus.value = 'Your Turn'
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
      if (!isProcessing.value && currentPlayer.value === 1) {
        hoveredColumn.value = colIndex
      }
    }

    const handleMouseLeave = () => {
      hoveredColumn.value = -1
    }

    return {
      board,
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
      isProcessing
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
  grid-template-columns: 1fr 2fr 1fr;
  gap: 2rem;
  align-items: start;
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

.new-game-btn {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.new-game-btn:hover {
  background: #45a049;
}

.board-container {
  position: relative;
  padding-top: 70px;
}

.hover-disc {
  position: absolute;
  top: 0;
  width: 60px;
  height: 60px;
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
  width: 70px;
  height: 70px;
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
  background: #2196F3;
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