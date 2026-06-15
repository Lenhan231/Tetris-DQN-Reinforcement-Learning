# 4️⃣ Deep Q-Learning (DQN) - Neural Network Q-Learning

## Tại Sao Cần Deep Q-Learning?

### Vấn Đề Với Tabular Q-Learning

```
Q-Learning cơ bản dùng Q-table:

Q = {
    (state1, action1): 50.5,
    (state1, action2): 45.2,
    (state2, action1): 60.1,
    ...
}

Vấn Đề:
1. State space quá lớn
   - Tetris: ~10^100+ possible states
   - Không thể lưu hết
   - Không thể visit hết

2. Không generalize
   - Mỗi state chỉ học 1 value
   - State mới không tận dụng kiến thức cũ
```

### Giải Pháp: Function Approximation

```
Thay vì Q-table:
Q(s, a) = table[s, a]

Dùng Neural Network:
Q(s, a) = network(s)[a]

network là một hàm phi tuyến học được
Có thể:
- Tổng quát hóa cho states tương tự
- Xử lý state space lớn vô hạn
- Reuse kiến thức giữa các states
```

## Deep Q-Network (DQN) Architecture

### Input & Output

```
Input:  State features (4 giá trị: lines_cleared, holes, bumpiness, height)
        ↓
        [Linear: 4 → 64 + ReLU]
        ↓
        [Linear: 64 → 64 + ReLU]
        ↓
        [Linear: 64 → 1]
        ↓
Output: Q-value (tương lai score kỳ vọng)
```

### Code

```python
import torch.nn as nn

class DeepQNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        
        # Feature extraction layers
        self.fc1 = nn.Linear(4, 64)    # Input: 4 features
        self.relu1 = nn.ReLU()
        
        self.fc2 = nn.Linear(64, 64)   # Hidden layer
        self.relu2 = nn.ReLU()
        
        self.fc3 = nn.Linear(64, 1)    # Output: Q-value
    
    def forward(self, x):
        # x shape: (batch_size, 4)
        x = self.relu1(self.fc1(x))
        x = self.relu2(self.fc2(x))
        q_value = self.fc3(x)          # shape: (batch_size, 1)
        return q_value
```

### Tại Sao Cấu Trúc Này?

```
Input layer: 4 features
- lines_cleared: số hàng đã xóa
- holes: số ô trống bị che
- bumpiness: độ gồ ghề
- height: chiều cao

Hidden layer: 64 neurons
- Tìm patterns phức tạp từ 4 input
- ReLU activation: phi tuyến hóa

Output layer: 1 value
- Dự đoán Q-value cho state này
```

## DQN Training Process

### Loss Function

```
Traditional Q-Learning:
Q(s, a) ← Q(s, a) + α[r + γ*max(Q(s')) - Q(s, a)]

DQN:
MSE Loss = (Target - Q_predicted)²

Trong đó:
Target = r + γ * max(Q_network(s'))
Q_predicted = Q_network(s)

Backpropagation điều chỉnh weights để minimize loss
```

### Update Rule

```python
# Forward pass
q_value = model(state)

# Compute target
with torch.no_grad():
    next_q_values = model(next_state)
    target = reward + gamma * torch.max(next_q_values)

# Compute loss
loss = criterion(q_value, target)

# Backward pass
optimizer.zero_grad()
loss.backward()
optimizer.step()
```

## Target Network (Cải Tiến Quan Trọng)

### Vấn Đề: Moving Target

```
Khi train DQN:
- Target = r + γ * max(Q_network(s'))  ← dùng same network

Problem:
- Sau một vài steps, Q_network đã thay đổi
- Target cũng thay đổi
- Như là "bắn vào mục tiêu đang chuyển động"
- Dẫn đến: training instability, divergence
```

### Giải Pháp: Target Network

```
Dùng 2 networks:
1. Q-network: cập nhật mỗi step
2. Target-network: copy từ Q-network mỗi N steps

Training:
q_value = Q_network(state)
target = r + γ * max(Target_network(next_state))
loss = (target - q_value)²
```

**Code:**
```python
# Mỗi C steps
if step % C == 0:
    target_network.load_state_dict(q_network.state_dict())

# Training
q_value = q_network(state)
with torch.no_grad():
    next_q_value = target_network(next_state)
    target = reward + gamma * next_q_value
loss = mse_loss(q_value, target)
```

## Experience Replay (Cải Tiến Quan Trọng)

### Vấn Đề: Correlated Data

