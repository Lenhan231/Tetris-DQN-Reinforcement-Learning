# 🎮 Tetris Deep Q-Learning: Từ Không Đến Có

Dự án này hướng dẫn bạn xây dựng một AI chơi Tetris bằng Deep Q-Learning từ đầu đến cuối.

## 📚 Nội Dung Học Tập

### **PHẦN 1: LÝ THUYẾT CỐ BẢN**
- [01_tetris_game.md](./docs/01_tetris_game.md) - Luật chơi Tetris
- [02_reinforcement_learning.md](./docs/02_reinforcement_learning.md) - Cơ bản về Reinforcement Learning
- [03_q_learning.md](./docs/03_q_learning.md) - Thuật toán Q-Learning
- [04_deep_q_learning.md](./docs/04_deep_q_learning.md) - Deep Q-Learning & DQN

### **PHẦN 2: THỰC HÀNH**

#### Step 1: Tetris Game Engine (Không AI)
```bash
python step1_tetris_basic.py
```
- Tạo game Tetris cơ bản
- Hiểu cách làm việc của game mechanics
- [step1_tetris_basic.py](./code/step1_tetris_basic.py)

#### Step 2: State Representation
```bash
python step2_state_features.py
```
- Extract features từ game state
- Đánh giá tầm quan trọng của mỗi feature
- [step2_state_features.py](./code/step2_state_features.py)

#### Step 3: Neural Network Design
```bash
python step3_neural_network.py
```
- Thiết kế Deep Q-Network
- Hiểu input/output của mạng
- [step3_neural_network.py](./code/step3_neural_network.py)

#### Step 4: Training DQN
```bash
python step4_train_dqn.py
```
- Huấn luyện mô hình
- Monitor các metrics (score, loss, etc.)
- [step4_train_dqn.py](./code/step4_train_dqn.py)

#### Step 5: Testing & Visualization
```bash
python step5_test_model.py
```
- Kiểm tra mô hình đã học
- Visualize gameplay
- [step5_test_model.py](./code/step5_test_model.py)

## 🎯 Các Khái Niệm Chính

1. **Tetris Game State**: (lines_cleared, holes, bumpiness, height)
2. **Actions**: Vị trí (x) + số lần rotate của piece
3. **Rewards**: Điểm từ lines cleared - penalty cho game over
4. **Q-Values**: Ước lượng giá trị tương lai của mỗi action
5. **DQN**: Mạng neural dự đoán Q-values

## 📊 Cấu Trúc Folder

```
tetris_from_scratch/
├── docs/                    # Tài liệu lý thuyết
│   ├── 01_tetris_game.md
│   ├── 02_reinforcement_learning.md
│   ├── 03_q_learning.md
│   └── 04_deep_q_learning.md
├── code/                    # Code theo từng step
│   ├── step1_tetris_basic.py
│   ├── step2_state_features.py
│   ├── step3_neural_network.py
│   ├── step4_train_dqn.py
│   └── step5_test_model.py
├── notebooks/               # Jupyter notebooks interactive
│   └── tetris_learning.ipynb
├── models/                  # Trained models
├── logs/                    # Training logs & tensorboard
└── README.md
```

## 🚀 Hướng Dẫn Nhanh

### 1. Cài đặt Requirements
```bash
pip install torch numpy pillow opencv-python tensorboardX
```

### 2. Học Lý Thuyết
Đọc các file markdown trong folder `docs/` theo thứ tự

### 3. Thực Hành Code
Chạy từng step theo thứ tự từ step 1 đến step 5

### 4. Hiểu Sâu Hơn
Sửa code, thử các hyperparameter khác nhau, quan sát kết quả

## 💡 Lời Khuyên Học Tập

- Đừng chỉ copy-paste code, hãy hiểu từng dòng
- Thay đổi hyperparameters và quan sát ảnh hưởng
- Thêm print statements để debug và hiểu logic
- Vẽ biểu đồ để visualize kết quả

## 📖 Tài Liệu Tham Khảo

- [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html)
- [Deep Q-Networks Paper](https://www.nature.com/articles/nature14236)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)

## 🤝 Hỗ Trợ

Nếu có câu hỏi, hãy kiểm tra:
1. Các comments trong code
2. Phần explanation trong mỗi step
3. Các file documentation

Happy Learning! 🎉
