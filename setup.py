import algo
import test
import pandas as pd


rm3_df = test.record(algo.recurse_median, 3000, n_boot=100, seed=573, i=None, sep=3)
rm5_df = test.record(algo.recurse_median, 3000, n_boot=100, seed=573, i=None, sep=5)
rm7_df = test.record(algo.recurse_median, 3000, n_boot=100, seed=573, i=None, sep=7)
crm3_df = test.record(algo.c_recurse_median, 3000, n_boot=100, seed=573, i=None, sep=3)
crm5_df = test.record(algo.c_recurse_median, 3000, n_boot=100, seed=573, i=None, sep=5)
crm7_df = test.record(algo.c_recurse_median, 3000, n_boot=100, seed=573, i=None, sep=7)

rm3_df['function'] = 'rm3'
rm5_df['function'] = 'rm5'
rm7_df['function'] = 'rm7'
crm3_df['function'] = 'crm3'
crm5_df['function'] = 'crm5'
crm7_df['function'] = 'crm7'

df = pd.concat([rm3_df, rm5_df, rm7_df, crm3_df, crm5_df, crm7_df])
df.to_csv('data.csv',index=False)
