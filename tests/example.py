from deepsnatcher.api import API
App = API(
    History = [
        {
            "role": "system", 
            "content": "Be informative."
        }
    ], 
    Stream = (input("Stream response? ( y / n )\n.").lower()=="y"),
    Model= "standard" #input("AI Model(online,math,standard): ") or "standard"
)

while True:
    try:
        Request = App.Request(input("[User]: "))
        if Request[0] and Request[1][0]==200:
            if App.Stream:
                print(f"[DeepAI]: ",end="")
                for Piece in Request[1][1]:
                    if Piece:
                        print(Piece, end="")
                print()
            else:
                print(f"[DeepAI]: {Request[1][1]}")
        else:
            print(f"An error occured: {Request[1]}")
    except Exception as E:
        print(f"Exiting script: {E}".replace("\n","")+"\n")
