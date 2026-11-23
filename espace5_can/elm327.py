"""Couche de transport ELM327 / Vgate iCar Pro BLE et réassemblage ISO-TP (ISO 15765-2)."""

from __future__ import annotations

import re
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple


class TransportError(Exception):
    """Erreur de communication avec l'interface Vgate / ELM327."""


class BaseAdapter(ABC):
    """Interface abstraite pour un adaptateur ELM327 / Vgate iCar Pro."""

    @abstractmethod
    def send_command(self, cmd: str, timeout: float = 1.5) -> str:
        """Envoie une commande AT ou une trame hexadécimale et retourne la réponse brute."""

    @abstractmethod
    def close(self) -> None:
        """Ferme la connexion série / Bluetooth."""


class SerialElmAdapter(BaseAdapter):
    """Adaptateur réel sur port série (COMx sous Windows ou /dev/rfcomm0 sous Linux)."""

    def __init__(self, port: str, baudrate: int = 38400, timeout: float = 1.5) -> None:
        try:
            import serial  # type: ignore
        except ImportError as exc:
            raise TransportError(
                "Le module 'pyserial' est requis. Installez-le avec: pip install pyserial"
            ) from exc

        self.port_name = port
        self.baudrate = baudrate
        try:
            self._ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout,
                write_timeout=timeout,
            )
        except Exception as exc:
            raise TransportError(
                f"Impossible d'ouvrir le port '{port}' ({exc}). "
                "Vérifiez que 'Android-Vlink' est appairé sous Windows (code 1234) et que le contact est mis."
            ) from exc

    def send_command(self, cmd: str, timeout: float = 1.5) -> str:
        if not self._ser or not self._ser.is_open:
            raise TransportError("Port série non ouvert.")

        self._ser.reset_input_buffer()
        payload = (cmd.strip() + "\r").encode("ascii", errors="ignore")
        self._ser.write(payload)
        self._ser.flush()

        deadline = time.monotonic() + timeout
        chunks: List[str] = []
        while time.monotonic() < deadline:
            waiting = self._ser.in_waiting
            data = self._ser.read(waiting if waiting > 0 else 1)
            if data:
                text = data.decode("ascii", errors="ignore")
                chunks.append(text)
                if ">" in text:
                    break

        raw = "".join(chunks)
        # Nettoyage de l'écho, des retours chariots et du prompt '>'
        cleaned_lines: List[str] = []
        for line in raw.replace("\r", "\n").split("\n"):
            stripped = line.strip().replace(">", "").strip()
            if not stripped:
                continue
            if stripped.upper() == cmd.strip().upper():
                continue
            cleaned_lines.append(stripped)
        return "\n".join(cleaned_lines)

    def close(self) -> None:
        if getattr(self, "_ser", None) and self._ser.is_open:
            self._ser.close()


