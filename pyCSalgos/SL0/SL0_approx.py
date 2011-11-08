# -*- coding: utf-8 -*-
"""
Created on Sat Nov 05 21:29:09 2011

@author: Nic
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 05 18:39:54 2011

@author: Nic
"""

import numpy as np

#function s=SL0(A, x, sigma_min, sigma_decrease_factor, mu_0, L, A_pinv, true_s)
def SL0_approx(A, x, eps, sigma_min, sigma_decrease_factor=0.5, mu_0=2, L=3, A_pinv=None, true_s=None):
  
  if A_pinv is None:
    A_pinv = np.linalg.pinv(A)
  
  if true_s is not None:
      ShowProgress = True
  else:
      ShowProgress = False
  
  # Initialization
  #s = A\x;
  s = np.dot(A_pinv,x)
  sigma = 2.0 * np.abs(s).max()
  
  # Main Loop
  while sigma>sigma_min:
      for i in np.arange(L):
          delta = OurDelta(s,sigma)
          s = s - mu_0*delta
          # At this point, s no longer exactly satisfies x = A*s
          # The original SL0 algorithm projects s onto {s | x = As} with
          # s = s - np.dot(A_pinv,(np.dot(A,s)-x))   # Projection
          # We want to project s onto {s | |x-As| < eps}
          # We move onto the direction -A_pinv*(A*s-x), but only with a
          # smaller step:
          direction = np.dot(A_pinv,(np.dot(A,s)-x))
          if (np.linalg.norm(np.dot(A,direction)) >= eps):
            s = s - (1.0 - eps/np.linalg.norm(np.dot(A,direction))) * direction

          #assert(np.linalg.norm(x - np.dot(A,s)) < eps + 1e-6)          
      
      if ShowProgress:
          #fprintf('     sigma=#f, SNR=#f\n',sigma,estimate_SNR(s,true_s))
          string = '     sigma=%f, SNR=%f\n' % sigma,estimate_SNR(s,true_s)
          print string
      
      sigma = sigma * sigma_decrease_factor
  
  return s
  
  
####################################################################
#function delta=OurDelta(s,sigma)
def OurDelta(s,sigma):
  
  return s * np.exp( (-np.abs(s)**2) / sigma**2)
  
####################################################################
#function SNR=estimate_SNR(estim_s,true_s)
def estimate_SNR(estim_s, true_s):
  
  err = true_s - estim_s
  return 10*np.log10((true_s**2).sum()/(err**2).sum())
