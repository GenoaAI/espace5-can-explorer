# Analyse Complète des Codes Défauts (DTC) — Renault Espace V Phase 2 (2.0 Blue dCi)

Ce document consigne et explique le rapport de lecture DTC complet réalisé sur les **16 calculateurs** de la Renault Espace V 2.0 Blue dCi (`Odometer: 278 483 km`).

---

## 1. Bilan de Santé Global par Calculateur

Sur les **16 calculateurs** interrogés :
- **10 calculateurs présentent `0` défaut** :
  - **Unité de commande de transmission (`TCM` - Boîte Auto EDC DW6 Getrag)** : **0 défaut**
  - **Module de dosage AdBlue / Urée (`UDM` - SCR Plastic Omnium)** : **0 défaut**
  - **Unité de commande ABS / ESP (`CONTI`)** : **0 défaut**
  - **Calculateur Airbags & Prétensionneurs (`SRS`)** : **0 défaut**
  - **Système Multimédia Easy Link 9.3" (`A-IVI Bosch`, firmware `283C33813R`)** : **0 défaut**
  - **Tableau de bord numérique (`Visteon`)** : **0 défaut**
  - **Affichage Tête Haute (`HMD`)** : **0 défaut**
  - **Module de Gestion d'Énergie 12V (`EMM`)** : **0 défaut**
  - **Passerelle de Sécurité (`S-GW3`)** : **0 défaut**
