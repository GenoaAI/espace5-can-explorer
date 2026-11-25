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

## 3. Ce que permet la variante `B1` (`283C33813R`) sur l'affichage Android Auto & l'IHM

1. **Android Auto Sans Fil (Wireless Android Auto via Wi-Fi 5 GHz)** :
   - Sur les unités Bosch A-IVI Branche 2 (`259159033R`) mises à jour en **`283C33813R`**, la pile logicielle Linux (`AI_PRJ_RN_AIVI_24.1V19`) supporte nativement **Android Auto Sans Fil** et **Apple CarPlay Sans Fil**.
   - Si le menu Wi-Fi n'apparaît pas encore dans `Réglages -> Système -> Gestionnaire d'appareils`, c'est uniquement parce que les bits `Wireless AA` / `WLAN 5GHz` sont à `0` dans la configuration du calculateur `0x712`.
2. **Plein Écran Vertical Android Auto (Coolwalk)** :
   - Le firmware `283C33813R` alloue une surface d'affichage agrandie à Android Auto.
   - Pour maximiser l'espace vertical et supprimer les barres inutiles, activez le **Mode Développeur d'Android Auto** sur le smartphone Android (`Paramètres -> Applications -> Android Auto -> Tapez 10 fois sur Version -> Menu ⋮ -> Paramètres pour les développeurs -> Résolution vidéo : Autoriser jusqu'à 1080p`).
3. **Architecture de Sécurité (`S-GW3`) pour l'écriture (`0x2E`)** :
   - **Lecture (`0x22`)** : 100 % libre via la prise OBD sous le volant avec le Vgate iCar Pro BLE.
   - **Écriture (`0x2E WriteDataByIdentifier`)** : Filtrée par la passerelle **`S-GW3` (`284Y66LE5C`)** si on passe par la prise OBD sous le volant. Pour modifier un octet dans l'Easy Link (`0x712`) ou le Compteur (`0x743`) avec *DDT4ALL*, il faut soit utiliser un adaptateur *SGW Bypass*, soit se connecter directement sur le bus **CAN Multimédia** derrière l'écran.
