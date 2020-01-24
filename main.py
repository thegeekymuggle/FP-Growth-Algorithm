def load_file(filename):
	file = open(filename, 'r')
	data = file.readlines()
	data = [x.strip() for x in data]
	
	transactions = []
	
	for t in data:
		transactions.append(t.split())

	return transactions


def create_freq_itemset(transactions, min_support):

	itemset = {}

	for transaction in transactions:
		for item in transaction:
			itemset[item] = itemset.get(item,0) + 1
	
	for key in list(itemset):
		if itemset[key] < min_support:
			del(itemset[key])

	frequent_pattern = {k: v for k, v in sorted(itemset.items(), key = lambda i: i[1], reverse = True)}

	return frequent_pattern

	
def create_ordered_itemset(transactions, frequent_pattern):

	ordered_itemset = []
	
	for transaction in transactions:
		temp = []
		for key in frequent_pattern:
			if key in transaction:
				temp.append(key)
		ordered_itemset.append(temp)
	# print(transactions)
	# print("==========")
	# print(frequent_pattern)
	# print("==========")	
	# print(ordered_itemset)
	return ordered_itemset

def creater_header_table(frequent_pattern):
	
	header_table = []

	for item in frequent_pattern.items():
		temp = []
		temp.append(item[0])
		temp.append(item[1])
		temp.append(None)
		header_table.append(temp)

	header_table_index = {}

	for row in header_table:
		header_table_index[row[0]] = header_table.index(row)

	# print(header_table)
	# print('==========')
	# print(header_table_index)
	return header_table, header_table_index


class FPTreeNode():

	def __init__(self, name, counter, parent):
		self.name = name
		self.counter = counter
		self.parent = parent
		self.children = {}
		self.nodeLink = None

	def increment_counter(self, counter):
		self.counter += 1


def create_FPTree(root, header_table, header_table_index, ordered_itemset):
	
	for item_list in ordered_itemset:
		add_node(item_list, root, header_table, header_table_index)


def add_node(item_list, root, header_table, header_table_index):
	# if not bool(root):
	# 	root.children[item_list[0]] = FPTreeNode(item_list[0], 1)
	# print(item_list[0], root.name)
	if item_list[0] in root.children:
		count = root.children[item_list[0]].counter
		root.children[item_list[0]].increment_counter(count)
	else:
		root.children[item_list[0]] = FPTreeNode(item_list[0], 1, root)
		update_header_table_nodelink(header_table, header_table_index, root.children[item_list[0]])

	if len(item_list) > 1:			
		add_node(item_list[1::], root.children[item_list[0]], header_table, header_table_index)


def update_header_table_nodelink(header_table, header_table_index, node):
	index = header_table_index[node.name]
	# print("node -", node.name, node.parent.name, node.nodeLink)
	if header_table[index][2] == None:
		header_table[index][2] = node
	else:
		temp = header_table[index][2]
		# print("temp -", temp.name, temp.parent.name, temp.nodeLink)
		while temp.nodeLink != None:
			temp = temp.nodeLink

		temp.nodeLink = node



def find_conditional_patterns(frequent_pattern, header_table, header_table_index):

	path_list = []
	# cf = 0
	conditional_patterns = []
	for item in list(header_table_index)[::-1]:
		# cf += 1
		index = header_table_index[item]
		# print("index -", index)
		node = header_table[index][2]
		# print("name -",node.name)
		# cw = 0
		conditional_patterns.append([item])
		while node != None:
			path = {}
			# cw += 1
			# print("In while loop...")
			# print("name inside while -", node.name)
			temp = find_path(node)
			if temp != None:
				conditional_patterns[-1].append([temp, node.counter])
				# path[temp] = node.counter
				# path_list.append(path)
			# print(path)
			node = node.nodeLink
			# if node == None:
			# 	break
	# 	print("cw -", cw)
	# print("cf -", cf)
	# print(conditional_patterns)
	common_set = []
	res_s = []
	for item in conditional_patterns:
		key = item[0]
		item = item[1:]
		path = []
		common = []
		s = 0

		for i in item:
			path.append(i[0])
			s += i[1]
		# print(path)
		if len(path) > 1:
			common = find_common_elements(path)
			common_set.append(common)
		elif len(path) == 1:
			common_set.append(path[0][0])
		res_s.append(s)
	# print(common_set, res_s)
		# for j in path:
			# common.append(j[0])
			# if len(j[1:]) > 0:
			# 	for x in j[1:]:
			# 		if x in common:
			# 			common.append(x)
			# 		else:
			# 			break
	# 	temp = [key, common, s]
	# 	common_set.append(temp)
	# print(common_set)
	i = 0
	result = []
	for c in common_set:
		l = header_table[i][0]
		size = len(c)
		if size == 1:
			for ele in c:
				temp = [l,ele]
				result.append(temp)
		elif size == 0:
			i+=1
			continue
		elif size > 1:
			for ele in c:
				temp = [ele, l]
				result.append(temp)
			t = c.copy()
			t.append(l)
			result.append(t)
		i += 1

	for ele in list(header_table_index):
		result.append(ele)

	print(result)




def find_path(node):

	temp=[]
	# print(node.name)
	# c = 0
	while node.parent.name != 'Root':
		# c += 1
		node = node.parent
		temp.append(node.name)
		# print(temp)
		# if node.parent.name == 'Root':
		# 	break
		# print(node.name, temp)
	# temp.remove('Root')
	temp = temp[::-1]
	# print("c -", c)
	# print(len(temp))
	if len(temp) != 0:
		return temp


def find_common_elements(arr):
	result = set([])
	for current_set in arr[1:]:
		result.intersection_update(current_set)
	return list(result)


filename = 'inp.txt'
transactions = load_file(filename)
frequent_pattern = create_freq_itemset(transactions, 3)
ordered_itemset = create_ordered_itemset(transactions, frequent_pattern)
header_table, header_table_index = creater_header_table(frequent_pattern)
root_node = FPTreeNode('Root', 0, None)
create_FPTree(root_node, header_table, header_table_index, ordered_itemset)
find_conditional_patterns(frequent_pattern, header_table, header_table_index)

# node = header_table[2][2]
# node1 = node.nodeLink
# node2 = node1.nodeLink
# print(node.name, node.counter, node.parent.name)
# print(node1.name, node1.counter, node1.parent.name)
# print(node2.name, node2.counter, node2.parent.name)



