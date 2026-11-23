# Rapport d'Exploration CAN / UDS - Renault Espace V Phase 2 (2.0 Blue dCi & Easy Link)

- **Date du scan** : `2026-11-23 14:48:59`
- **Interface** : `ELM327 v2.2 (Vgate iCar Pro BLE)` (SIMULATION ESPACE V 2.0 Blue dCi)
- **Tension Batterie 12V (ESM)** : `14.3V`
- **VIN détecté (DID F190)** : `VF1RFC00X66002021`
- **Calculateurs répondants** : **14 / 18**

## Synthèse des Calculateurs (ECUs)

| Code | Calculateur | TX/RX | Statut | Réf. Pièce (F187) | Version Logicielle (F195) | Fournisseur (F18A) |
|---|---|---|---|---|---|---|
| **ECM / INJ** | Injection Moteur 2.0 Blue dCi (M9R) | `7E0`/`7E8` | EN LIGNE | `237104892R` | `237105521R` | BOSCH |
| **TCM / BVA** | Boîte Automatique EDC 6 rapports (DW6) | `7E1`/`7E9` | EN LIGNE | `310321984R` | `310322105R` | GETRAG |
| **UDM / SCR** | Module Dépollution AdBlue (SCR) | `7E2`/`7EA` | EN LIGNE | `208993104R` | `208994412R` | BOSCH_SCR |
| **A-IVI / RadNav** | Système Multimédia Easy Link 9.3" | `712`/`732` | EN LIGNE | `283C36016R` | `283C36016R` | BOSCH_AIVI |
| **TDB / METER** | Tableau de Bord Numérique (Cockpit) | `743`/`763` | EN LIGNE | `248109452R` | `248109981R` | VISTEON |
| **UCH / BCM** | Unité Centrale Habitacle (BCM) | `745`/`765` | EN LIGNE | `284B17512R` | `284B18821R` | CONTI_BCM |
| **4WS / 4CONTROL** | Châssis 4 Roues Directrices (4Control) | `784`/`7A4` | EN LIGNE | `555014829R` | `555016011R` | AISIN_4WS |
| **AVS / SUSP** | Amortissement Piloté | `781`/`7A1` | EN LIGNE | `543028194R` | `543029004R` | KYB_AVS |
| **ABS / VDC / ESC** | Freinage ABS / ESP / Contrôle Trajectoire | `740`/`760` | EN LIGNE | `476607841R` | `476608912R` | ATE_CONTI |
| **DAE / EPS** | Direction Assistée Électrique | `742`/`762` | EN LIGNE | `491105612R` | `491106109R` | JTEKT |
| **CLIM / HVAC** | Climatisation Automatique | `744`/`764` | EN LIGNE | `275104821R` | `275105190R` | VALEO |
| **AIRBAG / SRS** | Calculateur Airbags & Prétensionneurs | `752`/`772` | Hors ligne / Non équipé | - | - | Autoliv / Continental |
| **FPA / EPB** | Frein de Parking Assisté Électrique | `755`/`775` | Hors ligne / Non équipé | - | - | TRW /ZF |
| **UPC / USM** | Unité de Protection et de Commutation (Compartiment Moteur) | `74D`/`76D` | Hors ligne / Non équipé | - | - | Continental |
| **AAU / AMP** | Amplificateur Audio Externe (Bose Surround) | `782`/`7A2` | EN LIGNE | `280634192R` | `280635011R` | BOSE_DSP |
| **FCAM / ADAS** | Caméra Frontale ADAS (Pare-brise) | `74B`/`76B` | EN LIGNE | `284G26182R` | `284G27901R` | VALEO_MOBILEYE |
| **FRAD / ACC** | Radar Frontal Régulateur Adaptatif (ACC) | `753`/`773` | EN LIGNE | `284387412R` | `284388109R` | BOSCH_FRAD |
| **HFM** | Module Mains-Libres (Accès & Démarrage) | `792`/`7B2` | Hors ligne / Non équipé | - | - | Continental |

## Détails UDS par Calculateur (Service 0x22 ReadDataByIdentifier)

