# returns a data frame with all not-round values of the sigmoid function

import pandas as pd
import numpy as np

def valuesSigmoid(ExpSigmoid):

    all_exponents = list(ExpSigmoid)

    df_results = pd.DataFrame(columns=['h(x)'], data=[])

    for iExp in range(0, len(all_exponents)):
        df_results = df_results.append({}, ignore_index=True)

        result = 1 / (1 + np.exp(-all_exponents[iExp]))

        if result < 0 or result > 1:
            print('Error: The result ' + result + ' is negative or bigger then one!')

        df_results['h(x)'][iExp] = result


    return df_results