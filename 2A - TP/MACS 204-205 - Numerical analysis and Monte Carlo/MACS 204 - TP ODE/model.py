import numpy as np

##############################################################################
# Définition des constantes et conditions initiales
##############################################################################

Atmosphere_Initial = 750
CarbonateRock_Initial = 100000000
DeepOcean_Initial = 38000
FossilFuel_Initial = 7500
Plant_Initial = 560
Soil_Initial = 1500
SurfaceOcean_Initial = 890
VegLandArea_percent_Initial = 100

# Vecteur d'état initial
# [Atmosphere, CarbonateRock, DeepOcean, FossilFuelCarbon,
#  Plants, Soils, SurfaceOcean, VegLandArea_percent]
x0 = np.array([
    Atmosphere_Initial,
    CarbonateRock_Initial,
    DeepOcean_Initial,
    FossilFuel_Initial,
    Plant_Initial,
    Soil_Initial,
    SurfaceOcean_Initial,
    VegLandArea_percent_Initial
])

# Autres constantes globales
Alk = 2.222446077610055
Kao = 0.278
SurfOcVol = 0.0362
Deforestation = 0  # Mis à zéro pour l'instant, ajustable si besoin

##############################################################################
# Fonctions auxiliaires
##############################################################################

def AtmCO2(Atmosphere):
    return Atmosphere * (280/Atmosphere_Initial)
def GlobalTemp(AtmCO2):
    return 15 + ((AtmCO2-280) * .01)
def CO2Effect(AtmCO2):
    return 1.5 * ((AtmCO2) - 40) / ((AtmCO2) + 80)
def WaterTemp(GlobalTemp):
    return 273+GlobalTemp
def TempEffect(GlobalTemp):
    return ((60 - GlobalTemp) * (GlobalTemp + 15)) / (((60 + 15) / 2) ** (2))/.96
def SurfCConc(SurfaceOcean):
    return (SurfaceOcean/12000)/SurfOcVol
def Kcarb(WaterTemp):
    return .000575+(.000006*(WaterTemp-278))
def KCO2(WaterTemp):
    return .035+(.0019*(WaterTemp-278))
def HCO3(Kcarb, SurfCConc):
    return(SurfCConc-(np.sqrt(SurfCConc**2-Alk*(2*SurfCConc-Alk)*(1-4*Kcarb))))/(1-4*Kcarb)
def CO3(HCO3):
    return (Alk-HCO3)/2
def pCO2Oc(KCO2, HCO3, CO3):
    return 280*KCO2*(HCO3**2/CO3)

##############################################################################
# Émissions fossiles (données historiques et projections simplifiées)
##############################################################################

FossFuelData = np.array([
    [1850.0, 0.00],
    [1875.0, 0.30],
    [1900.0, 0.60],
    [1925.0, 1.35],
    [1950.0, 2.85],
    [1975.0, 4.95],
    [2000.0, 7.20],
    [2025.0, 10.05],
    [2050.0, 14.85],
    [2075.0, 20.70],
    [2100.0, 30.00]
])

def FossilFuelsCombustion(t):
    i = 0
    if t >= FossFuelData[-1, 0]:
        return FossFuelData[-1, 1]

    while i + 1 < len(FossFuelData) and t >= FossFuelData[i, 0]:
        i += 1
    
    if i == 0:
        return FossFuelData[0, 1]
    else:
        t1, v1 = FossFuelData[i-1]
        t2, v2 = FossFuelData[i]
        return v1 + (t - t1) / (t2 - t1) * (v2 - v1)

##############################################################################
# Dérivée du système
##############################################################################

