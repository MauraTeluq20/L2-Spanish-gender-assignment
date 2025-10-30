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
library(loo)

df <- read.xlsx('Noun_phrases_Agreement_all_data_statst_Borealis25.xlsx') #L2 Spanish         Noun_phrases_Borealis4.xlsx
head(df)

table(df$Level)
summary(df)

df$Level <- factor(df$Level, levels = c("Beginner", "Intermediate", "Advanced"), ordered = TRUE)
unique(df$Level)

unique(df$Noun_det_assignment)


df %>%
  group_by(Level) %>%
  summarise(n_participantes = n_distinct(Subject_ID))

df %>%
  group_by(Level) %>%
  summarise(n_participantes = n_distinct(Adj))

df %>%
  group_by(Level) %>%
  summarise(n_participantes = n_distinct(Pre_noun))

n_distinct(df$Noun)
df %>%
  count(Noun, sort = TRUE) %>%
  head(20)

n_distinct(df$Adj)
df %>%
  count(Adj, sort = TRUE) %>%
  head(20)


#Research Question 2

# Convertimos: Correct = 1, Error = 0 (En Python: df['Noun_adj_binary'] = df['Noun_adj_agreement'].map({'correct': 1, 'error': 0}))

df <- df %>%
  mutate(Noun_adj_binary = recode(Noun_adj_agreement, 'correct' = 1, 'error' = 0))

df <- df[!is.na(df$Noun_adj_binary) & df$Noun_adj_binary %in% c(0, 1), ]
unique(df$Noun_adj_binary)

# Reordenar los niveles de los factores para cambiar la referencia

df$Protot_mark <- relevel(factor(df$Protot_mark), ref = "Protot")
df$Compare_L2_L1 <- relevel(factor(df$Compare_L2_L1), ref = "same")
df$Noun_gen <- relevel(factor(df$Noun_gen), ref = "Masc")
df$Pre_noun <- relevel(factor(df$Pre_noun), ref = "NO")


df.groupby('Level')['Subject_ID'].nunique()
df['Noun'].nunique()
df['Noun'].value_counts().head(10)


# Mostrar el dataframe filtrado
head(df)
unique(df$Noun_adj_binary)

table(df$Pre_noun)
prop.table(table(df$Pre_noun))
unique(df$Pre_noun)

# Bayesian Model 

model <- brm(
   Noun_adj_binary ~ Level + Protot_mark + Compare_L2_L1 + Noun_gen + Adj_Noun_Distance + Pre_noun + (1|Subject_ID) + (1|Noun_lemma ) + (1|Adj_lemma),
    data = df,
    family = bernoulli(),
    save_pars = save_pars(all = TRUE)  # Esto es obligatorio para moment_match
 )

summary(model)

emmeans(model, pairwise ~ Level, type = "response")

emmeans(model, pairwise ~ Protot_mark, type = "response")
emmeans(model, pairwise ~ Compare_L2_L1, type = "response")


loo(model)

loo_results <- loo(model)
loo_results_mm <- loo_moment_match(model, loo = loo_results)
loo_results_mm

prior_summary(model)

plot(model)


# Gráficos (cambiar el nombre del modelo si es necesario)

# Crear los efectos marginales para cada predictor
me1 <- conditional_effects(model, effects = "Protot_mark:Level")
me2 <- conditional_effects(model, effects = "Compare_L2_L1:Level")
me3 <- conditional_effects(model, effects = "Pre_noun:Level")
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
  ggtitle("Adjective position ") +
  theme(text = element_text(size = 14)) +
  scale_x_discrete(labels = c("NO" = "Postnominal", "YES" = "Prenominal"))

p4 <- plot(me4, plot = FALSE)[[1]] +
  scale_color_manual(values = c("Beginner" = "#F8766D",
                                "Intermediate" = "#619CFF",
                                "Advanced" = "#00BA38")) +
  theme_minimal() +
  labs(y = "", x = "") +
  ggtitle("Noun gender") +
  theme(text = element_text(size = 14))

p5 <- plot(me5, plot = FALSE)[[1]] +
  scale_color_manual(values = c("Beginner" = "#F8766D",
                                "Intermediate" = "#619CFF",
                                "Advanced" = "#00BA38")) +
  theme_minimal() +
  labs(y = "", x = "Distance entre noun et adjective") +
  ggtitle("Adj_Noun_Distance") +
  theme(text = element_text(size = 14))


# Combinar los cuatro en una sola figura (2 x 2)
combined <- (p1 + p2) / (p3 + p4) +
  plot_layout(guides = "collect") +
  plot_annotation(title = "Predictors of gender agreement accuracy",
                  tag_levels = "A")


combined

#Research Question 3 

df <- df %>%
  mutate(Det_adj_agreement = recode(Det_adj_agreement, 'correct' = "Yes", 'error' = "No"))


df <- df[!is.na(df$Det_adj_agreement) & df$Det_adj_binary %in% c("Yes",  "No"), ]
unique(df$Det_adj_agreement)



df <- df %>%
  mutate(Det_adj_agreement = recode(Det_adj_agreement, 'correct' = 1, 'error' = 0))

df <- df[!is.na(df$Det_adj_agreement) & df$Det_adj_agreement %in% c(0, 1), ]

unique(df$Det_adj_agreement)


tabla_resumen <- df %>%
  filter(!is.na(Det_adj_agreement)) %>%
  group_by(Noun_gen, Noun_det_assignment, Det_adj_agreement) %>%
  summarise(n = n(), .groups = "drop") %>%
  group_by(Noun_gen, Noun_det_assignment) %>%
  mutate(porcentaje = round(n / sum(n) * 100, 1)) %>%
  arrange(Noun_gen, Noun_det_assignment)

tabla_resumen


tabla_ancha <- tabla_resumen %>%
  select(-n) %>%
  pivot_wider(
    names_from = Det_adj_agreement,
    values_from = porcentaje,
    values_fill = 0
  )

tabla_ancha


plot(model)
plot(marginal_effects(model))  # Muestra efectos marginales (más interpretables)
plot(fixef(model))  # Coeficientes fijos del modelo


# Bayesian Model3: 

model3 <- brm(
  Det_adj_agreement ~  Level + Protot_mark + Compare_L2_L1 + Noun_gen + Adj_Noun_Distance + Pre_noun + (1|Subject_ID) + (1|Noun_lemma ) + (1|Adj_lemma),
  data = df,
  family = bernoulli(),
  save_pars = save_pars(all = TRUE) 
)
summary(model3)
emmeans(model3, pairwise ~ Level, type = "response")
loo(model3)
loo_results <- loo(model3, moment_match = TRUE)
loo_results

