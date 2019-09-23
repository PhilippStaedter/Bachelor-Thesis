# execute simulation script with all LINEAR SOLVERS

######################################################################################
# very important: linSol, nonLinSolIter, solAlg must be their corresponding integers #
#                                                                                    #
# linSol:           Dense == 1  GMRES == 6  BiCGStab == 7   SPTFQMR == 8    KLU == 9 #
# nonLinSolIter:    Functional == 1     Newton-type == 2                             #
# solAlg:           Adams == 1      BDF == 2                                         #
#                                                                                    #
######################################################################################

from SimAllSettings import *
from tqdm import trange

# settings
atol = [1e-12, 1e-10, 1e-8, 1e-16]                   # add 2 - 4 different interesting tolerance combinations from study 'Tolerances'
rtol = [1e-10, 1e-14, 1e-6, 1e-8]
linSol = [1, 6, 7, 8, 9]
solAlg = 2


for iLinSol in trange(0, len(linSol)):
    for iToleranceGroup in trange(0, len(atol)):
        simulate(atol[iToleranceGroup], rtol[iToleranceGroup], linSol[iLinSol], solAlg)
        useless_variable = os.system('clear')
        pass