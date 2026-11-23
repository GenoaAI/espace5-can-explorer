"""Cartographie CAN (500 kbps, 11-bit) et identifiants UDS (ISO-14229) pour Renault Espace V Phase 2."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class EcuDefinition:
    """Définition d'un calculateur (ECU) sur le réseau CAN Renault Espace V Phase 2."""

    key: str
    code_renault: str
    name: str
    supplier_hint: str
    tx_id: str  # Hex string, e.g. "7E0"
    rx_id: str  # Hex string, e.g. "7E8"
    bus: str = "CAN-V / CAN-Primaire (Pins 6 & 14)"
    description: str = ""


@dataclass(frozen=True)
class DidDefinition:
    """Data Identifier (DID) UDS (Service 0x22 ReadDataByIdentifier)."""

    did: str  # 4-char hex, e.g. "F190"
    label: str
    encoding: str = "ascii"  # "ascii", "hex", "mixed"
    description: str = ""


# Liste des principaux calculateurs multiplexés de la Renault Espace V Phase 2 (2.0 Blue dCi + Easy Link)
ESPACE5_ECUS: List[EcuDefinition] = [
    EcuDefinition(
        key="ecm",
        code_renault="ECM / INJ",
        name="Injection Moteur 2.0 Blue dCi (M9R)",
        supplier_hint="Bosch MD1CS006",
        tx_id="7E0",
        rx_id="7E8",
        description="Calculateur contrôle moteur 2.0 Blue dCi (injection, turbo, FAP, EGR)",
    ),
    EcuDefinition(
        key="tcm",
        code_renault="TCM / BVA",
        name="Boîte Automatique EDC 6 rapports (DW6)",
        supplier_hint="Getrag 6DCT450 (DW6)",
        tx_id="7E1",
        rx_id="7E9",
        description="Double embrayage humide 6 rapports",
    ),
    EcuDefinition(
        key="scr",
        code_renault="UDM / SCR",
        name="Module Dépollution AdBlue (SCR)",
        supplier_hint="Bosch Denoxtronic",
        tx_id="7E2",
        rx_id="7EA",
        description="Gestion dosage urée AdBlue / réduction catalytique sélective",
    ),
    EcuDefinition(
        key="easylink",
        code_renault="A-IVI / RadNav",
        name="Système Multimédia Easy Link 9.3\"",
        supplier_hint="Bosch Automotive Multimedia (Linux / A-IVI)",
        tx_id="712",
        rx_id="732",
        bus="CAN-Primaire (via passerelle) ou CAN-MM (Pins 12 & 13)",
        description="Unité centrale multimédia Easy Link, Navigation, Android Auto / CarPlay",
    ),
    EcuDefinition(
        key="tdb",
        code_renault="TDB / METER",
        name="Tableau de Bord Numérique (Cockpit)",
        supplier_hint="Visteon / Continental",
        tx_id="743",
        rx_id="763",
        description="Afficheur compteur numérique TFT, odomètre, alertes tableau de bord",
    ),
    EcuDefinition(
        key="uch",
        code_renault="UCH / BCM",
        name="Unité Centrale Habitacle (BCM)",
        supplier_hint="Continental",
        tx_id="745",
        rx_id="765",
        description="Gestion carrosserie, carte mains-libres, ouvrants, essuie-glaces, éclairage intérieur",
    ),
    EcuDefinition(
        key="4control",
        code_renault="4WS / 4CONTROL",
        name="Châssis 4 Roues Directrices (4Control)",
        supplier_hint="Renault / Aisin",
        tx_id="784",
        rx_id="7A4",
        description="Actionneur de braquage train arrière selon vitesse et mode Multi-Sense",
    ),
    EcuDefinition(
        key="avs",
        code_renault="AVS / SUSP",
        name="Amortissement Piloté",
        supplier_hint="KYB / Monroe",
        tx_id="781",
        rx_id="7A1",
        description="Gestion électronique en continu des 4 amortisseurs (Multi-Sense)",
    ),
    EcuDefinition(
        key="abs",
        code_renault="ABS / VDC / ESC",
        name="Freinage ABS / ESP / Contrôle Trajectoire",
        supplier_hint="ATE / Continental",
        tx_id="740",
        rx_id="760",
        description="Bloc hydraulique ABS/ESP, aide au démarrage en côte, freinage actif",
    ),
    EcuDefinition(
        key="eps",
        code_renault="DAE / EPS",
        name="Direction Assistée Électrique",
        supplier_hint="JTEKT / NSK",
        tx_id="742",
        rx_id="762",
        description="Assistance de direction variable et Easy Park Assist",
    ),
    EcuDefinition(
        key="hvac",
        code_renault="CLIM / HVAC",
        name="Climatisation Automatique",
        supplier_hint="Valeo",
        tx_id="744",
        rx_id="764",
        description="Régulation thermique habitacle avant/arrière",
    ),
    EcuDefinition(
        key="airbag",
        code_renault="AIRBAG / SRS",
        name="Calculateur Airbags & Prétensionneurs",
        supplier_hint="Autoliv / Continental",
        tx_id="752",
        rx_id="772",
        description="Sécurité passive, airbags et capteurs de choc",
    ),
    EcuDefinition(
        key="epb",
        code_renault="FPA / EPB",
        name="Frein de Parking Assisté Électrique",
        supplier_hint="TRW /ZF",
        tx_id="755",
        rx_id="775",
        description="Commande des étriers électriques arrière et Auto-Hold",
    ),
    EcuDefinition(
        key="usm",
        code_renault="UPC / USM",
        name="Unité de Protection et de Commutation (Compartiment Moteur)",
        supplier_hint="Continental",
        tx_id="74D",
        rx_id="76D",
        description="Distribution électrique moteur, gestion alternateur piloté ESM (12V)",
    ),
    EcuDefinition(
        key="bose",
        code_renault="AAU / AMP",
        name="Amplificateur Audio Externe (Bose Surround)",
        supplier_hint="Bose Automotive",
        tx_id="782",
        rx_id="7A2",
        bus="CAN-MM / CAN-Primaire",
        description="Traitement numérique DSP et amplification multi-canaux Bose",
    ),
    EcuDefinition(
        key="fcam",
        code_renault="FCAM / ADAS",
        name="Caméra Frontale ADAS (Pare-brise)",
        supplier_hint="Valeo / Mobileye",
        tx_id="74B",
        rx_id="76B",
        description="Lecture des panneaux, maintien de voie, permutation feux Matrix LED",
    ),
    EcuDefinition(
        key="frad",
        code_renault="FRAD / ACC",
        name="Radar Frontal Régulateur Adaptatif (ACC)",
        supplier_hint="Bosch",
        tx_id="753",
        rx_id="773",
        description="Régulateur adaptatif Stop & Go et freinage d'urgence AEBS",
    ),
    EcuDefinition(
        key="hfm",
        code_renault="HFM",
        name="Module Mains-Libres (Accès & Démarrage)",
        supplier_hint="Continental",
        tx_id="792",
        rx_id="7B2",
        description="Antennes de détection carte Renault Mains-Libres",
    ),
]

