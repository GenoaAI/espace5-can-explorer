"""Décodage des codes défauts (DTC) UDS (ISO-14229 Service 0x19) et dictionnaire Renault Espace V 2.0 Blue dCi."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


# Table officielle des Failure Type Bytes (FTB - 3e octet d'un DTC UDS ISO-14229 / SAE J2012-DA)
UDS_FAILURE_TYPE_BYTES: Dict[str, str] = {
    "00": "Aucune information de sous-type",
    "01": "Défaillance électrique générale",
    "02": "Défaillance générale du signal (General signal failure)",
    "04": "Défaillance interne du système / composant (System internal failure)",
    "08": "Défaillance de signal / message bus (Bus signal / message failure - LIN/CAN)",
    "11": "Court-circuit à la masse (Circuit short to ground)",
    "12": "Court-circuit au +12V (Circuit short to battery)",
    "13": "Circuit ouvert (Circuit open)",
    "15": "Court-circuit au +12V ou circuit ouvert",
    "64": "Défaut de plausibilité du signal (Signal plausibility failure)",
    "86": "Signal invalide reçu sur le bus (Signal invalid)",
    "87": "Message / trame CAN manquant (Missing message)",
    "8F": "Signal erratique / intermittent",
    "97": "Fonctionnement du composant ou système obstrué / bloqué (Component obstructed or blocked)",
    "F0": "Condition spécifique constructeur Renault",
}


# Base de connaissances des codes défauts connus sur Renault Espace V Phase 2 (2.0 Blue dCi & Easy Link)
KNOWN_ESPACE5_DTCS: Dict[str, Dict[str, str]] = {
    "P2002": {
        "system": "ECM / Injection 2.0 Blue dCi (OBD-II)",
        "title": "Efficacité du filtre à particules (FAP / DPF Bank 1) inférieure au seuil",
        "cause": (
            "1) Durite souple du capteur de pression différentielle FAP fissurée, poreuse ou bouchée "
            "(très fréquent autour de 200 000 - 280 000 km). "
            "2) Capteur de pression différentielle FAP dérive hors plage. "
            "3) Micro-fissure interne du monolithe céramique du FAP (vérifier présence de suie sèche en sortie d'échappement)."
        ),
        "severity": "MOYENNE (À diagnostiquer : vérifier la pression différentielle FAP au ralenti et en charge)",
    },
    "B272B": {
        "system": "SONAR / Aide au stationnement (0x74E)",
        "title": "Capteur radar ultrason de pare-chocs obstrué ou bloqué (FTB 0x97)",
        "cause": (
            "Un des capteurs ultrasons de stationnement (ou sa bague en silicone) est encrassé, "
            "humide ou recouvert d'une saleté empêchant la membrane de vibrer librement."
        ),
        "severity": "FAIBLE (Nettoyer les capteurs ultrasons des pare-chocs avant/arrière)",
    },
    "B274D": {
        "system": "SONAR / Aide au stationnement (0x74E)",
        "title": "Perte temporaire de communication CAN avec un calculateur distant (FTB 0x87)",
        "cause": "Trame CAN manquante temporairement lors d'une mise sous contact ou baisse de tension 12V.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "C1611": {
        "system": "DAE / Direction Assistée TRW (0x742)",
        "title": "Plausibilité du signal vitesse véhicule / angle volant (FTB 0x64)",
        "cause": "Transitoire lors d'une baisse de tension batterie 12V au démarrage.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "C161F": {
        "system": "DAE / Direction Assistée TRW (0x742)",
        "title": "Signal invalide reçu d'un autre calculateur sur le bus CAN (FTB 0x86)",
        "cause": "Transitoire au réveil CAN ou batterie faible.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B24E8": {
        "system": "CLIM / Climatisation (0x744)",
        "title": "Capteur ou actionneur de boucle climatisation - défaillance signal (FTB 0x02)",
        "cause": "Micro-coupure ou valeur hors plage passagère sur un capteur de climatisation.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "U1C00": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Réseau local LIN d'éclairage d'ambiance Multi-Sense / Habitacle (FTB 0x08)",
        "cause": "Erreur temporaire de trame sur le bus LIN des bandeaux LED d'ambiance.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "U1C02": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Communication bus LIN secondaire habitacle (FTB 0x08)",
        "cause": "Micro-coupure de communication LIN lors d'une mise en veille ou démarrage.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "U1C03": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Communication bus LIN tertiaire habitacle (FTB 0x08)",
        "cause": "Micro-coupure de communication LIN lors d'une mise en veille ou démarrage.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2C76": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Module LED d'éclairage d'ambiance Multi-Sense #1 (FTB 0x04)",
        "cause": "Sous-tension ponctuelle sur un bandeau LED d'ambiance intérieur.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2C78": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Module LED d'éclairage d'ambiance Multi-Sense #2 (FTB 0x04)",
        "cause": "Sous-tension ponctuelle sur un bandeau LED d'ambiance intérieur.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2C79": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Module LED d'éclairage d'ambiance Multi-Sense #3 (FTB 0x04)",
        "cause": "Sous-tension ponctuelle sur un bandeau LED d'ambiance intérieur.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2C7A": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Module LED d'éclairage d'ambiance Multi-Sense #4 (FTB 0x04)",
        "cause": "Sous-tension ponctuelle sur un bandeau LED d'ambiance intérieur.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2C7C": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Module LED d'éclairage d'ambiance Multi-Sense #5 (FTB 0x04)",
        "cause": "Sous-tension ponctuelle sur un bandeau LED d'ambiance intérieur.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2C7D": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Module LED d'éclairage d'ambiance Multi-Sense #6 (FTB 0x04)",
        "cause": "Sous-tension ponctuelle sur un bandeau LED d'ambiance intérieur.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2C7E": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Module LED d'éclairage d'ambiance Multi-Sense #7 (FTB 0x04)",
        "cause": "Sous-tension ponctuelle sur un bandeau LED d'ambiance intérieur.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2C7F": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Module LED d'éclairage d'ambiance Multi-Sense #8 (FTB 0x04)",
        "cause": "Sous-tension ponctuelle sur un bandeau LED d'ambiance intérieur.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2C80": {
        "system": "UCH / BCM Habitacle (0x745)",
        "title": "Module LED d'éclairage d'ambiance Multi-Sense #9 (FTB 0x04)",
        "cause": "Sous-tension ponctuelle sur un bandeau LED d'ambiance intérieur.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "U214F": {
        "system": "HFM / Carte Mains-Libres (0x792)",
        "title": "Trame CAN manquante temporaire au réveil (FTB 0x87)",
        "cause": "Asynchronisme ponctuel au réveil du bus CAN.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "U215B": {
        "system": "HFM / Carte Mains-Libres (0x792)",
        "title": "Trame CAN manquante temporaire avec BCM/Tableau de bord (FTB 0x87)",
        "cause": "Asynchronisme ponctuel au réveil du bus CAN.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2E13": {
        "system": "TCU / Appel d'Urgence SOS 4G (0x77A)",
        "title": "Signal intermittent antenne / réseau ou batterie de secours télématique (FTB 0x8F)",
        "cause": "Passage en zone blanche ou vieillissement de la pile interne du module eCall.",
        "severity": "INFO (Archivé / Inactif)",
    },
    "B2E17": {
        "system": "TCU / Appel d'Urgence SOS 4G (0x77A)",
        "title": "Événement interne module de communication télématique (FTB 0xF0)",
        "cause": "Événement réseau 4G / serveur Renault archivé.",
        "severity": "INFO (Archivé / Inactif)",
    },
}


@dataclass(frozen=True)
class DecodedDtc:
    """Représentation décodée d'un code défaut UDS 3 octets + octet de statut ISO-14229."""

    code: str            # Ex: "B272B(97)"
    base_code: str       # Ex: "B272B"
    ftb_hex: str         # Ex: "97"
    raw_hex: str         # Ex: "A72B97"
    status_byte: int     # Octet de statut UDS (bit 0 = testFailed / Actif, bit 3 = confirmedDTC)
    is_active: bool      # True si le défaut est présent dans le cycle courant (bit 0 ou 1)
    ftb_meaning: str
    title: str
    cause: str
    severity: str


