import random

class mathai:
    def __init__ (s):
        s.lvl, s.streak = 1,0

    def generate(s):
        while True:
            a, b = random.randint(2,10*s.lvl), random.randint(2,5*s.lvl)
            op = random.choice(['+', '-'])
            ans = eval(f"{a}{op}{b}")
            val = input(f"{a}{op}{b}=")

            if val.lower()=='q':
                print("Thanks for particpating")
                return False
            elif val.lower()=='s':
                s.streak= 0
                print(ans,"lowering difficulty")
                if s.lvl>1:
                    s.lvl-=1
            else:
                try:
                    if int(val)== ans:
                        s.streak+=1
                        print("correct!!! streak ",s.streak)
                        if s.streak >= 3: s.lvl += 1; s.streak = 0; print(">> Level Up!")
                    else:
                        raise ValueError
                except ValueError:
                    s.lvl=max(1,s.lvl-1)
                    s.streak=0
                    print(f"correct answer ={ans} \nlowering difficulty")
if __name__ == '__main__':
    ai=mathai()
    ai.generate()