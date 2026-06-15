# 📚 Hướng Dẫn Học Tập - Tetris Deep Q-Learning

## Hiểu Rõ Ý Tưởng

Tôi đã tạo một **framework học tập chi tiết** chứ không phải chỉ là code. Mỗi file được thiết kế để bạn:
1. **Đọc & Hiểu** lý thuyết trước
2. **Chạy & Quan sát** code demo
3. **Sửa & Thử nghiệm** bằng cách thay đổi values
4. **Viết lại** code của bạn khi hiểu rõ

## Cấu Trúc Học Tập (Tuần Tự)

### 📖 Giai Đoạn 1: Lý Thuyết Nền Tảng (Đọc)

Hãy **đọc lần lượt** các file documentation:

1. **[docs/01_tetris_game.md](docs/01_tetris_game.md)** - 10 phút
   - Hiểu luật chơi Tetris
   - Board, pieces, actions, rewards

2. **[docs/02_reinforcement_learning.md](docs/02_reinforcement_learning.md)** - 15 phút
   - Khái niệm agent, environment, state, action, reward
   - Policy & Value function
   - Exploration vs Exploitation

3. **[docs/03_q_learning.md](docs/03_q_learning.md)** - 15 phút
   - Q-Learning algorithm
   - Bellman equation
   - Experience replay
   - ε-Greedy strategy

4. **[docs/04_deep_q_learning.md](docs/04_deep_q_learning.md)** - 15 phút
   - Tại sao cần deep learning
   - DQN architecture
   - Target network & Experience replay
   - Training process

**Tổng cộng: ~1 giờ lý thuyết** 🎓

---

### 💻 Giai Đoạn 2: Thực Hành Code (Chạy & Học)

Sau khi hiểu lý thuyết, **chạy & học từng step**:

#### Step 1: Game Engine (30 phút)
```bash
cd code/
python step1_tetris_basic.py
```

📌 **Học được:**
- Cách xây dựng game Tetris
- Board representation
- Collision detection
- Feature extraction

🔧 **Bài tập:**
1. Chạy code mặc định
2. Sửa `pieces` để thêm một loại tetromino mới
3. Thay đổi board size sang 12×25 và test
4. Thêm more features (ví dụ: rows_with_one_hole)

---

#### Step 2: Features (20 phút)
```bash
python step2_state_features.py
```

📌 **Học được:**
- Cách tính features từ board
- Ý nghĩa của mỗi feature
- Tại sao features tốt hơn raw board

🔧 **Bài tập:**
1. Visualize các board states khác nhau
2. Tính features cho từng board
3. So sánh features của "good" vs "bad" states
4. Viết lại `_count_holes()` để hiểu logic

---

#### Step 3: Neural Network (20 phút)
```bash
python step3_neural_network.py
```

📌 **Học được:**
- DQN architecture (input → hidden → output)
- Forward pass
- Weight initialization
- Training a simple example

🔧 **Bài tập:**
1. Chạy code & quan sát Q-values
2. Sửa architecture: thay (4 → 64 → 64 → 1) thành (4 → 128 → 1)
3. Test với different batch sizes
4. Visualize weight distributions

---

#### Step 4: Training (2-4 giờ)
```bash
# Chạy với ít episodes để test
python step4_train_dqn.py --num_epochs 50

# Hoặc chạy đầy đủ (mất thời gian nhưng hiệu quả hơn)
python step4_train_dqn.py --num_epochs 1000
```

📌 **Học được:**
- Vòng lặp training hoàn chỉnh
- Experience replay
- ε-Greedy exploration
- Target network updates

🔧 **Bài tập:**
1. Chạy training và quan sát metrics
2. Thay đổi `lr` từ 0.001 → 0.01, quan sát sự khác biệt
3. Giảm `batch_size` từ 512 → 128, có nhanh hơn không?
4. Thay đổi `gamma` từ 0.99 → 0.95, impact như thế nào?

---

#### Step 5: Testing (10 phút)
```bash
# Test model bạn vừa train
python step5_test_model.py --model_path models/tetris_final.pth --num_games 10 --visualize
```

📌 **Học được:**
- Cách evaluate trained model
- Visualize gameplay
- Calculate metrics

🔧 **Bài tập:**
1. Test models từ different training epochs
2. Compare scores: model sau 50 epochs vs 1000 epochs
3. Visualize best & worst games
4. Analyze why model makes certain actions

