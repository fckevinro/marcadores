from .controller import SofaScoreController

def main():
    app = SofaScoreController()
    print(app.insert_partidos())
    app.mysql.close()