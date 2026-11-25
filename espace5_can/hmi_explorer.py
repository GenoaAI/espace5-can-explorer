"""Explorateur des registres de configuration IHM & Connectivité (UDS Service 0x22)
pour le système multimédia Bosch Easy Link 9.3" (0x712 -> 0x732, DiagVer B1, SW 283C33813R)
et le Tableau de Bord Numérique Visteon (0x743 -> 0x763)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Callable, Dict, List, Optional

from .ecus import ECU_BY_KEY, DidDefinition, EcuDefinition
from .uds_scanner import DidValue, Espace5UdsScanner


# Registres DIDs UDS connus sur Bosch A-IVI (Easy Link 0x712) pour l'IHM et la connectivité
EASYLINK_HMI_DIDS: List[DidDefinition] = [
    # Identification & Variantes Système Linux Bosch A-IVI
    DidDefinition("F187", "Référence Matérielle Unité Easy Link", "ascii"),
    DidDefinition("F188", "Version Logicielle Renault (SW 283C...)", "ascii"),
    DidDefinition("F194", "Branche Projet Logiciel Bosch A-IVI", "ascii"),
    DidDefinition("F195", "Numéro de Build & Date Compilation (6919_YYMMDD)", "ascii"),
    DidDefinition("F1A0", "Variante Diagnostic (DiagVersion)", "hex"),
    # Blocs de configuration IHM / Smartphone / Connectivité (Bosch A-IVI / RadNav)
    DidDefinition(
        "2001",
        "Configuration Connectivité Smartphone (Android Auto / CarPlay / Mirroring)",
        "hex",
        "Octets d'activation CarPlay USB/Wireless et Android Auto USB/Wireless (Wi-Fi 5 GHz)",
    ),
    DidDefinition(
        "2002",
        "Configuration Module Wi-Fi Interne & Point d'Accès (WLAN 2.4 / 5 GHz)",
        "hex",
        "État d'activation du contrôleur Wi-Fi interne de l'unité Bosch A-IVI",
    ),
    DidDefinition(
        "2003",
        "Configuration Thème IHM, Séquence d'Accueil & Marque (Welcome / Brand / Initiale)",
        "hex",
        "Animation et son d'accueil (Renault, Initiale Paris, RS, Alpine) et palette couleurs",
    ),
    DidDefinition(
        "2006",
        "Configuration Multi-Sense & Éclairage d'Ambiance IHM",
        "hex",
        "Modes Multi-Sense affichés à l'écran (MySense, Sport, Eco, Comfort) et zones LED",
    ),
    DidDefinition(
        "2008",
        "Configuration Architecture Audio (Bose DSP / Arkamys / Canaux)",
        "hex",
        "Sélection amplificateur externe Bose vs interne et profils d'égalisation",
    ),
    DidDefinition(
        "200B",
        "Configuration Aides au Stationnement & Caméras (Recul / 360° / Easy Park)",
        "hex",
        "Affichage gabarits dynamiques caméra et vue capteurs 360° sur l'écran 9.3\"",
    ),
    DidDefinition(
        "200E",
        "Configuration Widgets Climatisation, Qualité d'Air & Ioniseur",
        "hex",
        "Bandeau de rappel climatisation, purificateur/ioniseur et sièges chauffants/massants",
    ),
    DidDefinition(
        "2010",
        "Restrictions IHM en Roulant (Driving Eco2 / Verrouillage Menus Vitesse)",
        "hex",
        "Paramètres d'affichage Eco2 et seuils de verrouillage de sécurité en roulant",
    ),
]


# Registres DIDs UDS connus sur le Tableau de Bord Numérique Visteon (0x743)
DASHBOARD_HMI_DIDS: List[DidDefinition] = [
    DidDefinition("F187", "Référence Pièce Tableau de Bord Visteon", "ascii"),
    DidDefinition("F188", "Version Logicielle Tableau de Bord", "ascii"),
    DidDefinition("F194", "Version Application Interne Visteon", "ascii"),
    DidDefinition("F1A0", "Variante Diagnostic (DiagVersion)", "hex"),
    DidDefinition(
        "3001",
        "Configuration Styles Graphiques & Thèmes Compteur TFT",
        "hex",
        "Sélection des 4 styles d'affichage du combiné numérique liés au Multi-Sense",
    ),
    DidDefinition(
        "3004",
        "Configuration Widgets & Jauges Compteur (AdBlue, Boussole, Couple/Puissance, Nav)",
        "hex",
        "Activation des pages d'informations secondaires sur l'écran conducteur",
    ),
]


@dataclass
class HmiConfigParameter:
    """Paramètre IHM décodé à partir d'un registre DID de l'Easy Link ou du Tableau de bord."""

    did: str
    parameter_name: str
    raw_hex: str
    current_state: str
    details: str


def decode_easylink_hmi_dids(dids: Dict[str, DidValue]) -> List[HmiConfigParameter]:
    """Interprète les octets des registres de configuration IHM de l'Easy Link (0x712)."""
    decoded_params: List[HmiConfigParameter] = []

    # 1. Analyse Connectivité Smartphone (DID 0x2001)
    if "2001" in dids:
        raw = bytes.fromhex(dids["2001"].raw_hex)
        b0 = raw[0] if len(raw) >= 1 else 0
        aa_usb = bool(b0 & 0x01)
        cp_usb = bool(b0 & 0x02)
        aa_wireless = bool(b0 & 0x04)
        cp_wireless = bool(b0 & 0x08)
        decoded_params.append(
            HmiConfigParameter(
                did="2001",
                parameter_name="Projection Smartphone (Android Auto / CarPlay)",
                raw_hex=dids["2001"].raw_hex,
                current_state=(
                    f"AA USB: {'ON' if aa_usb else 'OFF'} | "
                    f"CarPlay USB: {'ON' if cp_usb else 'OFF'} | "
                    f"AA Sans-Fil (Wi-Fi): {'ON' if aa_wireless else 'OFF'} | "
                    f"CarPlay Sans-Fil: {'ON' if cp_wireless else 'OFF'}"
                ),
                details="En Branche 2 (SW 283C33813R), les bits 2 et 3 pilotent Android Auto et CarPlay sans fil via le Wi-Fi 5 GHz.",
            )
        )

    # 2. Analyse Module Wi-Fi Interne (DID 0x2002)
    if "2002" in dids:
        raw = bytes.fromhex(dids["2002"].raw_hex)
        b0 = raw[0] if len(raw) >= 1 else 0
        wifi_hw = "Présent & Actif (5 GHz)" if (b0 & 0x03) == 0x03 else ("Présent (2.4 GHz / Veille)" if (b0 & 0x01) else "Désactivé")
        decoded_params.append(
            HmiConfigParameter(
                did="2002",
                parameter_name="Contrôleur Wi-Fi Interne Bosch A-IVI",
                raw_hex=dids["2002"].raw_hex,
                current_state=wifi_hw,
                details="Requis pour le flux vidéo d'Android Auto Sans Fil (canal 5 GHz).",
            )
        )

    # 3. Analyse Thème & Séquence d'Accueil (DID 0x2003)
    if "2003" in dids:
        raw = bytes.fromhex(dids["2003"].raw_hex)
        theme_map = {
            0x00: "Renault Standard",
            0x01: "Initiale Paris",
            0x02: "R.S. Line / Renault Sport",
            0x03: "Alpine",
        }
        theme_id = raw[0] if len(raw) >= 1 else 0
        decoded_params.append(
            HmiConfigParameter(
                did="2003",
                parameter_name="Séquence d'Accueil & Habillage Graphique (Welcome Theme)",
                raw_hex=dids["2003"].raw_hex,
                current_state=theme_map.get(theme_id, f"Profil personnalisé (0x{theme_id:02X})"),
                details="Définit l'animation de démarrage et la signature sonore à l'ouverture de porte.",
            )
        )

    # 4. Analyse Multi-Sense (DID 0x2006)
    if "2006" in dids:
        decoded_params.append(
            HmiConfigParameter(
                did="2006",
                parameter_name="Profils Multi-Sense & Éclairage d'Ambiance",
                raw_hex=dids["2006"].raw_hex,
                current_state="Multi-Sense Actif (MySense / Sport / Eco / Comfort)",
                details="Synchronise la couleur de l'IHM Easy Link 9.3\", du compteur Visteon et des LEDs de portes.",
            )
        )

    return decoded_params


