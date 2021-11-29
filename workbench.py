'''
File containing random python code used when testing something.
Pretty much a "history" file for python tests.
'''

#### Count of index pairs with equal elements in an array
# def solution(A):

#     # brute forcing, needs to be optimized
#     pairs = []
#     for index in range(len(A)):
#         for next_num in range(len(A)):
#             next_num += 1
#             if next_num < len(A) and next_num != index and A[index] == A[next_num]:
#                 pair_found = (index, next_num)
#                 if not pair_found[0] >= pair_found[1]:
#                     pairs.append((index, next_num))

#     return(len(pairs))

# if __name__ == "__main__":
#     solution([3,5,6,3,3,5,0])


### Iterator Playground
# import re

# MAX_INT_ALLOWED = 1000_000_000
# MIN_INT_ALLOWED = -1000_000_000

# def solution(file_object):
#     return Iterator(file_object)

# class Iterator:
#     def __init__(self, file_content):

#         # I'm assuming I don't have to handle the open process of the file
#         lines = file_content.split('\n') 
#         self.current_index = 0
        
#         valid_nums = []
#         for line in lines:
#             try:
#                 parsed_int = int(line)
#                 if parsed_int < MAX_INT_ALLOWED and parsed_int > MIN_INT_ALLOWED:
#                     valid_nums.append(parsed_int)
#             except:
#                 pass

#         self.numbers = valid_nums

#     def __iter__(self):
#         return self

#     def __next__(self):
#         self.current_index += 1
#         try:
#             return self.numbers[self.current_index]
#         except:
#           raise StopIteration

# if __name__ == "__main__":
#     test_file_content = "137\n-104\n2 58\n+0\n++3\n+1\n23.9\n2000000000\n-0\nfive\n-1"

#     for c in solution(test_file_content):
#         print(c)


### Random, Misc
# book_titles = ["Book One","Book Two"]
# for book in book_titles:
#     print(book.lower())

# cities = ['City A', 'City C', 'City B']
# sorted_cities = sorted(cities)
# sorted_cities.remove(sorted_cities[0])
# print(sorted_cities)

# letters = ["a", "e", "i"]
# letters.append("o")
# letters.append("u")

# for index in range(len(letters)):
#     if letters[index] == "i":
#         letters[index] = "y"
# print(letters)

# words = ('the', 'student', 'likes', 'coding', 'the')
# counter = 0
# for word in words:
#     if word.lower() == 'the':
#         counter += 1
# print(counter)

# def get_favorite_words():
#     print("Please enter your three favorite words!")
#     word_one = input('Enter word one:')
#     word_two = input('Enter word two:')
#     word_three = input('Enter word three:')

#     return (word_one, word_two, word_three)

# my_list = ["a", "e", "i"]

# my_list.remove(my_list[len(my_list)-1])
# print(my_list)

# some_values = ["some_value_one", "some_value_two"]
# more_values = ["more_value_one", "more_value_two"]
# values = some_values + more_values
# print(values)


# for num in range(2,8):
#     if num% 2 ==0:
#         continue
#     print(num)

# for num in range(10,14):
#     for i in range(2,num):
#         if num%i == 1:
#             print(num)
#             break

# for num in range (2,-5,-1):
#     print(num, end=", ")

# numbers = [10, 20]
# items = ["Apple", "Banana", "Orange"]

# for number in numbers:
#     for item in items:
#         print(number, item, end= ", ")

# num = 3
# list = [2,5,8]
# for l in list:
#     num = num+l
# print(num)

# fruit_list = ['Apple', 'Banana', 'Orange']
# for fruit in fruit_list:
#     print(fruit*2)


