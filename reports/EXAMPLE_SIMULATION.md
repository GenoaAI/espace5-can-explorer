# Rapport d'Exploration CAN / UDS - Renault Espace V Phase 2 (2.0 Blue dCi & Easy Link)

- **Date du scan** : `2026-11-25 10:33:21`
- **Interface** : `ELM327 v2.2 (Vgate iCar Pro BLE)` (SIMULATION ESPACE V 2.0 Blue dCi)
- **Tension Batterie 12V (ESM)** : `14.2V`
- **VIN détecté (DID F190)** : `VF1RFC00X66XXXXXX`
- **Calculateurs répondants** : **16 / 16**

## Synthèse des Calculateurs (ECUs)

| Code | Calculateur | TX/RX | Statut | Réf. Pièce (F187) | Version Logicielle (F195) | Dernière Prog. (F199) | Fournisseur (F18A) |
|---|---|---|---|---|---|---|---|
| **ECM / INJ** | Unité de Contrôle Moteur 2.0 Blue dCi (ECM-EngineControl) | `18DA10F1`/`18DAF110` | EN LIGNE | `237101663S` | `237010816V` | `237101663S` | Robert Bosch GmbH (037) |
| **TCM / BVA** | Unité de Commande Transmission EDC 6 rapports (TCM0-TRANSMISCTRL) | `18DA18F1`/`18DAF118` | EN LIGNE | `310322081R` | `310392109R` | `310321915R` | GETRAG |
| **UDM / SCR** | Module de Dosage AdBlue / Urée (UDM-UreaDosingModule) | `18DAE1F1`/`18DAF1E1` | EN LIGNE | `237G00329R` | `237G00556R` | `285J97945R` | PLASTIC OMNIUM |
| **ABS / ESC** | Unité de Commande ABS / ESP (Freinage) | `18DA2DF1`/`18DAF12D` | EN LIGNE | `476601440R` | `476601440R` | `478514191R` | CONTI |
| **HMD / HUD** | Affichage Tête Haute Motorisé (Head-Up Display) | `18DA9BF1`/`18DAF19B` | EN LIGNE | `249416835R` | `249992983R` | `285J94233R` | BT2 |
| **S-GW3** | Passerelle de Sécurité CAN (Security Gateway Gen 3) | `18DAD1F1`/`18DAF1D1` | EN LIGNE | `284Y66LE5C` | `SWF007.0003.0032` | `285J96LA5D` | B408 |
| **A-IVI / RadNav** | Système Multimédia Easy Link 9.3" (Multimedia system) | `712`/`732` | EN LIGNE | `259159033R` | `283C33813R` | `285J95735R` | BOSCH |
| **TDB / METER** | Tableau de Bord Numérique (Dashboard / Instrument cluster) | `743`/`763` | EN LIGNE | `248105110R` | `248B33935R` | `250465577R` | 07-Visteon-Namestovo |
| **UCH / BCM** | Unité Centrale Habitacle (Body Control Module) | `745`/`765` | EN LIGNE | `284B13925R` | `284B37713R` | `284B21462R` | CONTINENTAL AUTOMOTIVE |
| **SRS / AIRBAG** | Calculateur Airbags & Prétensionneurs (SRS/Airbags) | `752`/`772` | EN LIGNE | `985102111R` | `285A42149R` | `285J93115R` | 255414 |
| **DAE / EPS** | Direction Assistée Électrique (Power steering) | `742`/`762` | EN LIGNE | `490044671R` | `285049500R` | `285007079R` | TRW |
| **CLIM / HVAC** | Climatisation & Chauffage (Heater & air conditioning) | `744`/`764` | EN LIGNE | `285252812R` | `1913` | - | 740 (Valeo) |
| **EMM / UPC** | Module de Gestion d'Énergie 12V (Energy Management Module) | `74D`/`76D` | EN LIGNE | - | `6560` | - | 414 (Continental) |
| **SONAR / UPA** | Aide au Stationnement Ultrasons (Sonar) | `74E`/`76E` | EN LIGNE | `284L00448R` | `284S92436R` | `285J97007R` | BOSCH3 |
| **HFM / HANDS FREE** | Module Carte Mains-Libres (Key hands free) | `792`/`7B2` | EN LIGNE | `285903089R` | `285J92452R` | `285E26475R` | CONTINENTAL |
| **TCU / SOS** | Module d'Appel d'Urgence SOS & Communication 4G (eCall / A-IVC) | `77A`/`75A` | EN LIGNE | `2591A9374R` | `282773501R` | `282A78506R` | Continental |

