# -*- coding: utf-8 -*-
# this is a code of MCMC
########
#proposal probability 
#if the graph cannot cut any edges. The probability of adding an edge is 1. 
#if the graph cannot add any more edges. The probability of removing an edge is 1.
#otherwise. The probability of adding or removing is 0.5.
########
#to use the code, you need to specify total nodes m
#positions of these nodes in a 2d grid
#total steps, istep
#weights related parameters r, T.

import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import random
import sys
import os.path
import operator
import ast
import pylab
parent = os.path.abspath(os.path.join(os.path.dirname(__file__),'.'))
sys.path.append(parent)
from init import init_grid

#initial parameters. m nodes/grid size
m=5
#initial parameter for r
r=2.0
#total time steps
istep=2000
#temperature
T=10

#genernate a m*m 2d grid
init=init_grid(m)
init.generate() 
#pick up m points in the grid as nodes. e.g. pick up 5 nodes, node #0 (0 denotes nodes index) (0,0) (this denotes the location of the node in the 2d grid)
#and node #1 (1,2), node #2 (1,3), node #3 (3,2), node #4 (4,4)

#the values in first [] is nodes' x coordine, respectively. the values in second [] is nodes' y coordines respectively.
init.coord([0,1,1,3,4],[0,2,3,2,4])

#xrange stores node's x coord in the grid
#yrange stores node's y coord in the grid
xrange=init.xrange
yrange=init.yrange
#xv, yv are the 2d grid coordines
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
    
#generate initial graph FG
FG=nx.Graph()
#initial graph. this generate an edge between node a and node b.
for (a,b) in [(0,1), (0,2), (0,3), (0,4)]:
    distance(a, b)
#output initial graph
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
    #if edge (a,b) already exists, genre new patterns of (a,b)
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
      
#define cut edge function. we cut an edge when this function is called
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
         #if the graph is connected after cut, cut successfully.
         if nx.is_connected(FG):
             cut=False
         #if the graph is disconnected after cut, we need to try another edge
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
  #at last, if no edges in the graph cannot be cut, return minmum true.
  return minmum

#define function that counts the number of edges cannot be cut
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

###########some initialization for the main loop######

#values of all steps are stored. i can also cacluate online, but here I prefer to store all of them for analysis and verification

#initialize number of edges connected to 0
expc_edgeto0=np.zeros(istep+1, dtype=np.float64)
expc_edgeto0[0]=len(FG.neighbors(0))

#initialize edges number in the graph
expc_edges=np.zeros(istep+1, dtype=np.float64)
expc_edges[0]=FG.number_of_edges()

#intialize maximum distance of the shortest path that connects vertex 0 to another vertex
#tmp_dist is used to compare and store the value temporarily
expc_max_dist=np.zeros(istep+1, dtype=np.float64)
#loop over all edges
for j in range(m):
    tmp_dist=nx.shortest_path_length(FG,source=0,target=j, weight='weight') 
    #compare current one and previous largest one, ensure we always store the large one
    if tmp_dist>expc_max_dist[0]:
        #find the intial value for maximum distance
        expc_max_dist[0]=tmp_dist        


 
#for post processing and visulization, initialize values averaged by all steps already calculated, this is not expected value.     
#initialize edges connected to 0 average
edgeto0_avr=np.zeros(istep+1, dtype=np.float64)
edgeto0_avr[0]=expc_edgeto0[0]   

edges_avr=np.zeros(istep+1, dtype=np.float64)
edges_avr[0]=expc_edges[0]  

max_dist_avr= np.zeros(istep+1, dtype=np.float64)  
max_dist_avr[0]=expc_max_dist[0]





#calculate initial theta. tmp stores previous step theta
tmp=calc_weight()

#initialize a list to store all edges
alledges_list=[None]*0
#write the intial graph to the list as string
alledges_list.append(str(FG.edges()))
##################################


