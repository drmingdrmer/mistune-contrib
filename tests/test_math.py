from mistune import Markdown
from mistune import BlockLexer
from mistune import InlineLexer
from mistune import Renderer
from mistune_contrib import math

MIXED_CASE = '''The entries of $C$ are given by the exact formula:
$$
C_{ik} = \sum_{j=1}^n A_{ij} B_{jk}
$$
but there are many ways to _implement_ this computation.   $\approx 2mnp$ flops
'''


def test_mixed():
    expected = MIXED_CASE.replace("_implement_", "<em>implement</em>")
    # result = md.parse(MIXED_CASE)
    # assert expected in result


CASE_0 = '''Water that is stored in $t$, $s_t$, must equal the storage content of the previous stage,
$s_{t-1}$, plus a stochastic inflow, $I_t$, minus what is being released in $t$, $r_t$.
With $s_0$ defined as the initial storage content in $t=1$, we have'''


CASE_1 = '''$C_{ik}$
$$
C_{ik} = \sum_{j=1}
$$
$C_{ik}$'''


CASE_2 = '''$m$
$$
C = \begin{pmatrix}
          0 & 0 & 0 & \cdots & 0 & 0 & -c_0 \\
          0 & 0 & 0 & \cdots & 0 & 1 & -c_{m-1}
    \end{pmatrix}
$$
$x^m$'''


CASE_3 = '''$r=\overline{1,n}$
$$ {\bf
b}_{i}^{r}(t)=(1-t)\,{\bf b}_{i}^{r-1}(t)+t\,{\bf b}_{i+1}^{r-1}(t),\:
 i=\overline{0,n-r}, $$
i.e. the $i^{th}$'''


def test_paragraph():
    pass

class MathBlockLexer(math.MathBlockMixin, BlockLexer):
    def __init__(self, *args, **kwargs):
        super(MathBlockLexer, self).__init__(*args, **kwargs)
        self.enable_math()

class MathInlineLexer(InlineLexer, math.MathInlineMixin):
    def __init__(self, *args, **kwargs):
        super(MathInlineLexer, self).__init__(*args, **kwargs)
        self.enable_math()

class MathRenderer(Renderer, math.MathRendererMixin):
    pass

class MathMarkdown(Markdown, math.MathMarkdownMixin):
    pass

def test_block_math():

    md = MathMarkdown(MathRenderer(),
                      block=MathBlockLexer)

    res = md('''
$$
y = x^2
$$
''')

    assert 'math-renderer-mixin-block' in res

def test_inline_math():

    r = MathRenderer()
    md = MathMarkdown(r,
                      inline=MathInlineLexer(r))

    res = md('foo: $ y = x^2 $')

    assert 'math-renderer-mixin-inline' in res

def test_latex_math():

    md = MathMarkdown(MathRenderer(),
                      block=MathBlockLexer)

    res = md('''
\\begin{foo}
y = x^2
\\end{foo}
''')

    print res

    assert 'math-renderer-mixin-latex' in res
