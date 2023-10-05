
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

s = 0
for i in range(3, 19):
    r = result[i]
    s += r
    print(f'{i}\t{r}\t{r/total:.3f}\t{s}\t{s / total:.3f}')