###############################
#main loop, starts form i=1
i=1
while i<=istep:    
  #store current graph as FT 
  FT=nx.Graph(FG)
  #by checki_min function, we know this is the 'cannot cut' case
  if check_min()==True:  
    #propprob=proposal probability q(j|i)
    #propprob_2=q(i|j)
    #now calculate(p(j|i)), which equals 1 divided by (all possible edges - edges already exist)
    prop_prob = 1.0/(m*(m-1)/2.0-1.0*FG.number_of_edges())
    #add an edge
    add_func()
    #calculate p(i|j)
    #if the graph is 'cannot add case', p(i|j)=1/current edge numbers
    prop_prob_2 = 1.0/(FG.number_of_edges())
    #otherwise, p(i|j)=0.5 (due to add/cut randomly) *1/current edge numbers
    if FG.number_of_edges()!=m*(m-1)/2:
        prop_prob_2 = 0.5*1.0/(FG.number_of_edges())
     
    
  #cannot add case. we can only remove an edge in the graph because all pairs are connected
  elif FG.number_of_edges()==m*(m-1)/2:
    #calculate(p(j|i))
    prop_prob = 1.0/(m*(m-1)/2.0)
    #cut an edge
    cut_func()
    #calculate p(i|j)
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
        #calculate p(j|i), which equals 1 divided by (all possible edges - edges already exist)
        prop_prob = 0.5/(m*(m-1)/2.0-1.0*FG.number_of_edges())
        #add an edge
        add_func()
        #calculate p(i|j)
        #if it's cannot add case, we can only cut. p(i|j)=1/number of edges exist
        prop_prob_2 = 1.0/(FG.number_of_edges())
        #if it can be cut or add, 0.5 need to be mutiplied
        if FG.number_of_edges()!=m*(m-1)/2:
            prop_prob_2 = 0.5/(FG.number_of_edges())
    #if a==0, cut an edge
    else:
        #calculate p(j|i), which equals 0.5 divided by (number of exist edges - edges cannot be cut)
        prop_prob = 0.5/(FG.number_of_edges()-check_nocut())
        #cut an edge
        cut_func()
        #calculate p(i|j)
        #if it's cannot cut case, we can only add an edge in this graph
        if check_min()==True:       
            prop_prob_2 = 1.0/(m*(m-1)/2.0-FG.number_of_edges())
        #otherwise, 0,5 need to be multiplied
        else:
            prop_prob_2 = 0.5/(m*(m-1)/2.0-FG.number_of_edges())
  #calculate stationary probaility
  sta_prob = np.exp(-(calc_weight()-tmp)/T)
  #generate a random number rand_uni between 0,1
  rand_uni=random.random()
  #if rand_uni<pi_j*q(i|j)/(pi_i*q(j|i)), accept it
  if rand_uni<(min(sta_prob*prop_prob_2/prop_prob ,1)):
        pass
  #otherwise, use the previous one
  else:
        FG=nx.Graph(FT) 
        
  #store previous theta
  tmp=calc_weight()
  #calculate the edges connected to 0
  expc_edgeto0[i]=len(FG.neighbors(0))
  #calculate the number of edges 
  expc_edges[i]=FG.number_of_edges()
  #calculate maximim distance
  for j in range(m):
    tmp_dist=nx.shortest_path_length(FG,source=0,target=j, weight='weight')    
    #compare current one and previous largest one, ensure we always store the larger one
    if tmp_dist>expc_max_dist[i]:
        #find the intial value for maximum distance
        expc_max_dist[i]=tmp_dist
            
  #most possible graph calculation, append all graphs' list info to the list 
  alledges_list.append(str(FG.edges()))
  
  #calcuate averaged number of edges connected to vertex 0
  edgeto0_avr[i]=np.average(expc_edgeto0[0:i])
  #calculate averaged edges number
  edges_avr[i]=np.average(expc_edges[0:i])
  #calculate averaged maximum distance 
  max_dist_avr[i]=np.average(expc_max_dist[0:i])
  
  #step increment
  i+=1

##########
#end of main loop


###########
#calculate expected edges
#store all values in steady state (assume steday after istep/2) in other arrays
expc_edgeto0_stat=expc_edgeto0[istep/2: istep+1]
expc_edges_stat=expc_edges[istep/2: istep+1]
expc_max_dist_stat=expc_max_dist[istep/2:istep+1]
#calculate average
#this is expected number of edges connected to vertex 0
expc_edgeto0_avr=np.average(expc_edgeto0_stat)
#this is expected edges number in the graph 
expc_edges_avr=np.average(expc_edges_stat)
#this is expected maximum distance 
expc_max_dist_avr=np.average(expc_max_dist_stat)



#find the most probable graph <thanks to xinyang li's idea>
#intialize a dictionary for counting later
hist={}
for edge in alledges_list:
    #if alread in the dictionary, add 1
    if edge in hist:
        hist[edge]+=1
    #otherwise, record it
    else:
        hist[edge]=1
#sorted the dictionary
hist_sort=sorted(hist.items(), key=operator.itemgetter(1), reverse=True)
#convert to edges list and pick the top one
high_freq_edge = ast.literal_eval(hist_sort[0][0])

#recover this most  graph
for (a,b) in high_freq_edge:
    distance(a, b)
#plot the most probable graph  
nx.draw(FG, with_labels=True)
plt.show()

#output average figure
plt.plot(edgeto0_avr, label='edges connected to 0')
plt.plot(edges_avr, label='total edges')
plt.plot(max_dist_avr, label='maximum distance')
pylab.legend(loc='best')
plt.title('average values')
plt.xlabel('time step')
plt.show()