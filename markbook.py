"""
Markbook Application
Group members: YingChen Ma, Simon Li, Charlie Guo
"""


def some_func():
    return True

d = {}
a = ["abc", "def"]
b = 2
for j in a:
    if j not in d:
        d[j] = []
    d[j].append(b)
print(d)