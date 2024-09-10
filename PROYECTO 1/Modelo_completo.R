install.packages("readxl")
install.packages("readr")
install.packages("writexl")
install.packages("PerformanceAnalytics")
install.packages("carData")
install.packages("car")
install.packages("xts")
install.packages("lmtest")
install.packages("psych")
install.packages("DescTools")



# Cargar las librerías necesarias
library(readr)
library(writexl)
library(readxl)
library(xts)
library(PerformanceAnalytics)
library(carData)
library(car)
library(lmtest)
library(ggplot2)
library(psych)
library(dplyr)
library(DescTools)

# Leer el archivo XLSX
df <- read_excel("Downloads/SeoulBikeData_utf8 limpiado.xlsx")


Datos <- read_excel("Downloads/SeoulBikeData_utf8 limpiado.xlsx")
View(Datos)

#Variables Auxiliares
beta <- Datos$`Rented Bike Count`
H<- Datos$Hour
T<- Datos$`Temperature(C)`
Hu<- Datos$`Humidity(%)`
W<- Datos$`Wind speed (m/s)`
V<- Datos$`Visibility (10m)`
D<- Datos$`Dew point temperature(C)`
S <- Datos$`Solar Radiation (MJ/m2)`
R <-Datos$`Rainfall(mm)`
Sn <-Datos$`Snowfall (cm)`
Ssp <-Datos$Seasons_Spring
Ssu <-Datos$Seasons_Summer
Sw <-Datos$Seasons_Winter
Ho <- Datos$Holiday
F <- Datos$`Functioning Day`

modeloCompleto<-lm(beta~H+T+Hu+W+V+D+S+R+Sn+Ssp+Ssu+Sw+Ho+F,data=Datos)
summary(modeloCompleto)

ANOVA1 <- aov(beta~H+T+Hu+W+V+D+S+R+Sn+Ssp+Ssu+Sw+Ho+F,data=Datos)
summary(ANOVA1)
residuos <- residuals(ANOVA1)
plot(residuos, ylab = "Residuos Modelo Completo", main = "Boxplot de Residuos Modelo Completo") #Grafico Residuos
abline(0,0) #Linea y = 0

#Autocorrelacion:
dwtest(modeloCompleto)#Hay problema de autocorrelacon positiva
library(lmtest)

#Correccion
length(residuos)
rho<-cor(residuos[2:8760],residuos[1:8759])
rho
e_t<-residuos[2:8760]
e_t1<-residuos[1:8759]*rho
modelo_auxiliar <- lm(e_t ~  e_t1)
summary(modelo_auxiliar)
# Transformar variables
beta_corr <- beta - rho * lag(Datos$`Rented Bike Count`)
H_corr <- H - rho * lag(Datos$Hour)
T_corr <- T - rho * lag(Datos$`Temperature(C)`)
Hu_corr <- Hu - rho *lag(Datos$`Humidity(%)`)
W_corr <- W -rho * lag(Datos$`Wind speed (m/s)`)
V_corr <- V -rho *lag(Datos$`Visibility (10m)`)
D_corr <- D - rho *lag(Datos$`Dew point temperature(C)`)
S_corr <- S -rho *lag(Datos$`Solar Radiation (MJ/m2)`)
R_corr <- R -rho *lag(Datos$`Rainfall(mm)`)
Sn_corr <- Sn -rho *lag(Datos$`Snowfall (cm)`)
Ssp_corr <- Ssp -rho *lag(Datos$Seasons_Spring)
Ssu_corr <- Ssu -rho *lag(Datos$Seasons_Summer)
Sw_corr <- Sw -rho *lag(Datos$Seasons_Winter)
Ho_corr <- Ho - rho*lag(Datos$Holiday)
F_corr <- F-rho *lag(Datos$`Functioning Day`)

modeloCompletoNuevo<-lm(beta_corr~H_corr+T_corr+Hu_corr+W_corr+V_corr+D_corr+S_corr+R_corr+Sn_corr+Ssp_corr+Ssu_corr+Sw_corr+Ho_corr+F_corr,data=Datos)
summary(modeloCompletoNuevo)

dwtest(modeloCompletoNuevo)#No hay problema de autocorrelacon
ANOVA_cor <- aov(beta_corr~H_corr+T_corr+Hu_corr+W_corr+V_corr+D_corr+S_corr+R_corr+Sn_corr+Ssp_corr+Ssu_corr+Sw_corr+H_corr+F_corr,data=Datos)
summary(ANOVA_cor)



#MULTICOLINEALIDAD al modelo corregido
fit<-lm(beta_corr~H_corr+T_corr+Hu_corr+W_corr+V_corr+D_corr+S_corr+R_corr+Sn_corr+Ssp_corr+Ssu_corr+Sw_corr+Ho_corr+F_corr,data=Datos)
summary(fit)
vif(fit)#La temperatura tiene multicolinealidad


#Solucion
#Correccion Multicolinealidad


promedio_corr <- (T_corr+D_corr)/2
fit<-lm(beta_corr~H_corr+promedio_corr+Hu_corr+W_corr+V_corr+S_corr+R_corr+Sn_corr+Ssp_corr+Ssu_corr+Sw_corr+Ho_corr+F_corr,data=Datos)
summary(fit)
vif(fit)#La temperatura tiene multicolinealidad

#Heterocedasticidad
bptest(modeloCompletoNuevo) #Existe heterocedasticidad por p-vale se rechaza hipotesis

#Correcion
# Calcular los residuos y los pesos
# Los pesos se calculan como la inversa del cuadrado de los residuos
residuos_he <- resid(modeloCompletoNuevo)
pesos <- 1 / (residuos_he^2)

#Ajustar el modelo WLS utilizando los pesos
modeloWLS <- lm(beta_corr ~ H_corr + T_corr + Hu_corr + W_corr + V_corr + D_corr + S_corr + R_corr + 
                  Sn_corr + Ssp_corr + Ssu_corr + Sw_corr + Ho_corr + F_corr, data = Datos, weights = pesos)

# Resumen del modelo WLS
summary(modeloWLS)
ANOVA_fi <-aov(modeloWLS)
summary(ANOVA_fi)
bptest(modeloWLS)

#Mejor Modelo
summary(modeloWLS)


