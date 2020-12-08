import random
class Gendata():
  def __init__(self,K=10,X=1000,Y=20,Z=0):
    ## Generate a random sequence
    seq=random.choices("AGCT",k=X)
    ## If Z not zero, insert repeat sequence Z times
    if Z!=0:
      repeat_seq=random.choices("AGCT",k=Y)
      i=0
      while i<Z:
        insert_pos=random.choice(range(1,X))
        seq=seq[0:insert_pos]+repeat_seq+seq[insert_pos:X]
        i+=1
      self.repeat=repeat_seq
    ## Kmer generation
    i=0
    kmers=[]
    while i+K<=len(seq):
      kmers.append("".join(seq[i:i+K]))
      i+=1
    self.seq="".join(seq)
    self.kmers=kmers
    
  def checkmatch(self,sequence):
    return sequence==self.seq
    