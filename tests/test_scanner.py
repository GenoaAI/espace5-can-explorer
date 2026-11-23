"""Tests unitaires pour le réassemblage ISO-TP et le scanner UDS Renault Espace V 2.0 Blue dCi & Easy Link."""

import unittest

from espace5_can.ecus import ECU_BY_KEY
from espace5_can.elm327 import SimulatedEspace5Adapter, parse_isotp_payload
from espace5_can.uds_scanner import Espace5UdsScanner


class TestIsoTpReassembly(unittest.TestCase):
    def test_single_frame_parsing(self) -> None:
        raw = "06 50 03 00 32 01 F4"
        payload = parse_isotp_payload(raw)
        self.assertEqual(payload, bytes.fromhex("5003003201F4"))

    def test_multi_frame_vin_parsing(self) -> None:
        # Réponse UDS 62 F1 90 + VIN 17 octets = 20 octets (0x014)
        adapter = SimulatedEspace5Adapter(vin="VF1RFC00X66002021")
        expected = bytes.fromhex("62F190") + b"VF1RFC00X66002021"
        raw_frames = adapter._encode_isotp_response(expected)
        reassembled = parse_isotp_payload(raw_frames)
        self.assertEqual(reassembled, expected)

    def test_no_data_returns_none(self) -> None:
        self.assertIsNone(parse_isotp_payload("NO DATA"))
        self.assertIsNone(parse_isotp_payload("CAN ERROR"))


class TestEspace5UdsScanner(unittest.TestCase):
    def test_scan_easylink_and_ecm(self) -> None:
        adapter = SimulatedEspace5Adapter(vin="VF1RFC00X66002021")
        scanner = Espace5UdsScanner(adapter)
        name, voltage = scanner.initialize_vgate()
        self.assertIn("ELM327", name)
        self.assertEqual(voltage, "14.3V")

        # Scan Easy Link (0x712 -> 0x732)
        easylink_res = scanner.scan_single_ecu(ECU_BY_KEY["easylink"])
        self.assertTrue(easylink_res.online)
        self.assertEqual(easylink_res.vin, "VF1RFC00X66002021")
        self.assertEqual(easylink_res.part_number, "283C36016R")
        self.assertEqual(easylink_res.sw_version, "283C36016R")

        # Scan Injection 2.0 Blue dCi (0x7E0 -> 0x7E8)
        ecm_res = scanner.scan_single_ecu(ECU_BY_KEY["ecm"])
        self.assertTrue(ecm_res.online)
        self.assertEqual(ecm_res.supplier, "BOSCH")
        self.assertEqual(ecm_res.part_number, "237104892R")


if __name__ == "__main__":
    unittest.main()
