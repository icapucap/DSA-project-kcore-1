from helper import core_number,Graph
def build_network(ppi_file):
    with open(ppi_file, "r") as ppi:
        PPInetwork = Graph()
        for interaction in ppi:
            nodes = interaction.rstrip("\n").split("\t")
            PPInetwork.add_edge(nodes[0], nodes[1])
    return PPInetwork

def find_kcores(ppi_file):
    kcores = {}          
    highestkcore =0  

    PPInetwork = build_network(ppi_file)        
    protein_cores = core_number(PPInetwork)   
    for protein, kcore in protein_cores.items():
        if highestkcore < kcore: 
            highestkcore = kcore
        if kcore in kcores:
            kcores[kcore].append(protein)
        else:
            kcores[kcore]=[protein]
    return highestkcore,kcores

ppi_file = 'TestfilesforPPI/GRIDforhuman.txt' 
highestkcore,kcores = find_kcores(ppi_file) 

print("The highest k-core is a {0}-core and there are {1} proteins. \n"
      "The proteins are: {2}".format(highestkcore,len(kcores[highestkcore]),kcores[highestkcore]))


