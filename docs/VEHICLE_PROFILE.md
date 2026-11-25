# Profil Matériel & Logiciel Réel — Renault Espace V Phase 2 (2.0 Blue dCi & Easy Link)

Ce document synthétise l'empreinte réelle des **16 calculateurs** extraite via **Vgate iCar Pro BLE** (protocole mixte `ISO 15765-4 CAN 29-bit 500 kbaud` + `11-bit 500 kbaud`).
*(Note de confidentialité : le numéro de série VIN complet est volontairement masqué sous la forme `VF1RFC00166XXXXXX`).*

---

## 1. Architecture Multiplexée Découverte

La Renault Espace V Phase 2 (2.0 Blue dCi M9R) répartit ses calculateurs sur deux modes d'adressage CAN à 500 kbps :
- **6 calculateurs en CAN 29-bit (`ATSP7`, `18DAxxF1` -> `18DAF1xx`)** : Contrôle moteur (`ECM`), Boîte EDC (`TCM`), Dosage AdBlue (`UDM`), Freinage (`ABS/ESC`), Affichage Tête Haute (`HMD`) et Passerelle de Sécurité (`S-GW3`).
- **10 calculateurs en CAN 11-bit (`ATSP6`, `7xx` -> `7xx`)** : Système Multimédia **Easy Link (`A-IVI`)**, Tableau de bord numérique (`Visteon`), Habitacle (`BCM/UCH`), Gestion d'énergie 12V (`EMM`), Airbags (`SRS`), Direction assistée (`TRW`), Climatisation, Radars (`Sonar`), Mains-libres (`HFM`) et Module d'appel d'urgence 4G (`TCU/SOS`).

---

## 2. Synthèse des 16 Calculateurs Identifiés

| Calculateur | Mode CAN | Équipementier | Réf. Pièce (F187) | Réf. Logicielle (F188) | Réf. Matérielle (F191) | Version / Branche (F194 / F195) | DiagVer (F1A0) |
|---|---|---|---|---|---|---|---|
| **ECM (Injection 2.0 Blue dCi)** | 29-bit (`0x15` / `18DA10F1`) | Robert Bosch GmbH (`037`) | `237101663S` | `237010816V` *(Cal: `237610818V`)* | `237101663S` | `7A00` / `6K00` *(Boot: `CB_015_IFX4B_3.10.0`)* | `8C` |
| **TCM (Boîte Auto EDC DW6)** | 29-bit (`0x18` / `18DA18F1`) | GETRAG (Cologne) | `310322081R` | `310392109R` | `310321915R` | `2541` / `8210` *(Kit: `320109956R`)* | `0C` |
| **UDM (Dosage AdBlue / SCR)** | 29-bit (`0xE1` / `18DAE1F1`) | PLASTIC OMNIUM | `237G00329R` | `237G00556R` *(Cal: `237G80562R`)* | `285J97945R` | `9000` / `F04` *(Boot: `SWBOOT-F00RC1`)* | `10` |
| **ABS / ESC (Freinage)** | 29-bit (`18DA2DF1`) | CONTI | `476601440R` | `476601440R` | `478514191R` | `HPIPB` / `N52CG001812 - MLC70/11` | `09` |
| **HMD (Affichage Tête Haute)** | 29-bit (`18DA9BF1`) | BT2 | `249416835R` | `249992983R` | `285J94233R` | `R25` / `V20B01` | `08` |
| **S-GW3 (Security Gateway)** | 29-bit (`18DAD1F1`) | B408 | `284Y66LE5C` | `SWF007.0003.0032` | `285J96LA5D` | `F005VT1793` / `SWF007.0003.0032` | `06` |
| **Easy Link 9.3" (Multimedia)** | 11-bit (`712`/`732`) | BOSCH | `259159033R` | **`283C33813R`** | `285J95735R` | **`AI_PRJ_RN_AIVI_24.1V19`** / **`6919_240710`** | `B1` |
| **Tableau de Bord (Dashboard)** | 11-bit (`743`/`763`) | 07-Visteon-Namestovo | `248105110R` | `248B33935R` | `250465577R` | `V09.05` / `2006` | `12` |
| **BCM / UCH (Habitacle)** | 11-bit (`745`/`765`) | CONTINENTAL | `284B13925R` | `284B37713R` | `284B21462R` | `142902` / `0710` *(Boot: `0550`)* | `90` |
| **SRS / Airbags** | 11-bit (`752`/`772`) | 255414 | `985102111R` | `285A42149R` | `285J93115R` | `S2_020OH.P72` / `P72` | `09` |
| **Direction Assistée (EPS)** | 11-bit (`742`/`762`) | TRW | `490044671R` | `285049500R` | `285007079R` | `S2RE03CD04` | `26` (`&`) |
| **Climatisation (HVAC)** | 11-bit (`744`/`764`) | 740 (Valeo) | `285252812R` | - | - | `F007` / `1913` | `04` |
| **EMM (Gestion Énergie 12V)** | 11-bit (`74D`/`76D`) | 414 (Continental) | `284B78775R` | - | - | `BA65` / `6560` | `64` |
| **Sonar (Aide Stationnement)** | 11-bit (`74E`/`76E`) | BOSCH3 | `284L00448R` | `284S92436R` | `285J97007R` | `1270RS593P_S1.144.1.4` | `08` |
| **HFM (Carte Mains-Libres)** | 11-bit (`792`/`7B2`) | CONTINENTAL | `285903089R` | `285J92452R` | `285E26475R` | `142A02` / `0630` | `05` |
| **TCU (Appel d'urgence SOS)** | 11-bit (`77A`/`75A`) | Continental | `2591A9374R` | `282773501R` | `282A78506R` | `SW9` | `04` |

---

## 3. Chronologie & Historique Décodés dans les Calculateurs

1. **Fabrication des boîtiers en usine (Juillet – Septembre 2020)** :
   - `TCU / SOS` : Numéro de série `200701202037888806` -> **1er juillet 2020**
   - `S-GW3` : Numéro de série `3712001436502C200720` -> **20 juillet 2020**
   - `TCM (Boîte EDC Getrag)` : Numéro de série `200821191214` -> **21 août 2020 à 19h12m14s**
   - `Sonar Bosch` : Numéro de série `2008270748` -> **27 août 2020**
   - `Tableau de bord Visteon` : Numéro de série `20_09_11__0044923786` -> **11 septembre 2020**
   - `ECM (Moteur Bosch)` : Numéro de série `94840016201222090737` -> **22 septembre 2020**
2. **Compteurs de cycles d'allumage (`IGNCNTR`) & Reprogrammations** :
   - Le module **AdBlue (`UDM`)** totalise **`3 631` cycles de démarrage** (`OBDCOND = 1 319`) depuis la sortie d'usine.
   - Le calculateur **Injection Moteur (`ECM`)** totalise **`839` cycles de démarrage** (`OBDCOND = 315`) depuis sa reprogrammation officielle Renault vers la calibration **`237610818V`** (logiciel `237010816V` / pièce `237101663S`).
3. **Mise à jour récente du système Easy Link (`A-IVI`)** :
   - Branche logicielle Bosch **`AI_PRJ_RN_AIVI_24.1V19`**, build **`6919_240710`** (compilé le **10 juillet 2024**), version Renault **`283C33813R`**.
