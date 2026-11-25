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
