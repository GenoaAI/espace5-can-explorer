# Renault Espace V (Phase 2 — 2.0 Blue dCi & Easy Link) CAN / UDS Explorer

Outil Python léger et **100 % lecture seule (Read-Only)** pour explorer le réseau multiplexé **CAN (500 kbps, 11-bit ISO 15765-4)** et interroger en **UDS (ISO-14229, Service `0x22 ReadDataByIdentifier`)** les **18 calculateurs principaux** de la **Renault Espace 5 Phase 2 (2.0 Blue dCi M9R + Boîte EDC DW6 + Écran Easy Link 9.3" Bosch A-IVI)** via un adaptateur Bluetooth **Vgate iCar Pro BLE**.

---

## Fonctionnalités

- **100 % sûr (Lecture seule)** : N'envoie que des commandes de lecture d'identification UDS (`0x10 0x03`, `0x3E 0x00`, `0x22 F1xx`). Aucune écriture (`0x2E`), aucun effacement ou réinitialisation (`0x11`, `0x14`), compatible avec la passerelle **SGW (Security Gateway)** de l'Espace 5 Phase 2.
- **Réassemblage ISO-TP (ISO 15765-2) intégré** : Décode les réponses Single Frame et Multi-Frame (First Frame + Consecutive Frames) pour extraire les chaînes longues comme le **VIN (17 caractères)** ou les versions logicielles **Easy Link (`283CxxxxxR`)**.
- **18 Calculateurs Renault Espace 5 cartographiés** :
  - `ecm` (`0x7E0` -> `0x7E8`) : Injection Moteur **2.0 Blue dCi (Bosch MD1CS006)**
  - `tcm` (`0x7E1` -> `0x7E9`) : Boîte Automatique **EDC 6 rapports (Getrag DW6 / 6DCT450)**
  - `scr` (`0x7E2` -> `0x7EA`) : Module Dépollution **AdBlue / SCR**
  - `easylink` (`0x712` -> `0x732`) : Système Multimédia **Easy Link 9.3" (Bosch A-IVI Linux)**
  - `tdb` (`0x743` -> `0x763`) : Tableau de Bord Numérique TFT
  - `uch` (`0x745` -> `0x765`) : Unité Centrale Habitacle (BCM)
  - `4control` (`0x784` -> `0x7A4`) : Châssis **4 Roues Directrices (4Control)**
  - `avs` (`0x781` -> `0x7A1`) : Amortissement Piloté (Multi-Sense)
  - `abs` (`0x740` -> `0x760`) : Freinage ABS / ESP / ESC
  - `eps` (`0x742` -> `0x762`) : Direction Assistée Électrique
  - `hvac` (`0x744` -> `0x764`) : Climatisation Automatique
  - `bose` (`0x782` -> `0x7A2`) : Amplificateur Audio **Bose Surround**
  - `fcam` (`0x74B` -> `0x76B`) : Caméra Frontale ADAS (Matrix LED / Maintien de voie)
  - `frad` (`0x753` -> `0x773`) : Radar Frontal Régulateur Adaptatif (ACC)
  - `airbag`, `epb` (Frein de parking), `usm` (UPC / Gestion batterie ESM 12V), `hfm` (Mains-libres)
- **Simulateur intégré (`--simulate`)** : Permet de tester l'outil et la génération de rapports Markdown/JSON sur PC sans être branché à la voiture.

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
