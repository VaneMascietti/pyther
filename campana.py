import numpy as np
#import solution_matrix as sm


#c    Starting from critical point    c    c
#    WRITE(nout,15) TCmod(icomp),Pc(icomp),Dc(icomp),Dc(icomp)
#    T = 0.9999 * TCmod(icomp)
#    Vc = 1/DC(icomp)
#    Vv = 1.03*Vc
#    Zc = Pc(icomp)*Vc/RGAS/T
#    aaa = min(0.89 + (Zc - 0.2) / 2, 0.95)
#    Vl = aaa*Vc
#    NS = 3
#    delXS = 0.10

# PARAMETER (nco=2, RGAS=0.08314472d0, NA=2)
nco = 2
RGAS=0.08314472
NA=2


Tc = 123
DC = 0.234
Pc = 23

RGAS = 0.80324234

temperature = 0.9999 * Tc
critical_volume = 1 / DC
vapor_volume = 1.03 * critical_volume
Zc = Pc * critical_volume / RGAS / temperature
liquid_volume = min(0.89 + (Zc - 0.2) / 2, 0.95) * critical_volume
NS = 2
delXS = 0.10

#------------------------------------------------------
XVAR = np.log([temperature, liquid_volume, vapor_volume])

#DFDS = 0.0
DFDS = np.zeros(3)
DFDS[2] = 1.0
print("DFDS = ", format(DFDS))

#RJAC=0.0
RJAC = np.zeros([3, 3])
RJAC[2, NS]=1.0
print("RJAC = ", format(RJAC))

NITER=0
T = np.exp(XVAR[0])
Vl = np.exp(XVAR[1])
Vv = np.exp(XVAR[2])


print("T = {0}, Vl = {1}, Vv = {2}".format(T, Vl, Vv))

FMAXOLD=8.0
FMAX=7.0
DMAXOLD=8.0
DMAX=7.0
F = np.zeros(3)

F[2]=0.0
delX=0.0
NV=0
#------------------------------------------------------


#if(NV.GE.5.and.T.LT.0.4*Tcmod(icomp))return
#      IF ((FMAX.GT.FMAXOLD.and.DMAX.GT.DMAXOLD).OR.NITER.eq.10) THEN
#            delXS=0.8*delXS
#            if(abs(delXS).lt.0.001)return
#            if(XOLD(1).NE.0.0D0)go to 7
#        END IF
#        NITER=NITER+1



criterio_1 = NV > 0.5 and T < 0.4*Tcmod

# IF ((FMAX.GT.FMAXOLD.and.DMAX.GT.DMAXOLD).OR.NITER.eq.10) THEN
if FMAX > FMAXOLD and DMAX > DMAXOLD or NITER == 10:
	# delXS=0.8*delXS
	delXS = 0.8 * delXS
	# if(abs(delXS).lt.0.001)return
	if abs(delXS) < 0.001:
		return
		# if(XOLD(1).NE.0.0D0)go to 7
		if XOLD[0] != 0:
			pass



#    NSOLD=NS

#    IF(VV.GT.1.1*VC)THEN  ! .and.T.GT.0.3*Tcmod(icomp)
#        NS=1
#    ELSE
#        NS=3
#    END IF

NSOLD = NS

if VV > 1.1 * VC:
	NS = 1
else:
	NS = 3

#    if(NS.ne.NSOLD)then
#        dSdSold=dXdS(NS)
#        dXdS=dXdS/dSdSold
#        RJAC(3,1:3)=0.0D0
#        RJAC(3,NS)=1.0D0
#    end if

#    NITER=min(niter,10)
#    delXS=delXS*5/NITER/dXdS(NSOLD)



if NS != NSOLD:
	dSdSold = dXdS[NS]
	dXdS = dXdS / dSdSold
	RJAC[3, 1:3] = 0.0
	RJAC[3, NS] = 1.0

NITER = min(niter,10)
delXS = delXS * 5 / NITER / dXdS[NSOLD]









#IF(delXS.LT.0)then
#        if(NS.EQ.1)
#            delXS=max(delXS,-0.008) ! Max lnT decrease allowed
#        if(NS.eq.2)
#            delXS=max(delXS,-0.01) ! Max lnVl decrease allowed: 0.01  ! DO NOT CHANGE !!!
#        if(NS.eq.3)
#            delXS=max(delXS,-0.10) ! Max lnVv decrease allowed: 0.20
#    ELSE
#        if(NS.EQ.1)
#            delXS=min(delXS,0.01) ! Max lnT increase allowed: 0.5 K
#        if(NS.eq.2)
#            delXS=min(delXS,0.05) ! Max lnVl increase allowed: 0.01
#        if(NS.eq.3)
#            delXS=min(delXS,0.20) ! Max lnVv increase allowed: 0.20
#    END IF



