import plotly.express as px
import plotly.graph_objects as go


def get_time_series_fig(fig_type, df, x, y, color, title, template=None, width=800, height=400):
    if fig_type == 'line':
        fig= px.line(df, x=x, y=y, color=color)
    elif fig_type == 'bar':
        fig= px.bar(df, x=x, y=y, color=color)
    elif fig_type == 'area':
        fig= px.area(df, x=x, y=y, color=color)
    else:
        fig= None

    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center'),
        xaxis_title=x,
        yaxis_title=y,
        # legend_title=color,
        template=template,
        width=width,
        height=height,
        hovermode='x unified',
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Arial", size=12, color="Black")
    )
    return fig

def get_hierarchical_fig(fig_type, df, path, values, title, template=None, width=800, height=400):
    if fig_type=="treemap":
        fig = px.treemap(df, path=path, values=values, title=title)
    elif fig_type=="sunburst":
        fig = px.sunburst(df, path=path, values=values, title=title)
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center'),
        template=template,
        width=width,
        height=height,
        margin=dict(l=40, r=40, t=60, b=40),
        font=dict(family="Arial", size=12, color="Black")
    )
    return fig  