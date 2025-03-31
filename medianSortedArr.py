from typing import List



def findMedianSortedArrays(nums1: List[int], nums2: List[int]) -> float:
    len1 = len(nums1)
    len2 = len(nums2)

    mergedList = []
    i = int(0) # iterator of nums1
    j = int(0) # Iterator of nums2
    while (i < len1) and (j < len2):
        if nums1[i] <= nums2[j]:
            mergedList.append(nums1[i])
            i += 1
        else:
            mergedList.append(nums2[j])
            j += 1
    
    while i < len1:
        mergedList.append(nums1[i])
        i+=1
    while j < len2:
        mergedList.append(nums2[j])
        j+=1
    
    # Result base on the mergeList length
    mergedLength = len(mergedList)
    res = float(0)
    # Case odd
    if mergedLength % 2 == 0:
        index = int(mergedLength / 2)
        res = (mergedList[index] + mergedList[index-1]) / 2
    else:
        index = int(mergedLength / 2)
        res = mergedList[index]

    # print("Res list: ", mergedList, " len = ", mergedLength)

    return float(res)


array1 = [int(x) for x in input("Type array 1: ").split()]
array2 = [int(x) for x in input("Type array 2: ").split()]

print("Median of two sorted Lists is: ", findMedianSortedArrays(array1, array2))