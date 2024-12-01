export const gameService = {
    async sendGameInfoToBackend(board, settings) {
    try {
      // console.log('Sending move to backend...');
      let body = {
        board: board,
        algorithm: settings.algorithm,
        aiTurn: settings.aiTurn,
        depth: settings.depth
      };
      // console.log(JSON.stringify(body, null, 2));
  
      const response = await fetch('http://localhost:5000/api/game/move', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
      });
      // console.log('Move sent to backend');

      const data = await response.json();
      return {
        board: data.board,
        playerScore: (settings.aiTurn === 2) ? data.player1_score : data.player2_score,
        aiScore: (settings.aiTurn === 1) ? data.player1_score : data.player2_score,
        expandedNodes: data.nodes_expanded,
        gameTree: {
          nodes: data.tree.nodes,
          edges: data.tree.edges
        }
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