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
    """Simulateur fidèle d'un Vgate iCar Pro BLE branché sur une Renault Espace V 2.0 Blue dCi Phase 2
    (données basées sur l'empreinte réelle des 16 calculateurs 29-bit + 11-bit, VIN anonymisé)."""

    def __init__(self, vin: str = "VF1RFC00X66XXXXXX") -> None:
        self.vin = vin
        self.protocol = "6"  # "6" = 11-bit 500k, "7" = 29-bit 500k
        self.current_cp = "18"
        self.current_tx = "7E0"
        self.current_rx = "7E8"
        self.voltage = "14.2V"
        self._ecu_data: Dict[str, Dict[str, bytes]] = self._build_mock_ecus()

    def _build_mock_ecus(self) -> Dict[str, Dict[str, bytes]]:
        vin_bytes = self.vin.encode("ascii")
        return {
            # --- 29-BIT ECUs (ATSP7) ---
            # Unité de contrôle moteur 2.0 Blue dCi (18DA10F1)
            "18DA10F1": {
                "F190": vin_bytes,
                "F187": b"237101663S",
                "F188": b"237010816V",
                "F18A": b"Robert Bosch GmbH (037)",
                "F191": b"237101663S",
                "F194": b"7A00",
                "F195": b"6K00 (Cal: 237610818V)",
                "F18C": b"94840016201222090737",
                "F199": bytes.fromhex("32333731303136363353"),
                "F1A0": bytes.fromhex("8C"),
            },
            # Unité de commande de transmission EDC DW6 (18DA18F1)
            "18DA18F1": {
                "F190": vin_bytes,
                "F187": b"310322081R",
                "F188": b"310392109R",
                "F18A": b"GETRAG",
                "F191": b"310321915R",
                "F194": b"2541",
                "F195": b"8210",
                "F18C": b"200821191214",
                "F199": bytes.fromhex("33313033323139313552"),
                "F1A0": bytes.fromhex("0C"),
            },
            # Module de dosage AdBlue UDM (18DAE1F1)
            "18DAE1F1": {
                "F190": vin_bytes,
                "F187": b"237G00329R",
                "F188": b"237G00556R",
                "F18A": b"PLASTIC OMNIUM",
                "F191": b"285J97945R",
                "F194": b"9000",
                "F195": b"F04 (Cal: 237G80562R)",
                "F18C": b"0000000002110564",
                "F199": bytes.fromhex("3238354A393739343552"),
                "F1A0": bytes.fromhex("10"),
            },
            # Unité de commande ABS / ESC (18DA2DF1)
            "18DA2DF1": {
                "F190": vin_bytes,
                "F187": b"476601440R",
                "F188": b"476601440R",
                "F18A": b"CONTI",
                "F191": b"478514191R",
                "F194": b"HPIPB",
                "F195": b"N52CG001812 - MLC70/11",
                "F18C": b"16717150062080100079",
                "F199": bytes.fromhex("34373835313431393152"),
                "F1A0": bytes.fromhex("09"),
            },
            # Affichage Tête Haute HMD (18DA9BF1)
            "18DA9BF1": {
                "F190": vin_bytes,
                "F187": b"249416835R",
                "F188": b"249992983R",
                "F18A": b"BT2",
                "F191": b"285J94233R",
                "F194": b"R25",
                "F195": b"V20B01",
                "F18C": b"00000000000000004251",
                "F199": bytes.fromhex("3238354A393432333352"),
                "F1A0": bytes.fromhex("08"),
            },
            # Security Gateway Gen 3 S-GW3 (18DAD1F1)
            "18DAD1F1": {
                "F190": vin_bytes,
                "F187": b"284Y66LE5C",
                "F188": b"SWF007.0003.0032",
                "F18A": b"B408",
                "F191": b"285J96LA5D",
                "F194": b"F005VT1793",
                "F195": b"SWF007.0003.0032",
                "F18C": b"3712001436502C200720",
                "F199": bytes.fromhex("3238354A39364C413544"),
                "F1A0": bytes.fromhex("06"),
            },
            # --- 11-BIT ECUs (ATSP6) ---
            # Système Multimédia Easy Link 9.3" (712)
            "712": {
                "F190": vin_bytes,
                "F187": b"259159033R",
                "F188": b"283C33813R",
                "F18A": b"BOSCH",
                "F191": b"285J95735R",
                "F194": b"AI_PRJ_RN_AIVI_24.1V19",
                "F195": b"6919_240710",
                "F18C": b"00000002BG0048M",
                "F199": bytes.fromhex("3238354A393537333552"),
                "F1A0": bytes.fromhex("B1"),
                # Registres IHM & Connectivité Easy Link (DIDs 0x20xx)
                "2001": bytes.fromhex("03010100"),  # AA USB=ON, CarPlay USB=ON, AA Wireless=OFF (bit 2=0), CarPlay Wireless=OFF
                "2002": bytes.fromhex("010500"),    # Wi-Fi 5GHz matériellement présent mais en veille
                "2003": bytes.fromhex("000102"),    # Thème 0x00 = Renault Standard
                "2006": bytes.fromhex("0F0701"),    # Multi-Sense 4 modes + LEDs portes/console
                "2008": bytes.fromhex("010200"),    # Config Audio
                "200B": bytes.fromhex("030101"),    # Caméra de recul + Sonar 360
                "200E": bytes.fromhex("010100"),    # Bandeau climatisation IHM
                "2010": bytes.fromhex("0105"),      # Driving Eco2 actif
            },
            # Tableau de Bord Numérique Visteon (743)
            "743": {
                "F190": vin_bytes,
                "F187": b"248105110R",
                "F188": b"248B33935R",
                "F18A": b"07-Visteon-Namestovo",
                "F191": b"250465577R",
                "F194": b"V09.05",
                "F195": b"2006",
                "F18C": b"20_09_11__0044923786",
                "F199": bytes.fromhex("32353034363535373752"),
                "F1A0": bytes.fromhex("12"),
                "3001": bytes.fromhex("0F01"),      # 4 styles graphiques compteur activés
                "3004": bytes.fromhex("1F03"),      # Widgets compteur (Nav, Audio, Eco, Boussole)
            },
            # Unité Centrale Habitacle BCM (745)
            "745": {
                "F190": vin_bytes,
                "F187": b"284B13925R",
                "F188": b"284B37713R",
                "F18A": b"CONTINENTAL AUTOMOTIVE",
                "F191": b"284B21462R",
                "F194": b"142902",
                "F195": b"0710",
                "F18C": b"0403426653",
                "F199": bytes.fromhex("32383442323134363252"),
                "F1A0": bytes.fromhex("90"),
            },
            # SRS / Airbags (752)
            "752": {
                "F190": vin_bytes,
                "F187": b"985102111R",
                "F188": b"285A42149R",
                "F18A": b"255414",
                "F191": b"285J93115R",
                "F194": b"S2_020OH.P72",
                "F195": b"P72",
                "F18C": b"U253JiD0045",
                "F199": bytes.fromhex("3238354A393331313552"),
                "F1A0": bytes.fromhex("09"),
            },
            # Direction Assistée Power Steering TRW (742)
            "742": {
                "F190": vin_bytes,
                "F187": b"490044671R",
                "F188": b"285049500R",
                "F18A": b"TRW",
                "F191": b"285007079R",
                "F194": b"S2RE03CD04",
                "F195": b"S2RE03CD04",
                "F18C": b"20267D840AN0530",
                "F199": bytes.fromhex("32383530303730373952"),
                "F1A0": bytes.fromhex("26"),
            },
            # Climatisation Heater & Air Conditioning (744)
            "744": {
                "F187": b"285252812R",
                "F18A": b"740 (Valeo)",
                "F194": b"F007",
                "F195": b"1913",
                "F1A0": bytes.fromhex("04"),
            },
            # Energy Management Module EMM (74D)
            "74D": {
                "F18A": b"414 (Continental)",
                "F194": b"BA65",
                "F195": b"6560",
                "F1A0": bytes.fromhex("64"),
            },
            # Sonar Bosch (74E)
            "74E": {
                "F190": vin_bytes,
                "F187": b"284L00448R",
                "F188": b"284S92436R",
                "F18A": b"BOSCH3",
                "F191": b"285J97007R",
                "F194": b"1270RS593P",
                "F195": b"1270RS593P_S1.144.1.4",
                "F18C": b"2008270748",
                "F199": bytes.fromhex("3238354A393730303752"),
                "F1A0": bytes.fromhex("08"),
            },
            # Key hands free HFM (792)
            "792": {
                "F190": vin_bytes,
                "F187": b"285903089R",
                "F188": b"285J92452R",
                "F18A": b"CONTINENTAL",
                "F191": b"285E26475R",
                "F194": b"142A02",
                "F195": b"0630",
                "F18C": b"0500486047",
                "F199": bytes.fromhex("32383545323634373552"),
                "F1A0": bytes.fromhex("05"),
            },
            # Emergency Call and Communication Module TCU/SOS (77A)
            "77A": {
                "F190": vin_bytes,
                "F187": b"2591A9374R",
                "F188": b"282773501R",
                "F18A": b"Continental",
                "F191": b"282A78506R",
                "F194": b"SW9",
                "F195": b"SW9",
                "F18C": b"200701202037888806",
                "F199": bytes.fromhex("32383241373835303652"),
                "F1A0": bytes.fromhex("04"),
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
        if upper.startswith("ATSP"):
            self.protocol = upper[4:]
            return "OK"
        if upper.startswith("ATCP"):
            self.current_cp = upper[4:]
            return "OK"
        if upper.startswith("ATSH"):
            sh_val = upper[4:]
            if self.protocol == "7" and len(sh_val) == 6:
                self.current_tx = f"{self.current_cp}{sh_val}"
            else:
                self.current_tx = sh_val
            return "OK"
        if upper.startswith("ATCRA"):
            self.current_rx = upper[5:]
            return "OK"
        if upper.startswith("ATFCSH"):
            return "OK"
        if upper.startswith("AT"):
            return "OK"

        if self.current_tx not in self._ecu_data:
            return "NO DATA"

        ecu_dids = self._ecu_data[self.current_tx]

        # Si ATCAF0 est actif, la requête commence par l'octet de longueur ISO-TP Single Frame (02..07)
        if len(upper) >= 4 and upper[:2] in ("02", "03", "04", "05", "06", "07"):
            expected_len = int(upper[:2], 16)
            if len(upper[2:]) == expected_len * 2:
                upper = upper[2:]

        if upper.startswith("10"):
            sub_fn = upper[2:4] if len(upper) >= 4 else "03"
            return self._encode_isotp_response(bytes.fromhex(f"50{sub_fn}003201F4"))

        if upper.startswith("3E"):
            return self._encode_isotp_response(bytes.fromhex("7E00"))

        if upper.startswith("22") and len(upper) == 6:
            did = upper[2:6]
            if did in ecu_dids:
                payload = bytes.fromhex(f"62{did}") + ecu_dids[did]
                return self._encode_isotp_response(payload)
            return self._encode_isotp_response(bytes.fromhex("7F2231"))

        return "NO DATA"

    @staticmethod
    def _encode_isotp_response(payload: bytes) -> str:
        length = len(payload)
        if length <= 7:
            sf_pci = f"{length:02X}"
            body = " ".join(f"{b:02X}" for b in payload)
            return f"{sf_pci} {body}".strip()

        ff_pci_high = 0x10 | ((length >> 8) & 0x0F)
        ff_pci_low = length & 0xFF
        first_chunk = payload[:6]
        lines = [
            f"{ff_pci_high:02X} {ff_pci_low:02X} " + " ".join(f"{b:02X}" for b in first_chunk)
        ]

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

    frame_bytes_list: List[List[int]] = []
    for line in lines:
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

    if frame_type == 0x0 and 1 <= (first_byte & 0x0F) <= 7:
        sf_len = first_byte & 0x0F
        if len(first_frame) >= 1 + sf_len:
            return bytes(first_frame[1 : 1 + sf_len])
        return bytes(first_frame)

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

    flat = [b for frame in frame_bytes_list for b in frame]
    return bytes(flat)


def list_serial_ports() -> List[Tuple[str, str]]:
    """Retourne la liste des ports COM / série détectés sur la machine (Windows / Linux)."""
    try:
        from serial.tools import list_ports  # type: ignore

        return [(p.device, p.description) for p in list_ports.comports()]
    except Exception:
        return []
