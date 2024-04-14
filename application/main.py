from fastapi import FastAPI
from fastapi.responses import JSONResponse 
from chess import GameBoard

app = FastAPI()
board = GameBoard()

def get_x_y(pos):
    s = 'abcdefgh'
    return s.index(pos[0]) + 1, int(pos[1])

@app.get("/board", response_model=list)
def return_board():
    js_data = {}
    for x in range(1, 9):  # Rows
        for y in range(1, 9):  # Columns
            piece = board.squares[(x, y)]
            js_data[f"{x}:{y}"] = piece.__dict__ if piece else None
    return JSONResponse(js_data)

    

@app.put("/move/{from_pos}/{to_pos}")
def move(from_pos: str, to_pos: str):
    board.make_move(get_x_y(from_pos), get_x_y(to_pos))
    return {"message": "Successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)