def isMatch(s, p):
    if p.isalpha():
        return s == p
    new_p = p.replace('.*', '0')
    len_p = len(new_p)
    s_idx = -1
    idx = 0
    while s_idx < len(s) - 1:
        s_idx += 1
        i = s[s_idx]
        # print(idx + 1 < len_p, '1111')
        # print(new_p[idx] == i or new_p[idx] == '.')
        if idx + 1 < len_p:
            if new_p[idx + 1] == '*':
                if new_p[idx] == i:
                    continue
                idx += 2
                s_idx -= 1
                continue

        if len_p == idx:
            return False

        if new_p[idx] == '0':
            if idx == len_p - 1:
                break

        # print(new_p[idx] != '.', new_p[idx] != i, '2222')
        if new_p[idx] != '.' and new_p[idx] != i:
            return False

        idx += 1

    return True


# print(isMatch("aab", "c*a*b"))
# print(isMatch('mississippi', "mis*is*p*."))
print(isMatch('a', "ab*a"))
