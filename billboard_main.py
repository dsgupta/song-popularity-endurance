import billboard
import pandas as pd

columns = ['title', 'artist', 'weeks', 'rank', 'peakPos', 'lastPos', 'isNew', 'date']

df = pd.DataFrame()

hits = []

chart = billboard.ChartData('hot-100')

while chart.previousDate:
    chart = billboard.ChartData('hot-100', chart.previousDate)
    for entry in chart.entries:
        hits.append({'title': entry.title, 'artist': entry.artist, 'weeks': entry.weeks, 'rank': entry.rank,
                     'peakPos': entry.peakPos, 'lastPos': entry.lastPos, 'isNew': entry.isNew, 'date': chart.date})
df = df.append(hits, ignore_index=True)
df.to_csv('../data/billboard_3.csv')
