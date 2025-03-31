
def removeBefore(m: dict, character: str) -> dict:
    tmpList = list()
    tmpList.append(character)
    for k in m:
        if k == character:
            break
        else:
            tmpList.append(k)
    for c in tmpList:
        del m[c]
    return m


def lengthOfLongestSubstring(s: str) -> int:
    map_str = dict()
    max_len = int(0)
    startInx = int(0)
    endInx = int(-1)

    for i in range(len(s)):
        # print("map: ", map_str, "with the start = ", startInx, " end = ", endInx)
        character = s[i]
        if character not in map_str:
            map_str[character] = i
        else:
            startInx = map_str[character] + 1
            removeBefore(map_str, character)
            map_str[character] = i
        endInx += 1

        max_len = max(max_len, endInx - startInx + 1)
        # print(startInx, "-", endInx)
        # print("maxlen = ", max_len)

    return max_len

s = input("Type your string: ")


print("Length of the longest substring: ", lengthOfLongestSubstring(s))


###                       The solution:
# class Solution:
#     def lengthOfLongestSubstring(self, s: str) -> int:
#         l = 0 
#         res = 0
#         charset = set()

#         for r in range(len(s)):
#             while s[r] in charset:
#                 charset.remove(s[l])
#                 l += 1
#             charset.add(s[r])
#             res = max(res, r -l + 1)
#             r += 1

#         return res