def comprobar_delXS(delXS, NS):

	if delXS < 0.0:
		if NS == 1:
			#! Max lnT decrease allowed
			delXS=max(delXS,-0.008) 
		elif NS == 2:
			#! Max lnVl decrease allowed: 0.01  ! DO NOT CHANGE !!!
			delXS=max(delXS,-0.01) 
		elif NS == 3:
			#! Max lnVv decrease allowed: 0.20
			delXS=max(delXS,-0.10) 
	else:
		if NS == 1:
			#! Max lnT increase allowed: 0.5 K
			delXS=min(delXS,0.01)
		if NS == 2:
			#! Max lnVl increase allowed: 0.01
			delXS=min(delXS,0.05)
		if NS == 3:
			#! Max lnVv increase allowed: 0.20
			delXS=min(delXS,0.20)

	return delXS


 
XOLD = XVAR
TOLD = T
POLD = Pv
DVOLD = RHOV
DLOLD = RHOL
NV = 0

S = XOLD(NS) + delXS

#! Initial estimates for the 3 variables in the next point
XVAR = XOLD + dXdS * delXS / dXdS[NS]

T = np.exp(XVAR[1])
Vl = np.exp(XVAR[2])
Vv = np.exp(XVAR[3])


#if(Pv.gt.1.D-20.and.(T.gt.0.25*TCmod(icomp).or.T>250)     ! modified April 6, 2016
#    1                              .and.T.lt.TCmod(icomp))go to 1
 
if (Pv > 1e-20 and (T > 0.25 * TCmod or T > 250) and T < TCmod):
	print("go to 1")
 

#      SUBROUTINE XTVTERMO(INDIC,T,V,P,rn,
#    1                    FUGLOG,DLFUGT,DLFUGV,DLFUGX)
#C
#C-------parameters of XTVTERMO (crit. point, LLV and CEP calculations)
#C
#C       rn        mixture mole numbers                     (input)
#C       t            temperature (k)                       (input)
#C       v            volume        (L)                     (input)
#C       p            pressure    (bar)                     (output)
#C       FUGLOG    vector of log. of fugacities (x*phi*P)   (output)    INDIC < 5
#C       DLFUGT    t-derivative of FUGLOG (const. vol,n)    (output)    INDIC = 2 or 4
#C       DLFUGV    vol-derivative of FUGLOG (const temp,n)  (output)    INDIC < 5
#C       DLFUGX    comp-derivative of FUGLOG (const t & v)  (output)    INDIC > 2
#C---------------------------------------------------
#C---  MODIFIED AND CORRECTED july 2005
#C---
#C---------------------------------------------------
#      IMPLICIT DOUBLE PRECISION (A-H,O-Z)
#      PARAMETER (MAXC=2,nco=2,RGAS=0.08314472d0)
#      DIMENSION DLFUGX(MAXC,MAXC)
#      DIMENSION FUGLOG(MAXC),DLFUGT(MAXC),DLFUGV(MAXC)
#    dimension rn(nco),Arn(nco),ArVn(nco),ArTn(nco),Arn2(nco,nco)
#    COMMON /MODEL/ NMODEL
#    COMMON/NG/NGR
#    COMMON /Pder/ DPDN(nco),DPDT,DPDV
#    NG=NGR
#    NC=2
#    IF(NMODEL.EQ.5.OR.NMODEL.EQ.7) CALL PARAGC(T,NC,NG,1)      
#    NTEMP=0
#      IGZ=0
#      NDER=1
#      IF (INDIC.GT.2) NDER=2
#      IF (INDIC.EQ.2 .OR. INDIC.EQ.4) NTEMP=1
#    TOTN = sum(rn)
#      RT = RGAS*T
#    call ArVnder(NDER,NTEMP,rn,V,T,Ar,ArV,ArTV,ArV2,Arn,ArVn,ArTn,Arn2)
#      P = TOTN*RT/V - ArV
#      DPDV = -ArV2-RT*TOTN/V**2
#      IF(INDIC.GT.4)GOTO 62
#c      Z = P*V/(TOTN*RT)
#    DPDT = -ArTV+TOTN*RGAS/V
#    DO 60 I=1,NC
#    IF(RN(I).EQ.0.0)GOTO 60
#C        FUGLOG(I)=-LOG(Z)+Arn(I)/RT + log(rn(I)/TOTN) + log(P)
#C        FUGLOG(I)=Arn(I)/RT + log(rn(I)/TOTN) + log(P/Z) this crashes at very low T LLV when Z=P=0.000000...
#        FUGLOG(I)=Arn(I)/RT + log(rn(I)) + log(RT/V)
#        DPDN(I) = RT/V-ArVn(I)
#        DLFUGV(I)=-DPDN(I)/RT                    ! term DPDV/P is cancelled out
#        IF(NTEMP.EQ.0) GOTO 60
#        DLFUGT(I)=(ArTn(I)-Arn(I)/T)/RT+1.D0/T    ! term DPDT/P is cancelled out
#   60 CONTINUE
#   62 IF(NDER.LT.2) GOTO 64
#      DO 63 I=1,NC
#      DO 61 K=I,NC
#        DLFUGX(I,K)=Arn2(I,K)/RT        ! term 1/TOTN is cancelled out
#   61        DLFUGX(K,I)=DLFUGX(I,K)
#        DLFUGX(I,I)=DLFUGX(I,I)+1.0/rn(I)
#   63 CONTINUE
#   64 RETURN
#      END



