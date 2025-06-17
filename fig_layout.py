my_figlayout = {
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'font': {
        'family': 'Roboto, Arial, sans-serif',
        'size': 12,
        'color': '#FFFFFF'
    },
    'title': {
        'font': {
            'family': 'Roboto, Arial, sans-serif',
            'size': 18,
            'color': '#FFFFFF'
        },
        'x': 0.5,
        'xanchor': 'center'
    },
    'xaxis': {
        'gridcolor': 'rgba(255,255,255,0.1)',
        'tickfont': {'color': '#FFFFFF'},
        'title': {
            'font': {'color': '#FFFFFF'}
        }
    },
    'yaxis': {
        'gridcolor': 'rgba(255,255,255,0.1)',
        'tickfont': {'color': '#FFFFFF'},
        'title': {
            'font': {'color': '#FFFFFF'}
        }
    },
    'legend': {
        'font': {'color': '#FFFFFF'},
        'bgcolor': 'rgba(0,0,0,0)',
        'bordercolor': 'rgba(255,255,255,0.2)',
        'borderwidth': 1
    },
    'hoverlabel': {
        'bgcolor': 'rgba(0,0,0,0.8)',
        'font': {'color': '#FFFFFF'}
    },
    'margin': {
        'l': 50,
        'r': 50,
        't': 50,
        'b': 50
    },
    'autosize': True,
    'height': 400
}


dark_theme_layout =  {
    'plot_bgcolor': '#0f172a',  # Slate-900
    'paper_bgcolor': '#020617',  # Slate-950
    'font': {
        'family': 'Inter, Segoe UI, Arial, sans-serif',
        'size': 14,
        'color': '#e2e8f0'  # Slate-200
    },
    'title': {
        'font': {
            'family': 'Inter, Segoe UI, Arial, sans-serif',
            'size': 24,
            'color': '#7dd3fc'  # Sky-300
        },
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    'xaxis': {
        'gridcolor': '#1e293b',  # Slate-800
        'zerolinecolor': '#38bdf8',  # Sky-400
        'tickcolor': '#475569',  # Slate-600
        'tickfont': {'color': '#cbd5e1'},  # Slate-300
        'titlefont': {'color': '#f1f5f9'},  # Slate-50
        'linecolor': '#475569',
        'mirror': True
    },
    'yaxis': {
        'gridcolor': '#1e293b',
        'zerolinecolor': '#4ade80',  # Green-400
        'tickcolor': '#475569',
        'tickfont': {'color': '#cbd5e1'},
        'titlefont': {'color': '#f1f5f9'},
        'linecolor': '#475569',
        'mirror': True
    },
    'legend': {
        'font': {'color': '#f9fafb'},  # Gray-50
        'bgcolor': 'rgba(2,6,23,0.85)',  # Slate-950 semi
        'bordercolor': '#334155',  # Slate-700
        'borderwidth': 1,
        'orientation': 'h',
        'x': 0.5,
        'xanchor': 'center',
        'y': -0.2
    },
    'hoverlabel': {
        'bgcolor': '#1e293b',  # Slate-800
        'font': {'color': '#f8fafc'},  # Slate-50
        'bordercolor': '#38bdf8'
    },
    'margin': {
        'l': 60,
        'r': 60,
        't': 60,
        'b': 60
    },
    'autosize': True,
    'height': 420
}