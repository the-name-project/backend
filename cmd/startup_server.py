if __name__ == "__main__":
    from os import system
    system("cd .. && uvicorn app.main:app --reload --reload-dir app")