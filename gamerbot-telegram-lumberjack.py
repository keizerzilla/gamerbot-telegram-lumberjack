import pyautogui as pag

config = {
    "left" : {
        "click_x" : 876,
        "click_y" : 924,
        "branch" : "left_branch.png",
        "region" : (824, 575, 111, 69),
    },
    "right" : {
        "click_x" : 1044,
        "click_y" : 924,
        "branch" : "right_branch.png",
        "region" : (985, 575, 111, 69),
    },
}

c = config["right"]

for i in range(400): # por que não infinitamente???
    if pag.locateOnScreen(c["branch"], grayscale=True, region=c["region"], confidence=0.9):
        c = config["right"] if c == config["left"] else config["left"]
    
    pag.click(c["click_x"], c["click_y"])

print("Game Over")
