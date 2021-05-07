import timer
from algo import naive_median
from tqdm import tqdm
import numpy as np
import pandas as pd

def unittest(func, test, n_boot=None,
             show_pbar=True, show_result=True,
             *args, **kwargs):
    if n_boot is None:
        n_boot = 1
    if len(test.shape) == 1:
        test = test.reshape((1, test.size))

    runtime = np.empty(test.size)
    
    if show_pbar: pbar = tqdm(total=test.size, desc=func.__name__)

    try:
        for j in range(test.shape[0]):
            for i in range(test.shape[1]):
                boot_res = np.empty(n_boot)
                res = naive_median(arr=test[j], i=i)
                timed_func = timer.exectime(func, return_result=True)
                for k in range(n_boot):
                    check = timed_func(arr=test[j], i=i, *args, **kwargs)
                    boot_res[k] = check[0]
                assert res == check[1]
                runtime[i+j] = np.nanmean(boot_res)
                if show_pbar: pbar.update(1)

        if show_pbar: pbar.close()

        rtime_mean = np.nanmean(runtime)
        rtime_std = np.nanstd(runtime)

        text = '\nTest Completed for {0} on {1} array(s) with size {2}' \
            .format(func.__name__,test.shape[0],test.shape[1])
        stat_text = 'Runtime Average: {0}; Runtime std: {1}' \
            .format(rtime_mean, rtime_std)

        if show_result:
            print(text)
            print(stat_text)

    except AssertionError:
        pbar.close()
        err_msg = 'Test fail: {0} on test {1} finding index {2}' \
            .format(func.__name__,j+1,i)
        raise AssertionError(err_msg)
    
    return rtime_mean, rtime_std


def record(func, n_low, n_high=None, n_boot=30,
           ci=95, seed=None, *args, **kwargs):
    if seed:
        np.random.seed(seed)

    if n_high is None:
        rindex = np.arange(n_low)
    else:
        rindex = np.arange(n_low,n_high)

    err = 100-ci
    result = np.empty((rindex.size, 3))
    time_func = timer.exectime(func)

    samples = generate(n_low, n_high)

    for row in range(rindex.size):
        boot_reps = np.empty(n_boot)
        for j in range(n_boot):
            boot_reps[j] = time_func(arr=samples[row], *args, **kwargs)
        result[row,0] = np.mean(boot_reps)
        result[row,1] = np.percentile(boot_reps, err/2)
        result[row,2] = np.percentile(boot_reps, 100-err/2)

    df = pd.DataFrame(result, columns=['mean', 'low', 'high'], index=rindex)
    df.reset_index(inplace=True)
    df.rename(columns={'index':'n'}, inplace=True)
    df['function'] = func.__name__

    return df

def generate(low, high=None, n_seed=None):
    if high is None:
        high = low
        low = 0
    if n_seed:
        np.random.seed(n_seed)
    
    r_list = list()

    for i in range(low, high):
        result = np.random.randint(127, size=i, dtype=np.int8)
        r_list.append(result)

    return r_list
