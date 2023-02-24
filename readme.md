# myplotlib

Make matplotlib consistent with latex. 

Install with 

`pip install git+https://github.com/SimiPixel/myplotlib`

Implements (mostly) what is described there https://jwalton.info/Embed-Publication-Matplotlib-Latex/.

## Getting started

In Python:

```python
import matplotlib.pyplot as plt
from myplotlib import savefig, setup, figsize

latex_page_width = 420 # pts
setup(latex_page_width)

# exactly halfpage wide in latex document
plt.figure(figsize=figsize(fraction=0.5, ratio=16/9))
plt.plot(...)

# saves by default as .pdf
savefig("my_figure")
```

In Latex:

```latex
\usepackage{graphicx}

% begin document

\begin{figure}
  \centering
  \includegraphics{my_figure.pdf}
\end{figure}
```

## Getting `latex_page_width`

Obtain the `width_pt` argument of `figsize` by using

```latex
% your document class here
\documentclass{report}
\begin{document}

% gives the width of the current document in pts
\showthe\textwidth

\end{document}
```