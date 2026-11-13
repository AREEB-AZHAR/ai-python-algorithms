import random

class MathAI:
    def __init__(self):
        self.level = 1
        self.total_streak = 0
        self.level_streak = 0  # Tracks progress specifically for leveling up

    def generate_problem(self):
        # Improved Logic: Defined scaling factors for clearer difficulty progression
        base_range = 10
        difficulty_multiplier = 5
        
        # Calculate max values based on level
        max_a = base_range + (self.level * 2 * difficulty_multiplier)
        max_b = base_range + (self.level * difficulty_multiplier)
        
        # Ensure minimum is always at least 2
        a = random.randint(2, max(2, max_a))
        b = random.randint(2, max(2, max_b))
        
        op = random.choice(['+', '-'])
        
        # Better Logic: Ensure subtraction doesn't result in negatives
        if op == '-' and b > a:
            a, b = b, a
            
        ans = a + b if op == '+' else a - b
        return a, b, op, ans

    def play(self):
        print("\n--- MathAI Trainer ---")
        print("Rules: 3 correct answers in a row to level up.")
        print("Controls: Type 'q' to quit, 's' to skip.\n")

        while True:
            a, b, op, ans = self.generate_problem()
            
            # Display Stats
            # Shows '●' for current progress towards next level
            progress_bar = "● " * self.level_streak + "○ " * (3 - self.level_streak)
            print(f"╔══════════════════════════════════════╗")
            print(f"║ LVL {self.level:<4} Streak: {self.total_streak:<4} Next: {progress_bar}║")
            print(f"╚══════════════════════════════════════╝")
            
            val = input(f"{a} {op} {b} = ")

            if val.lower() == 'q':
                print(f"\nGame Over. Final Level: {self.level}. Max Streak: {self.total_streak}")
                break
                
            elif val.lower() == 's':
                self.handle_fail("Skip", ans)
                
            else:
                try:
                    if int(val) == ans:
                        self.handle_success()
                    else:
                        raise ValueError
                except ValueError:
                    self.handle_fail("Incorrect", ans)

    def handle_success(self):
        self.level_streak += 1
        self.total_streak += 1
        print(f"✅ Correct!")
        
        if self.level_streak >= 3:
            self.level += 1
            self.level_streak = 0
            print(f"🚀 LEVEL UP! Difficulty increased to Level {self.level}")

    def handle_fail(self, reason, correct_ans):
        # Reset streaks on failure or skip
        self.total_streak = 0
        self.level_streak = 0
        
        old_level = self.level
        self.level = max(1, self.level - 1)
        
        msg = "Difficulty lowered." if old_level > self.level else "Keeping current difficulty."
        print(f"❌ {reason}. Answer was {correct_ans}. {msg}")

if __name__ == '__main__':
    ai = MathAI()
    ai.play()