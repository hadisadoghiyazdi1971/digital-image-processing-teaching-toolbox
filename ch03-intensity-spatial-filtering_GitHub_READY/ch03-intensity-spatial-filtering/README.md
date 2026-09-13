# Digital Image Processing Teaching Toolbox — Chapter 3

## Intensity Transformations and Spatial Filtering

A clean, classroom-oriented Python toolbox for **Chapter 3: Intensity Transformations and Spatial Filtering**. It provides a small interactive GUI plus **36 independent algorithm modules** so students can connect the mathematics of spatial-domain image processing to executable code and visual results.

This chapter package is intended to live inside the parent repository:

```text
digital-image-processing-teaching-toolbox/
└── chapters/
    └── ch03-intensity-spatial-filtering/
```

![Chapter 3 demo](docs/assets/demo_contact_sheet.png)

## What is covered

The code follows the chapter's main learning path:

1. **Spatial-domain model** — `g(x,y)=T[f(x,y)]` and point operations `s=T(r)`.
2. **Basic intensity transformations** — negative, log, power/gamma, piecewise-linear transforms, thresholding, intensity slicing, and bit-plane slicing.
3. **Histogram processing** — histogram interpretation, equalization, matching/specification, local equalization, and local-statistics enhancement.
4. **Fundamentals of spatial filtering** — neighborhoods, kernels, correlation, convolution, boundary handling, cascaded filters, composite kernels, and separability.
5. **Smoothing spatial filters** — box/averaging, Gaussian, median, and comparisons with nonlinear smoothing.
6. **Sharpening spatial filters** — discrete derivatives, Laplacian sharpening, unsharp masking, high-boost filtering, Roberts and Sobel gradients.
7. **Lowpass-derived filter families** — highpass, bandreject, and bandpass construction, including a zone-plate test image.
8. **Combining enhancement methods** — a multi-stage spatial enhancement pipeline.

The chapter's overall structure and learning goals are aligned with the source material, which distinguishes pixelwise intensity transformations from neighborhood-based spatial filtering and emphasizes smoothing, sharpening, lowpass/highpass relationships, and combinations of methods.

### Educational extensions beyond the core chapter

Several useful methods are clearly marked as **extensions** rather than textbook-core items:

- Sigmoid tone mapping
- `asinh` dynamic-range compression
- Window/level transform
- CLAHE
- Bilateral filtering
- Prewitt gradient
- Scharr gradient
- Additional order-statistic filters

These are included to show how the general models in the chapter connect to modern practical image processing.

## GUI

The GUI is implemented with **Tkinter**, Python's standard lightweight desktop GUI toolkit. Tkinter is only the visual shell: buttons, menus, parameter boxes, file browsing, and image display. The actual image-processing mathematics lives in separate files under `algorithms/`.

The GUI supports:

- built-in standard/synthetic images;
- browsing for a local input image;
- browsing for a separate reference image for histogram matching;
- algorithm category and algorithm selection;
- editable parameters;
- side-by-side input/output views;
- histogram display;
- output saving.

## Quick start on Windows — recommended Python 3.12 path

This repository deliberately avoids custom VPN/DNS installers. If Python 3.12 and the scientific packages are already available, use the simple path below.

First check the environment:

```text
CHECK_ENV.cmd
```

If all packages report a version and Tkinter reports `OK`, launch:

```text
RUN_TOOLBOX.cmd
```

### Manual installation

Recommended: **Python 3.12, 64-bit**.

```bat
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

If you prefer to use an existing Python 3.12 installation in which the packages are already installed:

```bat
py -3.12 app.py
```

Required packages are NumPy, SciPy, scikit-image, Pillow, and Matplotlib. Tkinter normally ships with the standard Windows Python installer.

## Run algorithms independently

Each method has its own file and can be studied without the GUI.

Examples:

```bat
py -3.12 algorithms\gamma_transform.py --param gamma=0.4 --output outputs\gamma.png
```

```bat
py -3.12 algorithms\median_filter.py --param size=5 --output outputs\median.png
```

A kernel containing commas can be passed safely with the repeatable `--param` syntax:

```bat
py -3.12 algorithms\convolution_filter.py --param "kernel=0,-1,0;-1,5,-1;0,-1,0" --output outputs\sharp.png
```

If `--input` is omitted, the standalone modules use `skimage.data.camera()`.

## Test the package

Run:

```text
RUN_SMOKE_TEST.cmd
```

or:

```bat
py -3.12 tests\smoke_test.py
```

The test exercises all **36 registered algorithms** using deterministic inputs and verifies that each returns a finite 2-D result.

## Project structure

```text
ch03-intensity-spatial-filtering/
├── app.py
├── algorithm_registry.py
├── image_sources.py
├── demo_all.py
├── algorithms/                  # 36 independent processing modules
├── samples/                     # redistributable and synthetic images
├── tests/                       # smoke test
├── docs/
│   ├── CHAPTER3_CONCEPTS_FA.md  # comprehensive Persian chapter/code guide
│   ├── CHAPTER3_MAPPING_FA.md   # chapter-to-code map
│   ├── OPTIONS_GUIDE_FA.md      # every GUI option and parameter
│   ├── TEACHING_PATH_FA.md      # suggested lab/lecture sequence
│   ├── TECHNICAL_NOTES.md
│   └── GITHUB_REFERENCES.md
├── outputs/                     # generated outputs (ignored by Git)
├── CHECK_ENV.cmd
├── RUN_TOOLBOX.cmd
├── RUN_SMOKE_TEST.cmd
├── requirements.txt
├── LICENSE
└── .gitignore
```

## Documentation

Persian teaching documentation is the main companion to the code:

- [`docs/CHAPTER3_CONCEPTS_FA.md`](docs/CHAPTER3_CONCEPTS_FA.md): complete conceptual map of the chapter, key equations, relationships, applications, and corresponding code.
- [`docs/OPTIONS_GUIDE_FA.md`](docs/OPTIONS_GUIDE_FA.md): all GUI algorithms, parameters, interpretation, and suggested values.
- [`docs/CHAPTER3_MAPPING_FA.md`](docs/CHAPTER3_MAPPING_FA.md): direct chapter-topic-to-source-file mapping.
- [`docs/TEACHING_PATH_FA.md`](docs/TEACHING_PATH_FA.md): a suggested sequence for class/lab/video teaching.
- [`docs/GITHUB_REFERENCES.md`](docs/GITHUB_REFERENCES.md): upstream scientific-library repositories and APIs.

## Images and copyright

This public package **does not redistribute figures or pages from the Gonzalez & Woods textbook**. Standard images loaded through `skimage.data` stay in the installed scikit-image package. Bundled samples are synthetic or documented as redistributable; see [`samples/SAMPLE_LICENSES.md`](samples/SAMPLE_LICENSES.md).

The code is an independent educational implementation. The textbook remains a recommended conceptual reference, but its copyrighted text and figures are not included here.

## License

Code in this chapter package is released under the MIT License. Third-party libraries and sample images remain under their own licenses/terms.
