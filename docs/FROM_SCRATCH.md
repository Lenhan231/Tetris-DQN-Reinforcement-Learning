# Learning Deep Q-Learning From Scratch

A complete beginner's guide. No prior knowledge needed.

---

## Part 1: What is Tetris? (5 min)

### The Game
You know Tetris, right? Blocks fall from the top. You arrange them. Clear lines = points.

```
Current Board:        New Piece Falls:
[ ][ ][ ][ ]          [ ][ ][ ][ ]
[X][ ][X][ ]          [X][X][X][X]  ← I-piece (4 blocks in a line)
[X][X][X][ ]               ↓
[X][X][X][X]          Position it to clear lines
```

### Goal
Make an AI that plays Tetris automatically. Better placements = more points.

---

## Part 2: How Does AI Learn? (10 min)

### The Learning Problem

Imagine teaching your friend to play Tetris:

```
You: "Where should I place this piece?"
Friend: "I don't know..."
You: "Place it HERE and you'll clear 2 lines!"
Friend: "Oh! So placing pieces to clear lines = good!"

After 100 games:
Friend learns patterns:
  - Avoid creating holes ✓
  - Keep the board flat ✓
  - Set up 4-line combos ✓
Friend plays better!
```

### This is Reinforcement Learning

```
AI learns by:
  1. Take action (place piece)
  2. Get reward (points)
  3. Learn what action was good/bad
  4. Repeat 1000 times
  5. Becomes expert
```

---

## Part 3: What is a Neural Network? (15 min)

### The Problem

How does the AI decide WHERE to place a piece?

```
Board looks like:
  [holes=3, height=15, lines=10, bumpiness=4]
        ↓
   AI needs to decide: "Is this a good position?"
```

### Simple Approach (Won't Work)

```
If holes < 5 and height < 10:
    Place piece
Else:
    Don't place

Problem: Too simple! Can't handle complex patterns.
```

### Better Approach: Neural Network

Think of it like a brain that learns:

```
Input (what the board looks like):
  [holes=3, height=15, lines=10, bumpiness=4]
    ↓
  Brain (learns patterns):
    - If many holes → bad
    - If height high → bad
    - If lines cleared → good
    ↓
Output (score for this position):
  "This position is worth 45.2 points in the future"
```

### How Neural Network Works

```
INPUT: [holes=3, height=15, lines=10, bumpiness=4]
  ↓
LAYER 1 (64 neurons - learn patterns):
  "Is there many holes?" → yes
  "Is height tall?" → yes
  "Will this position allow line clears?" → maybe
  ↓
LAYER 2 (32 neurons - combine patterns):
  "This looks like a bad position"
  "But could lead to better future"
  ↓
OUTPUT: Q-value = 45.2
  "Future reward will be 45.2 points"
```

### Why 64, then 32 neurons?

- **64 neurons**: Learn many individual patterns
- **32 neurons**: Combine and compress patterns
- **1 output**: Final decision (quality of position)

It's like:
```
Apprentice (64): Notices lots of details
Master (32): Combines details into wisdom
Sensei (1): Final judgment
```

---

## Part 4: The Bellman Equation - The Secret Sauce (20 min)

### The Key Insight

A good position = immediate reward + future potential

```
Example: You place a piece

Immediate: Clear 1 line = 101 points NOW
Future: This move sets up a 4-line combo soon = 400 points LATER

Total value of this move = 101 + 400 = 501 points!
```

### Bellman Equation (Fancy Math)

```
Q(position) = immediate_reward + future_reward
Q(position) = reward + 0.99 × Q(next_position)

English: "Value now = points now + most of the value later"
```

### Why 0.99?

```
0.99 = "Future is worth 99% of now"

Why not 1.0? Because:
  - Future is uncertain
  - We care about immediate points too
  - Prevents infinite loops

Why not 0.5? Because:
  - We care about good future plans
  - Want the AI to think ahead
```

### Real Example

```
Current position: [holes=2, height=10]
You place piece

Immediate reward: 50 points (some lines cleared)
Next position: [holes=1, height=9]
  Future Q-value: 80 (good position for more lines)

Bellman says:
Q = 50 + 0.99 × 80 = 50 + 79.2 = 129.2 points total
```

**This piece is worth 129.2 points!** (Not just 50)

---

## Part 5: How Does Network Learn? (20 min)

### The Training Loop

