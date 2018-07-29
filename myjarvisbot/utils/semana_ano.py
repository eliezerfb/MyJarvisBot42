from datetime import datetime


def get_semana_ano(date=None):
    if not date:
        date = datetime.today()

    semana = int(date.strftime('%U'))
    ano = int(date.strftime('%Y'))
    return semana, ano