### [ECM / INJ] Injection Moteur 2.0 Blue dCi (M9R) (`TX: 0x7E0` / `RX: 0x7E8`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `237104892R` *(Hex: `32333731303438393252`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `BOSCH` *(Hex: `424F534348`)*
  - **DID `0xF191` (Référence Matérielle (Hardware Number))** : `237100854R` *(Hex: `32333731303038353452`)*
  - **DID `0xF193` (Version Matérielle (Hardware Version))** : `H02` *(Hex: `483032`)*
  - **DID `0xF194` (Référence Logicielle (Software Number))** : `10SW063912` *(Hex: `31305357303633393132`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `237105521R` *(Hex: `32333731303535323152`)*
  - **DID `0xF188` (Calibration / Configuration Logicielle Renault)** : `237615521R` *(Hex: `32333736313535323152`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial))** : `BMD1CS0069941` *(Hex: `424D4431435330303639393431`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `54` *(Hex: `54`)*

### [TCM / BVA] Boîte Automatique EDC 6 rapports (DW6) (`TX: 0x7E1` / `RX: 0x7E9`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `310321984R` *(Hex: `33313033323139383452`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `GETRAG` *(Hex: `474554524147`)*
  - **DID `0xF191` (Référence Matérielle (Hardware Number))** : `310320742R` *(Hex: `33313033323037343252`)*
  - **DID `0xF194` (Référence Logicielle (Software Number))** : `DW6_P2_V18` *(Hex: `4457365F50325F563138`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `310322105R` *(Hex: `33313033323231303552`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial))** : `GT6DCT4502841` *(Hex: `47543644435434353032383431`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `1C` *(Hex: `1C`)*

### [UDM / SCR] Module Dépollution AdBlue (SCR) (`TX: 0x7E2` / `RX: 0x7EA`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `208993104R` *(Hex: `32303839393331303452`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `BOSCH_SCR` *(Hex: `424F5343485F534352`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `208994412R` *(Hex: `32303839393434313252`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `08` *(Hex: `08`)*

### [A-IVI / RadNav] Système Multimédia Easy Link 9.3" (`TX: 0x712` / `RX: 0x732`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (via passerelle) ou CAN-MM (Pins 12 & 13)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `283C36016R` *(Hex: `32383343333630313652`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `BOSCH_AIVI` *(Hex: `424F5343485F41495649`)*
  - **DID `0xF191` (Référence Matérielle (Hardware Number))** : `281158429R` *(Hex: `32383131353834323952`)*
  - **DID `0xF193` (Version Matérielle (Hardware Version))** : `GEN2.1` *(Hex: `47454E322E31`)*
  - **DID `0xF194` (Référence Logicielle (Software Number))** : `AIVI_LINUX_4.14` *(Hex: `414956495F4C494E55585F342E3134`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `283C36016R` *(Hex: `32383343333630313652`)*
  - **DID `0xF188` (Calibration / Configuration Logicielle Renault)** : `283C62148R` *(Hex: `32383343363231343852`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial))** : `AIVI93FR2021884` *(Hex: `414956493933465232303231383834`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `2A` *(Hex: `2A`)*

### [TDB / METER] Tableau de Bord Numérique (Cockpit) (`TX: 0x743` / `RX: 0x763`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `248109452R` *(Hex: `32343831303934353252`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `VISTEON` *(Hex: `56495354454F4E`)*
  - **DID `0xF191` (Référence Matérielle (Hardware Number))** : `248104110R` *(Hex: `32343831303431313052`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `248109981R` *(Hex: `32343831303939383152`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `19` *(Hex: `19`)*

### [UCH / BCM] Unité Centrale Habitacle (BCM) (`TX: 0x745` / `RX: 0x765`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `284B17512R` *(Hex: `32383442313735313252`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `CONTI_BCM` *(Hex: `434F4E54495F42434D`)*
  - **DID `0xF191` (Référence Matérielle (Hardware Number))** : `284B10984R` *(Hex: `32383442313039383452`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `284B18821R` *(Hex: `32383442313838323152`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `41` *(Hex: `41`)*

### [4WS / 4CONTROL] Châssis 4 Roues Directrices (4Control) (`TX: 0x784` / `RX: 0x7A4`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `555014829R` *(Hex: `35353530313438323952`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `AISIN_4WS` *(Hex: `414953494E5F345753`)*
  - **DID `0xF191` (Référence Matérielle (Hardware Number))** : `555011200R` *(Hex: `35353530313132303052`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `555016011R` *(Hex: `35353530313630313152`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `12` *(Hex: `12`)*

### [AVS / SUSP] Amortissement Piloté (`TX: 0x781` / `RX: 0x7A1`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `543028194R` *(Hex: `35343330323831393452`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `KYB_AVS` *(Hex: `4B59425F415653`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `543029004R` *(Hex: `35343330323930303452`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `0B` *(Hex: `0B`)*

### [ABS / VDC / ESC] Freinage ABS / ESP / Contrôle Trajectoire (`TX: 0x740` / `RX: 0x760`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `476607841R` *(Hex: `34373636303738343152`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `ATE_CONTI` *(Hex: `4154455F434F4E5449`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `476608912R` *(Hex: `34373636303839313252`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `23` *(Hex: `23`)*

### [DAE / EPS] Direction Assistée Électrique (`TX: 0x742` / `RX: 0x762`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `491105612R` *(Hex: `34393131303536313252`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `JTEKT` *(Hex: `4A54454B54`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `491106109R` *(Hex: `34393131303631303952`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `15` *(Hex: `15`)*

### [CLIM / HVAC] Climatisation Automatique (`TX: 0x744` / `RX: 0x764`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `275104821R` *(Hex: `32373531303438323152`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `VALEO` *(Hex: `56414C454F`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `275105190R` *(Hex: `32373531303531393052`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `0E` *(Hex: `0E`)*

### [AAU / AMP] Amplificateur Audio Externe (Bose Surround) (`TX: 0x782` / `RX: 0x7A2`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-MM / CAN-Primaire
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `280634192R` *(Hex: `32383036333431393252`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `BOSE_DSP` *(Hex: `424F53455F445350`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `280635011R` *(Hex: `32383036333530313152`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `07` *(Hex: `07`)*

### [FCAM / ADAS] Caméra Frontale ADAS (Pare-brise) (`TX: 0x74B` / `RX: 0x76B`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `284G26182R` *(Hex: `32383447323631383252`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `VALEO_MOBILEYE` *(Hex: `56414C454F5F4D4F42494C455945`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `284G27901R` *(Hex: `32383447323739303152`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `1A` *(Hex: `1A`)*

### [FRAD / ACC] Radar Frontal Régulateur Adaptatif (ACC) (`TX: 0x753` / `RX: 0x773`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-V / CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66002021` *(Hex: `5646315246433030583636303032303231`)*
  - **DID `0xF187` (Référence Pièce Renault (Part Number))** : `284387412R` *(Hex: `32383433383734313252`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier ID))** : `BOSCH_FRAD` *(Hex: `424F5343485F46524144`)*
  - **DID `0xF195` (Version Logicielle (Software Version))** : `284388109R` *(Hex: `32383433383831303952`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `14` *(Hex: `14`)*
