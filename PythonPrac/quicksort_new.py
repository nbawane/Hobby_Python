
def partition(arr, low, high):
	'''
	all small element than pivot should be shifted to to left
	:param arr:
	:param low:
	:param high:
	:return:
	'''
	if low<high:
		pivot = arr[high-1]	#select last element as pivot
		current_low_indicator = low-1
		for i in range(len(arr)):
			if arr[i] <= pivot:
				current_low_indicator += 1
				arr[i],arr[current_low_indicator] = arr[current_low_indicator],arr[i]
		arr[current_low_indicator+1],arr[high-1] = arr[high-1],arr[current_low_indicator+1]
		return current_low_indicator+1


def quicksort(arr, low, high):
	partition_index = partition(arr, low, high)
	quicksort(arr[low:partition_index],low, partition_index-1)
	quicksort(arr[partition_index:high-1],partition_index,high)

arr = [10,8,4,3,9,8,7,6,2,1,44,5,3,6]
quicksort(arr,0,len(arr))
print(arr)
