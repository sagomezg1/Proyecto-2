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


Datos <- read_excel("Downloads/SeoulBikeData_utf8 limpiado.xlsx")
View(Datos)


#Variables Auxiliares
beta <- Datos$`Rented Bike Count`
T<- Datos$`Temperature(C)`
S <- Datos$`Solar Radiation (MJ/m2)`
R <-Datos$`Rainfall(mm)`
Sn <-Datos$`Snowfall (cm)`
Ssp <-Datos$Seasons_Spring
Ssu <-Datos$Seasons_Summer
Sw <-Datos$Seasons_Winter
Ho <- Datos$Holiday
F <- Datos$`Functioning Day`

modeloReducido<-lm(beta~T+S+R+Sn+Ssp+Ssu+Sw+Ho+F,data=Datos)
summary(modeloReducido)

ANOVA1 <- aov(beta~T+S+R+Sn+Ssp+Ssu+Sw+Ho+F,data=Datos)
summary(ANOVA1)
residuos <- residuals(ANOVA1)
plot(residuos, ylab = "Residuos Modelo Completo", main = "Boxplot de Residuos Modelo Completo") #Grafico Residuos
abline(0,0) #Linea y = 0

#Autocorrelacion:
dwtest(modeloReducido)#Hay problema de autocorrelacon positiva
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
T_corr <- T - rho * lag(Datos$`Temperature(C)`)
S_corr <- S -rho *lag(Datos$`Solar Radiation (MJ/m2)`)
R_corr <- R -rho *lag(Datos$`Rainfall(mm)`)
Sn_corr <- Sn -rho *lag(Datos$`Snowfall (cm)`)
Ssp_corr <- Ssp -rho *lag(Datos$Seasons_Spring)
Ssu_corr <- Ssu -rho *lag(Datos$Seasons_Summer)
Sw_corr <- Sw -rho *lag(Datos$Seasons_Winter)
Ho_corr <- Ho - rho*lag(Datos$Holiday)
F_corr <- F-rho *lag(Datos$`Functioning Day`)

modeloReducidoNuevo<-lm(beta_corr~T_corr+S_corr+R_corr+Sn_corr+Ssp_corr+Ssu_corr+Sw_corr+Ho_corr+F_corr,data=Datos)
summary(modeloReducidoNuevo)


dwtest(modeloReducidoNuevo)#No hay problema de autocorrelacon
ANOVAr_cor <- aov(beta_corr~T_corr+S_corr+R_corr+Sn_corr+Ssp_corr+Ssu_corr+Sw_corr+Ho_corr+F_corr,data=Datos)
summary(ANOVAr_cor)

#MULTICOLINEALIDAD al modelo corregido
fitr<-lm(beta_corr~T_corr+S_corr+R_corr+Sn_corr+Ssp_corr+Ssu_corr+Sw_corr+Ho_corr+F_corr,data=Datos)
summary(fitr)
vif(fitr)#No hay multicolinealidad

#Heterocedasticidad
bptest(modeloReducidoNuevo) #hay heteerocedasticidad

#Correcion
# Calcular los residuos y los pesos
# Los pesos se calculan como la inversa del cuadrado de los residuos
residuosr_he <- resid(modeloReducidoNuevo)
pesosr <- 1 / (residuosr_he^2)
data_1 <- read_excel("Downloads/SeoulBikeData_utf8 limpiado.xlsx", skip = 1)


#Ajustar el modelo WLS utilizando los pesos
modelorWLS <- lm(beta_corr~T_corr+S_corr+R_corr+Sn_corr+Ssp_corr+Ssu_corr+Sw_corr+Ho_corr+F_corr,data = data_1, weights = pesosr)

# Verificar la dimensión de los datos
length(residuosr_he)
nrow(data_1)

# Resumen del modelo WLS
summary(modelorWLS)
ANOVAr_fi <-aov(modelorWLS)
summary(ANOVAr_fi)
bptest(modelorWLS)

#Mejor Modelo
summary(modelorWLS)

