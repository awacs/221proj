import random
import numpy as np
import pandas as pd
from copy import deepcopy
def BEST(nparray):
  indegree=np.diag(nparray.sum(axis=1))
  np.fill_diagonal(nparray.values,0) # set diagonals to zero befor sum
  Astar=-nparray+indegree
  # choose 1st cofactor, as all i cofactor has same value
  cG=np.linalg.det(Astar.iloc[1:,1:]) 
  ## For small read lengths, can have overflow issues
  ## Cap at 10k for convenience
  if cG*max([np.math.factorial(x) for x in np.diag(Astar)-1])>10000:
    return(10000)
  else:
    res=cG*np.prod([np.math.factorial(x) for x in np.diag(Astar)-1])
    return(res)
class DeBruijn():
  def __init__(self,kmers):
    ajac={}
    ## Convert Kmer into ajacency list
    k=len(kmers[0])
    for kmer in kmers:
      if kmer[0:k-1]  not in ajac.keys():
        ajac[kmer[0:k-1]]=[kmer[1:k]]
      else:
        ajac[kmer[0:k-1]].append(kmer[1:k])
    self.ajac=ajac
  def PrintGraph(self):
    for prefix in self.ajac.keys():
      print(prefix+"->"+",".join(self.ajac[prefix]))
  def FindEndpoint(self): # find start and end point for Eulerian path
    degree={} #node:[outdegree,indegree]
    # for each element of ajacency list, populate the degree table
    for prefix in self.ajac.keys():
      if prefix not in degree.keys():
        degree[prefix]=0
      degree[prefix]+=len(self.ajac[prefix])
      for affix in self.ajac[prefix]:
        if affix not in degree.keys():
          degree[affix]=0
        degree[affix]-=1
    # iterate through degree table, find start/end node
    self.start="NA"
    self.end="NA"
    nodes=iter(degree.keys())
    try:
      while self.start=="NA" or self.end=="NA":
        node=next(nodes)
        if degree[node]==1:
          self.start=node
        elif degree[node]==-1:
          self.end=node
        elif abs(degree[node])>1:
          raise ValueError("degrees should not go over 1")
    except StopIteration: # cases exist when the graph is eulerian cycle to begin with, then pick a random node as start and end node
      self.start=node
      self.end=node
    self.ajac2=deepcopy(self.ajac) ## duplicate for idempotence
    
    if self.start!=self.end: # if start and end are different, add one edge to make eulerian cycle
      self.extraedge=True
      if self.end in self.ajac2.keys():
        self.ajac2[self.end].append(self.start)
      else:
        self.ajac2[self.end]=[self.start]
    else:
      self.extraedge=False # tracker to keep track of whether extra edge is added

  def FindEulerianPath(self):
    ## First Eulerian Cycle
    ecycle=[self.start,self.ajac2[self.start].pop(random.choice(range(0,len(self.ajac2[self.start]))))] # return last element while deleting it from ajac list
    if self.ajac2[self.start]==[]:
      del self.ajac2[self.start]
    while self.ajac2!={}: # THE RANDOM WALK
      ## if cannot go, shift the ecycle until last element has out degree
      while ecycle[-1] not in self.ajac2.keys():
        ecycle=ecycle[1:]+[ecycle[1]]
      while ecycle[-1] in self.ajac2.keys(): # keep following path
        node=ecycle[-1]
        ecycle.append(self.ajac2[node].pop(random.choice(range(0,len(self.ajac2[node])))))
        # if a node has no more outdegree, delete node from ajacacency
        if self.ajac2[node]==[]:
          del self.ajac2[node]
        # print(ecycle[0])
    # Shift back until the start lines up
    while ecycle[0]!=self.start:
      ecycle=ecycle[1:]+[ecycle[1]]
    if self.extraedge==True:
      self.epath=ecycle[0:-1] # delete the artificial edge 
    else:
      self.epath=ecycle
    epath=deepcopy(self.epath)
    self.seq=epath.pop(0) 
    while epath!=[]:
      self.seq+=epath.pop(0)[-1]
  ## BEST THEOREM IMPLEMENTATION
  def CCycle(self):
    edges = [(a, b) for a, bs in self.ajac2.items() for b in bs]
    df = pd.DataFrame(edges)
    adj_matrix = pd.crosstab(df[0], df[1])
    self.adj_matrix=adj_matrix
    return(BEST(adj_matrix))