def XTVTERMO_cal(INDIC,T,V,P,rn, FUGLOG,DLFUGT,DLFUGV,DLFUGX):

	NG = NGR
    NC = 2
    
    NTEMP = 0
    IGZ = 0
    NDER = 1

    if INDIC > 2:
    	NDER =2

    if INDIC > 2 or INDIC == 4:
    	NTEMP = 1

    TOTN = sum(rn)
    RT = RGAS*T
    call ArVnder(NDER,NTEMP,rn,V,T,Ar,ArV,ArTV,ArV2,Arn,ArVn,ArTn,Arn2)
    
    P = TOTN*RT/V - ArV
    DPDV = -ArV2-RT*TOTN/V**2
    
    if INDIC > 4:
    	print("GOTO 62")

    Z = P * V / (TOTN * RT)
    DPDT = -ArTV + TOTN * RGAS / V

    #DO 60 I=1,NC
    
    #IF(RN(I).EQ.0.0)GOTO 60
    if rn[I] == 0:
    	print("GOTO 60")

    FUGLOG[I] = Arn[I] / RT + log(rn[I]) + log(RT / V)
    DPDN[I] = RT / V - ArVn[I]

    #! term DPDV/P is cancelled out
    DLFUGV[I] = -DPDN[I] / RT                    
    
    if NTEMP == 0:
    	print("GOTO 60")

    #! term DPDT/P is cancelled out
    DLFUGT[I] = (ArTn[I] - Arn[I] / T) / RT + 1.0 / T

    #60 CONTINUE
    #62 IF(NDER.LT.2) GOTO 64

    if NDER < 2:
    	DO 63 I=1,NC
    	DO 61 K=I,NC

    #! term 1/TOTN is cancelled out
    DLFUGX[I, K] = Arn2[I, K] / RT
    DLFUGX[K, I] = DLFUGX[I, K]
    DLFUGX[I, I] = DLFUGX[I, I] + 1.0 / rn[I]


















T = 123
TOLF = 1e-3
NS = 2
DFDS = np.zeros(3)
DFDS[2] = 1
F = np.ones(3)
F[2] = 0
RJAC = np.ones([3, 3])
RJAC[2, NS] = 0

delx_s = 0
NV = 0

Pl = 0.12
Pv = 3
FUGx = 2.3
FUGy = 3.7

condition_1 = Pl < 0.5 * Pv and (Pv - Pl) > 1e-8
condition_2 = Pl > 1.5 * Pv and (Pl - Pv) > 1e-8
print(Pl)
print(condition_1)
print(condition_2)

if condition_1:
	print('condition_1 = {0}'.format(condition_1))

if condition_2:
	print('condition_2 = {0}'.format(condition_2))

if condition_1 or condition_2:
	print(condition_1, condition_2)
	NV += 1
 
if Pl < 0:
	F[0] = TOLF
else:
	F[0] = np.log(Pl/Pv)

F[1] = FUGx - FUGy


#RJAC[0, 0] = T * (DPDTx / Pl - DPDTy / Pv)
#RJAC[0, 1] = Vl * DPDVx / Pl
#RJAC[0, 2] = -Vv * DPDVy / Pv

#RJAC[1, 0] = T * (FUGTx -FUGTy)
#RJAC[1, 1] = Vl * FUGVx
#RJAC[1, 2] = -Vv * FUGVy 

RJAC[0, 0] = 23
RJAC[0, 1] = 45
RJAC[0, 2] = -23

RJAC[1, 0] = 67
RJAC[1, 1] = 0.34
RJAC[1, 2] = -34.4 






print(F)
print(RJAC)
print(RJAC[2,2])

b = F
a = RJAC

print(a)

x = np.linalg.solve(a, b)
print(x)

print('sm.A = {0}'.format(sm.A))


