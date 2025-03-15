---

# Análise de Ossos 3D com IA

Este repositório tem como objetivo geral demonstrar um **pipeline** para **analisar ossos em 3D** usando **técnicas de Inteligência Artificial**, com aplicação voltada à **antropologia forense**.  
Atualmente, o projeto **possui** apenas o **conversor de arquivos DICOM para OBJ**, mas **futuramente** incluirá scripts de **pré-processamento, renderização de vistas 2D e treinamento de redes neurais** (CNN, etc.).

## Estrutura do Projeto

```
analysis_bones/
├── data_dicom/
│   └── humeral1/         # Exemplo de pasta com arquivos .dcm para um osso (úmero)
├── data_3d/
│   └── humeral1.obj      # Saída em formato .obj gerado a partir da conversão
├── scripts/
│   └── convert_dicom_to_obj.py
└── README.md
```

### O que está implementado até agora?

- **Conversor de DICOM para OBJ**: Script que lê arquivos `.dcm` (provenientes de tomografias), reconstrói o volume 3D e, por meio do algoritmo Marching Cubes, gera uma malha `.obj`.

### O que será implementado futuramente?

- **Pré-processamento** das malhas `.obj` (normalização de escala, alinhamento anatômico, redução de polígonos).
- **Renderização Multi-View** das malhas (geração de imagens 2D a partir de diferentes ângulos).
- **Treinamento e avaliação** de modelos de IA (como CNNs ou redes 3D) para classificação de ossos, detecção de fraturas etc.

---

## Conversor DICOM para OBJ

Arquivo principal: **`convert_dicom_to_obj.py`**

### Descrição

1. **Leitura de arquivos DICOM**:  
   - Pode ler uma pasta com múltiplos `.dcm` (fatiamento de tomografia) ou um único `.dcm` volumétrico.
2. **Reconstrução do volume** em um array NumPy.
3. **Extração da superfície** (do osso ou região de interesse) via Marching Cubes, aplicando um limite (threshold) de Hounsfield Units (HU).
4. **Geração de malha** em formato `.obj`, que pode ser visualizada e editada em ferramentas como Blender ou MeshLab.

### Dependências

- **Python 3.7+**
- [SimpleITK](https://simpleitk.org/) ou [pydicom](https://pydicom.github.io/) (para leitura de DICOM)
- [NumPy](https://numpy.org/) (manipulação de arrays)
- [scikit-image](https://scikit-image.org/) (função de Marching Cubes)
- [trimesh](https://github.com/mikedh/trimesh) (exportar e manipular malhas 3D)

Instale, por exemplo, com:
```bash
pip install SimpleITK numpy scikit-image trimesh
```

### Como usar

1. Se estiver no Windows (via PowerShell, por exemplo), navegar até a pasta `scripts/` (ou usar caminho completo para o script).
2. Executar o comando, passando o **caminho** da pasta (ou arquivo) DICOM como primeiro parâmetro e o **caminho de saída** do `.obj` como segundo parâmetro, além da flag `--threshold` para ajustar o valor de corte:

```bash
python convert_dicom_to_obj.py \
  "../data_dicom/humeral1" \
  "../data_3d/humeral1.obj" \
  --threshold 300
```

- Ajuste `--threshold` conforme necessário (valores típicos de HU para ossos variam entre 200 e 700, dependendo do tipo de tecido ósseo que se deseja extrair).

### Observações

- Se a pasta `.dcm` contiver muitas fatias (por exemplo, 100+ arquivos), isso geralmente corresponde a **um só osso** segmentado em várias “fatias” de tomografia.
- Verifique a qualidade da malha no Blender/MeshLab após a conversão para avaliar se foi capturado apenas o osso e se há necessidade de refinamento (remoção de ruído, oclusões, etc.).
- Se quiser apagar a pasta `.venv` ou outros arquivos não relevantes do versionamento, inclua no `.gitignore`.

---

## Próximos Passos

1. **Pré-processar** as malhas geradas em `.obj` (alinhamento, redução de polígonos, remoção de ruídos).
2. **Renderizar** as malhas em **vistas 2D** (usando `pyrender` ou similar).
3. **Treinar** modelos de IA (CNN 2D ou redes 3D tipo PointNet) para classificação e/ou detecção de fraturas.

Fique à vontade para **abrir issues** ou **enviar pull requests** com sugestões de melhoria!

---

**Autor(es)**: Luiz Guilherme Rezende Paes 
