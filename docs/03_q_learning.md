# 3️⃣ Q-Learning - Học Từ Experience

## Q-Learning là gì?

**Q-Learning** là một thuật toán RL off-policy đơn giản và mạnh mẽ để tìm optimal policy.

**Mục tiêu**: Học Q-function Q(s,a) - giá trị của mỗi cặp (state, action)

## Q-Learning Update Rule (Công Thức Cập Nhật)

```
Q(s, a) ← Q(s, a) + α * [r + γ * max_a'(Q(s', a')) - Q(s, a)]
          └─────────────┬─────────────────────────────────────┘
                        │
                     temporal difference (TD error)
```

### Giải Thích Công Thức

```
Q_new = Q_old + learning_rate × (target - prediction)

Trong đó:
- α (alpha): learning rate (0.01, tốc độ học)
- r: immediate reward
- γ * max_a'(Q(s', a')): estimated future reward
- Q(s, a): current Q-value

Target = r + γ * max_a'(Q(s', a'))
         = immediate reward + discounted future value

Error = Target - Q(s, a)
      = Sai số hiện tại của ước lượng
```

## Vị Dụ Minh Họa: Học Đơn Giản

```
Giả sử:
State s = "bàn chơi hiện tại"
Action a = "xoay + di chuyển"
Reward r = 41 (xóa được 2 hàng)

Q(s, a) cũ = 50

New state s' → có 3 hành động có thể:
- Q(s', a1) = 60
- Q(s', a2) = 55
- Q(s', a3) = 45

max_a'(Q(s', a')) = max(60, 55, 45) = 60

Cập nhật:
Target = r + γ * max_a'(Q(s', a'))
       = 41 + 0.99 * 60
       = 41 + 59.4
       = 100.4

Q_new = Q_old + α * (Target - Q_old)
      = 50 + 0.01 * (100.4 - 50)
      = 50 + 0.01 * 50.4
      = 50 + 0.504
      = 50.504

✓ Q-value tăng từ 50 → 50.504 (tốt hơn)
```

## Khi Nào Cần Cập Nhật?

```
Mỗi khi agent:
1. Ở state s
2. Thực hiện action a
3. Nhận reward r
4. Chuyển sang state s'
5. → Cập nhật Q(s, a)
```

## Replay Memory (Bộ Nhớ Trải Nghiệm)

Vấn đề: Data từ game experience có **correlation** cao (các state liên tiếp giống nhau)

Giải pháp: **Experience Replay**
```python
replay_memory = deque(maxlen=30000)

# Lưu experience
replay_memory.append((state, action, reward, next_state, done))

# Cập nhật từ batch random (break correlation)
batch = random.sample(replay_memory, batch_size=512)
for state, action, reward, next_state, done in batch:
    Q[state, action] ← update_rule(...)
```

**Lợi ích**:
- Tăng data efficiency
- Giảm correlation trong training data
- Cho phép reuse experience

## Training Loop Với Q-Learning

```python
# Khởi tạo
Q = init_q_table()  # hoặc neural network
replay_memory = empty deque

# Training
for episode in range(num_episodes):
    state = env.reset()
    done = False
    
    while not done:
        # 1. Chọn action (ε-greedy)
        if random() < epsilon:
            action = random_action()
        else:
            action = argmax(Q(state, :))
        
        # 2. Thực hiện action
        reward, next_state, done = env.step(action)
        
        # 3. Lưu experience
        replay_memory.append((state, action, reward, next_state, done))
        
        # 4. Update Q từ batch (nếu replay_memory đủ lớn)
        if len(replay_memory) > min_memory:
            batch = random.sample(replay_memory, batch_size)
            for s, a, r, s', d in batch:
                target = r if d else r + γ * max(Q(s', :))
                Q(s, a) ← Q(s, a) + α * (target - Q(s, a))
        
        state = next_state
        epsilon = decay_epsilon(epsilon)  # Giảm exploration
```

## Convergence (Hội Tụ)

Q-Learning được chứng minh là **hội tụ** đến optimal Q* nếu:

```
1. Tất cả (state, action) được visit vô hạn lần
2. Learning rate α:
   - Σ α(n) = ∞ (tổng vô hạn)
   - Σ α(n)² < ∞ (tổng bình phương hữu hạn)
   
   Ví dụ: α(n) = 1/n, α(n) = 0.01 đều thỏa
```

**Thực Tế**:
```
α = 0.01 (fixed) hoạt động tốt với neural networks
```

## Bellman Equation (Phương Trình Bellman)

```
Q(s, a) = E[r + γ * max_a'(Q(s', a')) | s, a]

Giải thích:
Q-value của (s,a) = 
  immediate reward + 
  discounted expected future Q-value
```

## Vấn Đề & Giải Pháp

### Vấn Đề 1: Overestimation
```
Problem: max_a'(Q(s', a')) có thể overestimate thực tế
Solution: Double Q-Learning (dùng 2 networks, trong Deep Q-Learning)
```

### Vấn Đề 2: Thay Đổi Target Quá Nhanh
```
Problem: Q(s', a') thay đổi mỗi bước → training không ổn định
Solution: Target Network (cập nhật chậm, trong Deep Q-Learning)
```

### Vấn Đề 3: State Space Quá Lớn
```
Problem: Không thể lưu Q-table cho tất cả states
         (Tetris: 10^100+ states có thể)
Solution: Function Approximation (Neural Network)
         → Deep Q-Learning
```

## Q-Learning vs Sarsa

| Aspect | Q-Learning | SARSA |
|--------|-----------|-------|
| **Type** | Off-policy | On-policy |
| **Update** | Dùng best Q | Dùng Q(s', a') thực tế |
| **Formula** | r + γ*max(Q) | r + γ*Q(s', a') |
| **Learning** | Từ optimal actions | Từ current policy |
| **Stability** | Rủi ro overestimate | Ổn định hơn |

## Recap

| Khái Niệm | Ý Nghĩa |
|-----------|---------|
| **Q(s,a)** | Giá trị kỳ vọng của action a tại state s |
| **TD Error** | r + γ*max(Q') - Q: sai số ước lượng |
| **α** | Learning rate: mức độ cập nhật |
| **γ** | Discount factor: ưu tiên future rewards |
| **Replay** | Lưu trữ & random sampling experiences |
| **ε-Greedy** | Cân bằng exploration & exploitation |

---

**Tiếp theo**: [04_deep_q_learning.md](./04_deep_q_learning.md)
