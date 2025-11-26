# flatten_chain.py

import json
import csv
from pathlib import Path


def flatten_chain(chain: dict):
    """
    Turn Schwab option chain into a flat iterable of dicts (one per contract).
    Works for both calls and puts.
    """
    underlying_symbol = chain.get("symbol")
    underlying_price = chain.get("underlyingPrice")
    interest_rate = chain.get("interestRate")
    base_iv = chain.get("volatility")

    rows = []

    def process_side(exp_map_key: str):
        exp_map = chain.get(exp_map_key, {}) or {}
        for exp_key, strikes in exp_map.items():
            # exp_key looks like "2025-11-28:3"
            exp_date, _, dte_str = exp_key.partition(":")
            for strike_str, contracts in strikes.items():
                for opt in contracts:
                    bid = opt.get("bid")
                    ask = opt.get("ask")
                    mid = None
                    if bid is not None and ask is not None and bid > 0 and ask > 0:
                        mid = (bid + ask) / 2.0

                    rows.append(
                        {
                            "underlying": underlying_symbol,
                            "underlying_price": underlying_price,
                            "put_call": opt.get("putCall"),
                            "option_symbol": opt.get("symbol"),
                            "root": opt.get("optionRoot"),
                            "expiry": exp_date,
                            "dte_key": dte_str,  # DTE encoded in the map key
                            "days_to_expiration": opt.get("daysToExpiration"),
                            "strike": opt.get("strikePrice"),
                            "bid": bid,
                            "ask": ask,
                            "mid": mid,
                            "last": opt.get("last"),
                            "mark": opt.get("mark"),
                            "volume": opt.get("totalVolume"),
                            "open_interest": opt.get("openInterest"),
                            "iv": opt.get("volatility"),
                            "delta": opt.get("delta"),
                            "gamma": opt.get("gamma"),
                            "theta": opt.get("theta"),
                            "vega": opt.get("vega"),
                            "rho": opt.get("rho"),
                            "intrinsic_value": opt.get("intrinsicValue"),
                            "extrinsic_value": opt.get("extrinsicValue"),
                            "in_the_money": opt.get("inTheMoney"),
                            "expiration_type": opt.get("expirationType"),
                            "exercise_type": opt.get("exerciseType"),
                            "interest_rate_chain": interest_rate,
                            "base_chain_iv": base_iv,
                        }
                    )

    process_side("callExpDateMap")
    process_side("putExpDateMap")

    return rows


def main():
    # Adjust path if needed
    input_path = Path("output") / "chains_AAPL.json"
    output_path = Path("output") / "aapl_chain_flat.csv"

    with input_path.open() as f:
        chain = json.load(f)

    rows = flatten_chain(chain)
    if not rows:
        print("No option rows found.")
        return

    # Use the keys of the first row as CSV header
    fieldnames = list(rows[0].keys())

    with output_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
