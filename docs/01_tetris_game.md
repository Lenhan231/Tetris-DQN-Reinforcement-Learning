# 1️⃣ Tetris Game Mechanics - Hiểu Luật Chơi

## Giới Thiệu

Tetris là trò chơi cổ điển nơi người chơi phải sắp xếp các khối (tetrominoes) rơi xuống.

## Các Khối (Tetrominoes)

Tetris có 7 loại khối, mỗi khối được xác định bởi:
- **Hình dạng**: Mảng 2D (3x3 hoặc 4x1)
- **Màu sắc**: Để phân biệt
- **Rotations**: Có thể xoay 0, 90, 180, 270 độ

```
O-piece (Vàng)     T-piece (Tím)      S-piece (Xanh)
[X][X]             [ ][X][ ]          [ ][X][X]
[X][X]             [X][X][X]          [X][X][ ]

I-piece (Xanh dương)    L-piece (Cam)      Z-piece (Đỏ)
[X][X][X][X]           [ ][ ][X]          [X][X][ ]
                        [X][X][X]          [ ][X][X]

J-piece (Cyan)
[X][ ][ ]
[X][X][X]
```

## Board (Bảng Chơi)

- **Kích thước tiêu chuẩn**: 10 cột × 20 hàng
- **Mục tiêu**: Điền đầy các hàng để loại bỏ chúng
- **Trạng thái**: Ma trận 2D where:
  - `0` = trống
  - `1-7` = khối đã cố định (color ID)

## Luật Chơi Cơ Bản

### 1. Spawning (Sinh Khối Mới)
```
Khối mới xuất hiện ở hàng 0, giữa bàn
Nếu khối va chạm ngay từ lúc sinh = Game Over
```

### 2. Điều Khiển
- **Trái/Phải**: Di chuyển khối theo chiều ngang
- **Xoay**: Thay đổi hướng (0°, 90°, 180°, 270°)
- **Xuống**: Khối tự động rơi hoặc bị đẩy xuống

### 3. Collision Detection (Phát Hiện Va Chạm)
```python
Khối va chạm khi:
1. Chạm đáy bàn (y > 19)
2. Chạm khối cố định khác
3. Vượt khỏi biên trái/phải
```

### 4. Line Clearing (Xóa Hàng)
```
Khi một hàng đầy (không có ô trống):
- Xóa hàng đó
- Các hàng trên rơi xuống
- Tính điểm: score += 1 + (lines_cleared² × width)
```

### 5. Game Over
```
Game Over xảy ra khi:
- Khối mới sinh ra nhưng không có chỗ
- Hoặc khối vượt quá đầu bàn trong quá trình di chuyển
```

## Các Bước Một Game Loop

```
1. Spawn khối mới
   ├─ Nếu va chạm → Game Over
   └─ Nếu ok → tiếp tục

2. Nhận action (vị trí x, số lần rotate)
   ├─ Rotate khối
   └─ Di chuyển đến vị trí x

3. Khối rơi xuống
   └─ Lặp cho đến khi va chạm

4. Cố định khối trên bàn
   ├─ Cập nhật board
   └─ Check xóa hàng

5. Tính điểm & reward
   └─ Trở về bước 1
```

## Ví Dụ: Action Space

Với mỗi khối, ta có thể:
- Di chuyển đến các vị trí x khác nhau (0-10)
- Xoay khối (0-4 lần)

**Action** = (x_position, num_rotations)

Ví dụ: `action = (5, 2)` nghĩa là:
- Xoay khối 2 lần (180 độ)
- Di chuyển đến vị trí x=5
- Khối tự động rơi xuống

## Tổng Kết

| Khía Cạnh | Mô Tả |
|-----------|-------|
| **Board** | 10×20 grid |
| **Pieces** | 7 loại tetrominoes |
| **Actions** | Di chuyển + Rotate |
| **Rewards** | Điểm từ lines cleared |
| **Goal** | Maximize score, tránh game over |

---

**Tiếp theo**: [02_reinforcement_learning.md](./02_reinforcement_learning.md)