## Détails UDS par Calculateur (Service 0x22 ReadDataByIdentifier)

### [ECM / INJ] Unité de Contrôle Moteur 2.0 Blue dCi (ECM-EngineControl) (`TX: 0x18DA10F1` / `RX: 0x18DAF110`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `237101663S` *(Hex: `32333731303136363353`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `237010816V` *(Hex: `32333730313038313656`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `Robert Bosch GmbH (037)` *(Hex: `526F6265727420426F73636820476D6248202830333729`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `237101663S` *(Hex: `32333731303136363353`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `7A00` *(Hex: `37413030`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `6K00 (Cal: 237610818V)` *(Hex: `364B3030202843616C3A203233373631303831385629`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `94840016201222090737` *(Hex: `3934383430303136323031323232303930373337`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `237101663S` *(Hex: `32333731303136363353`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `8C` *(Hex: `8C`)*

### [TCM / BVA] Unité de Commande Transmission EDC 6 rapports (TCM0-TRANSMISCTRL) (`TX: 0x18DA18F1` / `RX: 0x18DAF118`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `310322081R` *(Hex: `33313033323230383152`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `310392109R` *(Hex: `33313033393231303952`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `GETRAG` *(Hex: `474554524147`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `310321915R` *(Hex: `33313033323139313552`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `2541` *(Hex: `32353431`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `8210` *(Hex: `38323130`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `200821191214` *(Hex: `323030383231313931323134`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `310321915R` *(Hex: `33313033323139313552`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `0C` *(Hex: `0C`)*

### [UDM / SCR] Module de Dosage AdBlue / Urée (UDM-UreaDosingModule) (`TX: 0x18DAE1F1` / `RX: 0x18DAF1E1`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `237G00329R` *(Hex: `32333747303033323952`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `237G00556R` *(Hex: `32333747303035353652`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `PLASTIC OMNIUM` *(Hex: `504C4153544943204F4D4E49554D`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `285J97945R` *(Hex: `3238354A393739343552`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `9000` *(Hex: `39303030`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `F04 (Cal: 237G80562R)` *(Hex: `463034202843616C3A203233374738303536325229`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `0000000002110564` *(Hex: `30303030303030303032313130353634`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `285J97945R` *(Hex: `3238354A393739343552`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `10` *(Hex: `10`)*

### [ABS / ESC] Unité de Commande ABS / ESP (Freinage) (`TX: 0x18DA2DF1` / `RX: 0x18DAF12D`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `476601440R` *(Hex: `34373636303134343052`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `476601440R` *(Hex: `34373636303134343052`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `CONTI` *(Hex: `434F4E5449`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `478514191R` *(Hex: `34373835313431393152`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `HPIPB` *(Hex: `4850495042`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `N52CG001812 - MLC70/11` *(Hex: `4E35324347303031383132202D204D4C4337302F3131`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `16717150062080100079` *(Hex: `3136373137313530303632303830313030303739`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `478514191R` *(Hex: `34373835313431393152`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `09` *(Hex: `09`)*

### [HMD / HUD] Affichage Tête Haute Motorisé (Head-Up Display) (`TX: 0x18DA9BF1` / `RX: 0x18DAF19B`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `249416835R` *(Hex: `32343934313638333552`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `249992983R` *(Hex: `32343939393239383352`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `BT2` *(Hex: `425432`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `285J94233R` *(Hex: `3238354A393432333352`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `R25` *(Hex: `523235`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `V20B01` *(Hex: `563230423031`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `00000000000000004251` *(Hex: `3030303030303030303030303030303034323531`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `285J94233R` *(Hex: `3238354A393432333352`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `08` *(Hex: `08`)*

