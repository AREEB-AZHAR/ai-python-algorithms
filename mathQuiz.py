import random

for i in range (1,11):
    num2=random.randint(1,20)
    num1=random.randint(1,20)
    ans = num1 + num2
    question = int(input(f"Q{i}.\n what is {num1}+{num2} ="))
    if ans == question:
        print ("your answer is correct!!!")
    else:
        print (f"your answer is Wrong!! correct answer is {ans}")
    

