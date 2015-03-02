
def evm1_to_s(val) :
  ev   = 1.602 * pow(10,-19) # J
  hbar = 1.055 * pow(10,-34) # J s
  evm1 = hbar/ev # s
  return val * evm1

def m_to_evm1(val) :
  c    = 2.998 * pow(10,8)   # m s-1
  hbar = 1.055 * pow(10,-34) # J s
  ev   = 1.602 * pow(10,-19) # J
  evm1 = hbar*c/ev # m
  return val / evm1

def mm_to_mevm1(val) :
  m = val * pow(10,-3)
  evm1 = m_to_evm1( m )
  mevm1 = evm1 * pow(10,-6)
  return mevm1

def mevm1_to_ps(val) :
  evm1 = val * pow(10,6)
  s = evm1_to_s( evm1 )
  ps = s * pow(10,12)
  return ps



def LT(x = "D", m="1864.8", orivx="OWNPV") :
    # This function returns a string that can be fed to TTree::Draw:
    # myTree.Draw( LT() )
    # Please check the labels of the particle: "D",
    #              the value of the mass,
    #              and the label of the vertex in the tuple (ORIVX or OWNPV)

  l = "(entry.D_FD_OWNPV - entry.B_FD_OWNPV) * " + str(mm_to_mevm1(1))
  p = "entry.D_P"
  lt = "(("+m+"*"+l+")/("+p+")) * " + str(mevm1_to_ps(1))
  pm = "sign(entry.D_VZ - entry.B_VZ)"
  retval = "(" + pm + "*" + lt + ")"

  return retval
