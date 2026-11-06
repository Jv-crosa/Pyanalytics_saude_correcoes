"""Exibe gráfico Plotly + insight curto."""

import hashlib
from html import escape
import re

import streamlit as st

from charts.theme import adaptar_tema, tem_heatmap, tema_plotly


def plot(fig, insight: str | None = None) -> None:
    """Renderiza o gráfico em largura total, sem barra de ferramentas."""
    fig = adaptar_tema(fig)
    titulo = _extrair_titulo(fig)
    if insight:
        _insight(insight)
    st.markdown(
        '<p class="historia-evidencia">A evidência nos dados</p>',
        unsafe_allow_html=True,
    )
    if titulo:
        st.markdown(
            f'<p class="grafico-titulo">{escape(titulo)}</p>',
            unsafe_allow_html=True,
        )
    if tem_heatmap(fig):
        # O frontend do Streamlit mede primeiro a coluna estreita do celular.
        # Fixar também o canvas Plotly evita uma matriz pequena seguida de vazio.
        fig.update_layout(width=760, autosize=False)
        identidade = hashlib.sha1(titulo.encode("utf-8")).hexdigest()[:10]
        with st.container(key=f"heatmap_plot_{identidade}"):
            st.markdown(
                '<p class="heatmap-ajuda">Deslize para os lados e toque nas células '
                "para ver os valores.</p>",
                unsafe_allow_html=True,
            )
            _plotly(fig, width=760, responsive=False)
        return
    _plotly(fig)


def _extrair_titulo(fig) -> str:
    """Move o título para fora do canvas, onde ele quebra corretamente."""
    bruto = getattr(getattr(fig.layout, "title", None), "text", "") or ""
    texto = re.sub(r"<br\s*/?>", " ", str(bruto), flags=re.IGNORECASE)
    texto = " ".join(texto.split())
    margem = fig.layout.margin.to_plotly_json() if fig.layout.margin else {}
    margem["t"] = 20
    fig.update_layout(title=None, margin=margem)
    return texto


def _plotly(
    fig,
    width: str | int = "stretch",
    responsive: bool = True,
) -> None:
    """Renderiza a figura com a configuração comum do portal."""
    st.plotly_chart(
        fig,
        width=width,
        theme=tema_plotly(fig),
        config={
            "displayModeBar": False,
            "responsive": responsive,
            "scrollZoom": False,
        },
    )


def plot_or_caption(fig, insight: str | None = None) -> None:
    """Mostra o gráfico ou só o recado, se não houver figura."""
    if fig is None:
        _insight(insight or "Sem dados para este gráfico.")
        return
    plot(fig, insight)


def _insight(texto: str) -> None:
    """Apresenta a conclusão antes da evidência visual."""
    seguro = escape(str(texto))
    st.markdown(
        '<div class="historia-significado"><strong>Descoberta em destaque</strong>'
        f"<p>{seguro}</p></div>",
        unsafe_allow_html=True,
    )
