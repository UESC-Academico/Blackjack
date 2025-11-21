#!/usr/bin/env python3
"""
Script para converter todos os arquivos SVG para PNG
usando cairosvg ou inkscape
"""

import os
import sys
from pathlib import Path

def converter_com_cairosvg():
    """Tenta converter usando cairosvg"""
    try:
        import cairosvg
        from io import BytesIO
        from PIL import Image
    except ImportError:
        print("❌ cairosvg ou Pillow não instalado.")
        print("Execute: pip install cairosvg pillow")
        return False
    
    cartas_path = "Cartas"
    convertidos = 0
    erros = 0
    
    print("🎴 Convertendo SVGs para PNG usando cairosvg...\n")
    
    for root, dirs, files in os.walk(cartas_path):
        for file in files:
            if file.endswith(".svg"):
                svg_path = os.path.join(root, file)
                png_path = svg_path.replace(".svg", ".png")
                
                # Pula se PNG já existe
                if os.path.exists(png_path):
                    print(f"⏭️  Pulando {file} (PNG já existe)")
                    continue
                
                try:
                    print(f"🔄 Convertendo: {file}...", end=" ")
                    
                    # Lê o SVG
                    with open(svg_path, 'r', encoding='utf-8') as f:
                        svg_content = f.read()
                    
                    # Converte para PNG com tamanho fixo
                    png_data = cairosvg.svg2png(
                        bytestring=svg_content.encode('utf-8'),
                        output_width=240,
                        output_height=360
                    )
                    
                    # Salva o PNG
                    with open(png_path, 'wb') as f:
                        f.write(png_data)
                    
                    print("✅")
                    convertidos += 1
                    
                except Exception as e:
                    print(f"❌ Erro: {str(e)[:50]}")
                    erros += 1
    
    print(f"\n📊 Resultado:")
    print(f"   ✅ Convertidos: {convertidos}")
    print(f"   ❌ Erros: {erros}")
    
    return convertidos > 0

def converter_com_inkscape():
    """Tenta converter usando inkscape (linha de comando)"""
    import subprocess
    
    # Verifica se inkscape está instalado
    try:
        subprocess.run(['inkscape', '--version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Inkscape não está instalado.")
        print("Execute: sudo apt-get install inkscape")
        return False
    
    cartas_path = "Cartas"
    convertidos = 0
    
    print("🎴 Convertendo SVGs para PNG usando Inkscape...\n")
    
    for root, dirs, files in os.walk(cartas_path):
        for file in files:
            if file.endswith(".svg"):
                svg_path = os.path.join(root, file)
                png_path = svg_path.replace(".svg", ".png")
                
                # Pula se PNG já existe
                if os.path.exists(png_path):
                    print(f"⏭️  Pulando {file} (PNG já existe)")
                    continue
                
                try:
                    print(f"🔄 Convertendo: {file}...", end=" ")
                    
                    # Converte usando inkscape
                    subprocess.run([
                        'inkscape',
                        svg_path,
                        '--export-filename=' + png_path,
                        '--export-width=240',
                        '--export-height=360'
                    ], capture_output=True, check=True)
                    
                    print("✅")
                    convertidos += 1
                    
                except subprocess.CalledProcessError as e:
                    print(f"❌ Erro")
    
    print(f"\n📊 Resultado: {convertidos} arquivos convertidos")
    return convertidos > 0

if __name__ == "__main__":
    print("=" * 60)
    print("  CONVERSOR DE CARTAS SVG → PNG")
    print("=" * 60)
    print()
    
    # Tenta primeiro com cairosvg (mais rápido)
    sucesso = converter_com_cairosvg()
    
    # Se falhar, tenta com inkscape
    if not sucesso:
        print("\n" + "=" * 60)
        print("Tentando método alternativo com Inkscape...")
        print("=" * 60 + "\n")
        sucesso = converter_com_inkscape()
    
    if sucesso:
        print("\n✅ Conversão concluída com sucesso!")
        print("Agora você pode usar os arquivos PNG no seu jogo.")
    else:
        print("\n❌ Não foi possível converter os arquivos.")
        print("Instale uma das ferramentas:")
        print("  - pip install cairosvg pillow")
        print("  - sudo apt-get install inkscape")

