Details see https://jwalton.info/Embed-Publication-Matplotlib-Latex/.

Make sure to include `\usepackage{graphicx}` in your tex-preamble.

Obtain the `width` argument of `set_size` by using

```latex
% your document class here
\documentclass{report}
\begin{document}

% gives the width of the current document in pts
\showthe\textwidth

\end{document}
```