class SimulatedEspace5Adapter(BaseAdapter):
    """Simulateur fidèle d'un Vgate iCar Pro BLE branché sur une Renault Espace V 2.0 Blue dCi Phase 2."""

    def __init__(self, vin: str = "VF1RFC00X66002021") -> None:
        self.vin = vin
        self.current_tx = "7E0"
        self.current_rx = "7E8"
        self.voltage = "14.3V"
        self._ecu_data: Dict[str, Dict[str, bytes]] = self._build_mock_ecus()

    def _build_mock_ecus(self) -> Dict[str, Dict[str, bytes]]:
        vin_bytes = self.vin.encode("ascii")
        return {
            # Injection 2.0 Blue dCi (Bosch MD1CS006)
            "7E0": {
                "F190": vin_bytes,
                "F187": b"237104892R",
                "F18A": b"BOSCH",
                "F191": b"237100854R",
                "F193": b"H02",
                "F194": b"10SW063912",
                "F195": b"237105521R",
                "F188": b"237615521R",
                "F18C": b"BMD1CS0069941",
                "F18B": bytes.fromhex("20201118"),
                "F198": b"CLIP_FR_75015",
                "F199": bytes.fromhex("20230922"),
                "F1A0": bytes.fromhex("54"),
            },
            # Boîte Auto EDC DW6 (Getrag 6DCT450)
            "7E1": {
                "F190": vin_bytes,
                "F187": b"310321984R",
                "F18A": b"GETRAG",
                "F191": b"310320742R",
                "F194": b"DW6_P2_V18",
                "F195": b"310322105R",
                "F18C": b"GT6DCT4502841",
                "F18B": bytes.fromhex("20201112"),
                "F198": b"FACTORY_DOUAI",
                "F199": bytes.fromhex("20201204"),
                "F1A0": bytes.fromhex("1C"),
            },
            # Module AdBlue SCR
            "7E2": {
                "F190": vin_bytes,
                "F187": b"208993104R",
                "F18A": b"BOSCH_SCR",
                "F195": b"208994412R",
                "F18B": bytes.fromhex("20201110"),
                "F198": b"CLIP_FR_75015",
                "F199": bytes.fromhex("20230922"),
                "F1A0": bytes.fromhex("08"),
            },
            # Système Multimédia Easy Link 9.3" (Bosch A-IVI)
            "712": {
                "F190": vin_bytes,
                "F187": b"283C36016R",
                "F18A": b"BOSCH_AIVI",
                "F191": b"281158429R",
                "F193": b"GEN2.1",
                "F194": b"AIVI_LINUX_4.14",
                "F195": b"283C36016R",
                "F188": b"283C62148R",
                "F18C": b"AIVI93FR2021884",
                "F18B": bytes.fromhex("20201115"),
                "F198": b"OTA_RENAULT_FOTA",
                "F199": bytes.fromhex("20240314"),
                "F1A0": bytes.fromhex("2A"),
            },
            # Tableau de Bord Numérique TFT
            "743": {
                "F190": vin_bytes,
                "F187": b"248109452R",
                "F18A": b"VISTEON",
                "F191": b"248104110R",
                "F195": b"248109981R",
                "F18B": bytes.fromhex("20201109"),
                "F199": bytes.fromhex("20201204"),
                "F1A0": bytes.fromhex("19"),
            },
            # Unité Centrale Habitacle (UCH / BCM)
            "745": {
                "F190": vin_bytes,
                "F187": b"284B17512R",
                "F18A": b"CONTI_BCM",
                "F191": b"284B10984R",
                "F195": b"284B18821R",
                "F1A0": bytes.fromhex("41"),
            },
            # Châssis 4Control (4 roues directrices)
            "784": {
                "F190": vin_bytes,
                "F187": b"555014829R",
                "F18A": b"AISIN_4WS",
                "F191": b"555011200R",
                "F195": b"555016011R",
                "F1A0": bytes.fromhex("12"),
            },
            # Amortissement Piloté (AVS)
            "781": {
                "F190": vin_bytes,
                "F187": b"543028194R",
                "F18A": b"KYB_AVS",
                "F195": b"543029004R",
                "F1A0": bytes.fromhex("0B"),
            },
            # ABS / ESP
            "740": {
                "F190": vin_bytes,
                "F187": b"476607841R",
                "F18A": b"ATE_CONTI",
                "F195": b"476608912R",
                "F1A0": bytes.fromhex("23"),
            },
            # Direction Assistée (EPS)
            "742": {
                "F190": vin_bytes,
                "F187": b"491105612R",
                "F18A": b"JTEKT",
                "F195": b"491106109R",
                "F1A0": bytes.fromhex("15"),
            },
            # Climatisation (HVAC)
            "744": {
                "F190": vin_bytes,
                "F187": b"275104821R",
                "F18A": b"VALEO",
                "F195": b"275105190R",
                "F1A0": bytes.fromhex("0E"),
            },
            # Amplificateur Bose Surround
            "782": {
                "F190": vin_bytes,
                "F187": b"280634192R",
                "F18A": b"BOSE_DSP",
                "F195": b"280635011R",
                "F1A0": bytes.fromhex("07"),
            },
            # Caméra Frontale ADAS (Matrix LED)
            "74B": {
                "F190": vin_bytes,
                "F187": b"284G26182R",
                "F18A": b"VALEO_MOBILEYE",
                "F195": b"284G27901R",
                "F1A0": bytes.fromhex("1A"),
            },
            # Radar Frontal ACC
            "753": {
                "F190": vin_bytes,
                "F187": b"284387412R",
                "F18A": b"BOSCH_FRAD",
                "F195": b"284388109R",
                "F1A0": bytes.fromhex("14"),
            },
        }

    def send_command(self, cmd: str, timeout: float = 1.5) -> str:
        upper = cmd.strip().upper().replace(" ", "")
        if upper == "ATZ":
            return "ELM327 v2.2 (Vgate iCar Pro BLE)"
        if upper == "ATI":
            return "ELM327 v2.2"
        if upper == "ATRV":
            return self.voltage
        if upper.startswith("ATSH"):
            self.current_tx = upper[4:]
            return "OK"
        if upper.startswith("ATCRA"):
            self.current_rx = upper[5:]
            return "OK"
        if upper.startswith("ATFCSH"):
            return "OK"
        if upper.startswith("AT"):
            return "OK"

        # Vérifie si le calculateur est présent dans la simulation
        if self.current_tx not in self._ecu_data:
            return "NO DATA"

        ecu_dids = self._ecu_data[self.current_tx]

        # Si ATCAF0 est actif, la requête commence par l'octet de longueur ISO-TP Single Frame (02..07)
        if len(upper) >= 4 and upper[:2] in ("02", "03", "04", "05", "06", "07"):
            expected_len = int(upper[:2], 16)
            if len(upper[2:]) == expected_len * 2:
                upper = upper[2:]

        # Service 0x10 : DiagnosticSessionControl (ex: 10 03 Extended Diagnostic Session)
        if upper.startswith("10"):
            sub_fn = upper[2:4] if len(upper) >= 4 else "03"
            return self._encode_isotp_response(bytes.fromhex(f"50{sub_fn}003201F4"))

        # Service 0x3E : TesterPresent
        if upper.startswith("3E"):
            return self._encode_isotp_response(bytes.fromhex("7E00"))

        # Service 0x22 : ReadDataByIdentifier (ex: 22F190)
        if upper.startswith("22") and len(upper) == 6:
            did = upper[2:6]
            if did in ecu_dids:
                payload = bytes.fromhex(f"62{did}") + ecu_dids[did]
                return self._encode_isotp_response(payload)
            return self._encode_isotp_response(bytes.fromhex("7F2231"))  # RequestOutOfRange

        return "NO DATA"

    @staticmethod
    def _encode_isotp_response(payload: bytes) -> str:
        """Encode une charge utile UDS en trames ISO-TP (Single Frame ou Multi-Frame)."""
        length = len(payload)
        if length <= 7:
            sf_pci = f"{length:02X}"
            body = " ".join(f"{b:02X}" for b in payload)
            return f"{sf_pci} {body}".strip()

        # First Frame (FF): 1n nn + 6 premiers octets
        ff_pci_high = 0x10 | ((length >> 8) & 0x0F)
        ff_pci_low = length & 0xFF
        first_chunk = payload[:6]
        lines = [
            f"{ff_pci_high:02X} {ff_pci_low:02X} " + " ".join(f"{b:02X}" for b in first_chunk)
        ]

        # Consecutive Frames (CF): 21, 22, ... + 7 octets max par trame
        offset = 6
        seq = 1
        while offset < length:
            chunk = payload[offset : offset + 7]
            cf_pci = 0x20 | (seq & 0x0F)
            lines.append(f"{cf_pci:02X} " + " ".join(f"{b:02X}" for b in chunk))
            offset += 7
            seq = (seq + 1) & 0x0F
        return "\n".join(lines)

    def close(self) -> None:
        pass


