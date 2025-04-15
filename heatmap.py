import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import argparse
import os

def read_rtl_power_csv(filename):
    freqs = None
    times = []
    powers = []

    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            row = [field.strip() for field in row]  # Sanitize whitespace
            if len(row) < 6:
                continue
            try:
                timestamp = datetime.datetime.strptime(f"{row[0]}T{row[1]}", "%Y-%m-%dT%H:%M:%S")
                f_low = float(row[2])
                f_high = float(row[3])
                bin_size = float(row[4])  # Allow decimal values like '976.56'
                power_vals = list(map(float, row[6:]))
            except (ValueError, IndexError):
                continue

            times.append(timestamp)
            if freqs is None:
                freqs = np.linspace(f_low, f_high, len(power_vals))
            powers.append(power_vals)

    return np.array(freqs), np.array(times), np.array(powers).T

def plot_heatmap(freqs, times, powers, output_base=None, save_png=False, save_pdf=False, fmin=None, fmax=None, threshold=None):
    # Frequency trimming
    if fmin is not None or fmax is not None:
        mask = np.ones_like(freqs, dtype=bool)
        if fmin is not None:
            mask &= freqs >= fmin
        if fmax is not None:
            mask &= freqs <= fmax
        freqs = freqs[mask]
        powers = powers[mask, :]

    # Power threshold masking
    if threshold is not None:
        powers = np.where(powers >= threshold, powers, np.nan)

    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(
        powers,
        aspect='auto',
        extent=[times[0], times[-1], freqs[0], freqs[-1]],
        origin='lower',
        cmap='plasma'
    )
    plt.colorbar(im, ax=ax, label='Power (dB)')
    ax.set_title("RTL-SDR Spectrum Heatmap")
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequency (Hz)" if np.max(freqs) > 1e5 else "Frequency (MHz)")
    fig.autofmt_xdate()

    if output_base:
        if save_png:
            plt.savefig(f"{output_base}.png", dpi=200)
        if save_pdf:
            plt.savefig(f"{output_base}.pdf")
    else:
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a heatmap from rtl_power CSV output.")
    parser.add_argument("input", help="rtl_power CSV input file")
    parser.add_argument("--png", action="store_true", help="Save output as PNG")
    parser.add_argument("--pdf", action="store_true", help="Save output as PDF")
    parser.add_argument("--output", help="Base name for output file (no extension)")
    parser.add_argument("--fmin", type=float, help="Minimum frequency (Hz) to display")
    parser.add_argument("--fmax", type=float, help="Maximum frequency (Hz) to display")
    parser.add_argument("--threshold", type=float, help="Power threshold (dB), values below are dimmed")

    args = parser.parse_args()
    freqs, times, powers = read_rtl_power_csv(args.input)
    output_base = args.output or os.path.splitext(os.path.basename(args.input))[0]

    plot_heatmap(
        freqs, times, powers,
        output_base=output_base,
        save_png=args.png,
        save_pdf=args.pdf,
        fmin=args.fmin,
        fmax=args.fmax,
        threshold=args.threshold
    )