class Component(object):		

	def function_Ar_cal(self):
		
		self.bv = self.B / self.V
		self.f = np.log((self.V + self.s1 * self.B) / (self.V + self.s2 * self.B)) / self.B / (self.s1 - self.s2)
		self.g = self.R * np.log(1 - self.B / self.V)

		self.AUX = self.R * self.T / (self.V - self.B)
		self.fB = -(self.f + self.V * self.fv) / self.B
		self.FFB = self.nT * AUX - self.D * self.fB
		self.Di = 2 * self.nT * self.ac * self.alfa
		self.Bi = self.bc

		self.Ar = -self.nT * self.g * self.T - self.D * self.f
		'''Primera derivada de F con respecto al volumen Ecu. (68)'''
		self.gv = self.R * self.B / (self.V * (self.V - self.B))
		self.fv = - 1 / ((self.V + self.s1 * self.B) * (self.V + self.s2 * self.B))
		self.ArV = -self.nT * self.gv * self.T - self.D * self.fv
		''' Segunda derivada de F con respecto al volumen Ecu. (74) '''
		self.gv2 = self.R * (1 / self.V ** 2 - 1 / (self.V - self.B) ** 2)
		self.fv2 = (- 1 / (self.V + self.s1 * self.B) ** 2 + 1 / (self.V + self.s2 * self.B) ** 2) / self.B / (self.s1 - self.s2)
		self.ArV2 = - self.nT * self.gv2 * self.T - self.D * self.fv2
		''' pressure '''
		self.Pcal = self.nT * self.R * self.T / self.V - self.ArV
		self.dPdV = -self.ArV2 - self.R * self.T * self.nT / self.V ** 2

		if self.eq != "RKPR":
			self.Arn = -self.g * self.T + self.FFB * self.Bi - self.f * self.Di
		else:
			self.Arn = -self.g * self.T + self.FFB * self.Bi - self.f * self.Di - self.D * self.fD1 * self.dD1i

		ArT = -nT * g - dDdT * f
		ArTV = -nT * gv - dDdT * fV
		ArTn = -g + (nT * AUX/T - dDdT * fB) * dBi - f * dDiT - dDdT * fD1 * dD1i
		ArVn = - gv * T + FFBV * dBi - fv * dDi - D * fVD1 * dD1i

		return self.g, self.f, self.Ar


component = Component()
component.function_Ar_cal()



class Component(object):		

	def function_Ar_cal(self):
		
		self.bv = self.B / self.V
		self.f = np.log((self.V + self.s1 * self.B) / (self.V + self.s2 * self.B)) / self.B / (self.s1 - self.s2)
		self.g = self.R * np.log(1 - self.B / self.V)

		self.AUX = self.R * self.T / (self.V - self.B)
		self.fB = -(self.f + self.V * self.fv) / self.B
		self.FFB = self.nT * AUX - self.D * self.fB
		self.Di = 2 * self.nT * self.ac * self.alfa
		self.Bi = self.bc

		self.Ar = -self.nT * self.g * self.T - self.D * self.f
		'''Primera derivada de F con respecto al volumen Ecu. (68)'''
		self.gv = self.R * self.B / (self.V * (self.V - self.B))
		self.fv = - 1 / ((self.V + self.s1 * self.B) * (self.V + self.s2 * self.B))
		self.ArV = -self.nT * self.gv * self.T - self.D * self.fv
		''' Segunda derivada de F con respecto al volumen Ecu. (74) '''
		self.gv2 = self.R * (1 / self.V ** 2 - 1 / (self.V - self.B) ** 2)
		self.fv2 = (- 1 / (self.V + self.s1 * self.B) ** 2 + 1 / (self.V + self.s2 * self.B) ** 2) / self.B / (self.s1 - self.s2)
		self.ArV2 = - self.nT * self.gv2 * self.T - self.D * self.fv2
		''' pressure '''
		self.Pcal = self.nT * self.R * self.T / self.V - self.ArV
		self.dPdV = -self.ArV2 - self.R * self.T * self.nT / self.V ** 2

		if self.eq != "RKPR":
			self.Arn = -self.g * self.T + self.FFB * self.Bi - self.f * self.Di
		else:
			self.Arn = -self.g * self.T + self.FFB * self.Bi - self.f * self.Di - self.D * self.fD1 * self.dD1i

		ArT = -nT * g - dDdT * f
		ArTV = -nT * gv - dDdT * fV
		ArTn = -g + (nT * AUX/T - dDdT * fB) * dBi - f * dDiT - dDdT * fD1 * dD1i
		ArVn = - gv * T + FFBV * dBi - fv * dDi - D * fVD1 * dD1i

		return self.g, self.f, self.Ar


component = Component()
component.function_Ar_cal()



# this is a example for the calculate for one composi
component.function_Ar_cal()




# there is a form to convert a componet object in a molec

