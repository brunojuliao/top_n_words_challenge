import re
re_clean_punctuations = re.compile('[^\w\s]')

def popular_n_words(how_many_top_words, possible_words, phrases):
                         
    requests_array = []
    score = dict()
    
    possible_words_set = set(possible_words)
    for phrase in phrases:
        intersect_result = set(normalizeString(phrase).split()).intersection(possible_words_set)
        if len(intersect_result) > 0:
            requests_array.append(intersect_result)
        
    heap = MaxHeap()
    for words in requests_array:
        for word in words:
            temp_score = score.get(word)
            if temp_score != None:
                temp_score.increase_count()
            else:
                score[word] = Node(word, heap.recalculate_node)
                heap.push(score[word])
                
    result = []
    for x in range(0, how_many_top_words):
        node = heap.pop()
        result.append(node.word)
        
    return result

def normalizeString(input):
    return re_clean_punctuations.sub('', input.casefold())
    
class Node:
    def __init__(self, word, when_increase):
        self.word = word
        self.count = 1
        self.index = -1
        self.when_increase = when_increase

    def increase_count(self):
        self.count += 1
        if self.when_increase != None:
            self.when_increase(self)

    def __repr__(self):
        return self.word + " - " + str(self.count) + " - " + str(self.index)

    def is_more_than(self, other_node):
        if self.count > other_node.count:
            return True
        elif self.count < other_node.count:
            return False
        elif self.word < other_node.word:
            return True
        return False

class MaxHeap:
    def __init__(self):
        self.heap = []

    def get_parent_index(self, node):
        offset = 2 if node.index % 2 == 0 else 1
        parent_index = int((node.index - offset) / 2)
        return parent_index

    def push(self, node):
        self.heap.append(node)
        node.index = len(self.heap) - 1
        while(node.index > 0):
            parent_index = self.get_parent_index(node)
            if self.heap[parent_index].is_more_than(self.heap[node.index]):
                break
            self.heap[parent_index], self.heap[node.index] = self.heap[node.index], self.heap[parent_index]
            self.heap[node.index].index = node.index
            self.heap[parent_index].index = parent_index

    def pop(self):
        heap_length = len(self.heap)
        if heap_length == 0:
            return None
        elif heap_length == 1:
            return self.heap.pop()

        node = self.heap.pop(0)
        self.heap.insert(0, self.heap.pop())
        heap_length = len(self.heap)

        current_index = 0
        while(heap_length > 1 and current_index < heap_length - 1):
            right_index = (current_index * 2) + 2
            if right_index < heap_length and self.heap[right_index].is_more_than(self.heap[current_index]):
                self.heap[right_index], self.heap[current_index] = self.heap[current_index], self.heap[right_index]
                self.heap[current_index].index = right_index
                current_index = right_index
                continue

            left_index = (current_index * 2) + 1
            if left_index < heap_length and self.heap[left_index].is_more_than(self.heap[current_index]):
                self.heap[left_index], self.heap[current_index] = self.heap[current_index], self.heap[left_index]
                self.heap[current_index].index = left_index
                current_index = left_index
                continue

            break

        return node

    def recalculate_node(self, node):
        while node.index > 0 and node.count > self.heap[self.get_parent_index(node)].count:
            parent_index = self.get_parent_index(node)
            current_index = node.index
            self.heap[current_index], self.heap[parent_index] = self.heap[parent_index], self.heap[current_index]
            self.heap[current_index].index = current_index
            self.heap[parent_index].index = parent_index

    def print(self):
        print(self.heap)

    def get_repr(self):
        return self.heap.__repr__()

result = popular_n_words(2, 
    ["test", "fruit", "food", "python"], 
    [
        "I want to eat a fruit", 
        "Test your code", 
        "Ordering food online is a trend",
        "Why should I test this fruit?",
        "What are you testing?",
        "Can I order some food?",
        "Is test important?"
    ]
)

print("Expected: ['test', 'food']")
print("Result: ", result)