- **Seuls 2 codes défauts sont ACTIFS (présents dans le cycle de conduite actuel)**.
- **Tous les autres codes (20 codes) sont au statut `Archive (inactif)`** (anciens événements mémorisés, typiquement lors d'une baisse de tension batterie 12V).

---

## 2. Analyse Détaillée des 2 Défauts ACTIFS (À vérifier)

### A. `P2002 [0x2002]` — *Particulate trap, bank 1 - efficiency below threshold* (Statut : Confirmé)
- **Calculateur** : Contrôle Moteur 2.0 Blue dCi (`OBD-II` / `ECM`)
- **Signification technique** :
  Le calculateur compare la différence de pression entre l'entrée et la sortie du **Filtre à Particules (FAP / DPF)** par rapport au débit de gaz d'échappement (et/ou le signal de la sonde de particules aval). Il juge que la contre-pression mesurée est inférieure au modèle théorique.
- **Les 2 causes principales sur le 2.0 Blue dCi (M9R) à ~278 000 km** :
  1. **Cause n°1 (la plus fréquente et peu coûteuse) : Durites ou Capteur de Pression Différentielle FAP**
     Les deux petites durites haute température qui relient le FAP au capteur de pression différentielle deviennent poreuses, se fendillent ou se bouchent avec la suie. Si la durite amont fuit légèrement, le capteur lit une pression différentielle trop basse et déclenche `P2002`.
  2. **Cause n°2 : Vieillissement / Micro-fissure interne de la céramique du FAP**
     À **278 483 km**, le monolithe interne du FAP peut présenter une micro-fissure qui laisse passer une partie des gaz sans freiner le flux.
     - *Test visuel immédiat en 5 secondes* : Passez un mouchoir blanc ou le doigt à l'intérieur de la canule de sortie d'échappement arrière.
       - Si la sortie est **propre (métal gris sans suie noire épaisse)** : le FAP filtre bien, c'est très probablement le **capteur de pression différentielle ou ses durites** !
       - Si la sortie est **couverte de suie noire grasse/épaisse** : la céramique du FAP laisse passer des particules.
- **Vérification via le Vgate iCar Pro BLE dans Car Scanner** :
  Ouvrez **`Tous les capteurs`** dans Car Scanner (moteur tournant au ralenti, puis à 2 500 tr/min) et regardez :
  - `DPF Differential Pressure` (Pression différentielle FAP en `mbar` ou `hPa`) : au ralenti, elle doit être entre **3 et 12 mbar** (si elle reste figée à `0` ou négative, le capteur ou sa durite est HS).
  - `DPF Soot Mass` (Masse de suie en `g`) et `Distance since last DPF regeneration` (km depuis la dernière régénération).

#### Trame Figée (Freeze Frame) extraite pour `P2002`
Conditions exactes enregistrées par le calculateur Bosch `MD1CS006` au moment du déclenchement de `P2002` :

| Paramètre | Valeur Mesurée | Analyse Technique |
|---|---|---|
| **Durée depuis démarrage moteur** | `00:27:29` (27 min 29 s) | Fenêtre de test OBD atteinte (moteur stabilisé en température) |
| **Vitesse véhicule / Régime** | `46 km/h` @ `2 048 tr/min` | Phase de relance urbaine/périurbaine (pédale accélérateur à `33.7 %`) |
| **Température liquide refroidissement** | `78 °C` *(Air ambiant: `10 °C`)* | Moteur chaud, air aspiré après échangeur à `30 °C` |
| **Débit massique d'air (MAF)** | **`35.99 g/s`** | Débit d'air sain et franc déclenchant le test de contre-pression FAP |
| **Pression absolue admission (MAP)** | `160 kPa` *(Atmo: `98 kPa`)* | `+0.62 bar` de suralimentation turbo (charge calculée `34.9 %`, absolue `139.2 %`) |
| **Pression rampe Common Rail** | `112 300 kPa` (**`1 123 bar`**) | Haute pression gazole nominale |
| **Vanne EGR (Spécifié / Erreur)** | `0 %` / `0 %` *(Papillon: `92.9 %`)* | EGR parfaitement fermée en demande de charge, papillon grand ouvert |
| **Tension calculateur (UCE)** | `14.48 V` | Alternateur piloté en charge nominale |

> **Conclusion de la Trame Figée** : L'ensemble de la boucle d'air (turbo, débitmètre `36 g/s`, EGR `0 %` d'erreur) et d'injection (`1 123 bar`) fonctionne de manière nominale. Le défaut `P2002` est purement lié à la mesure de contre-pression/efficacité du FAP lorsque le débit de gaz atteint `~36 g/s` à `2 048 tr/min`.

#### Relevé Dynamique en Roulant (`80 km/h` stabilisé @ `1 500 tr/min`)
Mesures capturées en temps réel sur route :
- **Température d'entrée FAP (`DPF banc 1 Capteur de température d'entrée`)** : **`323.9 °C`** (Température d'échappement parfaitement normale en croisière).
- **Régénération FAP en cours** : **`0`** (Aucune régénération active/passive au moment de la mesure).
- **Pression différentielle FAP (`Banc de filtres à particules diesel 1 Delta Pressure`)** : **`16.2 kPa` (`162 mbar`)** à `1 500 tr/min`.
- **Pression d'entrée compresseur turbo** : **`99 kPa`** (= Pression atmosphérique `99 kPa`, confirmant que le filtre à air moteur n'a aucune perte de charge).
- **Pression rampe Common Rail en charge** : **`104 020 kPa`** mesurés pour **`104 430 kPa`** commandés (écart `< 0.4 %`, régulation haute pression parfaite).

> **Analyse de la mesure `16.2 kPa` (`162 mbar`) à `1 500 tr/min`** :
> Une pression différentielle de `162 mbar` à seulement `1 500 tr/min` est **élevée** (la valeur nominale d'un FAP peu chargé à `1 500 tr/min` se situe entre `2.0 et 5.5 kPa`, soit `20 à 55 mbar`).

#### Relevé Statique au Ralenti puis Moteur Coupé (Validation du Zéro Capteur)
Mesures capturées à l'arrêt (`13:00`) :

| État Moteur | Pression Différentielle FAP (`Delta Pressure`) | Équivalent `mbar` | Valeur Nominale Attendue | Verdict |
|---|---|---|---|---|
| **Moteur coupé (Contact mis, `0 tr/min`)** | **`0.00 kPa`** | **`0 mbar`** | `0.0 kPa` (`0 mbar`) | **Capteur 100 % sain électriquement** (aucun décalage/offset du zéro) |
| **Ralenti stabilisé (`~800 tr/min`)** | **`5.91 à 6.01 kPa`** *(oscillation pulsations)* | **`59 à 60 mbar`** | `0.5 à 1.5 kPa` (`5 à 15 mbar`) | **Contre-pression au ralenti 4x à 5x supérieure à la normale** |
| **Croisière (`1 500 tr/min` @ `80 km/h`)** | **`16.20 kPa`** | **`162 mbar`** | `2.5 à 5.5 kPa` (`25 à 55 mbar`) | **Contre-pression élevée en charge partielle** |

> **Diagnostic Final suite à la courbe Ralenti (`5.98 kPa`) -> Arrêt (`0.00 kPa`)** :
> 1. **Le capteur électronique lui-même est hors de cause** puisqu'il retombe pile à `0.00 kPa` à la seconde où le moteur s'arrête (`48:20` sur le graphe).
> 2. **Il ne reste que 2 causes physiques possibles pour expliquer `60 mbar` au ralenti et le code `P2002` à `278 483 km`** :
>    - **Cause A (À vérifier en premier, 5 min)** : **Le piquage ou la durite AVAL (sortie FAP) du capteur de pression différentielle est bouché par de la calamine/condensation**. Si le tube aval est obstrué, le capteur ne soustrait plus la pression aval et mesure la pression brute amont (~60 mbar au ralenti), ce qui fausse le modèle du calculateur et lève `P2002`. Un simple débouchage à l'air comprimé des deux conduites du capteur suffit à vérifier.
>    - **Cause B (Si les deux tubes sont débouchés)** : À **`278 483 km`**, le FAP est **saturé en cendres incombustibles** (et/ou suie), créant `60 mbar` de perte de charge dès le ralenti. Un **décalaminage / nettoyage hydro-dynamique du FAP** (ou remplacement) permettra de retrouver `~0.8 à 1.2 kPa` (`8 à 12 mbar`) au ralenti.

---

### B. `B272B(97) [0xA72B97]` — Aide au Stationnement (`Sonar` - `0x74E`)
- **Statut** : *Test échoué dans le cycle courant de conduite, Temporaire, Confirmé*
- **Signification du sous-code UDS `(97)`** :
  En norme ISO-14229, le Failure Type Byte `0x97` signifie : **`Component or system operation obstructed or blocked` (Capteur obstrué ou bloqué)**.
- **Action recommandée** :
  Nettoyer délicatement au chiffon microfibre les **capteurs ronds d'aide au stationnement** sur les pare-chocs avant et arrière (vérifier qu'aucun gravillon, insecte, couche de cire ou d'eau gelée ne bloque la petite bague souple autour d'un capteur).

---

## 3. Explication des Défauts ARCHIVÉS (`Archive (inactif)`)

Ces défauts ne sont **plus présents** aujourd'hui (ils datent d'un événement antérieur et restent simplement dans le journal historique tant qu'un effacement DTC `0x14` n'est pas effectué) :

| Calculateur | Codes Archivés | Décodage & Raison |
|---|---|---|
| **BCM / UCH (`0x745`)** | `U1C00(08)`, `U1C02(08)`, `U1C03(08)` + `B2C76(04)` à `B2C80(04)` (12 codes) | **Éclairage d'ambiance LED Multi-Sense (Bus LIN)**. Très courant sur Espace 5 : lors d'une chute de tension batterie 12V au démarrage, les petits contrôleurs LED des bandeaux de portes mettent quelques millisecondes de trop à répondre sur le bus LIN (`08 = Bus signal failure`). |
| **Climatisation (`0x744`)** | `B24E8(02)` *(enregistré à `278 483 km`)* | Défaut passager de signal (`02 = General signal failure`) sur un capteur ou volet de climatisation. Inactif. |
| **Direction Assistée (`0x742`)** | `C1611(64)`, `C161F(86)` | Défaut passager de plausibilité (`64`) / signal CAN invalide (`86`) lors d'une coupure ou baisse de tension 12V. Inactif. |
| **Carte Mains-Libres (`0x792`)** | `U214F(87)`, `U215B(87)` | Trame CAN manquante (`87 = Missing message`) temporaire au réveil d'un calculateur. Inactif. |
| **Appel d'Urgence SOS (`0x77A`)** | `B2E13(8F)`, `B2E17(F0)` | Perte temporaire de réception cellulaire 4G ou test de la pile de secours interne du module SOS. Inactif. |
