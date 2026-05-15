
# def containsNearbyDuplicate( nums, k):
    
#     # for i in range(len(nums)-1):
#     #     for j in range(1,len(nums)):
#     #         if nums[i]==nums[j] and abs(i-j)<=k:
#     #             return True
#     # return False
#     i=0
#     j=len(nums)-1
#     while i < len(nums) - 1:
#             if abs(i - j) <= k and j < len(nums):
#                 if nums[i] == nums[j]:
#                     return True
#                 j += 1
#             else:
#                 i += 1
#                 j = i + 1
#         return False  
# print(containsNearbyDuplicate([1,2,3,1,2,3],2))