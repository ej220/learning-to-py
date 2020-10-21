import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.constants import R as R
from scipy import optimize
import datetime as dt

def __ODEErrorFunc__(Ks, ReacPs, Yields, Proxanal, steps):
    error = []
    
    AQ_Exp = Yields[:,2]
    BC_Exp = Yields[:,0]
    GAS_Exp = Yields[:,3]
    
    Prot = Proxanal[:,2]
    Carb = Proxanal[:,0]
    Lipd = Proxanal[:,1]
    
    T_Exp = ReacPs[:,1]
    tf = ReacPs[:,0]
    
    for i in range(len(AQ_Exp)):
        AQ_test = AQ_Exp[i]
        BC_test = BC_Exp[i]
        GAS_test = GAS_Exp[i]
    
        Prot_test = Prot[i]
        Carb_test = Carb[i]
        Lipd_test = Lipd[i]
    
        T_test = T_Exp[i]
        tf_test = tf[i]
        
        args = tuple([AQ_test,BC_test,GAS_test,Prot_test,Carb_test,Lipd_test,T_test,tf_test,steps])
        
        er_return = __HTLODESolver__(Ks,args)
        
        
        error.append(er_return[0])
        error.append(er_return[1])
        error.append(er_return[2])
    
    SSE = 0
    for i in error:
        SSE += i**2
    
    RMSE = np.sqrt(SSE/len(error))
    
    #print(f"SSE: {SSE:.3e}, RMSE: {RMSE:.3e}")
    SSE_log.append(SSE)
    RMSE_log.append(RMSE)

    return error

def __HTLODESolver__(Ks, args):
    
# This script uses the Euler method to estimate a numerical solution to the set of ODEs
# proposed by Sheehan and Savage (2017), which describe the bulk reaction kinetics for
# Algal species under HTL conditions.

# Read the input arguments to the function
    #AQ_Exp = Yields[:,2]
    #BC_Exp = Yields[:,0]
    #GAS_Exp = Yields[:,3]
    
    #Prot = Proxanal[:,2]
    #Carb = Proxanal[:,0]
    #Lipd = Proxanal[:,1]
    
    #T_Exp = ReacPs[:,1]
    #tf = ReacPs[:,0]
    
    AQ_Exp = args[0]
    BC_Exp = args[1]
    GAS_Exp = args[2]
    
    Prot = args[3]
    Carb = args[4]
    Lipd = args[5]
    
    T_Exp = args[6]
    tf = args[7]
    steps = args[8]

# Set-up ODE method parameters

    t = 0                # Starting time for reaction
    tf = tf              # Reaction final time (minutes), for flow reactors set-this as mean residence time
    steps = steps        # Number of steps to take for the ODE estimation
    dt = tf / steps      # Step-size
    T = T_Exp + 273.15   # Isothermal reaction temp (Kelvin)



# Input the initial values for the t=0 boundary condition

    x0 = [Prot,     # Protein, daf wt. %
          Carb,     # Carbohydrate, daf wt. %
          Lipd,     # Lipid, daf wt%
          0,        # Aqueous phase, wt. %
          0,        # Bio-crude, wt. %
          0,        # Gas phase, wt. %
          100]      # Total solids, wt. %

    xt = x0         # xt is the array of values at time=t



# Input Arrhenius parameters for HTL of algale species,
# for each key, values represent log_10[A_i] (1/min), and E_a (kJ/mol)

    k_params = {"1,p" : [ Ks[0], 53.3],
                "1,c" : [ Ks[1], 57.9],
                "1,l" : [ Ks[2], 57.6],
                "2,p" : [ Ks[3], 51.9],
                "2,c" : [ Ks[4], 78.6],
                "2,l" : [ Ks[5], 65.8],
                "3"   : [ Ks[6], 65.6],
                "4"   : [ Ks[7], 66.2],
                "5"   : [ Ks[8],  142],
                "6"   : [ Ks[9], 89.8]
               }



# Set up and empty dictionary and compute individual k-values
# (rate constant) for the given reaction conditions

    k = {}
    for i in k_params.keys():
        logA = k_params[i][0]
        Ea = k_params[i][1]
        k[i] = (10**(logA))*np.exp(-Ea/(R*T/1000))
    
    


