
library(tidyverse)
library(openxlsx)
library(readxl)
library(dplyr)
library(nnet)
library(ggplot2)
library(readxl)
library(brms)
library(emmeans)
library(patchwork)
install.packages("loo")
library(loo)


df <- read.xlsx('Noun_phrases_Borealis4.xlsx') #L2 Spanish
head(df)

table(df$Level)

df$Level <- factor(df$Level, levels = c("Beginner", "Intermediate", "Advanced"), ordered = TRUE)
unique(df$Level)



# Contar las cantidades de cada valor en las columnas Noun_gen y Noun_fr_gen
noun_gen_counts <- table(df$Noun_gen)
noun_gen_counts
noun_fr_gen_counts<- table(df$Noun_fr_gen)
noun_fr_gen_counts

# Tabla de contingencia básica
tab <- table(df$Noun_gen, df$Noun_fr_gen)
tab

# Tabla con porcentajes
prop_tab <- prop.table(tab) * 100
round(prop_tab, 2)  # Redondear a dos decimales

# Tabla de contingencia básica

tab <- table(df$Det, df$Det_type)
tab


# Tabla con porcentajes
prop_tab <- prop.table(tab) * 100
round(prop_tab, 2)  # Redondear a dos decimales

df %>%
  group_by(Noun_gen, Noun_fr_gen) %>%
  summarise(count = n()) %>%
  mutate(percent = round(100 * count / sum(count), 2)) %>%
  arrange(desc(percent))

df %>%
  group_by(Noun_gen, Protot_mark) %>%
  summarise(count = n()) %>%
  mutate(percent = round(100 * count / sum(count), 2)) %>%
  arrange(desc(percent))



table(df$Subject_ID)
table(df$Noun)

df %>%
  group_by(Level) %>%
  summarise(n_participantes = n_distinct(Subject_ID))                    

n_distinct(df$Noun)
df %>%
  count(Noun, sort = TRUE) %>%
  head(20)

# Reordenar los niveles de los factores para cambiar la referencia

df$Protot_mark <- relevel(factor(df$Protot_mark), ref = "Protot")
df$Compare_L2_L1 <- relevel(factor(df$Compare_L2_L1), ref = "same")
df$Noun_gen <- relevel(factor(df$Noun_gen), ref = "Masc")
df$Det_type <- relevel(factor(df$Det_type), ref = "Def")

df.groupby('Level')['Subject_ID'].nunique()
df['Noun'].nunique()
df['Noun'].value_counts().head(10)



#Research Question 1

# Convertimos: Correct = 1, Error = 0 (En Python: df['Noun_det_binary'] = df['Noun_det_agreement'].map({'correct': 1, 'error': 0}))
df <- df %>%
  mutate(Noun_det_binary = recode(Noun_det_assignment, 'correct' = 1, 'error' = 0))

df <- df[!is.na(df$Noun_det_binary) & df$Noun_det_binary %in% c(0, 1), ]
unique(df$Noun_det_binary)

# Bayesian Model 

model <- brm(
  Noun_det_binary ~ Level + Protot_mark + Compare_L2_L1 + Noun_gen +  Det_type + (1|Subject_ID) +  (1|Noun_lemma ) ,
  data = df,
  family = bernoulli()
)
summary(model)


library(loo)
loo(model)
loo_results_mm <- moment_match(loo_results, model)
loo_results_mm
prior_summary(model)

# Comparaciones entre niveles de "Level"
emmeans(model, pairwise ~ Level, type = "response")

emmeans(model, pairwise ~ Protot_mark, type = "response")
emmeans(model, pairwise ~ Compare_L2_L1, type = "response")
emmeans(model, pairwise ~ Det_type, type = "response")

plot(model)
plot(marginal_effects(model))  # Muestra efectos marginales (más interpretables)
plot(fixef(model))  # Coeficientes fijos del modelo

library(emmeans)
emm <- emmeans(model, pairwise ~ Det_type, type = "response")
plot(emm$contrasts)  # Odds ratios con intervalos HPD


# Gráficos

me <- marginal_effects(model, effects = "Protot_mark:Level")
plot(me, plot = FALSE)[[1]] + 
  scale_color_manual(
    values = c(
      "Beginner" = "#F8766D",      # naranja suave
      "Intermediate" =  "#619CFF",  # azul claro
      "Advanced" = "#00BA38"       # verde intenso
    )
 
  ) +
  theme_minimal() +
  labs(y = "",  x = "Morfological gender marker") +
  ggtitle("Effect of prototypicality on accuracy in gender assignment") +
  theme(text = element_text(size = 16)) +
  theme(
    plot.margin = unit(c(1, 1, 1, 1), "cm"), # Ajusta los márgenes
    panel.spacing = unit(0.5, "lines") # Ajusta el espacio entre paneles
  )




me1 <- marginal_effects(model, effects = "Compare_L2_L1:Level")
plot(me1, plot = FALSE)[[1]] + 
  scale_color_manual(
    values = c(
      "Beginner" = "#F8766D",      # naranja suave
      "Intermediate" =  "#619CFF",  # azul claro
      "Advanced" = "#00BA38"       # verde intenso
    )
    
  ) +
  theme_minimal() +
  labs(y = "Probability of accuracy in gender assignment", x = "L2_L1 congruency") +
  ggtitle("Effect of congruency on accuracy in gender assignment") +
  theme(text = element_text(size = 14)) +
  theme(
    plot.margin = unit(c(1, 1, 1, 1), "cm"), # Ajusta los márgenes
    panel.spacing = unit(0.5, "lines") # Ajusta el espacio entre paneles
  ) 



