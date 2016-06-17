from urllib import urlopen
from reportlab.graphics.shapes import *
from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics import renderPDF

URL = 'http://services.swpc.noaa.gov/text/predicted-sunspot-radio-flux.txt'
COMMENT_CHARS="#:"

# Retrieve and Normalize Data
data = []
for line in urlopen(URL):
    if not line.isspace() and not line[0] in COMMENT_CHARS:
        data.append([float(n) for n in line.split()])
        
# Extract Features from Data
pred = [row[2] for row in data]
high = [row[3] for row in data]
low =[row[4] for row in data]
times = [row[0]+row[1]/12.0 for row in data]

# Set Painter and Computed Data
lp = LinePlot()
lp.x = 50
lp.y = 50
lp.height = 125
lp.width = 300
lp.data = [zip(times, pred), zip(times, high), zip(times, low)]
lp.lines[0].strokeColor = colors.blue #pred
lp.lines[1].strokeColor = colors.red #high
lp.lines[2].strokeColor = colors.green #low
        
# Draw Data
drawing = Drawing(400,200)
drawing.add(lp)
drawing.add(String(250, 150, 'Sunspot', fontSize=14, fillColor=colors.red))
renderPDF.drawToFile(drawing, "report.pdf", 'A PDF for Predicted Sunspot Number')