import csv
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
import plotly.graph_objs as go
import networkx as nx
from git import Repo


def eighty_percent_commit():
	totalcommit = 0
	for e in CommitNumb:
		totalcommit += e
	return totalcommit * 8 / 10

def monthNumber(date):
	return{
		'Jan': 1,
		'Feb': 2,
		'Mar': 3,
		'Apr': 4,
		'May': 5,
		'Jun': 6,
		'Jul': 7,
		'Aug': 8,
		'Sep': 9,
		'Oct': 10,
		'Nov': 11,
		'Dec': 12,
	}[date]

def somefunction():
	i = 0
	index_author = 0
	index_file = 0
	file_name = ''
	while i < len(Top_Authors):
		index_author = author_file_index.index(Top_Authors[i])
		j = 0
		while j < len(author_file[index_author]):
			file_name = author_file[index_author][j]
			index_file = Distinct_File_Names.index(file_name)
			edited_matrix[index_file][i] = 1
			j += 1
		i += 1
	

def checkLine(line):
	file_name = ''
	author_name = ''
	firstcomma = True
	if line[0] != 'M' and line[0] != 'A' and line[0] != 'D' and line[0] != '\n':
		i = 0
		j = 0
		k = 0
		while line[i] != '\n':
			if line[i] == '^' and line[i+1] == '*' and line[i+2] == '^' and firstcomma == False:
				k = i+3
				j = k
				while line[j] != ' ':
					j = j + 1
				k = j + 1
				j = j + 1
				while line[j] != ' ':
					j = j + 1
				Month.append(monthNumber(line[k:j]))
				k = j + 1
				j = j + 1
				while line[j] != ' ':
					j = j + 1
				Day.append(line[k:j])
				k = j + 1
				j = j + 1
				while line[j] != ' ':
					j = j + 1
				Time.append(line[k:j])
				k = j + 1
				j = j + 1
				while line[j] != ' ':
					j = j + 1
				Year.append(line[k:j])
				break
			elif line[i] == '^' and line[i+1] == '*' and line[i+2] == '^' and firstcomma == True:
				k = i+3
				j = k
				while line[j] != '^' and line[j+1] != '*' and line[j+2] != '^':
					j = j + 1
				Authors.append(line[k:j+2])
				firstcomma = False			
			i = i+1
	elif line[0] == 'M' or line[0] == 'A' or line[0] == 'D':
		i = 1
		while line[i] == '\t':
			i += 1
		j = i
		while line[j] != '\n':
			j += 1
		file_name = line[i:j]
		
		if file_name not in Distinct_File_Names:
			Distinct_File_Names.append(file_name)
		
		author_index = 0
		if Authors[-1] not in author_file_index:
			author_file_index.append(Authors[-1])
			author_file.append([])
			author_file[-1].append(file_name)
		else:
			author_index = author_file_index.index(Authors[-1])
			author_file[author_index].append(file_name)
		
author_file_index = []		
edited_matrix = []
author_file = []
Day = []
Month = []
Year = []
Time = []
Authors = []
CommitNumb = []
Distinct_Authors = []
Dates = []
File_Names = []
Distinct_File_Names = []

with open("son.txt") as f:
	for line in f:
		checkLine(line)


i = 0
j = 0
while i < len(Authors):
	index = 0
	if Authors[i] not in Distinct_Authors:
		Distinct_Authors.append(Authors[i])
		CommitNumb.append(1)
		Dates.append([])
		Dates[-1].append(Year[i] +'-'+str(Month[i]) +'-'+Day[i])
	else:
		index = Distinct_Authors.index(Authors[i])
		CommitNumb[index] = CommitNumb[index] + 1
		Dates[index].append(Year[i] +'-'+str(Month[i]) +'-'+Day[i])
	i = i + 1	

Top_Authors = []
Top_Commits = []
Top_Dates = []


eighty_commit = eighty_percent_commit()
totalscore = 0
maxscore = 0
index = 0
i = 0
while totalscore < eighty_commit:
	maxscore = max(CommitNumb)
	totalscore += maxscore
	index = CommitNumb.index(maxscore)
	Top_Authors.append(Distinct_Authors.pop(index))
	Top_Commits.append(CommitNumb.pop(index))
	Top_Dates.append([])
	Top_Dates[i].append(Dates.pop(index))
	i += 1


new_list = []
i = 0

while i < len(Top_Authors):
	new_list.append(i)
	i = i + 1

x = np.array(new_list)
y = np.array(Top_Commits)


plt.xticks(x, Top_Authors)

plt.bar(x,y)
plt.show()

edited_matrix = [[0 for x in range(len(Top_Authors))] for y in range(len(Distinct_File_Names))]
somefunction()

G = nx.Graph()


G.add_nodes_from(Top_Authors)


pos = nx.spring_layout(G)

#nx.draw_networkx_nodes(G,pos,nodelist = Top_Authors,node_color ='r')

i = 0
edge_arr = []
while i < len(Distinct_File_Names):
	j = 0
	while j < len(Top_Authors):
		if edited_matrix[i][j] == 1:
			edge_arr.append(j)
		j += 1
	j = 0
	t = 0
	while j < len(edge_arr) and len(edge_arr) > 1:
		t = j +1
		while t < len(edge_arr):		
			G.add_edge(Top_Authors[edge_arr[j]],Top_Authors[edge_arr[t]])			
			t += 1
		j += 1
	
	del edge_arr[:]
		
	i += 1

nx.draw_networkx_labels(G,pos)
nx.draw(G,pos)

plt.show()
