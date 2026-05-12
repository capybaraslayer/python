def containsDuplicate(nums):
    print(len(set(nums)))
    print(set(nums))
    print(len(nums))
    return len(nums) != len(set(nums))
print(containsDuplicate([1,1,1,3]))