```
STEP 1: Predict (guess)
  Network sees: [holes=2, height=10]
  Network guesses: Q = 40 points
  
STEP 2: Reality (truth)
  Bellman equation says: Q = 129.2 points (from real game)
  
STEP 3: Error
  Difference: 129.2 - 40 = 89.2 (huge error!)
  Network was VERY wrong
  
STEP 4: Learn
  Network updates weights
  Next time it sees similar board, it will guess higher
  
STEP 5: Test again
  Next time same board: Network says Q = 100 (closer!)
  
STEP 6: Repeat
  After 1000 games: Network says Q = 129 (correct!)
```

### Visualization: Learning Process

```
Game 1:
  Network: "I predict 10 points"
  Reality: "Actually 100 points!"
  Error: 90 ❌

Game 10:
  Network: "I predict 60 points"
  Reality: "Actually 100 points"
  Error: 40 ❌ (getting better)

Game 100:
  Network: "I predict 95 points"
  Reality: "Actually 100 points"
  Error: 5 ❌ (almost there!)

Game 1000:
  Network: "I predict 100 points"
  Reality: "Actually 100 points"
  Error: 0 ✅ (learned!)
```

---

## Part 6: Q-Learning vs Training (15 min)

### What's Q-Learning?

"Q" = Quality of an action

```
Q-Learning = Learn the QUALITY of positions

High Q = Good position (more future points)
Low Q = Bad position (fewer future points)
```

### Difference: Learning vs Playing

### TRAINING PHASE (Learning)

```python
for 300 games:
    # Play game, store experiences
    state = current_board
    action = place_piece()
    reward = points_earned
    next_state = new_board
    
    # Learn from experience
    Q_truth = reward + 0.99 * network(next_state)
    Q_predicted = network(state)
    error = Q_truth - Q_predicted
    
    # Update network weights
    network.learn(error)  # Network improves
```

**Network gets better and better!**

### TESTING PHASE (Playing)

```python
for 10 games:
    # Just play, don't learn
    while not game_over:
        # Get all possible moves
        moves = get_all_moves()
        
        # Pick move with highest Q
        best_move = max(moves, key=lambda m: network(m))
        
        # Execute it
        place_piece(best_move)
```

**Network uses what it learned!**

---

## Part 7: Exploration vs Exploitation (15 min)

### The Dilemma

```
Exploitation: "Use what I know works"
  Pro: Make good moves
  Con: Miss even better moves

Exploration: "Try new things"
  Pro: Discover better strategies
  Con: Make bad moves sometimes
```

### Real Example

```
Early training (Episode 10):
  Network knows: "Placing in middle is good"
  But doesn't know: "Placing on side can give 4-line combo"
  
If only exploit: Never discover the 4-line combo!
If only explore: Make random bad moves forever!

Solution: Mix them!
```

### Epsilon-Greedy Strategy

```
epsilon = 0.9  (90% random, 10% smart)

if random() < epsilon:
    action = random_move()  # EXPLORE
else:
    action = best_move()    # EXPLOIT

As training progresses:
  Episode 100: epsilon = 0.8   (80% random, 20% smart)
  Episode 500: epsilon = 0.3   (30% random, 70% smart)
  Episode 2000: epsilon = 0.001 (99.9% smart, 0.1% random)
  
Early: Try lots of things
Later: Trust what you learned
```

---

## Part 8: Experience Replay (10 min)

### The Problem

Sequential learning is biased:

```
Game 1 sequence:
  Move 1 → Move 2 → Move 3 → Game Over
  
These moves are RELATED. If you learn from them in order,
you learn false patterns:
  "After Move 1 always comes Move 2"
  But that's just because they happened in the same game!
```

### The Solution: Store Experiences

```python
experiences = []

for 1000 games:
    for each step:
        store(state, action, reward, next_state)
    experiences.append(...)

Now experiences = [
  {state_A, reward_10, state_B},
  {state_Z, reward_5, state_Y},
  {state_M, reward_100, state_N},
  ... (1000 random experiences)
]

Then train on RANDOM batch (not sequential)
experiences_batch = random.sample(experiences, 512)
```

### Why Random Helps

```
Sequential learning (BAD):
  Train on: A → B → C → D
  Network learns false patterns

Random learning (GOOD):
  Train on: Z, M, Q, D (random order)
  Network learns true patterns (not sequence-dependent)
```

---

## Part 9: Target Network (10 min)

