import math
import statistics
import scipy.stats as st

########################################
# PROBLEM 6
# --------------------------------------
# HAZ depth data:
# Non-high (m2=18 obs):
#    1.04,1.15,1.23,1.69,1.92,
#    1.98,2.36,2.49,2.72,
#    1.37,1.43,1.57,1.71,1.94,
#    2.06,2.55,2.64,2.82
# High (m1=9 obs):
#    1.55,2.02,2.02,2.05,2.35,
#    2.57,2.93,2.94,2.97
########################################

def problem6():
    nonhigh_data = [
        1.04,1.15,1.23,1.69,1.92,
        1.98,2.36,2.49,2.72,
        1.37,1.43,1.57,1.71,1.94,
        2.06,2.55,2.64,2.82
    ]
    high_data = [
        1.55,2.02,2.02,2.05,2.35,
        2.57,2.93,2.94,2.97
    ]
    
    # Descriptive stats
    xbar = statistics.mean(high_data)
    ybar = statistics.mean(nonhigh_data)
    s1 = statistics.pstdev(high_data) if len(high_data)>1 else 0.
    s2 = statistics.pstdev(nonhigh_data) if len(nonhigh_data)>1 else 0.
    n1 = len(high_data)
    n2 = len(nonhigh_data)
    
    # We'll do two-sample Welch t test:  Ha: mu1 > mu2 => upper tail
    # T = (xbar - ybar)/ sqrt(s1^2/n1 + s2^2/n2)
    mean_diff = xbar - ybar
    var1 = (statistics.pvariance(high_data) 
             if n1>1 else 0.)  # sample variance
    var2 = (statistics.pvariance(nonhigh_data)
             if n2>1 else 0.)
    
    # sample variance with "ddof=1" in python would be sample-based,
    # but "pvariance" is population-based in the python library. 
    # We'll do sample-based: 
    #  s1^2 = sample variance
    s1_sq = statistics.variance(high_data) 
    s2_sq = statistics.variance(nonhigh_data)
    
    # compute test stat
    denom = math.sqrt( s1_sq/n1 + s2_sq/n2 )
    t_val = mean_diff / denom
    
    # Welch-Satterthwaite df approximation
    # df ~ ( (s1^2/n1 + s2^2/n2)^2 ) / [ (s1^2/n1)^2/(n1-1) + (s2^2/n2)^2/(n2-1) ]
    # We'll do that carefully:
    a = s1_sq/n1
    b = s2_sq/n2
    numerator   = (a + b)**2
    denominator = (a**2)/(n1-1) + (b**2)/(n2-1)
    df_approx   = numerator/denominator
    
    # Because Ha: mu1>mu2 => p-value = 1 - F_t(t_val), where F_t is cdf with df_approx
    p_value = 1 - st.t.cdf(t_val, df_approx)
    
    alpha=0.01
    print("=== PROBLEM 6 RESULTS ===")
    print(f"High data size, mean, stdev= {n1}, {xbar:.3f}, {statistics.stdev(high_data):.3f}")
    print(f"Non-high data size,mean,stdev= {n2}, {ybar:.3f}, {statistics.stdev(nonhigh_data):.3f}")
    print(f"Sample difference (High-Nonhigh)= {mean_diff:.3f}")
    print(f"Welch t= {t_val:.3f}, df~ {df_approx:.3f}")
    print(f"One-sided p-value= {p_value:.4f}")
    if p_value < alpha:
        print(f"Reject H0 at alpha= {alpha}")
    else:
        print(f"Fail to reject H0 at alpha= {alpha}")
    print()

problem6()