def derivative(x, t):
    Atmosphere       = x[0]
    CarbonateRock    = x[1]
    DeepOcean        = x[2]
    FossilFuelCarbon = x[3]
    Plants           = x[4]
    Soils            = x[5]
    SurfaceOcean     = x[6]
    VegLandArea_pct  = x[7]
    
    PlantResp   = (Plants * (55 / Plant_Initial)) + Deforestation/2
    Litterfall  = (Plants * (55 / Plant_Initial)) + (Deforestation/2)
    SoilResp    = Soils * (55 / Soil_Initial)
    Volcanoes   = 0.1
    
    AtmCO2_       = AtmCO2(Atmosphere)
    GlobalTemp_   = GlobalTemp(AtmCO2_)
    WaterTemp_    = WaterTemp(GlobalTemp_)
    
    Photosynthesis = (110 
                      * CO2Effect(AtmCO2_) 
                      * (VegLandArea_pct / 100) 
                      * TempEffect(GlobalTemp_))
    
    HCO3_          = HCO3(Kcarb(WaterTemp_), SurfCConc(SurfaceOcean))
    pCO2Oc_        = pCO2Oc(KCO2(WaterTemp_), HCO3_, CO3(HCO3_))
    AtmOcExchange  = Kao * (AtmCO2_ - pCO2Oc_)
    
    if FossilFuelCarbon > 0:
        FossilFuelsCombustion_ = FossilFuelsCombustion(t)
    else:
        FossilFuelsCombustion_ = 0
    
    # d(Atmosphère)/dt
    dAtmosphere_dt = (PlantResp 
                      + SoilResp
                      + Volcanoes 
                      + FossilFuelsCombustion_
                      - Photosynthesis 
                      - AtmOcExchange)
    
    # Roches carbonatées
    Sedimentation = DeepOcean * (0.1 / DeepOcean_Initial)
    dCarbonateRock_dt = Sedimentation - Volcanoes
    
    # Échanges Océan profond
    Downwelling = SurfaceOcean * (90.1 / SurfaceOcean_Initial)
    Upwelling   = DeepOcean * (90   / DeepOcean_Initial)
    dDeepOcean_dt = Downwelling - Sedimentation - Upwelling
    
    # d(FossilFuelCarbon)/dt
    dFossilFuelCarbon_dt = -FossilFuelsCombustion_
    
    # d(Plants)/dt
    dPlants_dt = Photosynthesis - PlantResp - Litterfall
    
    # d(Soils)/dt
    dSoils_dt = Litterfall - SoilResp
    
    # d(SurfaceOcean)/dt
    dSurfaceOcean_dt = Upwelling + AtmOcExchange - Downwelling
    
    # d(VegLandArea_pct)/dt (simplifié)
    Development = (Deforestation / Plant_Initial * 0.2) * 100
    dVegLandArea_percent_dt = -Development
    
    return np.array([
        dAtmosphere_dt,
        dCarbonateRock_dt,
        dDeepOcean_dt,
        dFossilFuelCarbon_dt,
        dPlants_dt,
        dSoils_dt,
        dSurfaceOcean_dt,
        dVegLandArea_percent_dt
    ])

##############################################################################
# Méthodes d'intégration (Euler, RK4)
##############################################################################

def euler_step(x, t, dt, derivative_func):
    dxdt = derivative_func(x, t)
    return x + dt * dxdt

def rk4_step(x, t, dt, derivative_func):
    k1 = derivative_func(x, t)
    k2 = derivative_func(x + dt/2 * k1, t + dt/2)
    k3 = derivative_func(x + dt/2 * k2, t + dt/2)
    k4 = derivative_func(x + dt * k3, t + dt)
    return x + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

##############################################################################
# Fonction simulate() (Euler ou RK4)
##############################################################################

def simulate(x0, t0, t_final, dt, method='RK4'):
    if dt > 2.0:
        print(f"Attention: dt={dt} est élevé et peut causer des instabilités numériques. Limité à 2.0.")
        dt = 2.0
        
    n_steps = int((t_final - t0) / dt) + 1
    times = np.linspace(t0, t_final, n_steps)
    states = np.zeros((n_steps, len(x0)))
    states[0] = x0

    if method.lower() == 'euler':
        step_func = euler_step
    elif method.lower() == 'rk4':
        step_func = rk4_step
    else:
        raise ValueError("La méthode doit être 'Euler' ou 'RK4'")
    
    for i in range(1, n_steps):
        states[i] = step_func(states[i-1], times[i-1], dt, derivative)
    
    return times, states

##############################################################################
# Fonction compute_global_temp()
##############################################################################

def compute_global_temp(times, states):
    temps = np.zeros(states.shape[0])
    for i in range(states.shape[0]):
        atmosphere = states[i, 0]
        atm_co2 = AtmCO2(atmosphere)
        temps[i] = GlobalTemp(atm_co2)
    return times, temps

if __name__ == "__main__":
    t0 = 1850
    t1 = 2100
    dt = 0.1
    times, states = simulate(x0, t0, t1, dt, method='RK4')
    print("Exemple de simulation avec la méthode RK4:")
    print("Times:", times)
    print("Atmosphere:", states[:,0])