```
Agent trong game:
state₀ → action₀ → state₁ → action₁ → state₂ → action₂ → ...

Dữ liệu liên tiếp rất correlated:
- state₀ và state₁ gần giống nhau
- Nếu train tuần tự, bias trong training

Tương tự: nếu chỉ train từ recent batches
- Bỏ qua past experiences
- Overfitting trên recent patterns
```

### Giải Pháp: Replay Buffer

```python
from collections import deque
import random

replay_buffer = deque(maxlen=30000)  # Lưu 30k experiences

# Mỗi step
replay_buffer.append((state, action, reward, next_state, done))

# Train từ random batch
batch = random.sample(replay_buffer, batch_size=512)
for state, action, reward, next_state, done in batch:
    # Update Q-network
    ...
```

**Lợi Ích:**
1. Break correlation → diversify training data
2. Reuse experiences → data efficiency
3. Stable convergence

## Complete DQN Training Loop

```python
# Initialize
q_network = DeepQNetwork()
target_network = DeepQNetwork()
target_network.load_state_dict(q_network.state_dict())
replay_buffer = deque(maxlen=30000)
optimizer = torch.optim.Adam(q_network.parameters(), lr=0.001)
criterion = nn.MSELoss()

# Training
for episode in range(num_episodes):
    state = env.reset()
    done = False
    
    while not done:
        # ε-Greedy action selection
        epsilon = final_epsilon + max(0, decay_epochs - episode) * 
                  (initial_epsilon - final_epsilon) / decay_epochs
        
        if random() < epsilon:
            action = random_action()  # Explore
        else:
            next_states = env.get_next_states()
            with torch.no_grad():
                q_values = q_network(next_states)
            action = next_states[argmax(q_values)]  # Exploit
        
        # Execute action
        reward, done = env.step(action)
        next_state = env.get_state()
        
        # Store experience
        replay_buffer.append((state, reward, next_state, done))
        
        # Update Q-network if buffer is large enough
        if len(replay_buffer) > 3000:
            batch = random.sample(replay_buffer, batch_size=512)
            
            states, rewards, next_states, dones = zip(*batch)
            states = torch.stack(states)
            next_states = torch.stack(next_states)
            
            q_values = q_network(states)
            
            with torch.no_grad():
                next_q_values = target_network(next_states)
            
            targets = torch.where(
                torch.tensor(dones),
                torch.tensor(rewards),
                torch.tensor(rewards) + gamma * next_q_values
            )
            
            loss = criterion(q_values, targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        
        state = next_state
    
    # Update target network periodically
    if episode % 100 == 0:
        target_network.load_state_dict(q_network.state_dict())
```

## DQN Improvements (Double DQN, Dueling, etc.)

Các cải tiến DQN ban đầu:

### 1. Double DQN
```
Problem: max(Q') overestimates Q-values
Solution: 
  target = r + γ * Q_target(s', argmax_a Q_current(s', a))
```

### 2. Dueling DQN
```
Split network output into:
- Value stream V(s): state value
- Advantage stream A(s,a): advantage of action
Q(s,a) = V(s) + (A(s,a) - mean(A(s,:)))
```

### 3. Prioritized Experience Replay
```
Không sample uniformly
Sample experiences với probability ∝ |TD-error|
→ Học nhanh hơn từ surprising transitions
```

## Recap DQN

| Thành Phần | Mục Đích |
|-----------|---------|
| **Neural Network** | Approximate Q(s,a) function |
| **Target Network** | Stable training targets |
| **Replay Buffer** | Break correlation, data efficiency |
| **ε-Greedy** | Balance exploration/exploitation |
| **Loss Function** | MSE(target - prediction) |

## Flowchart Đầy Đủ DQN

```
    Initialize Q-network & Target-network
            ↓
    For episode = 1 to num_episodes:
        state ← env.reset()
        
        While NOT done:
            ├─ Get next possible states
            ├─ ε-Greedy: choose action
            ├─ Execute action → reward, next_state
            ├─ Store (state, reward, next_state) to buffer
            │
            ├─ If buffer is large:
            │   ├─ Sample batch from buffer
            │   ├─ Forward Q-network(batch)
            │   ├─ Forward Target-network(batch) (no_grad)
            │   ├─ Compute MSE loss
            │   ├─ Backprop & update Q-network
            │
            ├─ state ← next_state
            └─
        
        If episode % update_interval == 0:
            Update Target-network ← Q-network
```

---

**Tiếp theo**: Thực hành code với [Step-by-Step Implementation](../code/)
