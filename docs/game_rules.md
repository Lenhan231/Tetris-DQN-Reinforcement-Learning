# 🎮 Tetris - Luật Chơi & Thông Số Kỹ Thuật

## 📋 Luật Chơi

### 1. **Lưới Chơi (Game Board)**
```
Kích thước: 10 (width) × 20 (height) ô
Hệ tọa độ: 
  - Trục X: 0-9 (trái → phải)
  - Trục Y: 0-19 (trên → dưới)
```
- ✅ **Không có 2 hàng ẩn trên cùng** (tiêu chuẩn Tetris 40-line nhưng không implement ở đây)
- Mỗi ô có 2 trạng thái: Empty (0) hoặc Filled (1-7, mã loại piece)

### 2. **Tetromino Pieces (7 loại)**
```
Mã  Tên   Hình dạng              Màu
─────────────────────────────────────
1   O     ██ (2×2 square)         Vàng
        ██

2   T     ███ (T-shape)           Tím
         █

3   S      ██ (S-shape)           Xanh lá
        ██

4   Z     ██  (Z-shape)           Đỏ
          ██

5   I     ████ (line 1×4)         Xanh dương

6   L     ███ (L-shape)           Cam
         █

7   J     ███ (J-shape)           Xanh
        █
```

#### Rotation Mechanics:
- **O-piece (1)**: Không rotate (1 hướng)
- **S, Z, I-pieces (3, 4, 5)**: 2 hướng (90° = 180°)
- **T, L, J-pieces (2, 6, 7)**: 4 hướng (0°, 90°, 180°, 270°)

### 3. **Piece Spawning**
```
Spawn location: Giữa trên cùng
  - x = width / 2 - len(piece[0]) / 2
  - y = 0

Piece bag system (7-bag):
  - Shuffle [0, 1, 2, 3, 4, 5, 6] mỗi lần
  - Pop từ dưới lên (đảm bảo không 2 piece giống liên tiếp)
```

### 4. **Gameplay Mechanics**

#### **Dropping**
```
1. Piece spawn ở y=0
2. Kiểm tra collision mỗi frame
3. Khi collision detected:
   - Piece dừng lại
   - Lock piece lên board
   - Spawn piece mới

Game Over: Nếu piece không thể spawn (board quá cao)
```

#### **Line Clearing**
```
Điều kiện: Hàng nào không chứa ô trống (full row)
Xử lý:
  1. Tìm tất cả full rows
  2. Xóa từ dưới lên (tránh index shift)
  3. Insert hàng trống ở trên

Scoring:
  - 1 line = 1 + 1²  × 10 = 11 points
  - 2 lines = 1 + 4  × 10 = 41 points  
  - 3 lines = 1 + 9  × 10 = 91 points
  - 4 lines = 1 + 16 × 10 = 161 points (Tetris!)
```

#### **Collision Detection**
```
Check 3 điều kiện:
1. Vượt biên trái/phải? (x < 0 or x >= width)
2. Chạm đáy? (y >= height)
3. Chạm khối khác? (board[y][x] != 0)

→ Nếu có 1 điều → Collision!
```

---

## 🧠 State Features (AI Input)

Agent nhận thông tin dưới dạng **4 features**:

```python
state = (lines_cleared, holes, bumpiness, total_height)
```

### 1. **Lines Cleared** 
```
Số hàng đã xóa từ đầu game
Tốt = Cao
```

### 2. **Holes** (Ô trống bị che phủ)
```
Algorithm:
  - Duyệt từ trên xuống từng cột
  - Khi gặp block → flag=True
  - Nếu sau đó gặp empty → đó là hole

Tốt = Thấp (ít holes)
```

### 3. **Bumpiness** (Độ gồ ghề bề mặt)
```
Công thức: Bumpiness = Σ|height[i] - height[i+1]|

Tốt = Thấp (bề mặt phẳng)
```

### 4. **Total Height** (Chiều cao tổng)
```
Tính chiều cao mỗi cột:
  - Duyệt từ dưới lên
  - Gặp block → height = distance từ đáy
  - Sum tất cả heights

Tốt = Thấp (không quá cao)
```

---

## 🎮 Actions (AI Output)

Agent chọn action dưới dạng tuple: `(x_position, num_rotations)`

```
x_position ∈ [0, width - piece_width]
num_rotations ∈ [0, max_rotations]

Ví dụ:
  (3, 2) → Đặt piece ở x=3, rotate 2 lần
  (0, 0) → Đặt piece ở x=0, không rotate
  (9, 1) → Đặt piece ở x=9, rotate 1 lần
```

---

## 💰 Reward Shaping

```python
reward = points + penalties + bonuses

components:
  1. points = line_clear_score (0 hoặc 11-161)
  2. penalty_height = -0.5 * (height / 20)
  3. penalty_holes = -1.0 * (holes / 50)
  4. penalty_bumpiness = -0.1 * (bumpiness / 100)
  5. game_over_penalty = -10

Tổng: reward = points - 0.5*h - 1.0*holes - 0.1*bump - 10*done
```

---

## 🔧 Phạm Vi Kỹ Thuật

### Environment
```
❌ Không dùng OpenAI Gym framework
✅ Custom implementation (headless, pure Python)
✅ Tetris 10×20 board
✅ Deterministic (no randomness in mechanics, only piece selection)
```

### AI Algorithm
```
✅ Deep Q-Network (DQN)
  - Input: 4 state features
  - Architecture: 4 → 64 → 32 → 1
  - Activation: ReLU
  - Output: 1 Q-value

✅ Epsilon-Greedy Exploration
  - ε: 1.0 → 0.001 (linear decay)
  - Replay Buffer: 30,000 samples
  - Target Network: Updated every 100 episodes
```

### Tracking & Visualization
```
✅ Weights & Biases (W&B)
  - Game metrics: score, rewards, lines, pieces
  - Model metrics: loss, epsilon
  - Updated every 100 epochs

✅ Pygame Visualization
  - Real-time rendering
  - Shows: board, current piece, stats
  - Display: score, pieces, lines, action, reward, Q-value

✅ OpenCV Alternative
  - Lightweight rendering
  - Same information as Pygame
```

---

## 📊 Game Statistics

| Metric | Untrained | After 100 epochs | After 3000 epochs |
|--------|-----------|------------------|-------------------|
| Avg Score | 50-200 | 500-2000 | 2000-5000+ |
| Avg Lines | 5-20 | 50-150 | 200+ |
| Avg Pieces | - | - | 100+ |
| Stability | Very low | Medium | Very high |

---

## ✅ Checklist vs Standard Tetris

| Feature | Standard | Implementation |
|---------|----------|-----------------|
| 10×20 board | ✅ | ✅ |
| 7 pieces | ✅ | ✅ |
| Rotation | ✅ | ✅ |
| Line clearing | ✅ | ✅ |
| Game over | ✅ | ✅ |
| **2 hidden rows** | ✅ | ❌ (Not implemented) |
| **Next piece preview** | ✅ (in some versions) | ✅ (via piece_bag) |
| **Hold piece** | ✅ (modern) | ❌ (Not implemented) |

