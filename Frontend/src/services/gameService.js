export const gameService = {
  // async initializeGame(settings) {
  //   try {
  //     // Commented for now until backend is ready
  //     /* const response = await fetch('/api/game/initialize', {
  //       method: 'POST',
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //       body: JSON.stringify({
  //         algorithm: settings.algorithm,
  //         firstPlayer: settings.firstPlayer
  //       })
  //     });
      
  //     const data = await response.json();
  //     return {
  //       board: data.board,
  //       currentPlayer: data.currentPlayer,
  //       playerScore: data.playerScore,
  //       aiScore: data.aiScore,
  //       gameTree: data.gameTree
  //     }; */

  //     // Temporary mock response
  //     return {
  //       board: Array(6).fill().map(() => Array(7).fill(0)),
  //       currentPlayer: settings.firstPlayer === 'player' ? 1 : 2,
  //       playerScore: 0,
  //       aiScore: 0,
  //       gameTree: null
  //     };
  //   } catch (error) {
  //     console.error('Error initializing game:', error);
  //     return null;
  //   }
  // },
  async sendGameInfoToBackend(board,settings) {
    try {
      let body ={
        board: board,
        algorithm: settings.algorithm,
        firstPlayer: settings.firstPlayer,
        depth: settings.depth
      }
      console.log(JSON.stringify(body, null, 2))
     
      // Commented for now until backend is ready
      /* const response = await fetch('/api/game/move', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          board,
          
        })
      });
      
      const data = await response.json();
      return {
        board: data.board,
        playerScore: data.playerScore,
        aiScore: data.aiScore,
        expandedNodes: data.expandedNodes,
        gameTree: data.gameTree
      }; */

      // Temporary mock response
      
      return {
        board: this.mockAIMove(board),
        // board: Array(6).fill().map(() => Array(7).fill().map(() => Math.round(Math.random()))),
        playerScore: 12,
        aiScore: 7,
        expandedNodes: 5,
        gameTree: null
      };
    } catch (error) {
      console.error('Error sending move to backend:', error);
      return null;
    }
  },
  // Temporary mock AI move - will be replaced by backend
  mockAIMove(board) {
    const newBoard = board.map(row => [...row]);
    const availableCols = [];
    
    // Find available columns
    for (let col = 0; col < 7; col++) {
      if (newBoard[0][col] === 0) {
        availableCols.push(col);
      }
    }
    
    if (availableCols.length > 0) {
      const randomCol = availableCols[Math.floor(Math.random() * availableCols.length)];
      // Find lowest empty row in chosen column
      for (let row = 5; row >= 0; row--) {
        if (newBoard[row][randomCol] === 0) {
          newBoard[row][randomCol] = 2; // AI plays as 2
          break;
        }
      }
    }
    
    return newBoard;
  }
}