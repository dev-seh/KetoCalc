totalCarbs = 0
totalProteins = 0
totalKcal = 0

print ("Today you ate: %i carbs, %i protein and %i kcal." %(totalCarbs,totalProteins,totalKcal))
print ("Did you eat anything else?")
answer = input("Y/N: ")
if answer == "y":
    print ("What did you eat? /n")
    lastMeal = input()
    print ("How many carbs? /n")
    carbs = int(input())
    totalCarbs = totalCarbs + carbs
    print ("How many proteins? /n")
    proteins = int(input())
    totalProteins = totalProteins + proteins
    print ("How many kcal? /n")
    kcal = int(input())
    totalKcal = totalKcal + kcal
    print ("Daily values have been updated")
elif answer == "n":
    print ("Keep it up!")
else:
    print ("Wrong input")

print ("Today you ate: %i carbs, %i protein and %i kcal." %(totalCarbs,totalProteins,totalKcal))