def format_dtc_from_3bytes(b0: int, b1: int, b2: int, status_byte: int = 0x08) -> DecodedDtc:
    """Convertit 3 octets DTC ISO-15031-6 / ISO-14229 (ex: 0xA7, 0x2B, 0x97) en code lisible (ex: B272B(97))."""
    prefix_map = {0: "P", 1: "C", 2: "B", 3: "U"}
    prefix = prefix_map[(b0 >> 6) & 0x03]
    second_char = f"{(b0 >> 4) & 0x03:X}"
    third_char = f"{b0 & 0x0F:X}"
    fourth_fifth = f"{b1:02X}"

    base_code = f"{prefix}{second_char}{third_char}{fourth_fifth}"
    ftb_hex = f"{b2:02X}"
    code = f"{base_code}({ftb_hex})" if b2 != 0 else base_code
    raw_hex = f"{b0:02X}{b1:02X}{b2:02X}"

    is_active = bool(status_byte & 0x03)  # Bit 0 (testFailed) ou Bit 1 (testFailedThisOperationCycle)
    ftb_meaning = UDS_FAILURE_TYPE_BYTES.get(ftb_hex, "Sous-type constructeur")
    kb_entry = KNOWN_ESPACE5_DTCS.get(base_code, {})

    return DecodedDtc(
        code=code,
        base_code=base_code,
        ftb_hex=ftb_hex,
        raw_hex=raw_hex,
        status_byte=status_byte,
        is_active=is_active,
        ftb_meaning=ftb_meaning,
        title=kb_entry.get("title", f"Code défaut {code} ({ftb_meaning})"),
        cause=kb_entry.get("cause", "Consultez la documentation technique Renault pour ce code."),
        severity=kb_entry.get("severity", "ACTIF" if is_active else "ARCHIVÉ (Inactif)"),
    )


def parse_uds_1902_response(payload: bytes) -> List[DecodedDtc]:
    """Décode la réponse UDS au service 0x19 0x02 (ReadDTCByStatusMask -> réponse 0x59 0x02 [Mask] [DTC1_3B + Status1]...)."""
    if not payload or len(payload) < 3 or payload[0] != 0x59 or payload[1] != 0x02:
        return []

    dtcs: List[DecodedDtc] = []
    # Les enregistrements commencent à l'index 3, par blocs de 4 octets (3 octets DTC + 1 octet Status)
    offset = 3
    while offset + 4 <= len(payload):
        b0, b1, b2, status = payload[offset : offset + 4]
        dtcs.append(format_dtc_from_3bytes(b0, b1, b2, status))
        offset += 4
    return dtcs