### The Problem

```
Training without target network:

Q_predicted = network(state)
Q_target = reward + 0.99 * network(next_state)  ← Same network!

After update:
Q_predicted = network(state) ← Changed!
Q_target = reward + 0.99 * network(next_state) ← Also changed!

Target is always moving! Like chasing a ghost! 👻
```

### The Solution: Two Networks

```python
q_network = Network()        # Main network (learns)
target_network = Network()   # Copy network (frozen)

# Training:
Q_predicted = q_network(state)
Q_target = reward + 0.99 * target_network(next_state)  ← Different network!
loss = (Q_predicted - Q_target)²
q_network.update(loss)  ← Only this updates!

# Every 100 episodes:
target_network = copy(q_network)  ← Sync them
```

### Why This Works

```
Episode 1-99:
  q_network: Learning, changing weights
  target_network: Frozen, stable targets
  ✅ Network converges toward fixed targets

Episode 100:
  ✅ Update target_network (refresh targets with new knowledge)

Episode 101-199:
  q_network: Learning again
  target_network: Frozen with better knowledge
  ✅ Network converges to even better targets
```

---

## Part 10: Putting It All Together (10 min)

### The Complete Flow

```
┌─────────────────────────────────────┐
│  TRAINING LOOP                      │
└─────────────────────────────────────┘

FOR 300 EPISODES:
  
  1. PLAY ONE GAME:
     └─ Agent uses epsilon-greedy
     └─ 50% random moves (explore)
     └─ 50% network's best moves (exploit)
     └─ Store all experiences
  
  2. SAMPLE BATCH:
     └─ Take 512 random experiences from buffer
     └─ Breaks sequential correlation
  
  3. COMPUTE TARGETS (Bellman):
     └─ For each experience:
     │    Q_target = reward + 0.99 * target_net(next_state)
     └─ This defines "correct" Q-value
  
  4. TRAIN NETWORK:
     └─ Q_predicted = q_net(state)
     └─ loss = (Q_predicted - Q_target)²
     └─ Update weights to reduce loss
  
  5. EVERY 100 EPISODES:
     └─ Update target network (copy q_net → target_net)
     └─ Epsilon decays (less random, more greedy)

RESULT: Network learns to play Tetris!

┌─────────────────────────────────────┐
│  TESTING PHASE                      │
└─────────────────────────────────────┘

FOR 50 GAMES:
  
  1. USE LEARNED NETWORK:
     └─ Get all possible moves
     └─ Evaluate each: Q = network(move)
     └─ Pick action with highest Q
     └─ Execute it
  
  2. MEASURE PERFORMANCE:
     └─ Average lines cleared
     └─ Average score
     └─ Best game
  
RESULT: See how well the AI plays!
```

---

## Part 11: The Code Mapping (15 min)

### File 1: tetris.py (The Game)

```python
class TetrisGame:
    """The Tetris environment"""
    
    def reset(self):
        """Start new game"""
        return state  # [lines, holes, bumpiness, height]
    
    def get_next_states(self):
        """All possible moves"""
        return {action: resulting_state, ...}
    
    def step(self, action):
        """Play one move"""
        return reward, done, state
    
    def _get_state_features(self):
        """Extract the 4 features"""
        return (lines, holes, bumpiness, height)
```

### File 2: network.py (The Brain)

```python
class DeepQNetwork:
    """The neural network"""
    
    # Architecture:
    # Input (4) → Hidden (64) + ReLU → Hidden (32) + ReLU → Output (1)
    
    def forward(self, state):
        """Input: state features, Output: Q-value"""
        return q_value
```

### File 3: train.py (The Learning)

```python
class DQNAgent:
    """The trainer"""
    
    def play_episode(self):
        """Play one game, store experiences"""
        for step in game:
            action = select_action(epsilon)  # Explore vs Exploit
            reward, next_state = game.step(action)
            buffer.store(state, action, reward, next_state)
    
    def train(self):
        """Learn from experiences"""
        # Sample batch
        batch = buffer.sample(512)
        
        # Bellman equation
        Q_target = reward + 0.99 * target_net(next_state)
        
        # Train network
        Q_predicted = q_net(state)
        loss = (Q_predicted - Q_target)²
        optimize(loss)
```

### File 4: test.py (The Evaluation)

