#!/usr/bin/python3
"""
227. Basic Calculator II
Difficulty: Medium

Success
Runtime: 156 ms, faster than 14.26% of Python3 online submissions for Basic Calculator II
Memory Usage: 22.8 MB, less than 5.28% of Python3 online submissions for Basic Calculator II
"""
from typing import List
import time


class Solution:
    def calc_simple_unit(self, s: str) -> str:
        s += ' '
        i = 0
        operation_type = ''
        operation_start_idx = -1
        nums = []
        while True:
            if ''.join(s.split()).lstrip('-').isnumeric() or ''.join(s.split()).lstrip('+').isnumeric(): break
            if (len(nums) > 0) and ((s[i] == '+') or (s[i] == '-')): operation_type = s[i]
            if (s[i].isnumeric()) or \
                    ((len(nums) == 0) and ((s[i] == '+') or (s[i] == '-'))):
                if operation_start_idx == -1: operation_start_idx = i
                for j in range(i + 1, len(s)):
                    if not s[j].isnumeric():
                        nums.append(s[i:j])
                        i = j - 1
                        if (len(nums) == 2) and (operation_type != ''):
                            if operation_type == '+':
                                r0 = int(nums[0]) + int(nums[1])
                            else:
                                r0 = int(nums[0]) - int(nums[1])
                            s = s[:operation_start_idx] + str(r0) + s[j:]
                            operation_type = ''
                            operation_start_idx = -1
                            nums = []
                            i = -1
                        break
            i += 1
        s = ''.join(s.split())
        return s

    def optimizer(self, s: str) -> str:
        s = ''.join(s.split())
        minimal_optimized_len = 17
        i = 5
        while i <= len(s) - minimal_optimized_len - 1:
            if s[i].isnumeric() and (s[i + 1] == '+') and s[i + 2].isnumeric():
                start_idx = i + 2
                pidx0 = s.find('/', start_idx)
                if pidx0 < 0: pidx0 = len(s)
                pidx1 = s.find('*', start_idx)
                if pidx1 < 0: pidx1 = len(s)
                pidx = min(pidx0, pidx1)
                if pidx == len(s): break
                if pidx - start_idx > minimal_optimized_len:
                    while not ((s[pidx - 1].isnumeric()) and
                               ((s[pidx - 2] == '+') or (s[pidx - 2] == '-')) and
                               (s[pidx - 3].isnumeric())):
                        pidx -= 1
                    pidx -= 2
                    s0 = self.calc_simple_unit(s[start_idx:pidx])
                    negative_adjustment = 1 if int(s0) < 0 else 0
                    s = s[:start_idx - negative_adjustment] + s0 + s[pidx:]
                else:
                    i += pidx - start_idx - 1

            i += 1

        return s

    def processor(self, s: str, signs: str) -> str:
        s = ''.join(s.split())

        while True:
            s = ' ' + s + ' '
            sign_idx = len(s)
            sign = ''
            for sign0 in signs:
                candidate_sign_idx = s.find(sign0, 2)
                if (candidate_sign_idx > 0) and (candidate_sign_idx < sign_idx):
                    sign_idx = candidate_sign_idx
                    sign = sign0

            if sign_idx == len(s): break
            op1 = ''
            op2 = ''
            i = sign_idx - 1
            while op1 == '':
                if not s[i].isnumeric(): op1 = s[i:sign_idx]
                i -= 1
            start_idx = i + 1
            i = sign_idx + 1
            while op2 == '':
                if not s[i].isnumeric(): op2 = s[sign_idx + 1:i]
                i += 1
            end_idx = i - 1

            op1 = ''.join(op1.split())
            op2 = ''.join(op2.split())
            if (op1 == '') or (op2 == ''): break
            if sign == '*':
                if not op1[0].isnumeric():
                    op1 = op1[1:]
                    start_idx += 1
                s0 = str(int(op1) * int(op2))
            elif sign == '/':
                if not op1[0].isnumeric():
                    op1 = op1[1:]
                    start_idx += 1
                s0 = str(int(int(op1) / int(op2)))
            elif sign == '+':
                s0 = str(int(op1) + int(op2))
                if (int(s0) >= 0) and (start_idx > 0): s0 = '+' + s0
            elif sign == '-':
                s0 = str(int(op1) - int(op2))
                if (int(s0) >= 0) and (start_idx > 0): s0 = '+' + s0
            else:
                s0 = ''

            s = s[:start_idx] + s0 + s[end_idx:]
            s = ''.join(s.split())
            if (len(s) > 0) and (s[0] == '+'): s = s[1:]
            if s == '': s = '0'
        return s

    def frocessor(self, s: str) -> int:
        stack = []
        s = ''.join(s.split())
        i = 0
        while i < len(s):
            operations_type = ''
            if i == 0:
                operations_type = '+'
                i = -1
            elif i < len(s) - 1:
                if (not s[i].isnumeric()) and (s[i + 1].isnumeric()):
                    if (s[i] == '+') or (s[i] == '-') or (s[i] == '*') or (s[i] == '/'):
                        operations_type = s[i]

            i += 1
            num_start_idx = i
            num = ''
            while num == '':
                if (i > len(s) - 1) or (not s[i].isnumeric()): num = s[num_start_idx:i]
                i += 1
            i -= 1
            stack.append(operations_type + num)

        # process `*` and `/`
        i = 1
        while i < len(stack):
            operations_type = stack[i][0]
            if (operations_type == '*') or (operations_type == '/'):
                if operations_type == '*':
                    stack[i - 1] = stack[i - 1][0] + str(int(stack[i - 1][1:]) * int(stack[i][1:]))
                    stack.pop(i)
                    continue
                if operations_type == '/':
                    stack[i - 1] = stack[i - 1][0] + str(int(int(stack[i - 1][1:]) / int(stack[i][1:])))
                    stack.pop(i)
                    continue
            i += 1

        # process `+` and `-`
        int_stack = []
        for i in range(len(stack)):
            int_stack.append(int(stack[i]))

        return sum(int_stack)

    def calculate(self, s: str) -> int:

        return self.frocessor(s)

        # s = self.optimizer(s)
        # s = self.processor(s, '*/')
        # s = self.processor(s, '+-')
        # return int(s)


sol = Solution()
print(sol.calculate(s="1+2*5/3+6/4*2"))
#
# #

if sol.calculate(s="3+2*2") != 7: print('err-1')
if sol.calculate(s=" 3/2 ") != 1: print('err-2')
if sol.calculate(s=" 3+5 / 2 ") != 5: print('err-3')
if sol.calculate(s="0-2147483647") != -2147483647: print('err-63')
if sol.calculate(s="1-1+1") != 1: print('err-40')
if sol.calculate(s="2+3-4") != 1: print('err-40a')
if sol.calculate(s="0+0") != 0: print('err-16')
if sol.calculate(s="1+1+1") != 3: print('err-35')
if sol.calculate(s="2-3-4") != -5: print('err-42')
if sol.calculate(s="14/3*2") != 8: print('err-50')
if sol.calculate(s="1*2-3/4+5*6-7*8+9/10") != -24: print('err-61')
if sol.calculate(s="1+1-1") != 1: print('err-99')
if sol.calculate(s="1+2*5/3+6/4*2") != 6: print('err-100')


stime = time.time()
if sol.calculate(s=s) != -30762: print('err-108')
print(f'runtime: {time.time() - stime:.2f}sec')