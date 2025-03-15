import os
import argparse
import numpy as np

# Opção 1: Usando SimpleITK (leitura de DICOM em volume)
import SimpleITK as sitk

# Para gerar malha a partir do volume (módulo measure do scikit-image)
from skimage import measure

# Para salvar a malha em .obj
import trimesh


def load_dicom_volume(dicom_path):
    """
    Carrega um volume (ou série de fatias DICOM) usando SimpleITK.
    Se dicom_path for uma pasta contendo várias fatias .dcm,
    ou um único arquivo .dcm volumétrico.
    Retorna um NumPy array 3D (formato [z, y, x]) e o espaçamento dos voxels.
    """
    # Verifica se é um diretório (várias fatias) ou arquivo único
    if os.path.isdir(dicom_path):
        # Lê a série de imagens DICOM na pasta
        reader = sitk.ImageSeriesReader()
        dicom_files = reader.GetGDCMSeriesFileNames(dicom_path)
        reader.SetFileNames(dicom_files)
        image = reader.Execute()
    else:
        # Lê um único arquivo DICOM
        image = sitk.ReadImage(dicom_path)

    # Converte para array NumPy
    volume = sitk.GetArrayFromImage(image)  # Eixo 0 = fatias (z), 1 = y, 2 = x
    spacing = image.GetSpacing()           # Espaçamento em mm (x, y, z), dependendo de como foi salvo

    return volume, spacing


def volume_to_mesh(volume, level=300, spacing=(1.0, 1.0, 1.0)):
    """
    Converte um volume em malha 3D usando Marching Cubes.
    - volume: array 3D (z, y, x)
    - level: valor de limiar (threshold) para extrair a superfície do osso (em Hounsfield Units no caso de TC).
    - spacing: espaçamento do voxel em (x, y, z).
    Retorna vértices e faces.
    """
    # Marching cubes do scikit-image assume (z, y, x) como (plane, row, col).
    # Se seu volume estiver em Hounsfield Units, defina um valor de limiar que represente o osso cortical/trabecular.
    verts, faces, normals, values = measure.marching_cubes(volume, level=level, spacing=spacing)

    return verts, faces


def save_mesh_as_obj(verts, faces, output_path):
    """
    Cria uma malha trimesh a partir de vértices e faces, e salva em .obj.
    """
    mesh = trimesh.Trimesh(vertices=verts, faces=faces)
    mesh.export(output_path)
    print(f"Arquivo salvo: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Converter DICOM para OBJ.")
    parser.add_argument("dicom_path", type=str, help="Caminho para o arquivo/pasta DICOM.")
    parser.add_argument("output_obj", type=str, help="Caminho de saída para o arquivo .obj.")
    parser.add_argument("--threshold", type=float, default=300,
                        help="Threshold (HU) para o Marching Cubes (padrão=300).")
    args = parser.parse_args()

    # Carrega volume
    volume, spacing = load_dicom_volume(args.dicom_path)
    print("Volume shape:", volume.shape)
    print("Voxel spacing:", spacing)

    # Converte volume em malha
    verts, faces = volume_to_mesh(volume, level=args.threshold, spacing=(spacing[2], spacing[1], spacing[0]))
    # Observação: verifique a ordem do spacing, pois alguns datasets guardam (z, y, x) ou (x, y, z).

    # Salva em .obj
    save_mesh_as_obj(verts, faces, args.output_obj)


if __name__ == "__main__":
    main()
