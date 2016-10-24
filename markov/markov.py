# -*- coding: utf-8 -*-
# this is a code of MCMC
########
#proposal probality 
#if the graph cannot cut any edges. The probality of adding an edge is 1. 
#if the graph cannot add any more edges. The probality of removing an edge is 1.
#otherwise. The probality of adding or removing is 0.5.
########
#to use the code, you need to specify total nodes m
#positions of these nodes in a 2d grid
#total steps, istep
#weights realted paramters r, T.

import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import unittest
import random
from init import init_grid

#intial parameters. m nodes/grid size
m=5
#initial parameter for r
r=2.0
#total time steps
istep=500
#temperature
T=10



class calc_distance(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def distance(self, a_xcoord, a_ycoord, b_xcoord, b_ycoord):
        self.dist=np.sqrt((a_xcoord-b_xcoord)**2+(a_ycoord-b_ycoord)**2)
        FG.add_weighted_edges_from([(self.a,self.b,self.dist)],label=str(self.dist))
    
       
#genernate a m*m 2d grid
init=init_grid(m)
init.generate() 
#pick up m points in the grid as nodes. e.g. #0 (0,0) #1 (1,2) #2 (1,3) #3 (3,2) #4 (4,4)
init.coord([0,1,1,3,4],[0,2,3,2,4])
#xrange denotes node's x index in the grid
#yrange denotes node's y index in the grid
xrange=init.xrange
yrange=init.yrange
#xv, yv are the grid coordines
xv=init.xv
yv=init.yv


#define weights function. the function can calculate two points distance when given coordinates
#x_1,y_1, x_2,y_2 are x,y coordintes of two points
def cacl_weights(x_1, y_1, x_2, y_2):
    return np.sqrt((x_1-x_2)**2+(y_1-y_2)**2)
    
#define add edge function. add a weighted edge from nodes a and b
def distance(a, b):
    dist=cacl_weights(xv[xrange[a],yrange[a]], yv[xrange[a],yrange[a]],xv[xrange[b],yrange[b]], yv[xrange[b],yrange[b]])
    FG.add_weighted_edges_from([(a,b,dist)],label=str(dist))
    return None
    
#genereate intial graph FG
FG=nx.Graph()
#initial graph. this generete an edge between node a and node b. a, b denotes the index of different points
for (a,b) in [(0,1), (0,2), (0,3), (0,4)]:
    distance(a, b)
#output inital graph
nx.draw(FG, with_labels=True)
plt.show()

#define add edge function. we add an edge to the graph when this function is called
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
    else:    
      #if edge (a,b) not exist, add edge(a,b)
      distance(a,b)
      add=False
  return None
      
#define cut edge function. we cut an edge whenthis function is called
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
         #if the graph is connectted after cut, cut sucessfully.
         if nx.is_connected(FG):
             cut=False
         #if the graph is disconnectted after cut, we need to try another edge
         else:   
             #restore the graph
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


#####################main loop, starts form i=0
i=1
#iniital expected number of edges connected to 0
expc_edgeto0=len(FG.neighbors(0))
#initialexpected edges number
expc_edges=1.0*FG.number_of_edges()
#calculate initial theta. tmp stores last step theta
tmp=calc_weight()
while i<istep:
    
  #store current graph as FT 
  FT=nx.Graph(FG)
  #by checki_min function, we know this is the 'cannot cut' case
  if check_min()==True:  
    #propprob=proposal probaility q(j|i)
    #propprob_2=q(i|j)
    #now calculate(p(j|i))
    prop_prob = 1.0/(m*(m-1)/2.0-1.0*FG.number_of_edges())
    #add an edge
    add_func()
    #caclulate p(i|j)
    #if the graph is 'cannot add case', p(i|j)=1/current edge numbers
    prop_prob_2 = 1.0/(FG.number_of_edges())
    #otherwise, p(i|j)=0.5 (due to add/cut randomly) *1/current edge numbers
    if FG.number_of_edges()!=m*(m-1)/2:
        prop_prob_2 = 0.5*1.0/(FG.number_of_edges())
     
    
  #cannot add case. we can only remove an edge
  elif FG.number_of_edges()==m*(m-1)/2:
    #calculate(p(j|i))
    prop_prob = 1.0/(m*(m-1)/2.0)
    #cut an edge
    cut_func()
    #if the graph is 'cannot cut case', p(i|j)=1
    prop_prob_2=1.0
    #otherwise, we can add or cut. p(i|j)=0.5*1
    if check_min()==False:       
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
        #if it's cannot add case
        prop_prob_2 = 1.0/(FG.number_of_edges())
        #if it can be cut or add, 0.5 need to be mutiplied
        if FG.number_of_edges()!=m*(m-1)/2:
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
 # nx.draw(FG, with_labels=True)
 # plt.show()
  #print FG.number_of_edges()
  #cacluate the edges connected to 0 over all graphs
  expc_edgeto0=expc_edgeto0+len(FG.neighbors(0))
  #cacluate the sum of edges over all graphs
  expc_edges=expc_edges+1.0*FG.number_of_edges()


##########end of main loop




#calculate edges connected to 0 by averaging over all graphs
expc_edgeto0=expc_edgeto0/i
#calculate the expected edges number by averaging over all graphs
expc_edges=expc_edges/i
labels={}
for i in range(5):
    labels[i]=str(i)

#output final graph  
nx.draw(FG, with_labels=True)
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
  
         
        
tests =  unittest.TestLoader().loadTestsFromTestCase(Test_markov)
unittest.TextTestRunner().run(tests)
