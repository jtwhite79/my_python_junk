import numpy as np
import pylab

def calc_Q_rect(coeff_d,H,L,g=32.2):
    Q = coeff_d * (2./3.) * ((2. * g)**0.5) * L * H**(3./2.)
    return Q
   
def calc_Q_notch(coeff_d,theta,H,g=32.2):
    
    Q = coeff_d * (8./15.) * ((2. * g)**0.5) * np.tan(theta/2.) * H**(5./2.)
    return Q
def find_nearest(value,array):
    min_diff = 1.0e+32
    min_idx = -999
    
    for idx in range(array.shape[0]):
        diff = abs(array[idx] - value)
        if diff < min_diff:
            min_diff = diff
            min_idx = idx   
    return min_idx
    

#--rect sharp
L = 1.0
b = 5.0
kh_rect = 0.003 #ft pg 53
kl_rect=0.0025 * 3.281 #ft fig 2.23c
cde_rect = 0.585 #fig 2.23b

#vnotch 90degree
theta=90.0
theta_rad = np.pi/2.0
kh_v = 0.0033 #ft 
cde_v = 0.578 #fig 2.24b

P = 1.0

H_range = np.arange(0,0.5,0.001)
Q_r = np.zeros_like(H_range)
Q_n = np.zeros_like(H_range)

for h_idx in range(H_range.shape[0]):
    Q_r[h_idx] = calc_Q_rect(cde_rect,H_range[h_idx]+kh_rect,L+kl_rect)
    Q_n[h_idx] = calc_Q_notch(cde_v,theta_rad,H_range[h_idx]+kh_v)

fig = pylab.figure()
ax = pylab.subplot(111)
ax.plot(H_range,Q_r,'b-',lw=2.0,label='rectanglar')
ax.plot(H_range,Q_n,'g-',lw=2.0,label='v-notch')
h_s = [0.1,0.2,0.3,0.4]
for h in h_s:
    q_r = Q_r[find_nearest(h,H_range)]
    q_n = Q_n[find_nearest(h,H_range)]
    ax.plot((h,h),(q_r,q_n),'k--',lw=2.0)
    y = q_r-((q_r-q_n)/2.0)
    ax.text(h+0.005,y,'delta Q:{0:4.2f}'.format(q_r-q_n))

ax.set_xlabel('head (ft)')
ax.set_ylabel('Q (cfs)')
ax.legend()
pylab.show()
