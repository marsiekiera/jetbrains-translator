# the list "walks" is already defined
# your code here


count = 0
distance = 0
for day in walks:
    count += 1
    distance += int(day["distance"])

average = int(distance / count)
print(average)