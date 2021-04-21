import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go


class PlotlyHelper:
    def default_plotly_colors():
        return plotly.colors.DEFAULT_PLOTLY_COLORS

    def plotly_colors_used(fig):
        return list(set([trace['line']['color']for trace in fig['data']]))

    def recolor(fig):
        fig = go.Figure(fig)
        faded_colors = {'#636efa': '#ced1fd',
                        '#EF553B': '#fbd6d0',
                        '#19d3f3': '#b6f1fb',
                        '#FFA15A': '#ffe2cc',
                        '#B6E880': '#daf3be',
                        '#00cc96': '#ccfff1',
                        '#FF6692': '#ffccda',
                        '#ab63fa': '#e5cefd'}
        cluster_color = {}

        for trace in fig['data']:
            trace['showlegend'] = False
            old_color = trace['line']['color']
            if old_color in faded_colors:
                trace['line']['color'] = faded_colors[old_color]
                if trace['legendgroup'] not in cluster_color:
                    cluster_color[trace['legendgroup']] = old_color

        return fig, cluster_color

    def plot_cluster_center(model, train_data, fig, cluster_color, df_clusters=None):
        fig = go.Figure(fig)
        df_centers = pd.DataFrame(np.squeeze(model.cluster_centers_)).T
        df_centers.index = train_data.index
        max_val = df_clusters.groupby('Cluster')['Cases'].max()
        min_val = df_clusters.groupby('Cluster')['Cases'].min()
    #     if df_centers.max().max() <=1

        for col in df_centers.columns:
            fig = fig.add_scattergl(x=df_centers.index, y=df_centers[col], legendgroup=col, line={
                                    'color': cluster_color[str(col)]}, name=str(col))
        return fig
