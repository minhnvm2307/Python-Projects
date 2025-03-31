from typing import List, Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def print(self):
        while self:
            print(self.val, "-> " if self.next else "\n", end='')
            self = self.next

def addTwoNumbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
    # Pointer to list1
    tmp1 = l1
    # Pointer to list2
    tmp2 = l2
    # Remain after adding
    rem = int(0)

    # Result LinkList
    res = None
    # Pointer to result list
    resTmp = ListNode(0)

    while tmp1 and tmp2:
        addDigit = int(tmp1.val + tmp2.val + rem)
        rem = addDigit // 10 # Remain digit
        addDigit %= 10 # Digit to add

        if res is None:
            res = ListNode(addDigit)
            resTmp = res
            tmp1 = tmp1.next
            tmp2 = tmp2.next
            continue
        else:
            resTmp.next = ListNode(addDigit)

        # Continue
        tmp1 = tmp1.next
        tmp2 = tmp2.next
        resTmp = resTmp.next


    # Add the remaining
    if tmp1:
        print("continue on l1")
        while tmp1:
            addDigit = tmp1.val + rem
            rem = addDigit // 10
            addDigit %= 10

            resTmp.next = ListNode(addDigit)
            resTmp = resTmp.next
            tmp1 = tmp1.next
    if tmp2:
        print("continue on l2")
        while tmp2:
            addDigit = tmp2.val + rem
            rem = addDigit // 10
            addDigit %= 10

            resTmp.next = ListNode(addDigit)
            resTmp = resTmp.next
            tmp2 = tmp2.next

    return res



array1 = [int(x) for x in input("Type the ListNode1: ").split()]
array2 = [int(x) for x in input("Type the ListNode2: ").split()]

# Construct the first LinkList
l1 = None
tmp = None
for i in array1:
    if l1 is None:
        l1 = ListNode(i)
        tmp = l1
        continue
    tmp.next = ListNode(i)
    tmp = tmp.next

# Construct the second one
l2 = None
tmp = None
for i in array2:
    if l2 is None:
        l2 = ListNode(i)
        tmp = l2
        continue
    tmp.next = ListNode(i)
    tmp = tmp.next

# Print out list1
# l1.print()
# Print out list2
# l2.print()

addTwoNumbers(l1, l2).print()