me <- conditional_effects (model, effects = "Level")
plot(me, plot = FALSE)[[1]] + 
  theme_minimal() +
  labs(y = "Probability of accuracy in gender assignment", x = "Proficiency level") +
  ggtitle("Effect of proficiency on accuracy in gender assignment") +
  theme(text = element_text(size = 12)) +
  theme(
    plot.margin = unit(c(1, 1, 1, 1), "cm"), # Ajusta los márgenes
    panel.spacing = unit(0.5, "lines") # Ajusta el espacio entre paneles
  )

me2 <- marginal_effects(model, effects = "Det_type")
plot(me2, plot = FALSE)[[1]] + 
  theme_minimal() +
  labs(y = "Probability of accuracy in gender assignment", x = "Determiner type") +
  ggtitle("Effect of determiner type on accuracy in gender assignment") +
  theme(text = element_text(size = 14))

me3 <- marginal_effects(model, effects = "Det_type:Level")
plot(me3, plot = FALSE)[[1]] + 
  scale_color_manual(
    values = c(
      "Beginner" = "#F8766D",      # naranja suave
      "Intermediate" =  "#619CFF",  # azul claro
      "Advanced" = "#00BA38"       # verde intenso
    )
    
  ) +
  theme_minimal() +
  labs(y = "Probability of accuracy in gender assignment", x = "Determiner type") +
  ggtitle("Effect of determiner type on accuracy in gender assignment") +
  theme(text = element_text(size = 14)) +
  theme(
    plot.margin = unit(c(1, 1, 1, 1), "cm"), # Ajusta los márgenes
    panel.spacing = unit(0.5, "lines") # Ajusta el espacio entre paneles
  )


me4 <- marginal_effects(model, effects = "Noun_gen:Level")
plot(me4, plot = FALSE)[[1]] + 
  scale_color_manual(
    values = c(
      "Beginner" = "#F8766D",      # naranja suave
      "Intermediate" =  "#619CFF",  # azul claro
      "Advanced" = "#00BA38"       # verde intenso
    )
    
  ) +
  theme_minimal() +
  labs(y = "", x = "") +
  ggtitle("") +
  theme(text = element_text(size = 16)) +
  theme(
    plot.margin = unit(c(1, 1, 1, 1), "cm"), # Ajusta los márgenes
    panel.spacing = unit(0.5, "lines") # Ajusta el espacio entre paneles
  )

# Crear los efectos marginales o condicionales para cada predictor 

me <- conditional_effects (model, effects = "Level")
plot(me, plot = FALSE)[[1]] + 
  
  theme_minimal() +
  labs(y = "Probability of accuracy in gender assignment", x = "Proficiency level") +
  ggtitle("Effect of proficiency on accuracy in gender assignment") +
  theme(text = element_text(size = 16)) +
  # coord_flip() # Para ponerlo horizontal, pero no me conviene
  theme(
    plot.margin = unit(c(1, 1, 1, 1), "cm"), # Ajusta los márgenes
    panel.spacing = unit(0.5, "lines") # Ajusta el espacio entre paneles
  )


me1 <- conditional_effects(model, effects = "Protot_mark:Level")
me2 <- conditional_effects(model, effects = "Compare_L2_L1:Level")
me3 <- conditional_effects(model, effects = "Det_type:Level")
me4 <- conditional_effects(model, effects = "Noun_gen:Level")

p1 <- plot(me1, plot = FALSE)[[1]] +
  scale_color_manual(values = c("Beginner" = "#F8766D",
                                "Intermediate" = "#619CFF",
                                "Advanced" = "#00BA38")) +
  theme_minimal() +
  labs(y = "", x = "") +
  ggtitle("Prototypicality") +
  theme(text = element_text(size = 14))

p2 <- plot(me2, plot = FALSE)[[1]] +
  scale_color_manual(values = c("Beginner" = "#F8766D",
                                "Intermediate" = "#619CFF",
                                "Advanced" = "#00BA38")) +
  theme_minimal() +
  labs(y = "", x = "") +
  ggtitle("L2–L1 Congruency") +
  theme(text = element_text(size = 14))+
  scale_x_discrete(labels = c("same" = "Same", "both" = "Both","different" = "Different" ))

p3 <- plot(me3, plot = FALSE)[[1]] +
  scale_color_manual(values = c("Beginner" = "#F8766D",
                                "Intermediate" = "#619CFF",
                                "Advanced" = "#00BA38")) +
  theme_minimal() +
  labs(y = "", x = "") +
  ggtitle("Determiner type") +
  theme(text = element_text(size = 14))

p4 <- plot(me4, plot = FALSE)[[1]] +
  scale_color_manual(values = c("Beginner" = "#F8766D",
                                "Intermediate" = "#619CFF",
                                "Advanced" = "#00BA38")) +
  theme_minimal() +
  labs(y = "", x = "") +
  ggtitle("Noun gender") +
  theme(text = element_text(size = 14))

# Combinar los cuatro en una sola figura (2 x 2)
combined <- (p1 + p2) / (p3 + p4) +
  plot_layout(guides = "collect") +
  plot_annotation(title = "Predictors of gender assignment accuracy",
                  tag_levels = "A")

combined




model <- brm(
  formula = Noun_det_binary ~ Level + Protot_mark + Compare_L2_L1 + (1 | Subject_ID) + (1 | Noun),
  data = df,
  family = bernoulli(),  # porque es una variable binaria
  chains = 4, iter = 2000, warmup = 1000, cores = 4,
  seed = 123
)

