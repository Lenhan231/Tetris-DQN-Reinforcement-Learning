# 📚 Hướng Dẫn Code - Tetris DQN (Đơn Giản Hóa)

## 🎯 Quick Start

### 1️⃣ Hiểu Game (5 phút)
```bash
python code/step1_tetris_basic.py
```
→ Xem demo: AI chơi Tetris ngẫu nhiên

### 2️⃣ Hiểu Features (5 phút)
```bash
python code/step2_state_features.py
```
→ Xem 4 features được trích xuất từ board

### 3️⃣ Hiểu Neural Network (5 phút)
```bash
python code/step3_neural_network.py
```
→ Xem network architecture, forward pass, training step

### 4️⃣ Train Model (30-60 phút)
```bash
python code/step4_train_dqn.py --num_epochs 100
```
→ Huấn luyện AI học chơi Tetris

### 5️⃣ Test Model (1 phút)
```bash
python code/step5_test_model.py --model_path models/tetris_final.pth
```
→ Xem AI chơi, tính statistics

### 6️⃣ Visualize (Interactive)
```bash
python code/visualize_gameplay.py --model_path models/tetris_final.pth --speed 2
```
→ Xem AI chơi real-time với pygame

---

## 📖 Chi Tiết Mỗi File

### step1_tetris_basic.py (Game Engine)

**Chứa gì:**
- `TetrisGame` class: Game logic
  - `__init__()` - Khởi tạo board 20×10
  - `reset()` - Reset game
  - `step(action)` - Thực hiện 1 bước
  - `get_next_states()` - Tất cả possible next states
  - `print_board()` - In board debug

**Key Methods:**
```python
game = TetrisGame()
game.reset()

# Chọn vị trí & rotate
action = (x_pos, num_rotations)
reward, done, state = game.step(action)

# Get tất cả possible states
next_states = game.get_next_states()
```

**Features trả về:**
```python
state = (lines_cleared, holes, bumpiness, height)
```

---

### step2_state_features.py (Feature Extraction)

**Chứa gì:**
- `FeatureExtractor` class: Trích xuất features
  - `extract()` - Tính 4 features
  - `_count_holes()` - Đếm holes
  - `_get_bumpiness_and_height()` - Tính bumpiness & height

**4 Features:**
1. **lines_cleared** - Hàng đã xóa (tốt)
2. **holes** - Ô trống bị che (xấu)
3. **bumpiness** - Độ gồ ghề (xấu)
4. **height** - Tổng chiều cao (xấu)

**Demo:**
```python
extractor = FeatureExtractor()
features = extractor.extract(board)
# Output: (lines, holes, bumpiness, height)
```

---

### step3_neural_network.py (DQN Model)

**Chứa gì:**
- `DeepQNetwork` class: Neural network
  - Architecture: `4 → 64 → 64 → 1`
  - `forward(x)` - Forward pass
  - `_init_weights()` - Xavier initialization
  - `count_params()` - Đếm parameters

**Usage:**
```python
model = DeepQNetwork()
model = model.to(device)

# Single sample
state = torch.FloatTensor([10, 5, 20, 15])  # shape: (4,)
q = model(state)  # shape: (1,)

# Batch
batch = torch.FloatTensor([...])  # shape: (batch_size, 4)
qs = model(batch)  # shape: (batch_size, 1)
```

**Output:**
- Q-value: dự đoán điểm kỳ vọng từ state này
- Cao → state tốt, Thấp → state xấu

---

### step4_train_dqn.py (Training)

**Chứa gì:**
- `DQNAgent` class: Agent training
  - `select_action()` - ε-greedy selection
  - `train_step()` - 1 bước training
  - `play_episode()` - Chơi 1 game
  - `train()` - Main training loop

**Training Loop:**
1. Play episode: collect experiences
2. Store in replay buffer
3. Sample random batch
4. Forward: predict Q
5. Compute target: reward + γ*Q(next)
6. Loss: (target - prediction)²
7. Backward: update weights
8. Repeat

**Hyperparameters:**
- `--num_epochs 100` - Episodes
- `--batch_size 512` - Batch size
- `--lr 0.001` - Learning rate
- `--gamma 0.99` - Discount factor
- `--initial_eps 1.0` → `--final_eps 0.001` - Epsilon decay

**Output:**
- Saves model every 100 episodes
- Final model: `models/tetris_final.pth`

---

### step5_test_model.py (Testing & Evaluation)

