
result = {}
for i in range(3, 19):
    result[i] = 0
total = 0

for a in range(1, 7):
    for b in range(1, 7):
        for c in range(1, 7):
            r = a + b + c
            result[r] += 1
            total += 1

sum = 0
for i in range(3, 19):
    r = result[i]
    sum += r
    print(f'{i}\t{r}\t{r/total:.3f}\t{sum}\t{sum/total:.3f}')