---

## 🎯 Cách Học Hiệu Quả

### ❌ KHÔNG NÊN:
- Copy-paste code mà không hiểu
- Chạy code một lần xong
- Chỉ đọc lý thuyết không thực hành

### ✅ NÊN:
- **Đọc từng dòng code** & hiểu nó làm gì
- **Sửa code** & chạy lại để thấy kết quả
- **Viết documentation** cho code của riêng bạn
- **So sánh** kết quả khi thay đổi parameters
- **Vẽ diagrams** để hiểu flow
- **Hỏi "Tại sao?"** cho mỗi decisions

## 📋 Checklist Học Tập

### Phần 1: Lý Thuyết
- [ ] Hiểu Tetris game mechanics
- [ ] Hiểu Markov Decision Process
- [ ] Hiểu Q-Learning algorithm
- [ ] Hiểu Deep Q-Learning & DQN
- [ ] Có thể giải thích bằng lời

### Phần 2: Step-by-Step Code
- [ ] Chạy & hiểu Step 1 (Game Engine)
- [ ] Sửa code Step 1 & test
- [ ] Chạy & hiểu Step 2 (Features)
- [ ] Tính features cho custom board
- [ ] Chạy & hiểu Step 3 (Neural Network)
- [ ] Thay đổi architecture & test
- [ ] Chạy Step 4 training (patience! ⏳)
- [ ] Chạy Step 5 testing & visualize

### Phần 3: Thực Hành Nâng Cao
- [ ] Viết code từ scratch (không copy)
- [ ] Implement một feature khác
- [ ] Train model với different hyperparameters
- [ ] Visualize training progress (loss, score, etc)
- [ ] Compare different architectures

## 🤔 Nếu Bạn Stuck

### Không hiểu lý thuyết?
→ Đọc lại file markdown, vẽ diagram, hỏi từng khái niệm

### Code error?
→ Đọc error message kỹ, thêm print statements, debug step-by-step

### Training quá chậm?
→ Giảm num_epochs, giảm batch_size, dùng GPU (nếu có)

### Model không learn?
→ Check: learning_rate, gamma, epsilon decay, reward scaling

## 💡 Gợi Ý Mở Rộng

Sau khi hoàn thành base, bạn có thể:

1. **Implement Double DQN** - Giảm overestimation
2. **Add Dueling Network** - Separate value & advantage streams
3. **Prioritized Experience Replay** - Sample high-importance experiences
4. **Implement Tetris AI Evaluation** - So sánh với baselines
5. **Visualize Training Progress** - TensorBoard integration
6. **Test Different Architectures** - Convolutional nets, recurrent nets

## 📞 Tài Liệu Tham Khảo

Nếu bạn muốn đọc thêm:

- **Sutton & Barto** - Reinforcement Learning: An Introduction
- **DeepMind DQN Paper** - https://www.nature.com/articles/nature14236
- **PyTorch Tutorials** - https://pytorch.org/tutorials/
- **OpenAI Gym** - Environment library

## 🚀 Tiến Độ Học Tập

```
Tuần 1:
├─ Đọc lý thuyết (1-2 giờ)
├─ Step 1: Game (1 giờ)
└─ Step 2: Features (1 giờ)

Tuần 2:
├─ Step 3: Network (1 giờ)
├─ Step 4: Training (4-6 giờ)
└─ Step 5: Testing (1 giờ)

Tuần 3+:
├─ Sửa & thay đổi hyperparameters
├─ Experiment với architectures
└─ Implement extensions
```

---

## 🎓 Mục Tiêu Cuối Cùng

Sau khi hoàn thành:

✅ **Hiểu:**
- Cách RL & Q-Learning hoạt động
- Tại sao cần Deep Q-Learning
- Cách train DQN từ đầu

✅ **Có thể:**
- Viết DQN từ scratch
- Train trên game khác
- Debug & optimize hyperparameters
- Giải thích code cho người khác

✅ **Thành công khi:**
- Model của bạn chơi Tetris better than random
- Hiểu từng dòng code
- Có thể modify & experiment

---

**Happy Learning! 🎮🤖**

Nhớ rằng: Learning by doing! Đừng chỉ đọc, hãy chạy code, thay đổi nó, quan sát kết quả!
