import sys
import os
import subprocess

def compress_pdf(input_file, output_file, min_size_kb=300, max_size_kb=400):
    # Define quality levels
    quality_levels = ['/screen', '/ebook', '/prepress', '/printer', '/default']

    for quality in quality_levels:
        # Ghostscript command
        gs_command = [
            'gs', '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
            f'-dPDFSETTINGS={quality}', '-dNOPAUSE', '-dQUIET', '-dBATCH',
            f'-sOutputFile={output_file}', input_file
        ]

        # Run Ghostscript
        subprocess.run(gs_command, check=True)

        # Check the size of the compressed file
        output_size = os.path.getsize(output_file) / 1024  # Size in KB

        if min_size_kb <= output_size <= max_size_kb:
            print(f"Successfully compressed PDF to {output_size:.2f} KB using quality setting {quality}")
            return True
        elif output_size < min_size_kb:
            print(f"File size {output_size:.2f} KB is below minimum size with quality {quality}. Trying higher quality.")
        else:
            print(f"File size {output_size:.2f} KB is above maximum size with quality {quality}. Trying lower quality.")

    print(f"Could not compress to target range. Final size: {output_size:.2f} KB with quality {quality}")
    return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_compressor_ghostscript_balanced.py <input_pdf_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = "compressed_" + os.path.basename(input_file)

    compress_pdf(input_file, output_file)