### [S-GW3] Passerelle de Sécurité CAN (Security Gateway Gen 3) (`TX: 0x18DAD1F1` / `RX: 0x18DAF1D1`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `284Y66LE5C` *(Hex: `3238345936364C453543`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `SWF007.0003.0032` *(Hex: `5357463030372E303030332E30303332`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `B408` *(Hex: `42343038`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `285J96LA5D` *(Hex: `3238354A39364C413544`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `F005VT1793` *(Hex: `46303035565431373933`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `SWF007.0003.0032` *(Hex: `5357463030372E303030332E30303332`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `3712001436502C200720` *(Hex: `3337313230303134333635303243323030373230`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `285J96LA5D` *(Hex: `3238354A39364C413544`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `06` *(Hex: `06`)*

### [A-IVI / RadNav] Système Multimédia Easy Link 9.3" (Multimedia system) (`TX: 0x712` / `RX: 0x732`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `259159033R` *(Hex: `32353931353930333352`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `283C33813R` *(Hex: `32383343333338313352`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `BOSCH` *(Hex: `424F534348`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `285J95735R` *(Hex: `3238354A393537333552`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `AI_PRJ_RN_AIVI_24.1V19` *(Hex: `41495F50524A5F524E5F414956495F32342E31563139`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `6919_240710` *(Hex: `363931395F323430373130`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `00000002BG0048M` *(Hex: `30303030303030324247303034384D`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `285J95735R` *(Hex: `3238354A393537333552`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `B1` *(Hex: `B1`)*

### [TDB / METER] Tableau de Bord Numérique (Dashboard / Instrument cluster) (`TX: 0x743` / `RX: 0x763`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `248105110R` *(Hex: `32343831303531313052`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `248B33935R` *(Hex: `32343842333339333552`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `07-Visteon-Namestovo` *(Hex: `30372D56697374656F6E2D4E616D6573746F766F`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `250465577R` *(Hex: `32353034363535373752`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `V09.05` *(Hex: `5630392E3035`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `2006` *(Hex: `32303036`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `20_09_11__0044923786` *(Hex: `32305F30395F31315F5F30303434393233373836`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `250465577R` *(Hex: `32353034363535373752`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `12` *(Hex: `12`)*

### [UCH / BCM] Unité Centrale Habitacle (Body Control Module) (`TX: 0x745` / `RX: 0x765`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `284B13925R` *(Hex: `32383442313339323552`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `284B37713R` *(Hex: `32383442333737313352`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `CONTINENTAL AUTOMOTIVE` *(Hex: `434F4E54494E454E54414C204155544F4D4F54495645`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `284B21462R` *(Hex: `32383442323134363252`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `142902` *(Hex: `313432393032`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `0710` *(Hex: `30373130`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `0403426653` *(Hex: `30343033343236363533`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `284B21462R` *(Hex: `32383442323134363252`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `90` *(Hex: `90`)*

### [SRS / AIRBAG] Calculateur Airbags & Prétensionneurs (SRS/Airbags) (`TX: 0x752` / `RX: 0x772`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `985102111R` *(Hex: `39383531303231313152`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `285A42149R` *(Hex: `32383541343231343952`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `255414` *(Hex: `323535343134`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `285J93115R` *(Hex: `3238354A393331313552`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `S2_020OH.P72` *(Hex: `53325F3032304F482E503732`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `P72` *(Hex: `503732`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `U253JiD0045` *(Hex: `553235334A694430303435`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `285J93115R` *(Hex: `3238354A393331313552`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `09` *(Hex: `09`)*

### [DAE / EPS] Direction Assistée Électrique (Power steering) (`TX: 0x742` / `RX: 0x762`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `490044671R` *(Hex: `34393030343436373152`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `285049500R` *(Hex: `32383530343935303052`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `TRW` *(Hex: `545257`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `285007079R` *(Hex: `32383530303730373952`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `S2RE03CD04` *(Hex: `53325245303343443034`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `S2RE03CD04` *(Hex: `53325245303343443034`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `20267D840AN0530` *(Hex: `323032363744383430414E30353330`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `285007079R` *(Hex: `32383530303730373952`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `26` *(Hex: `26`)*