**Chứa gì:**
- `DQNTester` class: Load & test model
  - `select_best_action()` - Greedy action
  - `play_game()` - Chơi 1 game
  - `test_games()` - Chơi nhiều games
  - `print_stats()` - In statistics

**Usage:**
```bash
# Test 10 games
python step5_test_model.py --model_path models/tetris_final.pth --num_games 10

# With visualization
python step5_test_model.py --model_path models/tetris_final.pth --visualize
```

**Output:**
- Average score, pieces, lines cleared
- Min/max scores

---

### visualize_gameplay.py (Pygame Visualization)

**Chứa gì:**
- `TetrisVisualizer` class: Pygame visualization
  - `select_action()` - Choose best action
  - `draw_board()` - Vẽ board
  - `draw_stats()` - Vẽ statistics
  - `play()` - Main loop

**Controls:**
- `SPACE` - Pause/Resume
- `ESC` - Quit

**Speed:**
- `--speed 1` - Chậm
- `--speed 5` - Bình thường
- `--speed 10` - Nhanh

---

## 🔄 Data Flow

```
step1: Game engine
       ↓
       Generates: (state, action, reward, next_state)
       ↓
step2: Feature extraction
       ↓
       Converts: board → (lines, holes, bumpiness, height)
       ↓
step3: Neural network
       ↓
       Predicts: features → Q-value
       ↓
step4: Training
       ↓
       Updates weights: loss = (target - prediction)²
       ↓
step5: Testing
       ↓
       Evaluates: average score, statistics
       ↓
visualize: Pygame
       ↓
       Shows: real-time gameplay
```

---

## 🧮 Mathematical Concepts

### Bellman Equation
```
Q(state) = reward + γ × max(Q(next_state))

γ (gamma) = 0.99
- Điều cân bằng immediate vs future rewards
- 0.99 = ưu tiên future rewards
```

### Loss Function
```
loss = (target_Q - predicted_Q)²

Where:
target_Q = reward + γ × max(Q(next_state))
predicted_Q = neural_network(state)
```

### Epsilon-Greedy
```
if random() < ε:
    action = random_action()  # Explore
else:
    action = best_action()    # Exploit

ε decays: 1.0 → 0.001 over epochs
```

---

## 💡 Key Insights

1. **Why Features?**
   - Board: 20×10 = 200 values (too large)
   - Features: 4 values (semantic meaning)
   - Faster training, better generalization

2. **Why Replay Buffer?**
   - Sequential experiences are correlated
   - Random sampling breaks correlations
   - Improves training stability

3. **Why Target Network?**
   - Prevents divergence
   - Decouples target from prediction
   - More stable training

4. **Why Epsilon-Greedy?**
   - Explore early: try different actions
   - Exploit later: use best learned actions
   - Balance between learning & performance

---

## 🎯 Learning Goals Per File

| File | Learn | Practice |
|------|-------|----------|
| step1 | Game mechanics | Run demo |
| step2 | State representation | Run demo |
| step3 | Neural networks | Run demo |
| step4 | Training loop | Train model |
| step5 | Evaluation | Test model |
| visualize | Visualization | Watch gameplay |

---

## ⚡ Quick Tips

**Training too slow?**
- Reduce `--num_epochs` first time (--num_epochs 50)
- Increase later (--num_epochs 500) for better results

**Model not improving?**
- Increase training time
- Adjust learning rate (try 0.0005 or 0.002)
- Increase batch size

**GPU not detected?**
- CPU is fine for this project (Tetris is small)
- Training still completes in reasonable time

**Out of memory?**
- Reduce `--batch_size` (512 → 256)
- Reduce `--replay_memory_size` (30000 → 15000)

---

## 📝 Code Simplifications

Changes from original:
1. **Removed unnecessary comments** - Code speaks for itself
2. **Renamed variables** - `piece_pos` → `piece_x/piece_y`
3. **Simplified functions** - Removed duplicates
4. **Better organization** - Logical method ordering
5. **Added docstrings** - Explain only the WHY
6. **Vietnamese comments** - Easy to understand

Total lines: Reduced from ~1200 to ~900 (25% smaller!)

---

## 🚀 Next Steps

1. ✅ Understand each step
2. ✅ Run all demos
3. ✅ Train model (be patient!)
4. ✅ Test model
5. ✅ Visualize real-time

Then:
- Modify hyperparameters
- Try different architectures
- Add features (e.g., next_piece info)
- Implement improvements

---

**Happy Learning!** 🎓
