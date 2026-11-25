"""Scanner UDS (ISO-14229) pour les calculateurs de la Renault Espace V Phase 2."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from .ecus import ESPACE5_ECUS, STANDARD_IDENTIFICATION_DIDS, DidDefinition, EcuDefinition
from .elm327 import BaseAdapter, parse_isotp_payload


@dataclass
class DidValue:
    """Valeur lue et décodée d'un DID UDS (Service 0x22)."""

    did: str
    label: str
    raw_hex: str
    decoded: str


@dataclass
class EcuScanResult:
    """Résultat du scan UDS d'un calculateur (ECU) Renault Espace V."""

    key: str
    code_renault: str
    name: str
    supplier_hint: str
    tx_id: str
    rx_id: str
    bus: str
    online: bool
    session_opened: str = ""
    identifications: Dict[str, DidValue] = field(default_factory=dict)
    error: str = ""

    @property
    def vin(self) -> str:
        val = self.identifications.get("F190")
        return val.decoded if val else ""

    @property
    def part_number(self) -> str:
        val = self.identifications.get("F187")
        return val.decoded if val else ""

    @property
    def supplier(self) -> str:
        val = self.identifications.get("F18A")
        return val.decoded if val else self.supplier_hint

    @property
    def sw_version(self) -> str:
        val = self.identifications.get("F188") or self.identifications.get("F195") or self.identifications.get("F194")
        return val.decoded if val else ""

    @property
    def hw_number(self) -> str:
        val = self.identifications.get("F191")
        return val.decoded if val else ""

    @property
    def programming_date(self) -> str:
        val = self.identifications.get("F199") or self.identifications.get("F18B")
        return val.decoded if val else ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def decode_did_bytes(data: bytes, encoding: str = "ascii") -> str:
    """Décode proprement la charge utile d'un DID Renault (ASCII imprimable, Date BCD ou Hex)."""
    if not data:
        return ""
    if encoding == "hex":
        return data.hex().upper()

    cleaned = data.strip(b"\x00\xff ")
    if not cleaned:
        return data.hex().upper()

    if encoding == "date_bcd":
        if all(32 <= b <= 126 for b in cleaned) and len(cleaned) in (6, 8, 10):
            txt = cleaned.decode("ascii", errors="ignore").strip()
            if len(txt) == 8 and txt.isdigit():
                return f"{txt[0:4]}-{txt[4:6]}-{txt[6:8]}"
            if len(txt) == 6 and txt.isdigit():
                return f"20{txt[0:2]}-{txt[2:4]}-{txt[4:6]}"
            return txt
        hx = data.hex().upper()
        if len(data) == 4 and hx.isdigit():
            return f"{hx[0:4]}-{hx[4:6]}-{hx[6:8]}"
        if len(data) == 3 and hx.isdigit():
            return f"20{hx[0:2]}-{hx[2:4]}-{hx[4:6]}"

    printable_count = sum(1 for b in cleaned if 32 <= b <= 126)
    if printable_count / len(cleaned) >= 0.75:
        return "".join(chr(b) if 32 <= b <= 126 else "." for b in cleaned).strip()

    return data.hex().upper()


