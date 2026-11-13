import random

lvl, streak = 1, 0
while True:
    # Generate numbers based on level size
    a, b = random.randint(1, 5 * lvl), random.randint(1, 5 * lvl)
    op = random.choice(['+', '-', '*'])
    ans = eval(f"{a}{op}{b}")

    val = input(f"Lvl {lvl} ({streak}/3) | {a} {op} {b} = ")

    if val.lower() == 's':
        lvl = max(1, lvl - 1) # Reduce difficulty
        streak = 0
        print(f"Suggestion: Answer is {ans}. Difficulty lowered.")
    else:
        try:
            if int(val) == ans:
                streak += 1
                print("Correct!")
                if streak >= 3: lvl += 1; streak = 0; print(">> Level Up!") 
            else:
                raise ValueError # Trigger failure logic
        except ValueError:
            lvl = max(1, lvl - 1)
            streak = 0
            print(f"Wrong. Answer was {ans}. Difficulty lowered.")