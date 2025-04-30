from number_line import NumberLine
n1 = NumberLine()
n1.add_range(0,True, 9,True)
n1.add_range(19,True, 30,True)
n1.add_range(41,True, 50,True)

n2 = NumberLine()
n2.add_range(0,True, 10,True)
n2.add_range(20,True, 30,True)
n2.add_range(40,True, 50,True)
total_vals = 0
og = n1
for range in n1.get_ranges():
    total_vals += range["upper value"] - range["lower value"] 
for range in n2.get_ranges():
    n1.add_range(range["lower value"], True, range["upper value"], True)
    
print(n1.get_ranges())
print(n2.get_ranges())
for range in og.get_ranges():
    try:
        n1.remove_range(range["lower value"], True, range["upper value"], True)
    except Exception as e:
        if str(e) == "Some of the values in the range you listed are not currently included in the number line":
            pass
print(n1.get_ranges())
wrong_vals = 0
for range in n1.get_ranges():
    wrong_vals += range["upper value"] - range["lower value"]

print(wrong_vals)
print(total_vals)
print(1 - wrong_vals/total_vals)