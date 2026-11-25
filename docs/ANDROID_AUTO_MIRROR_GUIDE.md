# Guide du Miroir d'Écran Smartphone & Tableau de Bord CAN sur l'Easy Link 9.3"

Ce guide explique comment exploiter l'écran vertical **9,3 pouces Easy Link (`283C33813R`)** de la Renault Espace V Phase 2 pour :
1. **Afficher les jauges CAN en direct** (FAP, pression différentielle, régénération, turbo, batterie 12V) via **Car Scanner** dans Android Auto,
2. **Dupliquer l'écran complet du smartphone Android (Mirroring)** sur l'écran 9,3" de la voiture via **`Fermata Mirror` / `FS Mirror`** (sans modifier ni démonter l'Easy Link).

---

## 1. Afficher le Tableau de Bord CAN en Direct (Déjà prêt avec Car Scanner)

L'application **Car Scanner ELM OBD2** installée sur votre téléphone intègre nativement un module **Android Auto** :
1. Branchez le **Vgate iCar Pro BLE** sous le volant et connectez **Car Scanner** sur le téléphone.
2. Branchez le téléphone en USB sur l'Espace 5 pour lancer **Android Auto**.
3. Sur l'écran 9,3" de la voiture, appuyez sur le bouton de la **grille d'applications Android Auto** (en bas à gauche) et ouvrez **Car Scanner**.
4. Vous pouvez faire défiler les pages de jauges en direct sur l'écran de la voiture (et personnaliser les jauges affichées depuis le menu `Tableau de bord` sur le téléphone : `Delta Pressure FAP`, `Température entrée FAP`, `Régénération en cours`, `Tension UCE`, etc.).

---

## 2. Activer le Mode Développeur d'Android Auto & le 1080p sur le Smartphone

Pour autoriser les applications de **Miroir d'écran (`Fermata Mirror` / `FS Mirror` / `Screen2Auto`)** et maximiser la résolution sur l'écran vertical 9,3" :

1. Sur votre smartphone Android : **Paramètres → Applications → Android Auto → Paramètres supplémentaires dans l'application**.
2. Faites défiler tout en bas et **tapez 10 fois sur `Version`** pour débloquer le mode développeur.
3. Appuyez sur le menu **`⋮`** en haut à droite → **`Paramètres pour les développeurs`** :
   - **Mode d'application** : Choisissez **`Développeur`**.
   - **Résolution vidéo** : Choisissez **`Autoriser jusqu'à 1080p`** (améliore nettement la finesse et l'espace vertical sur l'écran 9,3" Easy Link).
   - **Sources inconnues** (tout en bas) : **Cochez la case** (indispensable pour que `Fermata Mirror` apparaisse dans le lanceur Android Auto).

---

## 3. Installer `Fermata Mirror` / `FS Mirror` via ADB (Compatible Android 13 / 14 / 15 / 16)

Sur les versions récentes d'Android, Google Android Auto masque les applications de mirroring si elles n'ont pas été installées avec l'identifiant du Google Play Store (`com.android.vending`).

### Procédure avec notre script [`tools/install_android_mirror.bat`](../tools/install_android_mirror.bat) :

1. Téléchargez le fichier `.apk` officiel de **Fermata Auto** depuis les *Releases* GitHub du développeur (`https://github.com/AndreyPavlenko/Fermata/releases`).
2. Activez le **Débogage USB** sur votre smartphone Android et branchez-le à votre PC Windows.
3. Glissez-déposez le fichier `.apk` sur **`tools\install_android_mirror.bat`** (ou exécutez en ligne de commande) :
   ```powershell
   adb install -r -i "com.android.vending" fermata-auto.apk
   ```
4. Sur votre téléphone, ouvrez une première fois l'application **Fermata Auto** pour lui accorder l'autorisation de capture d'écran (`MediaProjection`) et, si souhaité, le service d'accessibilité.
5. Dans Android Auto sur votre téléphone (`Personnaliser le lanceur`), vérifiez que **`Fermata Mirror`** et **`FS Mirror`** (Full Screen Mirror) sont bien cochés : ils s'afficheront désormais sur l'écran 9,3" de votre Espace 5 !
