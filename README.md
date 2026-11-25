# Renault Espace V (Phase 2 — 2.0 Blue dCi & Easy Link) CAN / UDS Explorer

Outil Python léger et **100 % lecture seule (Read-Only)** pour explorer le réseau multiplexé **CAN (500 kbps, 11-bit ISO 15765-4)** et interroger en **UDS (ISO-14229, Service `0x22 ReadDataByIdentifier`)** les **18 calculateurs principaux** de la **Renault Espace 5 Phase 2 (2.0 Blue dCi M9R + Boîte EDC DW6 + Écran Easy Link 9.3" Bosch A-IVI)** via un adaptateur Bluetooth **Vgate iCar Pro BLE**.

---

## Fonctionnalités

- **100 % sûr (Lecture seule)** : N'envoie que des commandes de lecture d'identification UDS (`0x10 0x03`, `0x3E 0x00`, `0x22 F1xx`) et de lecture DTC (`0x19 0x02`). Aucune écriture (`0x2E`), aucun effacement ou réinitialisation (`0x11`, `0x14`), compatible avec la passerelle **S-GW3 (Security Gateway Gen 3)** de l'Espace 5 Phase 2.
- **Architecture CAN Mixte 29-bit (`ATSP7`) + 11-bit (`ATSP6`) à 500 kbps** :
  - **6 Calculateurs en CAN 29-bit (`18DAxxF1` -> `18DAF1xx`)** :
    - `ecm` (`18DA10F1`) : Unité de Contrôle Moteur **2.0 Blue dCi (Bosch MD1CS006 - `237010816V` / `237610818V`)**
    - `tcm` (`18DA18F1`) : Boîte Automatique **EDC 6 rapports (Getrag DW6 / 6DCT450 - `310392109R`)**
    - `udm` (`18DAE1F1`) : Module de Dosage **AdBlue / Urée SCR (Plastic Omnium - `237G00556R`)**
    - `abs` (`18DA2DF1`) : Freinage **ABS / ESP (Continental - `476601440R`)**
    - `hmd` (`18DA9BF1`) : Affichage Tête Haute Motorisé (**Head-Up Display - `249416835R`**)
    - `sgw` (`18DAD1F1`) : Passerelle de Sécurité **S-GW3 (`284Y66LE5C` / `SWF007.0003.0032`)**
  - **10 Calculateurs en CAN 11-bit (`7xx` -> `7xx`)** :
    - `easylink` (`712` -> `732`) : Système Multimédia **Easy Link 9.3" (Bosch A-IVI `283C33813R`, branche `AI_PRJ_RN_AIVI_24.1V19`, build `6919_240710`)**
    - `tdb` (`743` -> `763`) : Tableau de Bord Numérique TFT (**Visteon `248105110R`**)
    - `bcm` (`745` -> `765`) : Unité Centrale Habitacle (**Continental `284B13925R`**)
    - `airbag` (`752` -> `772`) : Airbags & Prétensionneurs (**SRS `985102111R`**)
    - `eps` (`742` -> `762`) : Direction Assistée Électrique (**TRW `490044671R`**)
    - `hvac` (`744` -> `764`) : Climatisation Automatique (**Valeo `285252812R`**)
    - `emm` (`74D` -> `76D`) : Module de Gestion d'Énergie 12V (**EMM Continental `BA65`**)
    - `sonar` (`74E` -> `76E`) : Aide au Stationnement Ultrasons (**Bosch `284L00448R`**)
    - `hfm` (`792` -> `7B2`) : Module Carte Mains-Libres (**Continental `285903089R`**)
    - `tcu` (`77A` -> `75A`) : Module Appel d'Urgence SOS & 4G (**Continental `2591A9374R`**)
- **Documentation & Rapports Techniques inclus** :
  - [`docs/VEHICLE_PROFILE.md`](docs/VEHICLE_PROFILE.md) : Empreinte matérielle/logicielle complète des 16 calculateurs et chronologie décodée.
  - [`docs/DTC_ANALYSIS.md`](docs/DTC_ANALYSIS.md) : Analyse détaillée des codes défauts (DTC), trame figée `P2002` et télémétrie FAP en roulant.

---

## Utilisation sur Smartphone Android (Car Scanner ELM OBD2 + Android Auto)

1. Branchez le **Vgate iCar Pro BLE** sous le volant (trappe à gauche) et mettez le contact.
2. Dans **Car Scanner ELM OBD2** :
   - **Connexion** : `Bluetooth LE (4.0+)` -> sélectionnez **`IOS-Vlink`** (ou Bluetooth classique -> `Android-Vlink`, code `1234`).
   - **Profil de connexion** : `Renault` -> sélectionnez **`Koleos II 2.0 dCi M9R [EN]`** *(c'est le seul profil 2.0 dCi M9R de Car Scanner qui interroge automatiquement les 6 calculateurs 29-bit + les 10 calculateurs 11-bit de l'Espace V Phase 2)*.

---

## Guide d'utilisation rapide sous Windows avec le Vgate iCar Pro BLE

### Étape 1 : Brancher et appairer le Vgate iCar Pro BLE sous Windows

1. Dans votre Espace 5, ouvrez la petite trappe située **tout en bas à gauche du volant** et branchez le **Vgate iCar Pro BLE** sur la prise OBD-II.
2. Mettez le contact (appui sur **START** sans appuyer sur la pédale de frein, ou moteur tournant).
3. Sur votre PC Windows :
   - Ouvrez **Paramètres → Bluetooth et appareils → Ajouter un appareil**.
   - Le Vgate expose deux canaux : **`Android-Vlink`** (Bluetooth Classique SPP) et **`IOS-Vlink`** (BLE).
   - Sélectionnez **`Android-Vlink`** et entrez le code PIN **`1234`**.
4. Pour connaître le numéro de port **`COM`** attribué par Windows :
   - Lancez simplement `run_windows.bat` (ou `python scan_espace5.py --list-ports`), qui détecte et affiche les ports `COM` disponibles (choisissez le port *Sortant / Outgoing* `Android-Vlink`).

### Étape 2 : Lancer le scan en 1 clic sous Windows

Double-cliquez sur **`run_windows.bat`** ou lancez dans PowerShell / CMD :

```powershell
pip install -r requirements.txt

# 1. Lister les ports COM Bluetooth détectés
python scan_espace5.py --list-ports

# 2. Lancer un scan complet sur le Vgate (remplacez COM4 par votre port)
python scan_espace5.py --port COM4 --md-out reports\mon_espace5.md --json-out reports\mon_espace5.json

# 3. Ou scanner uniquement l'écran Easy Link (0x712)
python scan_espace5.py --port COM4 --ecu easylink
```

### Étape 3 : Tester dès maintenant sans le boîtier (Mode Simulation)

```powershell
python scan_espace5.py --simulate --md-out reports\EXAMPLE_SIMULATION.md
```

---

## Confidentialité

Les rapports générés dans `reports/*.json` et `reports/*.md` contiennent le **numéro de châssis (VIN)** de votre véhicule. Ils sont automatiquement ignorés par `.gitignore` pour ne jamais être publiés par erreur sur GitHub.
