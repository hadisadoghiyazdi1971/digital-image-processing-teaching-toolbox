# Technical Notes

- Internal intensity representation: float64 in [0,1].
- Most Chapter 3 operations convert RGB input to grayscale.
- Derivative responses may be signed; GUI-oriented modules normalize signed responses when `display_scale=True`.
- Boundary default is `reflect` to avoid strong artificial zero-padding edges in demonstrations.
- Histogram matching needs a second reference image.
