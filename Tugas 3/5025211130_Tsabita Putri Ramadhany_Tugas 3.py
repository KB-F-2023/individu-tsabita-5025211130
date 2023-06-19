import plotly.express as px

countries = ["Canada", "Mexico", "United States"]

colors = ["blue", "red", "yellow"]

graphOfCountries = {"Canada": ["United States"],
                    "Mexico": ["United States"],
                    "United States": ["Canada", "Mexico"]
                    }

def sortCountries(graph, unSortedCountries):
    newCountry = {}
    retCountries = []
    for country in unSortedCountries:
        newCountry.update({country: len(graph[country])})

    newCountry = list(sorted(newCountry.items(), key=lambda kv: kv[1]))

    i = len(newCountry) - 1
    while i > -1:
        retCountries.append(newCountry[i][0])
        i -= 1

    return retCountries

def isColoredTheTrue(graph, testMap):
    for node in graph:
        edges = (graph[node])
        if node in testMap.keys():
            colorOfNode = testMap[node]
            for edge in edges:
                if edge in testMap.keys():
                    colorOfEdge = testMap[edge]
                    if colorOfNode == colorOfEdge:
                        return False
    return True

def colorTheCountry(graph, colorMap, unSortedCountries):
    sortedCountries = sortCountries(graphOfCountries, unSortedCountries)
    clr_ix = 1
    cntry_ix = 0
    solverCounter = 0
    isSolved = True
    while cntry_ix < len(sortedCountries):
        if solverCounter == len(colors):
            print("Unsolved Problem")
            isSolved = False
            break
        tmpIx = cntry_ix
        colorMap.update({sortedCountries[cntry_ix]: colors[clr_ix]})
        if not isColoredTheTrue(graph, colorMap):
            cntry_ix -= 1
        if clr_ix < 3:
            clr_ix += 1
        else:
            clr_ix = 0
        cntry_ix += 1
        if tmpIx == cntry_ix:
            solverCounter += 1
        else:
            solverCounter = 0
    return colorMap, isSolved

def plot_choropleth(colormap):
    fig = px.choropleth(locationmode="country names",
                        locations=countries,
                        color=countries,
                        color_discrete_sequence=[colormap[c] for c in countries],
                        scope="north america")
    fig.show()

if __name__ == "__main__":
    # coloring test
    colormap_test = {"Canada": "blue", "Mexico": "red", "United States": "yellow"}

    print(f"colormap_test {isColoredTheTrue(graphOfCountries, colormap_test)} colored.")
    coloringMap = {}
    coloringMap, isTrue = colorTheCountry(graphOfCountries, coloringMap, countries)
    print(f"coloringMap {isColoredTheTrue(graphOfCountries, coloringMap)} colored.")
    if isTrue:
        plot_choropleth(colormap=coloringMap)