class Espace5UdsScanner:
    """Orchestrateur d'initialisation Vgate iCar Pro BLE et d'exploration UDS CAN 500 kbps (29-bit + 11-bit)."""

    def __init__(self, adapter: BaseAdapter) -> None:
        self.adapter = adapter
        self.adapter_name: str = ""
        self.battery_voltage: str = ""
        self._active_can_bits: int = 0

    def initialize_vgate(self) -> Tuple[str, str]:
        """Initialise le Vgate iCar Pro BLE en CAN 500 kbps (ISO 15765-4)."""
        self.adapter_name = self.adapter.send_command("ATZ", timeout=2.0).strip()
        init_sequence = [
            "ATE0",     # Désactive l'écho
            "ATL0",     # Désactive les sauts de ligne superflus
            "ATS1",     # Conserve les espaces entre octets hexadécimaux
            "ATH0",     # Masque l'en-tête CAN dans la réponse pour isoler l'ISO-TP
            "ATSP7",    # Démarre en Protocole 7 : ISO 15765-4 CAN (29 bit ID, 500 kbaud)
            "ATCAF0",   # Désactive le formatage auto pour gérer les trames UDS multi-octets proprement
            "ATST32",   # Timeout d'attente CAN ~200 ms
        ]
        for cmd in init_sequence:
            self.adapter.send_command(cmd)
        self._active_can_bits = 29

        self.battery_voltage = self.adapter.send_command("ATRV").strip()
        return self.adapter_name, self.battery_voltage

    def select_ecu(self, ecu: EcuDefinition) -> None:
        """Configure dynamiquement le protocole 29-bit (ATSP7) ou 11-bit (ATSP6) et l'adressage TX/RX."""
        if ecu.can_bits == 29:
            if self._active_can_bits != 29:
                self.adapter.send_command("ATSP7")
                self.adapter.send_command("ATCAF0")
                self._active_can_bits = 29
            # Sur ELM327 en 29-bit (ex: 18DA10F1), ATCP définit l'octet de priorité (18) et ATSH les 3 octets suivants (DA10F1)
            cp_byte = ecu.tx_id[:2]
            sh_bytes = ecu.tx_id[2:]
            self.adapter.send_command(f"ATCP{cp_byte}")
            self.adapter.send_command(f"ATSH{sh_bytes}")
            self.adapter.send_command(f"ATCRA{ecu.rx_id}")
            self.adapter.send_command(f"ATFCSH{ecu.tx_id}")
            self.adapter.send_command("ATFCSD300000")
            self.adapter.send_command("ATFCSM1")
        else:
            if self._active_can_bits != 11:
                self.adapter.send_command("ATSP6")
                self.adapter.send_command("ATCAF0")
                self._active_can_bits = 11
            self.adapter.send_command(f"ATSH{ecu.tx_id}")
            self.adapter.send_command(f"ATCRA{ecu.rx_id}")
            self.adapter.send_command(f"ATFCSH{ecu.tx_id}")
            self.adapter.send_command("ATFCSD300000")
            self.adapter.send_command("ATFCSM1")

    def send_uds_request(self, service_and_data_hex: str) -> Optional[bytes]:
        """Encapsule une requête UDS (inférieure ou égale à 7 octets) dans une Single Frame ISO-TP."""
        clean_hex = service_and_data_hex.replace(" ", "").upper()
        byte_len = len(clean_hex) // 2
        if byte_len == 0 or byte_len > 7:
            raise ValueError(f"Longueur de requête UDS invalide ({byte_len} octets): {clean_hex}")

        sf_frame = f"{byte_len:02X}{clean_hex}"
        raw_resp = self.adapter.send_command(sf_frame)
        return parse_isotp_payload(raw_resp)

    def read_did(self, did_def: DidDefinition) -> Optional[DidValue]:
        """Exécute un service UDS 0x22 (ReadDataByIdentifier) sur le calculateur sélectionné."""
        did_hex = did_def.did.upper()
        resp = self.send_uds_request(f"22{did_hex}")
        if not resp or len(resp) < 3:
            return None

        # Réponse positive au service 0x22 = 0x62 + DID (2 octets) + payload
        expected_prefix = bytes.fromhex(f"62{did_hex}")
        if not resp.startswith(expected_prefix):
            return None

        payload = resp[3:]
        decoded = decode_did_bytes(payload, encoding=did_def.encoding)
        return DidValue(
            did=did_hex,
            label=did_def.label,
            raw_hex=payload.hex().upper(),
            decoded=decoded,
        )

    def scan_single_ecu(
        self,
        ecu: EcuDefinition,
        dids: Optional[List[DidDefinition]] = None,
    ) -> EcuScanResult:
        """Interroge un calculateur Renault Espace V et extrait toutes ses références logicielles/matérielles."""
        target_dids = dids if dids is not None else STANDARD_IDENTIFICATION_DIDS
        result = EcuScanResult(
            key=ecu.key,
            code_renault=ecu.code_renault,
            name=ecu.name,
            supplier_hint=ecu.supplier_hint,
            tx_id=ecu.tx_id,
            rx_id=ecu.rx_id,
            bus=ecu.bus,
            online=False,
        )

        self.select_ecu(ecu)

        # 1. Ouverture d'une session diagnostic étendue UDS (10 03) ou par défaut (10 01)
        session_resp = self.send_uds_request("1003")
        if session_resp and session_resp[0] == 0x50:
            result.online = True
            result.session_opened = "ExtendedDiagnosticSession (0x10 0x03)"
        else:
            # Certains calculateurs répondent directement aux lectures DID 0x22 ou à TesterPresent 0x3E00
            ping_resp = self.send_uds_request("3E00")
            if ping_resp and ping_resp[0] in (0x7E, 0x7F):
                result.online = True
                result.session_opened = "DefaultSession (0x3E 0x00)"

        # 2. Lecture des DIDs d'identification (F190 VIN, F187 Part Number, F195 SW Version...)
        for did_def in target_dids:
            val = self.read_did(did_def)
            if val is not None:
                result.online = True
                if not result.session_opened:
                    result.session_opened = "DirectRead (0x22)"
                result.identifications[did_def.did] = val

        return result

    def scan_all_ecus(
        self,
        ecus: Optional[List[EcuDefinition]] = None,
        progress_cb: Optional[Callable[[EcuDefinition, int, int], None]] = None,
    ) -> List[EcuScanResult]:
        """Scanne séquentiellement tous les calculateurs de la Renault Espace 5."""
        target_ecus = ecus if ecus is not None else ESPACE5_ECUS
        results: List[EcuScanResult] = []
        total = len(target_ecus)
        for idx, ecu in enumerate(target_ecus, start=1):
            if progress_cb:
                progress_cb(ecu, idx, total)
            res = self.scan_single_ecu(ecu)
            results.append(res)
        return results
