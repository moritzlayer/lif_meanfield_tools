import requests

color_ranges = [(95, 'brightgreen'),
                (90, 'green'),
                (75, 'yellowgreen'),
                (60, 'yellow'),
                (40, 'orange'),
                (0, 'red')]

# get coverage from coverage report
with open('report.txt', 'r') as file:
    data = file.read().replace('\n', '')
    
# extract total coverage without percept sign
coverage = int(data.split()[-1][:-1])

# get color
for color_range in color_ranges:
    if coverage >= color_range[0]:
        color = color_range[1]
        print(color)
        break

# download respective badge from shields.io and save to readme_figures
image_url = f"https://img.shields.io/badge/coverage-{coverage}%25-{color}.svg"
print(image_url)
img_data = requests.get(image_url).content
with open('readme_figures/coverage.svg', 'wb') as handler:
    handler.write(img_data)
