"""Interface en ligne de commande (CLI) et export rapport pour Renault Espace 5 CAN Explorer."""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path
from typing import List, Optional

from .ecus import ECU_BY_KEY, ESPACE5_ECUS, EcuDefinition
from .elm327 import (
    BaseAdapter,
    SerialElmAdapter,
    SimulatedEspace5Adapter,
    TransportError,
    list_serial_ports,
)
from .uds_scanner import EcuScanResult, Espace5UdsScanner


def format_markdown_report(
    results: List[EcuScanResult],
    adapter_name: str,
    voltage: str,
    mode_label: str,
) -> str:
    """Génère un rapport Markdown complet de tous les calculateurs détectés sur l'Espace 5."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    online_ecus = [r for r in results if r.online]
    vins = sorted({r.vin for r in online_ecus if r.vin})
    vehicle_vin = vins[0] if vins else "Non détecté"

    lines = [
        "# Rapport d'Exploration CAN / UDS - Renault Espace V Phase 2 (2.0 Blue dCi & Easy Link)",
        "",
        f"- **Date du scan** : `{now}`",
        f"- **Interface** : `{adapter_name}` ({mode_label})",
        f"- **Tension Batterie 12V (ESM)** : `{voltage}`",
        f"- **VIN détecté (DID F190)** : `{vehicle_vin}`",
        f"- **Calculateurs répondants** : **{len(online_ecus)} / {len(results)}**",
        "",
        "## Synthèse des Calculateurs (ECUs)",
        "",
        "| Code | Calculateur | TX/RX | Statut | Réf. Pièce (F187) | Version Logicielle (F195) | Dernière Prog. (F199) | Fournisseur (F18A) |",
        "|---|---|---|---|---|---|---|---|",
    ]

    for r in results:
        status = "EN LIGNE" if r.online else "Hors ligne / Non équipé"
        part = f"`{r.part_number}`" if r.part_number else "-"
        sw = f"`{r.sw_version}`" if r.sw_version else "-"
        prog = f"`{r.programming_date}`" if r.programming_date else "-"
        sup = r.supplier if r.online else r.supplier_hint
        lines.append(
            f"| **{r.code_renault}** | {r.name} | `{r.tx_id}`/`{r.rx_id}` | {status} | {part} | {sw} | {prog} | {sup} |"
        )

    lines.extend(["", "## Détails UDS par Calculateur (Service 0x22 ReadDataByIdentifier)", ""])
    for r in online_ecus:
        lines.extend(
            [
                f"### [{r.code_renault}] {r.name} (`TX: 0x{r.tx_id}` / `RX: 0x{r.rx_id}`)",
                f"- **Session Diagnostic** : `{r.session_opened}`",
                f"- **Bus CAN** : {r.bus}",
            ]
        )
        for did_key, did_val in r.identifications.items():
            lines.append(
                f"  - **DID `0x{did_key}` ({did_val.label})** : `{did_val.decoded}` *(Hex: `{did_val.raw_hex}`)*"
            )
        lines.append("")

    return "\n".join(lines)


def print_console_summary(
    results: List[EcuScanResult],
    adapter_name: str,
    voltage: str,
    mode_label: str,
) -> None:
    """Affiche un tableau clair dans le terminal (compatible Windows PowerShell / CMD et Linux)."""
    online_ecus = [r for r in results if r.online]
    vins = sorted({r.vin for r in online_ecus if r.vin})
    vehicle_vin = vins[0] if vins else "N/A"

    print("\n" + "=" * 114)
    print(" RENAULT ESPACE V (PHASE 2 - 2.0 Blue dCi & EASY LINK) - EXPLORATEUR CAN / UDS (ISO-14229)")
    print("=" * 114)
    print(f" Interface : {adapter_name} [{mode_label}]")
    print(f" Batterie  : {voltage:<12} | VIN (F190) : {vehicle_vin:<20} | ECUs en ligne : {len(online_ecus)}/{len(results)}")
    print("-" * 114)
    header = f" {'CLÉ':<9} | {'CODE RENAULT':<14} | {'TX/RX':<7} | {'STATUT':<8} | {'RÉF. PIÈCE':<11} | {'VERSION SW':<11} | {'DATE PROG.':<10} | {'FOURNISSEUR'}"
    print(header)
    print("-" * 114)

    for r in results:
        status = "EN LIGNE" if r.online else "ABSENT"
        part = r.part_number or "-"
        sw = r.sw_version or "-"
        prog = r.programming_date or "-"
        sup = r.supplier if r.online else r.supplier_hint
        print(
            f" {r.key:<9} | {r.code_renault:<14} | {r.tx_id}/{r.rx_id} | {status:<8} | {part:<11} | {sw:<11} | {prog:<10} | {sup}"
        )

    print("=" * 114)

    # Zoom spécial sur le système multimédia Easy Link (A-IVI) s'il a répondu
    easylink = next((r for r in online_ecus if r.key == "easylink"), None)
    if easylink:
        print("\n [ZOOM SYSTÈME MULTIMÉDIA EASY LINK 9.3\" (A-IVI / BOSCH - 0x712 -> 0x732)]")
        for did_key, did_val in easylink.identifications.items():
            print(f"   - DID 0x{did_key} ({did_val.label:<42}) : {did_val.decoded}")
    print("")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="espace5-can",
        description="Scanner UDS (ISO-14229) des calculateurs Renault Espace V 2.0 Blue dCi & Easy Link via Vgate iCar Pro BLE.",
    )
    parser.add_argument(
        "--port",
        type=str,
        default=None,
        help="Port série du Vgate iCar Pro BLE (ex: COM4 sous Windows ou /dev/rfcomm0 sous Linux).",
    )
    parser.add_argument(
        "--baudrate",
        type=int,
        default=38400,
        help="Vitesse du port série (défaut: 38400 ou 115200 pour Vgate iCar Pro BLE).",
    )
    parser.add_argument(
        "--simulate",
        action="store_true",
        help="Exécute le scan sur le simulateur intégré Renault Espace 5 2.0 Blue dCi + Easy Link (sans boîtier branché).",
    )
    parser.add_argument(
        "--list-ports",
        action="store_true",
        help="Liste tous les ports COM / Bluetooth détectés sur ce PC Windows/Linux.",
    )
    parser.add_argument(
        "--ecu",
        type=str,
        default=None,
        help=f"Scanne uniquement un calculateur précis parmi : {', '.join(ECU_BY_KEY.keys())}",
    )
    parser.add_argument(
        "--json-out",
        type=str,
        default=None,
        help="Chemin du fichier JSON où sauvegarder l'extraction complète (ex: reports/scan.json).",
    )
    parser.add_argument(
        "--md-out",
        type=str,
        default=None,
        help="Chemin du rapport Markdown où sauvegarder la fiche d'identité (ex: reports/scan.md).",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_ports:
        ports = list_serial_ports()
        if not ports:
            print("Aucun port COM / série détecté.")
            print("Astuce Windows : Appairez 'Android-Vlink' (code 1234) dans Paramètres Bluetooth -> Plus d'options Bluetooth -> Onglet Ports COM.")
            return 0
        print("Ports série / COM détectés :")
        for dev, desc in ports:
            print(f"  - {dev:<12} : {desc}")
        return 0

    if not args.simulate and not args.port:
        print("Erreur : Spécifiez un port COM (--port COM4) ou lancez le mode simulation (--simulate).")
        print("Utilisez --list-ports pour voir les ports Bluetooth COM sous Windows.")
        return 1

    target_ecus: List[EcuDefinition] = ESPACE5_ECUS
    if args.ecu:
        ecu_key = args.ecu.lower().strip()
        if ecu_key not in ECU_BY_KEY:
            print(f"Calculateur inconnu '{args.ecu}'. Valeurs possibles : {', '.join(ECU_BY_KEY.keys())}")
            return 1
        target_ecus = [ECU_BY_KEY[ecu_key]]

    adapter: BaseAdapter
    if args.simulate:
        adapter = SimulatedEspace5Adapter()
        mode_label = "SIMULATION ESPACE V 2.0 Blue dCi"
    else:
        try:
            adapter = SerialElmAdapter(port=args.port, baudrate=args.baudrate)
        except TransportError as exc:
            print(f"[ERREUR CONNEXION] {exc}", file=sys.stderr)
            return 2
        mode_label = f"PORT {args.port} @ {args.baudrate} bps"

    try:
        scanner = Espace5UdsScanner(adapter)
        adapter_name, voltage = scanner.initialize_vgate()

        def on_progress(ecu: EcuDefinition, idx: int, total: int) -> None:
            print(f" [{idx:02d}/{total:02d}] Interrogation UDS 0x{ecu.tx_id}->0x{ecu.rx_id} : {ecu.name}...")

        results = scanner.scan_all_ecus(ecus=target_ecus, progress_cb=on_progress)
        print_console_summary(results, adapter_name, voltage, mode_label)

        if args.json_out:
            out_path = Path(args.json_out)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "timestamp": datetime.datetime.now().isoformat(),
                "adapter": adapter_name,
                "mode": mode_label,
                "battery_voltage": voltage,
                "ecus": [r.to_dict() for r in results],
            }
            out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
            print(f" -> Export JSON sauvegardé dans : {out_path}")

        if args.md_out:
            md_path = Path(args.md_out)
            md_path.parent.mkdir(parents=True, exist_ok=True)
            report = format_markdown_report(results, adapter_name, voltage, mode_label)
            md_path.write_text(report, encoding="utf-8")
            print(f" -> Rapport Markdown sauvegardé dans : {md_path}")

    finally:
        adapter.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
