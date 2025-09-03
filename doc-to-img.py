from selenium import webdriver # type: ignore
from selenium.webdriver.common.by import By # type: ignore
import numpy as np # type: ignore

# URL links
#url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
url = "https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub"

driver = webdriver.Chrome()
driver.get(url)


rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

def printArray(arr: list)->None:
    for row in arr:
        print("".join(row))

xMax, yMax = 0, 0
for row in rows[1:]:
    cells = row.find_elements(By.CSS_SELECTOR, "td p span")
    if len(cells) == 3: 
        xValue = int(cells[0].text) # First column with x-coordinates
        yValue = int(cells[2].text) # Third column with x-coordinates
        # Getting the max x and y coordinate to create a new matrix
        xMax = max(xMax, xValue)
        yMax = max(yMax, yValue)

# Printing to check the max x and y values
# print("xMax:", xMax, "yMax:", yMax)

def printGrid(url):
    # Creating an array with blank space
    arr = [['⠀' for _ in range(yMax+1)] for _ in range(xMax+1)]

    # This will fill the array with the correct char
    for row in rows[1:]:
        cells = row.find_elements(By.CSS_SELECTOR, "td p span")
        if len(cells) == 3: 
            x_coordinate = int(cells[0].text)
            char = cells[1].text
            y_coordinate = int(cells[2].text)

            #if char in ('█', '░', '▀'):
            arr[x_coordinate][y_coordinate] = char
            #print("y_coordinate:", y_coordinate, "x_coordinate", x_coordinate, "char", char)
            # else: #Don't need anymore since I already set the value to blank
            #     arr[y_coordinate-1][x_coordinate-1] = '⠀'

    # Normal Print is tiled 90 degrees clockwise
    #printArray(arr)



    # Using numpy I can have it rotate 90 degress counter-clockwise
    npArr = np.array(arr) 
    rotated = np.rot90(npArr, k=1) 
    printArray(rotated.tolist())
 
printGrid(url) # This function takes one argument that prints the grid of characters

driver.quit()