```python
class DQNTester:
    """The tester"""
    
    def play_game(self):
        """Play one game, don't learn"""
        while not done:
            # Get best moves
            best_action = max(moves, 
                            key=lambda a: q_net(a))
            step(best_action)
    
    def test(self, num_games=50):
        """Measure performance"""
        for game in num_games:
            play_game()
        print(f"Average lines: {average}")
```

---

## Part 12: Key Concepts Summary

| Concept | What It Is | Why It Matters |
|---------|-----------|----------------|
| **Q-value** | Expected future reward | Tells network if position is good |
| **Bellman Equation** | Q = reward + future | Defines what network should learn |
| **Neural Network** | Function that learns | Maps board → quality score |
| **Exploration** | Try random moves | Discover new strategies |
| **Exploitation** | Use learned moves | Use what you know works |
| **Experience Replay** | Random sampling | Avoid learning false patterns |
| **Target Network** | Frozen copy | Stable targets for learning |
| **Epsilon-Greedy** | Balanced exploration | Start random, end greedy |
| **Training Phase** | Learning | Network improves |
| **Testing Phase** | Playing | Measure learned performance |

---

## Part 13: Quick Reference

### Understanding the Numbers

When you run `python train.py --num_epochs 300`:

```
Ep   10/300 | Score:  1234 | Pieces: 120 | Lines:  25 | Loss: 0.5234 | ε: 0.967
  ↑           ↑              ↑            ↑           ↑              ↑
  |           |              |            |           |              |
Episode    Points in       Blocks in   Lines cleared  How wrong   How random
number     that game       that game   in that game    network is
```

### Understand Loss

```
Loss = 0.5234  (HIGH - network is very wrong)
Loss = 0.0234  (LOW - network is pretty accurate)
Loss = 0.0001  (VERY LOW - network learned well!)

Loss should DECREASE over training ✅
```

### Understand Epsilon

```
ε = 0.967 (96.7% random, 3.3% smart) - Early training
ε = 0.500 (50% random, 50% smart) - Mid training
ε = 0.001 (99.9% smart, 0.1% random) - Late training

ε should DECREASE over training ✅
```

---

## Part 14: Let's Trace One Step

### Step-by-Step Example

```python
# CURRENT STATE
board = [lines=10, holes=2, bumpiness=3, height=12]

# POSSIBLE MOVES
moves = {
    (x=2, r=0): [lines=10, holes=2, bumpiness=4, height=13],
    (x=5, r=1): [lines=11, holes=1, bumpiness=2, height=11],  ← Good!
    (x=8, r=0): [lines=10, holes=3, bumpiness=5, height=14],
}

# EVALUATE EACH MOVE
Q_move1 = network([10, 2, 4, 13]) = 32.5
Q_move2 = network([11, 1, 2, 11]) = 78.3  ← Best!
Q_move3 = network([10, 3, 5, 14]) = 45.1

# PICK BEST
best_move = move2  (x=5, r=1)

# EXECUTE IT
new_state = [11, 1, 2, 11]
reward = 101 + custom_bonus = 110

# NEXT ITERATION
future_q = network([11, 1, 2, 11]) = ?
Q_target = 110 + 0.99 * future_q

# NETWORK LEARNS
Network's prediction for [10, 2, 3, 12] should be closer to this Q_target!
```

---

## Summary: The Big Picture

```
TETRIS GAME
    ↓
AI TRIES MOVES (explore + exploit)
    ↓
GETS REWARDS (points)
    ↓
NEURAL NETWORK LEARNS (Bellman equation)
    ↓
NETWORK IMPROVES (target network, experience replay)
    ↓
AI PLAYS BETTER
    ↓
REPEAT 300 TIMES
    ↓
AI IS EXPERT!
```

---

## Next Steps

1. **Understand tetris.py**: How the game works
2. **Understand network.py**: How the brain works
3. **Understand train.py**: How learning happens
4. **Run it**: `python train.py --num_epochs 100`
5. **Test it**: `python test.py --model_path models/tetris_final.pth`
6. **Experiment**: Try different hyperparameters

---

## Questions to Ask Yourself

- ✅ Why does network need Bellman equation?
- ✅ Why do we need exploration?
- ✅ Why do we need experience replay?
- ✅ Why do we need target network?
- ✅ What is loss?
- ✅ What is epsilon?
- ✅ How does network learn?

If you can answer all these, you understand Deep Q-Learning! 🎉

---

**Ready? Start with: `python code/tetris.py`** 🚀