ECU_BY_KEY: Dict[str, EcuDefinition] = {ecu.key: ecu for ecu in ESPACE5_ECUS}


# DIDs UDS standardisés ISO-14229-1 + extensions Renault (Service 0x22)
STANDARD_IDENTIFICATION_DIDS: List[DidDefinition] = [
    DidDefinition(
        did="F190",
        label="VIN (Numéro de châssis)",
        encoding="ascii",
        description="Numéro de série à 17 caractères du véhicule (VF1RFC...)",
    ),
    DidDefinition(
        did="F187",
        label="Référence Pièce Renault (Part Number)",
        encoding="ascii",
        description="Référence OEM Renault à 10 caractères (ex: 283C34951R pour Easy Link)",
    ),
    DidDefinition(
        did="F18A",
        label="Fournisseur Système (Supplier ID)",
        encoding="ascii",
        description="Code ou nom de l'équipementier (BOSCH, CONTI, VALEO, GETRAG...)",
    ),
    DidDefinition(
        did="F191",
        label="Référence Matérielle (Hardware Number)",
        encoding="ascii",
        description="Référence matérielle du boîtier électronique",
    ),
    DidDefinition(
        did="F193",
        label="Version Matérielle (Hardware Version)",
        encoding="ascii",
        description="Indice de révision matérielle PCB",
    ),
    DidDefinition(
        did="F194",
        label="Référence Logicielle (Software Number)",
        encoding="ascii",
        description="Numéro de programme/firmware interne équipementier",
    ),
    DidDefinition(
        did="F195",
        label="Version Logicielle (Software Version)",
        encoding="ascii",
        description="Version du firmware en cours d'exécution (ex: SW 283C36016R)",
    ),
    DidDefinition(
        did="F188",
        label="Calibration / Configuration Logicielle Renault",
        encoding="ascii",
        description="Identifiant de calibration ou de configuration véhicule",
    ),
    DidDefinition(
        did="F18C",
        label="Numéro de Série Calculateur (ECU Serial)",
        encoding="ascii",
        description="Numéro de série unitaire usine du calculateur",
    ),
    DidDefinition(
        did="F1A0",
        label="Variante Diagnostic Renault (DiagVersion)",
        encoding="hex",
        description="Numéro de variante diagnostic Renault (utilisé par CLIP / PyRen / DDT4ALL)",
    ),
]
