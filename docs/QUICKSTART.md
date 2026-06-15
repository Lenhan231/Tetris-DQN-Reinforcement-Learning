# ⚡ Quick Start Guide

## 1. Cài Đặt (2 phút)

```bash
# Vào folder tetris_from_scratch
cd tetris_from_scratch

# Cài dependencies
pip install -r requirements.txt
```

## 2. Bắt Đầu Học (Lần Đầu)

### Lựa chọn A: Học từ đầu (Recommended)
```bash
# 1. Đọc lý thuyết
cat docs/01_tetris_game.md
cat docs/02_reinforcement_learning.md
cat docs/03_q_learning.md
cat docs/04_deep_q_learning.md

# 2. Chạy Step 1: Game Engine
cd code/
python step1_tetris_basic.py

# 3. Chạy Step 2: Features
python step2_state_features.py

# 4. Chạy Step 3: Neural Network
python step3_neural_network.py

# 5. Train (takes time ~2-4 hours for 1000 episodes)
python step4_train_dqn.py --num_epochs 100

# 6. Test trained model
python step5_test_model.py --model_path models/tetris_final.pth
```

### Lựa Chọn B: Nhanh (Skip lý thuyết)
```bash
# Chỉ chạy code
cd code/
python step1_tetris_basic.py        # 5 mins
python step2_state_features.py      # 5 mins
python step3_neural_network.py      # 5 mins
python step4_train_dqn.py --num_epochs 50   # 1 hour
python step5_test_model.py --model_path models/tetris_final.pth
```

## 3. Tùy Chỉnh Training

```bash
# Quick training (testing)
python step4_train_dqn.py --num_epochs 50 --batch_size 256

# Full training (production)
python step4_train_dqn.py --num_epochs 1000 --batch_size 512 --lr 0.001

# Custom hyperparameters
python step4_train_dqn.py \
    --num_epochs 500 \
    --batch_size 512 \
    --lr 0.001 \
    --gamma 0.99 \
    --initial_epsilon 1.0 \
    --final_epsilon 0.001
```

## 4. Kiểm Tra Kết Quả

```bash
# Test với 20 games
python step5_test_model.py \
    --model_path models/tetris_final.pth \
    --num_games 20 \
    --visualize
```

## 5. Tiếp Theo?

- 📖 Đọc [LEARNING_GUIDE.md](LEARNING_GUIDE.md) để hiểu cách học tập tối ưu
- 🔧 Sửa code từng step để hiểu sâu hơn
- 📊 Visualize training progress
- 🎯 Implement extensions (Double DQN, Dueling DQN, etc.)

## Tệp Quan Trọng

```
tetris_from_scratch/
├── README.md                  # Overview
├── QUICKSTART.md             # File này
├── LEARNING_GUIDE.md         # Chi tiết cách học
├── requirements.txt          # Dependencies
│
├── docs/                     # Lý thuyết (ĐỌC TRƯỚC)
│   ├── 01_tetris_game.md
│   ├── 02_reinforcement_learning.md
│   ├── 03_q_learning.md
│   └── 04_deep_q_learning.md
│
├── code/                     # Code từng step (CHẠY LẦN LƯỢT)
│   ├── step1_tetris_basic.py
│   ├── step2_state_features.py
│   ├── step3_neural_network.py
│   ├── step4_train_dqn.py
│   └── step5_test_model.py
│
└── models/                   # Trained models (generated)
    └── tetris_final.pth
```

## Troubleshooting

### Error: ModuleNotFoundError
```bash
pip install torch numpy opencv-python pillow
```

### Training quá chậm
```bash
# Giảm num_epochs
python step4_train_dqn.py --num_epochs 50

# Hoặc giảm batch_size
python step4_train_dqn.py --batch_size 256
```

### CUDA/GPU không tìm thấy
→ Code tự động fallback to CPU, không cần lo!

## Có Câu Hỏi?

- Kiểm tra comments trong code
- Đọc lại documentation
- Thay đổi hyperparameters & quan sát kết quả
- Thêm print statements để debug

---

**Sẵn sàng để bắt đầu? 🚀**
