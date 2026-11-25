"""Cartographie CAN réelle (Mixte 29-bit ISO 15765-4 ATSP7 + 11-bit ATSP6, 500 kbps)
pour Renault Espace V Phase 2 (2.0 Blue dCi M9R + Boîte EDC DW6 + Easy Link Bosch A-IVI)."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class EcuDefinition:
    """Définition d'un calculateur (ECU) sur le réseau CAN Renault Espace V Phase 2."""

    key: str
    code_renault: str
    name: str
    supplier_hint: str
    tx_id: str          # Ex: "18DA10F1" (29-bit) ou "712" (11-bit)
    rx_id: str          # Ex: "18DAF110" (29-bit) ou "732" (11-bit)
    can_bits: int = 11  # 29 (ATSP7) ou 11 (ATSP6)
    bus: str = "CAN-Primaire (Pins 6 & 14)"
    description: str = ""


@dataclass(frozen=True)
class DidDefinition:
    """Data Identifier (DID) UDS (Service 0x22 ReadDataByIdentifier)."""

    did: str  # 4-char hex, e.g. "F190"
    label: str
    encoding: str = "ascii"  # "ascii", "hex", "date_bcd"
    description: str = ""


# Cartographie des 16+ calculateurs validée sur Renault Espace V Phase 2 (2.0 Blue dCi - Millésime 2021)
ESPACE5_ECUS: List[EcuDefinition] = [
    # --- CALCULATEURS 29-BIT (ISO 15765-4 CAN 29-bit ID, 500 kbaud - ATSP7) ---
    EcuDefinition(
        key="ecm",
        code_renault="ECM / INJ",
        name="Unité de Contrôle Moteur 2.0 Blue dCi (ECM-EngineControl)",
        supplier_hint="Robert Bosch GmbH (MD1CS006)",
        tx_id="18DA10F1",
        rx_id="18DAF110",
        can_bits=29,
        description="Injection 2.0 Blue dCi (Pièce: 237101663S, SW: 237010816V, Cal: 237610818V, DiagVer: 8C)",
    ),
    EcuDefinition(
        key="tcm",
        code_renault="TCM / BVA",
        name="Unité de Commande Transmission EDC 6 rapports (TCM0-TRANSMISCTRL)",
        supplier_hint="GETRAG (6DCT450 / DW6)",
        tx_id="18DA18F1",
        rx_id="18DAF118",
        can_bits=29,
        description="Boîte auto double embrayage humide (Pièce: 310322081R, SW: 310392109R, HW: 310321915R, DiagVer: 0C)",
    ),
    EcuDefinition(
        key="udm",
        code_renault="UDM / SCR",
        name="Module de Dosage AdBlue / Urée (UDM-UreaDosingModule)",
        supplier_hint="PLASTIC OMNIUM",
        tx_id="18DAE1F1",
        rx_id="18DAF1E1",
        can_bits=29,
        description="Contrôle injection urée SCR (Pièce: 237G00329R, SW: 237G00556R, Cal: 237G80562R, DiagVer: 10)",
    ),
    EcuDefinition(
        key="abs",
        code_renault="ABS / ESC",
        name="Unité de Commande ABS / ESP (Freinage)",
        supplier_hint="CONTI (Continental)",
        tx_id="18DA2DF1",
        rx_id="18DAF12D",
        can_bits=29,
        description="Bloc hydraulique ABS/ESC (Pièce/SW: 476601440R, HW: 478514191R, Version: MLC70/11, DiagVer: 09)",
    ),
    EcuDefinition(
        key="hmd",
        code_renault="HMD / HUD",
        name="Affichage Tête Haute Motorisé (Head-Up Display)",
        supplier_hint="BT2",
        tx_id="18DA9BF1",
        rx_id="18DAF19B",
        can_bits=29,
        description="Afficheur tête haute (Pièce: 249416835R, SW: 249992983R, HW: 285J94233R, Version: R25/V20B01, DiagVer: 08)",
    ),
    EcuDefinition(
        key="sgw",
        code_renault="S-GW3",
        name="Passerelle de Sécurité CAN (Security Gateway Gen 3)",
        supplier_hint="B408 (Continental/Renault)",
        tx_id="18DAD1F1",
        rx_id="18DAF1D1",
        can_bits=29,
        description="Passerelle sécurité OBD/CAN (Pièce: 284Y66LE5C, HW: 285J96LA5D, SW: SWF007.0003.0032, DiagVer: 06)",
    ),
    # --- CALCULATEURS 11-BIT (ISO 15765-4 CAN 11-bit ID, 500 kbaud - ATSP6) ---
    EcuDefinition(
        key="easylink",
        code_renault="A-IVI / RadNav",
        name="Système Multimédia Easy Link 9.3\" (Multimedia system)",
        supplier_hint="BOSCH (AI_PRJ_RN_AIVI_24.1V19)",
        tx_id="712",
        rx_id="732",
        can_bits=11,
        description="Unité Easy Link Branche 2 (Pièce: 259159033R, SW: 283C33813R, Build: 6919_240710, HW: 285J95735R, DiagVer: B1)",
    ),
    EcuDefinition(
        key="tdb",
        code_renault="TDB / METER",
        name="Tableau de Bord Numérique (Dashboard / Instrument cluster)",
        supplier_hint="07-Visteon-Namestovo",
        tx_id="743",
        rx_id="763",
        can_bits=11,
        description="Combiné d'instruments TFT (Pièce: 248105110R, SW: 248B33935R, HW: 250465577R, V09.05, DiagVer: 12)",
    ),
    EcuDefinition(
        key="bcm",
        code_renault="UCH / BCM",
        name="Unité Centrale Habitacle (Body Control Module)",
        supplier_hint="CONTINENTAL AUTOMOTIVE",
        tx_id="745",
        rx_id="765",
        can_bits=11,
        description="Gestion habitacle (Pièce: 284B13925R, SW: 284B37713R, HW: 284B21462R, Soft: 142902, DiagVer: 90)",
    ),
    EcuDefinition(
        key="airbag",
        code_renault="SRS / AIRBAG",
        name="Calculateur Airbags & Prétensionneurs (SRS/Airbags)",
        supplier_hint="255414 (Autoliv / Continental)",
        tx_id="752",
        rx_id="772",
        can_bits=11,
        description="Sécurité passive (Pièce: 985102111R, SW: 285A42149R, HW: 285J93115R, Soft: S2_020OH.P72, DiagVer: 09)",
    ),
    EcuDefinition(
        key="eps",
        code_renault="DAE / EPS",
        name="Direction Assistée Électrique (Power steering)",
        supplier_hint="TRW",
        tx_id="742",
        rx_id="762",
        can_bits=11,
        description="Direction assistée (Pièce: 490044671R, SW: 285049500R, HW: 285007079R, Soft: S2RE03CD04)",
    ),
    EcuDefinition(
        key="hvac",
        code_renault="CLIM / HVAC",
        name="Climatisation & Chauffage (Heater & air conditioning)",
        supplier_hint="740 (Valeo)",
        tx_id="744",
        rx_id="764",
        can_bits=11,
        description="Climatisation automatique (Pièce: 285252812R, Soft: F007, Version: 1913, DiagVer: 04)",
    ),
    EcuDefinition(
        key="emm",
        code_renault="EMM / UPC",
        name="Module de Gestion d'Énergie 12V (Energy Management Module)",
        supplier_hint="414 (Continental)",
        tx_id="74D",
        rx_id="76D",
        can_bits=11,
        description="Pilotage charge batterie 12V ESM & Start/Stop (Soft: BA65, Version: 6560, DiagVer: 64)",
    ),
    EcuDefinition(
        key="sonar",
        code_renault="SONAR / UPA",
        name="Aide au Stationnement Ultrasons (Sonar)",
        supplier_hint="BOSCH3",
        tx_id="74E",
        rx_id="76E",
        can_bits=11,
        description="Radars de stationnement (Pièce: 284L00448R, SW: 284S92436R, HW: 285J97007R, Soft: 1270RS593P, DiagVer: 08)",
    ),
    EcuDefinition(
        key="hfm",
        code_renault="HFM / HANDS FREE",
        name="Module Carte Mains-Libres (Key hands free)",
        supplier_hint="CONTINENTAL",
        tx_id="792",
        rx_id="7B2",
        can_bits=11,
        description="Accès et démarrage mains-libres (Pièce: 285903089R, SW: 285J92452R, HW: 285E26475R, Soft: 142A02, DiagVer: 05)",
    ),
    EcuDefinition(
        key="tcu",
        code_renault="TCU / SOS",
        name="Module d'Appel d'Urgence SOS & Communication 4G (eCall / A-IVC)",
        supplier_hint="Continental",
        tx_id="77A",
        rx_id="75A",
        can_bits=11,
        description="Télématique 4G & bouton SOS (Pièce: 2591A9374R, SW: 282773501R, HW: 282A78506R, Soft: SW9, DiagVer: 04)",
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
        label="Référence Pièce Renault (Spare Part Number)",
        encoding="ascii",
        description="Référence pièce OEM Renault (ex: 259159033R pour Easy Link)",
    ),
    DidDefinition(
        did="F188",
        label="Référence Logicielle Renault (Manufacturer ECU Software Number)",
        encoding="ascii",
        description="Version logicielle Renault (ex: 283C33813R pour Easy Link, 237010816V pour ECM)",
    ),
    DidDefinition(
        did="F18A",
        label="Fournisseur Système (Supplier Code)",
        encoding="ascii",
        description="Code ou nom de l'équipementier (BOSCH, GETRAG, CONTI, VISTEON...)",
    ),
    DidDefinition(
        did="F191",
        label="Référence Matérielle Renault (Manufacturer ECU Hardware Number)",
        encoding="ascii",
        description="Référence matérielle Renault du boîtier électronique (ex: 285J95735R)",
    ),
    DidDefinition(
        did="F194",
        label="Identification Logicielle Interne (Soft Version / Project)",
        encoding="ascii",
        description="Nom de branche logicielle équipementier (ex: AI_PRJ_RN_AIVI_24.1V19)",
    ),
    DidDefinition(
        did="F195",
        label="Version / Build Logiciel (Version)",
        encoding="ascii",
        description="Version / Date de build interne (ex: 6919_240710 pour Easy Link compilé le 10/07/2024)",
    ),
    DidDefinition(
        did="F18C",
        label="Numéro de Série Calculateur (ECU Serial Number)",
        encoding="ascii",
        description="Numéro de série unitaire usine (contient souvent la date de fabrication AA-MM-JJ)",
    ),
    DidDefinition(
        did="F18B",
        label="Date de Fabrication Calculateur (Manufacturing Date)",
        encoding="date_bcd",
        description="Date de production usine du calculateur",
    ),
    DidDefinition(
        did="F198",
        label="Code Atelier / Outil Garage (Repair Shop / Tester Serial)",
        encoding="ascii",
        description="Identifiant de l'outil concessionnaire ayant programmé le calculateur",
    ),
    DidDefinition(
        did="F199",
        label="Date / Réf. de Programmation (Programming Date / Hex)",
        encoding="date_bcd",
        description="Date de reprogrammation ou référence matériel de base gravée à la programmation",
    ),
    DidDefinition(
        did="F1A0",
        label="Variante Diagnostic Renault (DiagVersion)",
        encoding="hex",
        description="Numéro de variante diagnostic Renault (ex: B1 pour Easy Link, 8C pour ECM)",
    ),
]
