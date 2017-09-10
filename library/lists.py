from random import randint

__author__ = 'tomarcher'
__version__ = '0.0.1'

# Returns a randomised list of numbers from 1 to maxElement
def get_list(max_element):
    target_list = []
    source_list = list(range(1, max_element + 1))

    for x in range(max_element -1, -1, -1):
        # select an element from the sourcelist
        index = randint(0, x)
        element = source_list[index]

        target_list.append(element)
        source_list.remove(element)

    return target_list

def get_length(input_list):
    return len(input_list)

def swap_pair(input_list, left, right):
    temp = input_list[left]
    input_list[left] = input_list[right]
    input_list[right] = temp
    
if __name__ == '__main__':
    my_list = get_list(10)
    print(my_list)