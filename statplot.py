import matplotlib.pyplot as plt
import seaborn as sns

def graph(df, figsize, pal='Paired', alpha=0.5):
    df['function'] = df['function'].astype('category')
    fig, g = plt.subplots(figsize=figsize)

    sns.lineplot(data=df, x='n', y='mean', hue='function',
                 ci=None, ax=g, palette=pal)

    n_cats = df['function'].cat.categories.size
    colors = [g.get_lines()[i].get_color() for i in range(n_cats)]
    
    for (_, bounds), i in zip(df.groupby('function'), range(n_cats)):
        g.fill_between(bounds['n'], y1=bounds['low'], y2=bounds['high'],
                       alpha=alpha, color=colors[i])

    return fig, g