# Initialise an empty Pandas DataFrame and commence iteration through time-steps
    
    xHist = pd.DataFrame()
    for step in range(steps):
        
    ## Copy current values from xt into the 'xHist' DataFrame
    #    xHist.loc[t,"timestep"] = t
    #    for i in range(len(xt)):
    #        xHist.loc[t,f"tag_{i}"] = xt[i]
    
    # Determine gradient for each x at current t
        dxProtDt = -(k["1,p"] + k["2,p"]) * xt[0]
        
        
        dxCarbDt = -(k["1,c"] + k["2,c"]) * xt[1]
        
        
        dxLipdDt = -(k["1,l"] + k["2,l"]) * xt[2]
        
        
        dxAqDt = (-(k["4"]+k["5"])*xt[3])+(k["1,p"]*xt[0])+(k["1,c"]*xt[1])+(k["1,l"]*xt[2])+(k["3"]*xt[4])
         
        
        dxBcDt = (-(k["3"]+k["6"])*xt[4])+(k["2,p"]*xt[0])+(k["2,c"]*xt[1])+(k["2,l"]*xt[2])+(k["4"]*xt[3])
        
        
        dxGasDt = k["5"]*xt[3] + k["6"]*xt[4]
        
    
    # Estimate current x based on projecting gradient and timestep from previous x
        xt[0] += dt*dxProtDt
        xt[1] += dt*dxCarbDt
        xt[2] += dt*dxLipdDt
        xt[3] += dt*dxAqDt
        xt[4] += dt*dxBcDt
        xt[5] += dt*dxGasDt
        xt[6] = xt[0] + xt[1] + xt[2]
        
    # Increment time-step
        t += dt
    
    AQ_pred  = xt[3]#xHist.loc[tf, "tag_3"]
    BC_pred  = xt[4]#xHist.loc[tf, "tag_4"]
    GAS_pred = xt[5]#xHist.loc[tf, "tag_5"]
    
    AQ_err  = (AQ_Exp - AQ_pred)  /AQ_Exp
    BC_err  = (BC_Exp - BC_pred)  /BC_Exp
    GAS_err = (GAS_Exp - GAS_pred) /GAS_Exp
    
    error = np.column_stack((AQ_err, BC_err, GAS_err)).flatten()
    return error
    
StartTime = dt.datetime.now()

SSE_log, RMSE_log = [],[]

df = pd.read_csv("MacroODE.csv")
df.dropna(inplace=True)

ReacPs   = df.loc[:,"t (min)":"T (K)"].to_numpy(dtype=np.float64) 
Yields   = df.loc[:,"EXP_BC_daf":"EXP_GAS_DAF"].to_numpy(dtype=np.float64) 
Proxanal = df.loc[:,"Carb (daf wt. %)":"Prot (daf wt. %)"].to_numpy(dtype=np.float64) 

K0 =[5.37,
     4.15,
     4.52,
     5.29,
     5.25,
     5.32,
     3.41,
     3.52,
     3.36,
     4.63]

K0 = np.array(K0, dtype=np.float64)

steps = 10

result = optimize.least_squares(__ODEErrorFunc__, K0, args=(ReacPs, Yields, Proxanal, steps), bounds=(0,10), ftol=1e-6, verbose=2)

delta = dt.datetime.now() - StartTime

print(f"\nCalculation complete!\n\nTotal time taken: {delta}\n\n    Number of function evalutions to reach convergence: {result.nfev}\n    Time taken per function evaluation: {delta/result.nfev}")

df2 = pd.DataFrame()
for i in range(len(SSE_log)):
    df2.loc[i,"Step"] = i
    df2.loc[i,"SSE"] = SSE_log[i]
    df2.loc[i,"RMSE"] = RMSE_log[i]
    

f, (ax1, ax2) = plt.subplots(1,2, figsize =(30, 10))

sns.scatterplot(x="Step", y="SSE", data=df2, ax=ax1)   
ax1.set_xlabel('Number of least-squares regression iterations (-)', fontsize=20)
ax1.set_ylabel('Sum of Square Error (all conditions)', fontsize=20)
ax1.set_yscale('log') 
    
sns.scatterplot(x="Step", y="RMSE", data=df2, ax=ax2)
ax2.set_xlabel('Number of least-squares regression iterations (-)', fontsize=20)
ax2.set_ylabel('Root-Mean Square Error (all conditions)', fontsize=20)
ax2.set_yscale('log') 