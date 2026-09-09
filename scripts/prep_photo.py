import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prepare_photo(input_path: str):
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"Erro: imagem não encontrada: {input_path}")
        sys.exit(1)

    print(f"Lendo imagem: {input_path}")

    # ---------------------------------------------------------
    # 1. Remover fundo usando rembg
    # ---------------------------------------------------------
    print("Removendo fundo...")

    image = Image.open(input_path).convert("RGBA")

    # O rembg retorna uma imagem RGBA.
    # As partes removidas ficam transparentes.
    image_no_bg = remove(image)

    # ---------------------------------------------------------
    # 2. Colocar a pessoa sobre um fundo branco
    # ---------------------------------------------------------
    print("Adicionando fundo branco...")

    white_background = Image.new(
        "RGBA",
        image_no_bg.size,
        (255, 255, 255, 255)
    )

    white_background.alpha_composite(image_no_bg)

    image_rgb = white_background.convert("RGB")

    # Converter PIL -> NumPy/OpenCV
    image_cv = np.array(image_rgb)

    # ---------------------------------------------------------
    # 3. Converter para escala de cinza
    # ---------------------------------------------------------
    gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)

    # ---------------------------------------------------------
    # 4. Aplicar CLAHE
    # Melhora o contraste local do rosto, cabelo, roupa etc.
    # ---------------------------------------------------------
    print("Aplicando contraste CLAHE...")

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # ---------------------------------------------------------
    # 5. Salvar resultado
    # ---------------------------------------------------------
    output_path = input_path.parent / "source-prepped.png"

    cv2.imwrite(str(output_path), enhanced)

    print()
    print("Foto preparada com sucesso!")
    print(f"Arquivo gerado: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("python scripts/prep_photo.py source-photo.jpg")
        sys.exit(1)

    prepare_photo(sys.argv[1])