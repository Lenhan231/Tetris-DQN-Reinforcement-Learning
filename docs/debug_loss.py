"""
Debug script to diagnose loss explosion
Run this after training to see what went wrong
"""

import torch
import numpy as np
from tetris import TetrisGame
from network import DeepQNetwork

def test_network_output():
    """Test if network outputs are reasonable"""
    print("=" * 70)
    print("TESTING NETWORK OUTPUT STABILITY")
    print("=" * 70)

    network = DeepQNetwork()
    game = TetrisGame()

    # Test with various states
    print("\n1. Testing with random states:")
    for i in range(10):
        game.reset()
        state = game._get_state_features()
        state_tensor = torch.FloatTensor(list(state))

        q_value = network(state_tensor)
        print(f"  State {state} → Q = {q_value.item():.2f}")

        if abs(q_value.item()) > 1000:
            print("    ❌ WARNING: Q-value too large!")

def check_gradient_flow():
    """Check if gradients are exploding"""
    print("\n" + "=" * 70)
    print("TESTING GRADIENT FLOW")
    print("=" * 70)

    network = DeepQNetwork()
    optimizer = torch.optim.Adam(network.parameters(), lr=0.001)

    # Simulate one training step
    state = torch.FloatTensor([[5, 2, 3, 12]])
    q_pred = network(state)

    # Simulate target (normal value)
    q_target = torch.FloatTensor([[50.0]])

    loss = (q_pred - q_target) ** 2
    print(f"\nLoss: {loss.item():.4f}")

    loss.backward()

    # Check gradient magnitudes
    print("\nGradient magnitudes:")
    for name, param in network.named_parameters():
        if param.grad is not None:
            grad_norm = param.grad.norm().item()
            print(f"  {name}: {grad_norm:.6f}", end="")

            if grad_norm > 1.0:
                print(" ❌ TOO LARGE!")
            elif grad_norm < 0.00001:
                print(" ⚠️  VERY SMALL")
            else:
                print(" ✅ OK")

def diagnose_training():
    """Check common training problems"""
    print("\n" + "=" * 70)
    print("COMMON PROBLEMS CHECKLIST")
    print("=" * 70)

    checks = {
        "Learning rate too high (>0.001)": "Try --lr 0.0001",
        "Reward values too large": "Scale rewards down in tetris.py",
        "Target network not updating": "Check update frequency (every 100 eps)",
        "Batch size too small": "Try --batch_size 512 or larger",
        "Buffer not filled": "Make sure you train only after buffer > memory_size/10",
        "Gamma too high": "Default 0.99 is usually good",
    }

    for problem, solution in checks.items():
        print(f"\n❓ {problem}")
        print(f"   Fix: {solution}")

def test_loss_values():
    """Simulate loss progression"""
    print("\n" + "=" * 70)
    print("SIMULATING LOSS PROGRESSION")
    print("=" * 70)

    network = DeepQNetwork()
    optimizer = torch.optim.Adam(network.parameters(), lr=0.001)

    print("\nLoss over 10 training steps:")
    for step in range(10):
        # Random batch
        states = torch.randn(32, 4)  # 32 samples, 4 features

        # Network predicts
        q_pred = network(states)

        # Target (random for testing)
        q_target = torch.randn(32, 1)

        # Compute loss
        loss = torch.nn.functional.mse_loss(q_pred, q_target)

        # Backprop
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"  Step {step+1}: loss = {loss.item():.4f}", end="")

        if step > 0:
            if loss.item() > 10:
                print(" ❌ EXPLODING!")
            else:
                print(" ✅")

if __name__ == "__main__":
    print("\n🔍 TETRIS DQN DEBUGGING SUITE\n")

    test_network_output()
    check_gradient_flow()
    diagnose_training()
    test_loss_values()

    print("\n" + "=" * 70)
    print("RECOMMENDED FIXES (in order of likelihood):")
    print("=" * 70)
    print("""
1. REDUCE LEARNING RATE:
   python train.py --num_epochs 50 --lr 0.0001

2. INCREASE TARGET NETWORK UPDATE FREQUENCY:
   In train.py, change: if (ep + 1) % 100 == 0:
   To: if (ep + 1) % 10 == 0:

3. SCALE DOWN REWARDS:
   In tetris.py, divide rewards by 10-100

4. INCREASE BATCH SIZE:
   python train.py --num_epochs 50 --batch_size 1024

5. CHECK REWARD CALCULATION:
   Make sure rewards aren't returning negative infinity
    or NaN values
""")
