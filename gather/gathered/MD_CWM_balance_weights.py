import numpy as np
import pandas
import pst_handler as ph

pst = ph.pst('umd03.pst')
blu_fix = ['petm02','petm07','petm08','petm09']
for pidx,par in pst.parameter_data.iterrows():
    for fix in blu_fix:        
        if par['parnme'].startswith(fix):
            pst.parameter_data.parval1[pidx] = 0.0
            pst.parameter_data.partrans[pidx] = 'fixed'
    pass
pst.reconcile_prior_2_pars()
pst.update()
pst.write_pst('umd03_blufixed.pst')

obs = pst.observation_data
obs.index = pandas.MultiIndex.from_arrays((obs.obsnme,obs.obgnme))
res = df = pandas.read_csv('umd03.res',sep='\s+',index_col=[0,1])
obs = obs.merge(res,left_index=True,right_index=True)

#--get the contribution of stage/head and baseflow to obj func
#--the baseflow group names end with 's'
resid_grouped = obs['Weight*Residual'].groupby(lambda x:x.endswith('s'),level=1)
phi_components = resid_grouped.aggregate(lambda x:np.sum(x**2))
print phi_components.values

#--mod bf weights they contribute a fraction of all the other obs to the obj function
bf_frac = 0.25
frac = np.sqrt((bf_frac*phi_components[False]) / phi_components[True])

obs['Weight'][resid_grouped.groups[True]] *= frac
obs['Weight*Residual'] = obs['Weight'] * obs['Residual']
resid_grouped = obs['Weight*Residual'].groupby(lambda x:x.endswith('s'),level=1)
phi_components = resid_grouped.aggregate(lambda x:np.sum(x**2))
print phi_components.values

pst.observation_data['weight'] = obs.Weight
pst.write_pst('umd03_reweight.pst')




