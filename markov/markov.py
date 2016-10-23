# -*- coding: utf-8 -*-
# this is a code of MCMC
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import unittest
import random
import sys

#generate 2d grid
#intial parameters. m nodes
m=5
#initial parameter for r
r=2.0
#total time steps
istep=200
#temperature
T=10

#generate 2D grid, dx=dy=1
nxx, nyy = (m,m)
x = np.linspace(0, m-1, nxx)
y = np.linspace(0, m-1, nyy)
xv, yv = np.meshgrid(x, y)

#pick up 5 points in the grid as nodes. e.g. #0 (0,0) #1 (1,2) #2 (1,3) #3 (3,2) #4 (4,4)
xrange=[0, 1, 1, 3, 4]
yrange=[0, 2, 3, 2, 4]

#define weights function. the function can calculate two points distance when given coordinates
def cacl_weights(x_1, y_1, x_2, y_2):
    return np.sqrt((x_1-x_2)**2+(y_1-y_2)**2)
    
#define add edge function. add a weighted edge from nodes a and b
def distance(a, b):
    dist=cacl_weights(xv[xrange[a],yrange[a]], yv[xrange[a],yrange[a]],xv[xrange[b],yrange[b]], yv[xrange[b],yrange[b]])
    FG.add_weighted_edges_from([(a,b,dist)],label=str(dist))
    return None
    
#genereate intial graph FG
FG=nx.Graph()
#this generete an edge between node a and node b,a, b denotes the index of different points
a=0
b=1
distance(a, b)
a=0
b=2
distance(a, b)
a=0
b=3
distance(a, b)
a=0
b=4
distance(a, b)
a=1
b=4
distance(a, b)
a=1
b=3
distance(a, b)
a=1
b=2
distance(a, b)
a=2
b=4
distance(a, b)
a=2
b=3
distance(a, b)
a=3
b=4
distance(a, b)

#print FG.number_of_edges()

nx.draw(FG, with_labels=True)
plt.show()

#output inital graph


#proposal probality 
#if the graph cannot cut any edges. The probality of adding an edge is 1. 
#if the graph cannot add any more edges. The probality of removing an edge is 1.
#otherwise. The probality of adding or removing is 0.5.

#define add edge function
def add_func(): 
  add=True
  #pick 2 nodes randomly, make sure a not equal b
  a=random.randint(0,m-1)
  b=random.randint(0,m-1)
  while a==b:
    b=random.randint(0,m-1)
  while(add):   
    #if edge (a,b) already exists, genrete new patterns of (a,b)
    if (((a,b) in FG.edges() ) or ((b,a) in FG.edges() )):
      a=random.randint(0,m-1)
      b=random.randint(0,m-1)
      while a==b:
        b=random.randint(0,m-1)
      add=True
     #if edge (a,b) not exist, add edge(a,b)
    else:    
      distance(a,b)
      add=False
  return None
      
#define cut edge function
def cut_func():
    cut=True
    #pick 2 nodes randomly, make sure a not equal b
    while(cut):      
      a=random.randint(0,m-1)
      b=random.randint(0,m-1)
      while a==b:
         b=random.randint(0,m-1)  
    #if (a,b) already exists, we can try to cut it
      if (((a,b) in FG.edges() ) or ((b,a) in FG.edges() )):           
         FG.remove_edge(a,b)
         #if the graph is disconnectted after cut, we need to try another edge
         if nx.is_connected(FG):
             cut=False
         else:            
             distance(a,b)
             cut=True
      else:         
         cut=True  

#define theta calculation function
def calc_weight():   
    #first part of theta
    weight_1=r*FG.size(weight='weight')
    #second part of theta
    weight_2=0.0
    for i in range(m):
        weight_2=weight_2+nx.shortest_path_length(FG,source=0,target=i, weight='weight')
    return weight_1+weight_2        
         

         
#the function checks if the graph can be cut // if it cannot, meaning we can only add an edge
def check_min():
  minmum=True
  #test edges in the graph one by one and remove it. 
  for a, b in FG.edges():
     FG.remove_edge(a,b)
     #if remove any edges make the graph disconnected, it's 'cannot remove case/minimum case'
     if nx.is_connected(FG):
        minmum=False
     #recover the graph by adding the removed edge back
     distance(a,b)
  return minmum

