'''

using https://youtu.be/-RdOwhmqP5s
create a interactive visualization to show and manipulate the colored region
'''

import roots as r


test = r.POLY([5, 4, 3, 2, 1, 10], n=50)
testD = r.POLY(test.derivative, n=20)
# print(test.roots)
print(testD.roots)