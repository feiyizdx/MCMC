# -*- coding: utf-8 -*-
# this is a code of MCMC
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import unittest
import random
import sys
#generate 2d grid
#m nodes
m=5
r=2.0
istep=200
T=10
#generate 2D grid, dx=dy=1
nxx, nyy = (m,m)
x = np.linspace(0, m-1, nxx)
y = np.linspace(0, m-1, nyy)
xv, yv = np.meshgrid(x, y)
#pick up 5 points as vertex e.g. #0 (0,0) #1 (1,2) #2 (1,3) #3 (3,2) #4 (4,4)
xrange=[0, 1, 1, 3, 4]
yrange=[0, 2, 3, 2, 4]

test=xrange[4]
#define weights function
def cacl_weights(x_1, y_1, x_2, y_2):
    return np.sqrt((x_1-x_2)**2+(y_1-y_2)**2)
#define add edge function. add an edge from nodes a and b
def distance(a, b):
    dist=cacl_weights(xv[xrange[a],yrange[a]], yv[xrange[a],yrange[a]],xv[xrange[b],yrange[b]], yv[xrange[b],yrange[b]])
    FG.add_weighted_edges_from([(a,b,dist)],label=str(dist))
    return None
    
FG=nx.Graph()
#genereate intial graph
#a, b denotes the index of different points/vertex can read from a file
a=0
b=1
distance(a, b)
a=0
b=2
#distance=cacl_weights(xv[xrange[a],yrange[a]], yv[xrange[a],yrange[a]],xv[xrange[b],yrange[b]], yv[xrange[b],yrange[b]])
#FG.add_weighted_edges_from([(a,b,distance)],label=str(distance))
distance(a, b)
a=0
b=3
distance(a, b)
a=0
b=4
distance(a, b)

#print FG.number_of_edges()
nx.draw(FG, with_labels=True)
plt.show()
#generate spanning tree
#T=nx.minimum_spanning_tree(FG)
#span_tree=sorted(T.edges(data=True))

#proposal probality 
#if the graph cannot cut any edges. The probality of adding an edge is 1. 
#else if the graph cannot add any more edges. The probality of removing an edge is 1.
#otherwise. The probality of adding or removing is 0.5.

#write add edge function
def add_func(): 
  add=True
  a=random.randint(0,m-1)
  b=random.randint(0,m-1)
  while a==b:
    b=random.randint(0,m-1)
  while(add):   
    if (((a,b) in FG.edges() ) or ((b,a) in FG.edges() )):
      a=random.randint(0,m-1)
      b=random.randint(0,m-1)
      while a==b:
        b=random.randint(0,m-1)
      add=True
    else:    
      distance(a,b)
      add=False
  return None
      
#write cut edge function

def cut_func():
    cut=True
    while(cut):      
      a=random.randint(0,m-1)
      b=random.randint(0,m-1)
      while a==b:
         b=random.randint(0,m-1)  
      if (((a,b) in FG.edges() ) or ((b,a) in FG.edges() )):           
         FG.remove_edge(a,b)
         if nx.is_connected(FG):
             cut=False
         else:            
             distance(a,b)
             cut=True
      else:         
         cut=True  

#calculate stationary probality function
def calc_weight():   
    weight_1=r*FG.size(weight='weight')
    weight_2=0.0
    for i in range(m):
        weight_2=weight_2+nx.shortest_path_length(FG,source=0,target=i, weight='weight')
    return weight_1+weight_2        
         
#print nx.edge_connectivity(FG, 4,0)
         
#the function checks if the graph can be cut // if it cannot, meaning we can only add an edge
def check_min():
  minmum=True
  for a, b in FG.edges():
     FG.remove_edge(a,b)
     if nx.is_connected(FG):
        minmum=False
     distance(a,b)
  return minmum

#define function that counts the edges cannot be cut
def check_nocut():
    nocut=0
    for (a, b) in FG.edges():
        FG.remove_edge(a,b)
        if nx.is_connected(FG):
            pass
        else:
            nocut=nocut+1
        distance(a, b)
    return nocut

#main loop

i=0
#initial theta
tmp=calc_weight()
while i<istep:
   #cannot cut case
   #propprob=proposal probaility q(j|i)
   #propprob_2=q(i|j)
  FT=nx.Graph(FG)
  if check_min()==True:
    #store current graph as ft   
    prop_prob = 1.0/(m*(m-1)/2.0-1.0*FG.number_of_edges())
    add_func()
    if FG.number_of_edges()==m*(m-1)/2:
        prop_prob_2 = 1.0/(FG.number_of_edges())
    else:
        prop_prob_2 = 0.5*1.0/(FG.number_of_edges())
   
    
    
    
   #cannot add case
  elif FG.number_of_edges()==m*(m-1)/2:
    prop_prob = 1.0/(m*(m-1)/2.0)
    cut_func()
    if check_min()==True:       
        prop_prob_2 = 1.0
    else:
        prop_prob_2 = 0.5*1.0
        
    
   #choose add cut randomly
  else:
    a=random.randint(0,1)
    if a==1:
        prop_prob = 0.5*1.0/(m*(m-1)/2.0-1.0*FG.number_of_edges())
        add_func()
        if FG.number_of_edges()==m*(m-1)/2:
            prop_prob_2 = 1.0/(FG.number_of_edges())
        else:
            prop_prob_2 = 0.5*1.0/(FG.number_of_edges())
    else:
        totaledge = FG.number_of_edges()
        prop_prob = 0.5*1.0/(totaledge-check_nocut())
        cut_func()
        if check_min()==True:       
            prop_prob_2 = 1.0/(m*(m-1)/2.0-FG.number_of_edges())
        else:
            prop_prob_2 = 0.5*1.0/(m*(m-1)/2.0-FG.number_of_edges())
        
  sta_prob = np.exp(-(calc_weight()-tmp)/T)
  rand_uni=random.random()
  if rand_uni<(min(sta_prob*prop_prob/prop_prob_2 ,1)):
        pass
  else:
        FG=nx.Graph(FT)    
  tmp=calc_weight()
  
  i=i+1
  print FG.number_of_edges()
  #output test
 # nx.draw(FG, with_labels=True)
 # plt.show()
            


labels={}
for i in range(5):
    labels[i]=str(i)
    
nx.draw(FG, with_labels=True)
plt.show()

edge_labels =dict([((u, v), d['label']) 
                   for u, v, d in FG.edges(data=True)])



plt.show()




####unit test
class Test_markov(unittest.TestCase):
     # test weights cal function
     def test_weights(self):
        self.assertEquals(cacl_weights(0.0, 1.0, 0.0, 2.0), 1.0)
    #test distance calculation
     def test_coordine(self):
         self.assertEquals(cacl_weights(xv[xrange[1],yrange[1]], yv[xrange[1],yrange[1]],xv[xrange[1],yrange[1]], yv[xrange[1],yrange[1]]),0)
    #test shortest path length
     def test_len(self):
         self.assertEqual(nx.shortest_path_length(FG,source=2,target=2, weight='weight'),0)
     def test_prop_prob(self):
         self.assertlessEqual(prop_prob, 1.0)
         
        
tests =  unittest.TestLoader().loadTestsFromTestCase(Test_markov)
unittest.TextTestRunner().run(tests)