#define function that counts the edges cannot be cut
def check_nocut():
    #nocut denotes the number of edges cannot be cut
    nocut=0
    #loop over all edges
    for (a, b) in FG.edges():
        #try to remove the edge
        FG.remove_edge(a,b)
        #if still connected, pass
        if nx.is_connected(FG):
            pass
        #if disconcected, the number of edges cannot be cut is added by 1
        else:
            nocut=nocut+1
        #recover the graph by adding the removed edge back
        distance(a, b)
    return nocut


#main loop
i=0
#calculate initial theta. tmp stores last step theta
tmp=calc_weight()
while i<istep:
    
  #store current graph as ft  
  FT=nx.Graph(FG)
  #by checki_min function, we know this is the 'cannot cut' case
  if check_min()==True:
    #store current graph as ft   
    #propprob=proposal probaility q(j|i)
    #propprob_2=q(i|j)
    #calculate(p(j|i))
    prop_prob = 1.0/(m*(m-1)/2.0-1.0*FG.number_of_edges())
    #add an edge
    add_func()
    #caclulate p(i|j)
    #if the graph is 'cannot add case', p(i|j)=1/current edge numbers
    if FG.number_of_edges()==m*(m-1)/2:
        prop_prob_2 = 1.0/(FG.number_of_edges())
    #otherwise, p(i|j)=0.5 (due to add/cut randomly) *1/current edge numbers
    else:
        prop_prob_2 = 0.5*1.0/(FG.number_of_edges())
   
    
    
    
   #cannot add case
  elif FG.number_of_edges()==m*(m-1)/2:
    #calculate(p(j|i))
    prop_prob = 1.0/(m*(m-1)/2.0)
    #cut an edge
    cut_func()
    #if the graph is 'cannot cut case', p(i|j)=1
    if check_min()==True:       
        prop_prob_2 = 1.0
    #otherwise, we can add or cut. p(i|j)=0.5*1
    else:
        prop_prob_2 = 0.5*1.0
        
    
   #for normal cases, choose add/cut randomly
  else:
    #generate random number 
    a=random.randint(0,1)
    #if a==1, add an edge
    if a==1:
        #calculate p(j|i)
        prop_prob = 0.5*1.0/(m*(m-1)/2.0-1.0*FG.number_of_edges())
        add_func()
        #calculate p(i|j)
        if FG.number_of_edges()==m*(m-1)/2:
            prop_prob_2 = 1.0/(FG.number_of_edges())
        else:
            prop_prob_2 = 0.5*1.0/(FG.number_of_edges())
    #if a==0, cut an edge
    else:
        #total edge is the number of all edges
        totaledge = FG.number_of_edges()
        #calculate p(j|i)
        prop_prob = 0.5*1.0/(totaledge-check_nocut())
        #cut an edge
        cut_func()
        #calculate p(i|j)
        if check_min()==True:       
            prop_prob_2 = 1.0/(m*(m-1)/2.0-FG.number_of_edges())
        else:
            prop_prob_2 = 0.5*1.0/(m*(m-1)/2.0-FG.number_of_edges())
  #calculate stationary probaility
  sta_prob = np.exp(-(calc_weight()-tmp)/T)
  #generate a random number rand_uni between 0,1
  rand_uni=random.random()
  #if rand_uni<pi_j*q(i|j)/(pi_i*q(j|i)), accept it
  if rand_uni<(min(sta_prob*prop_prob_2/prop_prob ,1)):
        pass
  #otherwise, use the old one
  else:
        FG=nx.Graph(FT) 
  #store previous theta
  tmp=calc_weight()
  #step increment
  i=i+1
  #print FG.number_of_edges()


labels={}
for i in range(5):
    labels[i]=str(i)
    
nx.draw(FG, with_labels=True)
plt.show()
#output final graph



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
         self.assertLessEqual(prop_prob, 1.0)
         
        
tests =  unittest.TestLoader().loadTestsFromTestCase(Test_markov)
unittest.TextTestRunner().run(tests)
