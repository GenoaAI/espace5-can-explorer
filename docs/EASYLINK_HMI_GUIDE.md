# Exploration & Personnalisation de l'IHM Easy Link 9.3" (`0x712`) & Tableau de Bord (`0x743`)

Ce guide documente le fonctionnement interne de l'unité multimédia **Bosch Easy Link (`A-IVI`)** identifiée sur le véhicule :
- **Référence Matérielle (`F187`)** : `259159033R` (Unité Branche 2 Navigation)
- **Référence Logicielle Renault (`F188`)** : **`283C33813R`**
- **Branche Logicielle Interne Bosch (`F194` / `F195`)** : **`AI_PRJ_RN_AIVI_24.1V19`** (Build **`6919_240710`** du **10 juillet 2024**)
- **Variante Diagnostic (`F1A0`)** : **`0xB1`**

---

## 1. Comment lire les registres IHM de votre Easy Link (`0x712`) depuis votre Smartphone Android

Sans même sortir le PC Windows, vous pouvez interroger en direct les registres internes de votre écran **Easy Link (`0x712` -> `0x732`)** depuis le **Terminal ELM327** intégré à **Car Scanner** (`Configuration -> Adaptateur OBDII ELM327 -> Terminal`) ou avec l'application gratuite **Serial Bluetooth Terminal** connectée à `Android-Vlink` / `IOS-Vlink`.

Voici la séquence exacte de commandes **100 % lecture seule** à taper ligne par ligne pour entrer en communication avec l'OS de l'Easy Link :

```text
ATSP6
ATSH712
ATCRA732
ATFCSH712
ATFCSD300000
ATFCSM1
1003
```
*(L'Easy Link doit répondre `50 03 ...` ce qui confirme que la session diagnostic étendue est ouverte sur l'écran !)*

Ensuite, vous pouvez lire ses registres de configuration IHM avec la commande **`22` + code registre** :
- **`22F188`** : Lit la version logicielle (`283C33813R`)
- **`222001`** : Lit la configuration **Android Auto / CarPlay (USB & Sans-Fil Wi-Fi)**
- **`222002`** : Lit l'état du **module Wi-Fi 5 GHz interne** de l'Easy Link
- **`222003`** : Lit le **thème d'accueil** (*Renault Standard*, *Initiale Paris*, *R.S.*, *Alpine*)
- **`222006`** : Lit la configuration **Multi-Sense & Éclairage d'ambiance LED**
- **`22200B`** : Lit la configuration **Caméra de recul / Sonar 360°**
- **`22200E`** : Lit les widgets **Climatisation / Ioniseur / Qualité d'air**

*(Pour revenir ensuite au calculateur moteur 29-bit normal dans Car Scanner, il suffit de quitter le terminal et de cliquer sur Connecter).*

---

## 2. Depuis votre PC Windows avec `espace5-can-explorer`

Nous avons ajouté l'option **`--scan-hmi`** qui automatise toute cette exploration sur l'Easy Link (`0x712`) et sur le Tableau de bord numérique Visteon (`0x743`) :

```powershell
# Tester en simulation sur PC
python scan_espace5.py --simulate --scan-hmi

# Lancer sur la voiture via le port COM du Vgate iCar Pro BLE
python scan_espace5.py --port COM4 --scan-hmi
```

---

## 3. Registres Internes Bosch A-IVI (`0x712`) Vérifiés en Direct sur le Véhicule

L'interrogation en direct du calculateur **Easy Link (`0x712` -> `0x732`, variante `B1`, SW `283C33813R`)** via le **Vgate iCar Pro BLE** a permis de lire l'état réel des paramètres internes suivants :

### A. Connectivité Sans Fil (`Wireless Android Auto & Apple CarPlay`)
- **État lu d'origine** : **`Désactivé`**
- **Flags système Linux / Bosch A-IVI associés** :
  - `Wireless_Android_Auto_function` (Android Auto sans fil)
  - `Bluetooth_function`
  - `Wireless_CarPlay_function` (Apple CarPlay sans fil)
  - `WiFi_IVC_tethering` (Partage de connexion Wi-Fi véhicule)
  - `Wifi_5GHz_support` (Support bande Wi-Fi 5 GHz requis pour le flux vidéo AA/CarPlay sans fil)
  - `Wifi_function` (Activation contrôleur WLAN interne)

### B. Verrouillage des Menus et de la Vidéo en Roulant (`Video in Motion` — 3 étapes)
- **État lu d'origine** : **`Activée` (Verrouillage actif en roulant)**
- **Paramètres système associés** :
  - **Step 1/3** : `Speed_lock_max_threshold_for_use_restriction` (Seuil de vitesse haut déclenchant le verrouillage IHM)
  - **Step 2/3** : `Speed_lock_min_threshold_for_use_restriction` (Seuil de vitesse bas libérant l'IHM)
  - **Step 3/3** : `Speed_lock_restrictions` (`Activée` = menus grisés/barrés et vidéo coupée en roulant ; `Désactivé` = IHM et vidéo déverrouillées en roulant)

### C. Autres Paramètres IHM & Audio Exposés sur `0x712`
- `BOSE sound improvement - step #1/3` & `step #2/3` (Profils DSP audio Bose)
- `4WD information display` (Affichage widget châssis / inclinomètre)
- `Climate area` & `Climate mode selection` (Widgets de climatisation à l'écran)
