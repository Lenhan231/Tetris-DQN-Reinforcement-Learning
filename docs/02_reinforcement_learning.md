# 2️⃣ Reinforcement Learning - Tìm Hiểu ML Từ Tương Tác

## Định Nghĩa

**Reinforcement Learning (RL)** là một phương pháp machine learning nơi agent học cách hành động bằng cách:
1. Tương tác với môi trường
2. Nhận rewards/penalties
3. Điều chỉnh chiến lược hành động

## MDP - Markov Decision Process

RL được mô hình hóa dưới dạng MDP với 5 thành phần:

```
(S, A, P, R, γ)

S : State space       - Tập hợp tất cả các trạng thái
A : Action space     - Tập hợp tất cả các hành động
P : Transition prob  - Xác suất chuyển từ state s sang s'
R : Reward function  - Phần thưởng cho action a ở state s
γ : Discount factor  - Tầm quan trọng của rewards tương lai (0.99)
```

## Các Thành Phần Chính

### 1. **State (Trạng Thái)**
Mô tả tình huống hiện tại của hệ thống

**Ví dụ Tetris:**
```
state = {
    'lines_cleared': 10,   # Số hàng đã xóa
    'holes': 5,            # Số ô trống bị che phủ
    'bumpiness': 15,       # Độ gồ ghề bề mặt
    'height': 12           # Chiều cao trung bình
}
```

### 2. **Action (Hành Động)**
Thứ agent làm để ảnh hưởng đến environment

**Ví dụ Tetris:**
```
action = (x_position, num_rotations)
- x_position: 0-10 (vị trí ngang)
- num_rotations: 0-3 (số lần xoay)
```

### 3. **Reward (Phần Thưởng)**
Phản hồi từ environment về hành động

**Ví dụ Tetris:**
```
reward = {
    'clear 1 line': 1 + (1²) × 10 = 11
    'clear 2 lines': 1 + (4) × 10 = 41
    'clear 3 lines': 1 + (9) × 10 = 91
    'clear 4 lines': 1 + (16) × 10 = 161
    'game over': -2
}
```

### 4. **Transition**
Từ (state, action) → new state

**Tetris:**
```
(board_state, action=(5, 1))
    ↓ [agent thực hiện action]
    ↓ [piece rơi xuống]
    ↓ [kiểm tra lines cleared]
    ↓
(new_board_state, reward)
```

## Policy (Chiến Lược)

**Policy** π là hàm quyết định action dựa trên state:

```
π(a|s) = xác suất chọn action a khi ở state s

Có 2 loại:
1. Deterministic: π(s) = a (một action cố định)
2. Stochastic: π(a|s) = P(a|s) (xác suất)
```

**Mục tiêu RL**: Tìm policy tối ưu π* để maximize expected reward

## Value Function & Q-Function

### Value Function: V(s)
Expected cumulative reward khi bắt đầu từ state s

```
V(s) = E[R_t + γ*R_{t+1} + γ²*R_{t+2} + ...]
       = Giá trị dự kiến của state s

Ý nghĩa: Nếu ở state này, tôi sẽ kiếm được bao nhiêu điểm về sau?
```

### Q-Function: Q(s, a)
Expected reward khi thực hiện action a ở state s

```
Q(s, a) = E[R_t + γ*V(S_{t+1}) | S_t=s, A_t=a]
        = Giá trị của cặp (state, action)

Ý nghĩa: Nếu ở state này và làm action này, 
         tôi sẽ kiếm được bao nhiêu điểm về sau?
```

## Vòng Lặp RL Cơ Bản

```
┌─────────────────────────┐
│  Khởi tạo: s₀           │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│  Nhận state s            │
│  (ví dụ: bàn chơi)      │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│  Chọn action a          │
│  (dùng policy π)        │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│  Thực hiện action       │
│  Nhận reward r          │
│  & new state s'         │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│  Cập nhật policy        │
│  (dùng r + V(s'))       │
└────────────┬────────────┘
             │
             ├─→ Game Over? Kết thúc
             │
             └─→ s = s', lặp lại
```

## On-Policy vs Off-Policy

### On-Policy: Học từ policy hiện tại
```
Ví dụ: SARSA
- Thực hiện action theo policy hiện tại
- Cập nhật dựa trên policy đó
- Chậm nhưng ổn định
```

### Off-Policy: Học từ policy khác
```
Ví dụ: Q-Learning
- Thực hiện action ngẫu nhiên hoặc exploratory
- Cập nhật dựa trên best Q-value
- Nhanh nhưng cần cân bằng exploration/exploitation
```

## Exploration vs Exploitation

**Dilemma**: Nên làm gì khi chọn action?

```
1. Exploitation: Chọn best action (tối đa Q-value)
   → Dùng kiến thức đã học
   → Rủi ro: Bỏ qua hành động tốt hơn

2. Exploration: Chọn ngẫu nhiên hoặc random
   → Khám phá các hành động mới
   → Rủi ro: Hành động tồi có thể nhân lên losses

Giải pháp: ε-Greedy
- Với xác suất ε: chọn random (explore)
- Với xác suất 1-ε: chọn best Q (exploit)
- ε giảm dần qua thời gian
```

**Ví dụ ε-Greedy:**
```python
epsilon = 0.5  # Đầu training: 50% explore, 50% exploit

if random() < epsilon:
    action = random_action()  # Explore
else:
    action = argmax(Q[state])  # Exploit
```

## Return & Discount Factor

```
R_t = r_t + γ*r_{t+1} + γ²*r_{t+2} + ...

Ý nghĩa:
- r_t: reward ngay lập tức
- γ*r_{t+1}: reward 1 bước sau (yếu hơn)
- γ²*r_{t+2}: reward 2 bước sau (còn yếu hơn)
- ...

γ = 0.99: Ưu tiên rewards gần, có xem xét rewards xa
```

## Recap

| Khái Niệm | Ý Nghĩa |
|-----------|---------|
| **State** | Tình huống hiện tại |
| **Action** | Quyết định của agent |
| **Reward** | Phản hồi từ environment |
| **Policy** | Chiến lược chọn action |
| **Value** | Giá trị kỳ vọng của state |
| **Q-value** | Giá trị kỳ vọng của (state, action) |
| **Gamma** | Tầm quan trọng của future rewards |

---

**Tiếp theo**: [03_q_learning.md](./03_q_learning.md)
