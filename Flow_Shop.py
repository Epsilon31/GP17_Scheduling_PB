#!/usr/bin/env python
# coding: utf-8

# # Scheduling problem in Flow shop situation
# 

# ThThe objective of this session is to explore how to apply several heuristics to flow shop problems using python.
# 
# **Flow shop with 2 machines**
# 
# Hypotheses of this problem : 
# 
# n = 6 (number of tasks)
# 
# m = 2 (number of machines)
# 
# Preemptive tasks are not allowed
# 
# Each machine must perform tasks one by one.
# 
# 

# In[32]:


P = [[9,3],[5,12],[16,9],[11,2],[7,15],[4,18]] #Matrix of processing times 
n= 6
m=2


# **Johnson Rule**

# In[13]:


S_Beg = []
S_End = []
def Johnson_sort(P,S_Beg,S_End):
   

    for i in range(len(P)):
        if P[i][0] < P[i][1]:
            S_Beg.append(i)
        else:
            S_End.append(i)
    return S_Beg, S_End
    
    """ P : Matrix of processing times
       S_Beg : List of tasks whose processing time is shorter on the first machine
       S_End : List of tasks whose processing time is longer on the first machine than on the second machine """


# In[14]:


S_Beg, S_End = Johnson_sort(P,S_Beg,S_End)


# In[15]:


print(S_Beg)
print(S_End)


# In[18]:


S_Beg = sorted(S_Beg, key = lambda i : P[i][0], reverse = False) # Sort S_Beg by increasing processing times
print(S_Beg)


# In[20]:


S_End = sorted(S_End, key= lambda i : P[i][1], reverse = True) # Sort _ S_End by decreasing processing times
print(S_End)


# In[101]:


S = S_Beg + S_End # Final sequence 
print(S)


# In[102]:


def Johnson_Rule(P,n,m):
    S_Beg = []
    S_End = []
    S = []
    S_Beg,S_End = Johnson_sort(P,S_Beg,S_End)
    S_Beg = sorted(S_Beg, key = lambda i : P[i][0], reverse = False)
    S_End = sorted(S_End, key= lambda i : P[i][1], reverse = True)
    S = S_Beg + S_End
    return S
    


# **Calculate Cmax**

# In[23]:


def Cmax(S,n,m,P):
    C = [] # Empty list C
    for i in range(0,n):
        C.append([]) # Create a new list in the list C for each task
        for j in range(0,m):
            C[i].append([]) # Create a new list int he list i of the list C for each machine
    for i in range(0,n):
        for j in range(0,m):
            if i ==0: # First task
                if j == 0: # First machin
                    C[i][j] = P[S[i]][j]  # At the beginning of the production, the completion time is equal to the processing time of the first task in the sequence
                else: 
                    C[i][j] = C[i][j-1] + P[S[i]][j] # Then to calculate the completion time, we sum the previous processing times
            elif j == 0: #Première machine
                C[i][j] = C[i-1][j] + P[S[i]][j]
            else: #Cas général
                C[i][j] = max(C[i-1][j],C[i][j-1]) + P[S[i]][j]
    return C[n-1][m-1]


# In[34]:


Cmax_Johnson = Cmax(S,n,m,P)
print(Cmax_Johnson)


# **Flow shop with several machines**

# In[43]:


n = 4
m = 3
P=[[5,2,1],[2,3,4],[4,7,9],[9,4,3]] 


# **Palmer Heuristic**
# 

# In[47]:


def Palmer_Heuristic(P,n,m):
    S = [i for i in range(n)]
    SP = [0]*n
    
    for i in range(n):
        for j in range(m):
            SP[i] += (2*(j+1) - (m+1))*P[i][j] # The range function finish at m-1 ! 
    return sorted(S, key = lambda i : SP[i], reverse = True)


# In[48]:


S_Palmer = Palmer_Heuristic(P,n,m)
print(S_Palmer)


# In[96]:


Cmax_Palmer = Cmax(S_Palmer,n,m,P)


# **Gupta Heuristic**
# 

# In[58]:


def binary(P,j,m):
    ej = -1
    if P[j][0] < P[j][m-1]:
        ej = 1
    return ej
    


# In[59]:


def Gupta(P,n,m):
    S = [i for i in range(n)]
    S_Gupta = [0]*n
    Min = []
    for i in range(n):
        Min.clear()
        for j in range(m-1):
            Min.append(P[i][j] + P[i][j+1])
        minimum = min(Min)
        S_Gupta[i] = binary(P,i,m)/minimum
    return sorted(S, key = lambda i : S_Gupta[i], reverse = True)


# In[61]:


S_Gupta = Gupta(P,n,m)


# In[95]:


Cmax_Gupta = Cmax(S_Gupta,n,m,P)


# **NEH**

# In[89]:


def Sorted(n,m,P):
    S = [i for i in range(n)]
    return sorted(S, key = lambda i : sum(P[i]),reverse = True)


# In[90]:


def NEH(S,n,m):
    R=[]
    R.append(S[0])
    del(S[0])
    for j in range(0,len(S)):
        LR = []
        Cmax_LR = 0
        for k in range(0,len(R)+1):
            R_jk = R.copy()
            R_jk.insert(k,S[j])
            LR.append(R_jk)
            Cmax_LR_C = Cmax(R_jk,len(R_jk),m,P)
            if Cmax_LR_C <= Cmax_LR:
                Cmax_LR = Cmax(R_jk,len(R_jk),m,P)
        R = LR[k].copy()
    return R
                    


# **Etapes** : 
# - Créer la liste S des tâches triées dans l'ordre y en  utilisant la fonction sorted
# - Affecter la tâche S[0] comme premier élément d'une liste R qui contiendra la séquence finale
# - Pour chaque tâche j de S : 
#     - Créer une liste LR vide qui contiendra les permutations.
#     - Pour chaque k de 1 à len(R)
#         - Créer la liste R_jk à partir de R
#         - Insérer la tâche j à la position k dans R_jk en utilisant la fonction insert(k,j)
#         - Insérer R_jk dans LR en utilisant append
#     - Récupérer la meilleur permutation de LR selon son Cmax et l'affecter à R
#     

# In[91]:


S = Sorted(n,m,P)


# In[92]:


S_NEH = NEH(S,n,m)
print(S_NEH)


# In[94]:


Cmax_NEH = Cmax(S_NEH,n,m,P)


# **CDS**

# In[136]:


def CDS(n,m,P):
    LS = []
    C = []
    pDeriv = [[0 for i in range(2)] for i in range(n)]
    for j in range(0,m):
        for k in range(n):
            for i in range(j):
                pDeriv[k][0] += P[k][i]
                pDeriv[k][1] += P[k][m-j]
        LS.append(Johnson_Rule(pDeriv,n,m))
        C.append(Cmax(LS[j],n,m,P))
    
    
    
    return LS[C.index(min(C))],min(C)
    #return sorted(LS, key = lambda i : C[i], reverse = False)
    
            
        
        


# In[138]:


S,Cmax_CDS = CDS(n,m,P)
print(S)
print(Cmax_CDS)


# In[139]:


C = [Cmax_CDS,Cmax_Gupta,Cmax_NEH,Cmax_Palmer]


# In[142]:


print(C.index(min(C)))
print(min(C))


# La meilleure solution est donc CDS !

# In[111]:





# In[112]:





# In[ ]:




