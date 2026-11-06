"""Perfis de cuidado e tratamento na farmácia básica."""

import streamlit as st

from charts import med_perfis as graficos
from data.prepare_med import load_med, periodo_med
from views.common import exige
from views.sim_tema import cabecalho, descoberta_ativa, secao


def render() -> None:
    """Página de perfis (notebook Sprint 2)."""
    df = exige(load_med, "Nenhuma dispensação encontrada.")
    periodo = periodo_med(df)
    cabecalho(
        "Quais perfis de cuidado e tratamento aparecem?",
        f"Farmácia Básica · {periodo} · {len(df):,} registros",
        "medicamentos",
        total_descobertas=6,
    )
    secao("Distribuição dos perfis", graficos.volume_por_perfil(df, periodo))
    secao("Perfis menos frequentes", graficos.perfis_menos_frequentes(df, periodo))
    secao("Participação percentual", graficos.participacao_pizza(df, periodo))
    secao("Top 5 medicamentos por perfil", (None, "Veja a tabela detalhada abaixo."))
    if descoberta_ativa(3):
        st.dataframe(graficos.top5_por_perfil(df), hide_index=True, width='stretch')
    secao("Top 10 geral", graficos.top10_medicamentos(df, periodo))
    secao("Evolução mensal", graficos.evolucao_mensal_perfis(df, periodo))
