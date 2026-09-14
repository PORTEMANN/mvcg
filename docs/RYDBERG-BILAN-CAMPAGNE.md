# Campagne croisée Rydberg — bilan

Date de clôture : 2026-09-14. Statut : campagne close, trois contacts pesés, un témoin négatif.

## Les contacts

| Contact | Registre | Voie | Verdict | Écart | θ |
|---|---|---|---|---|---|
| `H1s_Rydberg` | micro / eV | 1ʳᵉ voie — E₁ₛ = −R∞ (CODATA-2018 gelé) | **S+** | 0,0 | 1 × 10⁻¹² eV |
| `H1s_Rydberg_Voie2` | micro / eV | 2ᵉ voie — R∞ = α² m_e c² / 2e vs Rydberg_eV déclaré | **S+** | 1,00 × 10⁻¹⁰ eV | 5,84 × 10⁻⁹ eV (= u, GUM k = 1) |
| `SPEC_CO_Rot_Dunham` | meso / Hz | pendant — 2B₀ − 4D₀ (NIST) vs ν(1-0) NIST | **S+** | 280 Hz | 10 000 Hz |
| `H1s_Rydberg_13p6` | micro / eV | **témoin négatif** — levier vintage R∞ = 13,6 | **S−** | 4,18 × 10⁻⁴ eV | 1 × 10⁻¹² eV |

## Ce que la machine a réellement mesuré

Les deux S+ Rydberg ne sont pas deux confirmations indépendantes : Rydberg_eV,
α et m_e c² participent du **même ajustement CODATA-2018**. La voie 2 ne teste
pas la physique de l'atome d'hydrogène ; elle teste la **cohérence interne du
catalogue** — que les constantes publiées sont mutuellement conformes à
~10⁻¹⁰ eV près. C'est exactement le pendant du contact Dunham (même dette,
côté spectroscopie rotationnelle : B₀, D₀ et ν(1-0) viennent du même
ajustement NIST).

Le verdict S+ porté à θ = u (incertitude propagée, k = 1) dit donc :

> la fibre électrodynamique est **calibrée** — le transport de table à travers
> la chaîne de calcul tient dans l'incertitude déclarée de la source.

Ce n'est pas une prédiction. La note du registre le dit sans détour :
« formule = constante déclarée ; pas un atome ontologique ».

## Pourquoi le témoin négatif compte autant

`H1s_Rydberg_13p6` substitue R∞ = 13,6 eV (vintage) et casse : S− à
4,18 × 10⁻⁴ eV, soit ~4 × 10⁸ θ. Un θ trop serré n'est pas satisfait
vacuum — la règle de verdict discrimine. Sans ce témoin, deux S+ à identité
annoncée pourraient être lus comme une tautologie ; avec lui, la machine
démontre que son S+ n'est pas un oui automatique.

## Leçon méthodologique

1. **Circularité assumée > circularité cachée.** La dette est écrite dans la
   note du contact et verrouillée par test (`tests/test_open_rydberg_voie2.py`).
   Un lecteur sait exactement quel credit accorder au S+.
2. **Deux voies S+ partageant une source valent une certification, pas une
   découverte.** La force du dispositif est ailleurs : les campagnes où le
   local et le déclaré viennent d'ajustements disjoints (HVP ππ CMD-3,
   Karplus Vogeli-Bax).
3. **θ = u est une convention honnête** quand le test est la propagation :
   le verdict devient « l'écart est-t-il compatible avec l'incertitude
   déclarée », ce qui est la bonne question pour un contact de calibre.

## Trace

- Table : `data/tables/codata2018_rydberg_voie2.json`
- Protocoles gelés avant run : `docs/RYDBERG-VOIE2-CONTACT-OUVERT.md`,
  protocoles Dunham et première voie (contacts antérieurs, registre figé)
- Mots découverts, pas choisis ; estimations pré-run conservées dans les notes.
