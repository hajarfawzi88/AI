# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states 
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """

        
        
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        Remaining_number_Food=len(newFood.asList())
        Remaining_Food=(newFood).asList()
        newghostposition= successorGameState.getGhostPositions()
        

        
        Big_food=len(successorGameState.getCapsules())
        
        #prints to check:
        print("newPos",newPos)
        print("newScaredTimes",newScaredTimes)
        print("Food Remaining Positions ",Remaining_Food)
        print("number of Food Remaining ",Remaining_number_Food)
        print("food",Big_food)
        print("newGhostStates",newGhostStates)
        #print("newGhostStates",newscaredghostposition)
        
        
        #        Variables to evaluate: 
        #               Food:   min distance, remaining food, Big food
        #               Ghosts: min distance, scared ghosts
        #               Score:  pacman      , state    
               
        
        
        #Distances    
        
        ghostdistances=[manhattanDistance(newPos,ghostState) for ghostState in newghostposition]
        min_ghost_dist = min([manhattanDistance(newPos,ghostState) for ghostState in newghostposition],default=1)
        
        food_dist=[manhattanDistance(newPos,foodstate)for foodstate in Remaining_Food]
        min_food_dist=min([manhattanDistance(newPos,foodstate)for foodstate in Remaining_Food],default=1)
        
        #newscaredghostposition=[ghostState for ghostState in newGhostStates if ghostState.scaredTimer]
        min_scared_ghost_dist=0

        newscaredghostposition=[]
        for ghostState in newGhostStates:
            if ghostState.scaredTimer:
                newscaredghostposition.append(ghostState)
                print("The ghost state is",ghostState)
        if newscaredghostposition:
                min_scared_ghost_dist = min([manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newscaredghostposition], default=0)
            
        #prints to check:
        #print("ghost_dist",ghostdistances)
        print("min_ghost_dist",min_ghost_dist)
        print("min_food_dist",min_food_dist)
        
        #Scores
        game_score=successorGameState.getScore()
        if min_ghost_dist!=0:
              State_score=game_score- min_food_dist -3.5*Remaining_number_Food-(3./ min_ghost_dist)-30*Big_food  -2*min_scared_ghost_dist
        else:
              State_score=game_score- min_food_dist -3.5*Remaining_number_Food                     -30*Big_food  -2*min_scared_ghost_dist 
        
        

        "*** YOUR CODE HERE ***"
        return State_score

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)




class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    
    def Recursive_minmax(self,gameState,depth,agent):
        
             if depth==0 or gameState.isWin() or gameState.isLose():
                 evaluation = self.evaluationFunction(gameState)
                 #print("youuuuuuuuuu",evaluation)
                 return evaluation
                 
             if agent==True: #maximizing-pacman
                 Maxaeval= float('-inf')  
                 """for each child of node do  
                    eva= minimax(child, depth-1, false)  
                    maxEva= max(maxEva,eva)        //gives Maximum of the values  
                    return maxEva  """
                 agent_index=0
                 legal_actions=gameState.getLegalActions(agent_index)
                 for legal in legal_actions:
                     new_successor_game_state=gameState.generateSuccessor(agent_index, legal)
                     evaluation=self.Recursive_minmax(new_successor_game_state,depth-1,False)
                     Maxaeval=max(Maxaeval,evaluation)
                 return Maxaeval
             
             else: #minimizing-ghosts
                 Minaeval= float('inf')  
                 """ minEva= +infinity   
                     for each child of node do  
                     eva= minimax(child, depth-1, true)  
                     minEva= min(minEva, eva)         //gives minimum of the values  
                     return minEva  """
                 number_of_agents=gameState.getNumAgents()
                 for ghost_index in range(1,number_of_agents):
                     legal_actions=gameState.getLegalActions(ghost_index)
                     for legal in legal_actions:
                         new_successor_game_state=gameState.generateSuccessor(ghost_index, legal)
                         evaluation=self.Recursive_minmax(new_successor_game_state,depth,True)
                         Minaeval=min(Minaeval,evaluation)
                 return Minaeval
             
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action
        
        from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):                                             xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):                                   xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game                                    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

        gameState.isWin():                                                                xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state                            xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        """
        "*** YOUR CODE HERE ***"
        minimax_action=None
        initial_eval=float('-inf')
        #index of pacman
        agentIndex=0
        legal_actions=gameState.getLegalActions(agentIndex)
        
        for legal_action in legal_actions:
             successor_game_state=gameState.generateSuccessor(agentIndex, legal_action)
             #starting the loop with the first ghost
             #agentIndex_of_ghosts=1
             Evaluation=self.Recursive_minmax(successor_game_state,self.depth,True)
             if Evaluation>initial_eval:
                 initial_eval=Evaluation
                 minimax_action=legal_action
                
                 print("minimax_action",minimax_action)
                      
        # totatl_agents=gameState.getNumAgents()
        # gameState.isWin()
        # gameState.isLose()
        
        return minimax_action
        
        
        

                 
             
             
             

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def Recursive_minmax(self,gameState,depth,agent,alpha,beta):
            
             if depth==0 or gameState.isWin() or gameState.isLose():
                 evaluation = self.evaluationFunction(gameState)
                 #print("youuuuuuuuuu",evaluation)
                 return evaluation
              
              
             if agent==True: #maximizing-pacman
                 Maxaeval= float('-inf')  
                 """for each child of node do  
                    eva= minimax(child, depth-1, false)  
                    maxEva= max(maxEva,eva)        //gives Maximum of the values  
                    return maxEva  """
                 agent_index=0
                 legal_actions=gameState.getLegalActions(agent_index)
                 for legal in legal_actions:
                     #legal_actions=gameState.getLegalActions(agent_index) 
                     new_successor_game_state=gameState.generateSuccessor(agent_index, legal)
                     evaluation=max(self.Recursive_minmax(new_successor_game_state,depth-1,False,alpha,beta),Maxaeval)
                     
                     Maxaeval=max(Maxaeval,evaluation)
                     alpha=max(alpha,evaluation)
                     if alpha>=beta:
                         break
                 return Maxaeval
             
             else: #minimizing-ghosts
                 Minaeval= float('inf')  
                 """ minEva= +infinity   
                     for each child of node do  
                     eva= minimax(child, depth-1, true)  
                     minEva= min(minEva, eva)         //gives minimum of the values  
                     return minEva  """
                 number_of_agents=gameState.getNumAgents()
                 for ghost_index in range(1,number_of_agents):
                     legal_actions=gameState.getLegalActions(ghost_index)
                     for legal in legal_actions:
                         new_successor_game_state=gameState.generateSuccessor(ghost_index, legal)
                         evaluation=min(self.Recursive_minmax(new_successor_game_state,depth-int(ghost_index == 0),True,alpha,beta),Minaeval)
                         Minaeval=min(Minaeval,evaluation)
                         beta=min(evaluation,beta)
                         if alpha>=beta:
                             break
                         
                 return Minaeval
             
    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha=float('-inf')  
        beta=float('inf')  
        alphabeta_action=None
        #index of pacman
        agentIndex=0
        agent=True
        legal_actions=gameState.getLegalActions(agentIndex)
        
        for legal_action in legal_actions:
             successor_game_state=gameState.generateSuccessor(agentIndex, legal_action)
             #starting the loop with the first ghost
             #agentIndex_of_ghosts=1
             Evaluation=self.Recursive_minmax(successor_game_state,self.depth,agent,alpha,beta)
             if Evaluation>alpha:
                 alpha=Evaluation
                 alphabeta_action=legal_action
 
        return alphabeta_action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """
    def Recursive_minmax(self, gameState, depth, agent_index):
        
             if depth==0 or gameState.isWin() or gameState.isLose():
                 evaluation = self.evaluationFunction(gameState)
                 #print("youuuuuuuuuu",evaluation)
                 return evaluation
              
             legal_actions=gameState.getLegalActions(agent_index)
             total_actions=len(legal_actions)
             if agent_index==0: #maximizing-pacman
                 Maxaeval= float('-inf')  
                 """for each child of node do  
                    eva= minimax(child, depth-1, false)  
                    maxEva= max(maxEva,eva)        //gives Maximum of the values  
                    return maxEva  """
                 #agent_index=0
                 
                 for legal in legal_actions:
                     #legal_actions=gameState.getLegalActions(agent_index) 
                     new_successor_game_state=gameState.generateSuccessor(agent_index, legal)
                     evaluation=self.Recursive_minmax(new_successor_game_state,depth-1,1)
                     Maxaeval=max(Maxaeval,evaluation)
                 return Maxaeval
             
             else: #minimizing-ghosts
                 #Minaeval= float('inf')
                 expected=0  
                 """ minEva= +infinity   
                     for each child of node do  
                     eva= minimax(child, depth-1, true)  
                     minEva= min(minEva, eva)         //gives minimum of the values  
                     return minEva  """
                 for legal in legal_actions:
                         
                         new_successor_game_state=gameState.generateSuccessor(agent_index, legal)
                         number_of_agents=gameState.getNumAgents()
                         next_index=agent_index +1 %number_of_agents
                         check=int(agent_index == gameState.getNumAgents() - 1)
                         evaluation=self.Recursive_minmax(new_successor_game_state,depth-check ,next_index)
                         expected+=evaluation * 1/total_actions 

                         
             return expected

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        initial_eval=float('-inf')  
        #beta=float('inf')  
        Expect_action=None
        #index of pacman
        agentIndex=0
        agent=True
        legal_actions=gameState.getLegalActions(agentIndex)
        
        for legal_action in legal_actions:
             successor_game_state=gameState.generateSuccessor(agentIndex, legal_action)
             #starting the loop with the first ghost
             #agentIndex_of_ghosts=1
             Evaluation=self.Recursive_minmax(successor_game_state,self.depth,agentIndex)
             if Evaluation>initial_eval:
                 initial_eval=Evaluation
                 Expect_action=legal_action
 
        return Expect_action
    
    
    

def betterEvaluationFunction(currentGameState):
        """
              Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
            evaluation function (question 5).
        """
        # Useful information you can extract from a GameState (pacman.py)
        #successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        Remaining_number_Food=len(newFood.asList())
        Remaining_Food=(newFood).asList()
        newghostposition= currentGameState.getGhostPositions()
        

        
        Big_food=len(currentGameState.getCapsules())
        
        #prints to check:
        print("newPos",newPos)
        print("newScaredTimes",newScaredTimes)
        print("Food Remaining Positions ",Remaining_Food)
        print("number of Food Remaining ",Remaining_number_Food)
        print("food",Big_food)
        print("newGhostStates",newGhostStates)
        #print("newGhostStates",newscaredghostposition)
        
        
        #        Variables to evaluate: 
        #               Food:   min distance, remaining food, Big food
        #               Ghosts: min distance, scared ghosts
        #               Score:  pacman      , state    
               
        
        
        #Distances    
        
        ghostdistances=[manhattanDistance(newPos,ghostState) for ghostState in newghostposition]
        min_ghost_dist = min([manhattanDistance(newPos,ghostState) for ghostState in newghostposition],default=1)
        
        food_dist=[manhattanDistance(newPos,foodstate)for foodstate in Remaining_Food]
        min_food_dist=min([manhattanDistance(newPos,foodstate)for foodstate in Remaining_Food],default=1)
        
        #newscaredghostposition=[ghostState for ghostState in newGhostStates if ghostState.scaredTimer]
        min_scared_ghost_dist=0

        newscaredghostposition=[]
        for ghostState in newGhostStates:
            if ghostState.scaredTimer:
                newscaredghostposition.append(ghostState)
                print("The ghost state is",ghostState)
        if newscaredghostposition:
                min_scared_ghost_dist = min([manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newscaredghostposition], default=0)
            
        #prints to check:
        #print("ghost_dist",ghostdistances)
        print("min_ghost_dist",min_ghost_dist)
        print("min_food_dist",min_food_dist)
        
        #Scores
        game_score=currentGameState.getScore()
        if min_ghost_dist!=0:
              State_score=game_score- min_food_dist -3.5*Remaining_number_Food-(3./ min_ghost_dist)-30*Big_food  -2*min_scared_ghost_dist
        else:
              State_score=game_score- min_food_dist -3.5*Remaining_number_Food                     -30*Big_food  -2*min_scared_ghost_dist 
        
        return State_score


# Abbreviation
better = betterEvaluationFunction
