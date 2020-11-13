import random
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
    while self.start=="NA" or self.end=="NA":
      node=next(nodes)
      if degree[node]==1:
        self.start=node
      elif degree[node]==-1:
        self.end=node
      elif abs(degree[node])>1:
        raise ValueError("degrees should not go over 1")
    ## Add one connection between end and start node, to make ajac full eulerian cycle
    self.ajac2=self.ajac.copy() ## duplicate for idempotence
    if self.end in self.ajac2.keys():
      self.ajac2[self.end].append(self.start)
    else:
      self.ajac2[self.end]=[self.start]
    ## If the deBruijn graph is just one eulerian cycle, then pick random single node as start/end node
    ## No need to connect end to start here
    if self.start==self.end:
      self.start=node
      self.end=node
  def FindEulerianPath(self):
    ## First Eulerian Cycle
    ecycle=[self.start,self.ajac2[self.start].pop(random.choice(range(0,len(self.ajac2[self.start]))))] # return last element while deleting it from ajac list
    if self.ajac2[self.start]==[]:
      del self.ajac2[self.start]
    while self.ajac2!={}: # while there are still edges to consider
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
    while ecycle[0]!=self.start:
      ecycle=ecycle[1:]+[ecycle[1]]
    self.epath=ecycle[0:-1]
    epath=self.epath.copy()
    self.seq=epath.pop(0)
    while epath!=[]:
      self.seq+=epath.pop(0)[-1]

# import genData
# a=genData.Gendata(Z=0)
# print(a.seq)
# b=DeBruijn(a.kmers)
# b.FindEndpoint()
# b.FindEulerianPath()
# print(b.start)
# print(b.end)
# print(b.epath)
# print(b.seq)
# print(a.checkmatch(b.seq))