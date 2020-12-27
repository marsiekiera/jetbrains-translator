# the list with classes; please, do not modify it
groups = ['1A', '1B', '1C', '2A', '2B', '2C', '3A', '3B', '3C']

# your code here
groups_dict = {}
for group in groups:
    groups_dict[group] = None

amount = int(input())

for i in range(0, amount):
    groups_dict[groups[i]] = int(input())

print(groups_dict)