def parse_isotp_payload(raw_response: str) -> Optional[bytes]:
    """Réassemble une réponse ISO-TP (Single Frame ou Multi-Frame) issue d'un ELM327 / Vgate."""
    if not raw_response:
        return None

    upper = raw_response.upper()
    if any(err in upper for err in ("NO DATA", "ERROR", "UNABLE TO CONNECT", "CAN ERROR", "STOPPED", "?")):
        return None

    lines = [ln.strip() for ln in upper.splitlines() if ln.strip()]
    if not lines:
        return None

    # Extraction des octets hexadécimaux ligne par ligne
    frame_bytes_list: List[List[int]] = []
    for line in lines:
        # Supprime d'éventuels préfixes type "0:" ou "1:" si ATH0/ATS1 varient
        if ":" in line and len(line.split(":")[0]) <= 3:
            line = line.split(":", 1)[1].strip()
        tokens = re.findall(r"\b[0-9A-F]{2}\b", line)
        if tokens:
            frame_bytes_list.append([int(tok, 16) for tok in tokens])

    if not frame_bytes_list:
        return None

    first_frame = frame_bytes_list[0]
    first_byte = first_frame[0]
    frame_type = (first_byte >> 4) & 0x0F

    # Cas 1 : Single Frame (0x01 .. 0x07)
    if frame_type == 0x0 and 1 <= (first_byte & 0x0F) <= 7:
        sf_len = first_byte & 0x0F
        if len(first_frame) >= 1 + sf_len:
            return bytes(first_frame[1 : 1 + sf_len])
        # Certains modes ELM retournent déjà la charge utile sans l'octet PCI si CAF1 est actif
        return bytes(first_frame)

    # Cas 2 : First Frame (0x1n nn) + Consecutive Frames (0x21, 0x22...)
    if frame_type == 0x1 and len(first_frame) >= 2:
        total_len = ((first_byte & 0x0F) << 8) | first_frame[1]
        assembled: List[int] = list(first_frame[2:])
        for cf in frame_bytes_list[1:]:
            if not cf:
                continue
            cf_type = (cf[0] >> 4) & 0x0F
            if cf_type == 0x2:
                assembled.extend(cf[1:])
        return bytes(assembled[:total_len])

    # Cas 3 : L'ELM327 a déjà retiré l'octet PCI (réponse directe commençant par 0x50, 0x62, 0x7F...)
    flat = [b for frame in frame_bytes_list for b in frame]
    return bytes(flat)


def list_serial_ports() -> List[Tuple[str, str]]:
    """Retourne la liste des ports COM / série détectés sur la machine (Windows / Linux)."""
    try:
        from serial.tools import list_ports  # type: ignore

        return [(p.device, p.description) for p in list_ports.comports()]
    except Exception:
        return []