### [CLIM / HVAC] Climatisation & Chauffage (Heater & air conditioning) (`TX: 0x744` / `RX: 0x764`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `285252812R` *(Hex: `32383532353238313252`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `740 (Valeo)` *(Hex: `373430202856616C656F29`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `F007` *(Hex: `46303037`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `1913` *(Hex: `31393133`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `04` *(Hex: `04`)*

### [EMM / UPC] Module de Gestion d'Énergie 12V (Energy Management Module) (`TX: 0x74D` / `RX: 0x76D`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `414 (Continental)` *(Hex: `3431342028436F6E74696E656E74616C29`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `BA65` *(Hex: `42413635`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `6560` *(Hex: `36353630`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `64` *(Hex: `64`)*

### [SONAR / UPA] Aide au Stationnement Ultrasons (Sonar) (`TX: 0x74E` / `RX: 0x76E`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `284L00448R` *(Hex: `3238344C303034343852`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `284S92436R` *(Hex: `32383453393234333652`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `BOSCH3` *(Hex: `424F53434833`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `285J97007R` *(Hex: `3238354A393730303752`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `1270RS593P` *(Hex: `31323730525335393350`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `1270RS593P_S1.144.1.4` *(Hex: `313237305253353933505F53312E3134342E312E34`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `2008270748` *(Hex: `32303038323730373438`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `285J97007R` *(Hex: `3238354A393730303752`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `08` *(Hex: `08`)*

### [HFM / HANDS FREE] Module Carte Mains-Libres (Key hands free) (`TX: 0x792` / `RX: 0x7B2`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `285903089R` *(Hex: `32383539303330383952`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `285J92452R` *(Hex: `3238354A393234353252`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `CONTINENTAL` *(Hex: `434F4E54494E454E54414C`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `285E26475R` *(Hex: `32383545323634373552`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `142A02` *(Hex: `313432413032`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `0630` *(Hex: `30363330`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `0500486047` *(Hex: `30353030343836303437`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `285E26475R` *(Hex: `32383545323634373552`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `05` *(Hex: `05`)*

### [TCU / SOS] Module d'Appel d'Urgence SOS & Communication 4G (eCall / A-IVC) (`TX: 0x77A` / `RX: 0x75A`)
- **Session Diagnostic** : `ExtendedDiagnosticSession (0x10 0x03)`
- **Bus CAN** : CAN-Primaire (Pins 6 & 14)
  - **DID `0xF190` (VIN (Numéro de châssis))** : `VF1RFC00X66XXXXXX` *(Hex: `5646315246433030583636585858585858`)*
  - **DID `0xF187` (Référence Pièce Renault (Spare Part Number))** : `2591A9374R` *(Hex: `32353931413933373452`)*
  - **DID `0xF188` (Référence Logicielle Renault (Manufacturer ECU Software Number))** : `282773501R` *(Hex: `32383237373335303152`)*
  - **DID `0xF18A` (Fournisseur Système (Supplier Code))** : `Continental` *(Hex: `436F6E74696E656E74616C`)*
  - **DID `0xF191` (Référence Matérielle Renault (Manufacturer ECU Hardware Number))** : `282A78506R` *(Hex: `32383241373835303652`)*
  - **DID `0xF194` (Identification Logicielle Interne (Soft Version / Project))** : `SW9` *(Hex: `535739`)*
  - **DID `0xF195` (Version / Build Logiciel (Version))** : `SW9` *(Hex: `535739`)*
  - **DID `0xF18C` (Numéro de Série Calculateur (ECU Serial Number))** : `200701202037888806` *(Hex: `323030373031323032303337383838383036`)*
  - **DID `0xF199` (Date / Réf. de Programmation (Programming Date / Hex))** : `282A78506R` *(Hex: `32383241373835303652`)*
  - **DID `0xF1A0` (Variante Diagnostic Renault (DiagVersion))** : `04` *(Hex: `04`)*