class EasyLinkHmiExplorer:
    """Scanner spécialisé pour extraire et décoder les registres IHM de l'Easy Link (0x712) et du Compteur (0x743)."""

    def __init__(self, scanner: Espace5UdsScanner) -> None:
        self.scanner = scanner

    def probe_ecu_dids(
        self,
        ecu: EcuDefinition,
        dids: List[DidDefinition],
        progress_cb: Optional[Callable[[DidDefinition, int, int], None]] = None,
    ) -> Dict[str, DidValue]:
        """Lit une liste de DIDs UDS sur un calculateur spécifique (ex: 0x712 Easy Link)."""
        self.scanner.select_ecu(ecu)
        # Ouvre la session diagnostic étendue (0x10 0x03) pour débloquer la lecture des DIDs 0x20xx/0x30xx
        self.scanner.send_uds_request("1003")

        found: Dict[str, DidValue] = {}
        total = len(dids)
        for idx, did_def in enumerate(dids, start=1):
            if progress_cb:
                progress_cb(did_def, idx, total)
            val = self.scanner.read_did(did_def)
            if val is not None:
                found[did_def.did] = val
        return found

    def discover_did_range(
        self,
        ecu: EcuDefinition,
        start_did: int = 0x2000,
        end_did: int = 0x2030,
    ) -> Dict[str, str]:
        """Balaye une plage de DIDs UDS (Service 0x22) en lecture seule pour découvrir tous les registres actifs."""
        self.scanner.select_ecu(ecu)
        self.scanner.send_uds_request("1003")

        discovered: Dict[str, str] = {}
        for did_int in range(start_did, end_did + 1):
            did_hex = f"{did_int:04X}"
            resp = self.scanner.send_uds_request(f"22{did_hex}")
            if resp and len(resp) >= 3 and resp[:3] == bytes.fromhex(f"62{did_hex}"):
                discovered[did_hex] = resp[3:].hex().upper()
        return discovered
