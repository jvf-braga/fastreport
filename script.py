import mysql.connector
import datetime

# Configuração da conexão com o banco de dados
config = {
    'user': 'nomedouser@adb-mariadb-csi-hom',
    'password': 'pass',
    'host': 'adb-mariadb-csi-hom.mariadb.database.azure.com',
    'database': 'babytracking_homologacao'
}


def calcular_dia_laudo(data_inicial, data_final=None):
    try:
        partes_data_inicial = data_inicial.split("-")
        if data_final:
            partes_data_final = data_final.split("-")
        else:
            data_final_obj = datetime.datetime.now()

        if len(partes_data_inicial) == 3:
            data_inicial_obj = datetime.datetime(int(partes_data_inicial[0]), int(partes_data_inicial[1]), int(partes_data_inicial[2]))
            if data_final:
                data_final_obj = datetime.datetime(int(partes_data_final[0]), int(partes_data_final[1]), int(partes_data_final[2]))

            diferenca_ms = (data_final_obj - data_inicial_obj).total_seconds() * 1000
            diferenca_dias = int(diferenca_ms / (1000 * 60 * 60 * 24)) + 1

            if not isinstance(diferenca_dias, int):
                return 0
            else:
                # Limitar ao máximo de 10 dias
                return min(diferenca_dias, 10)
        else:
            return 0
    except Exception as e:
        print(f"Erro ao calcular dias entre {data_inicial} e {data_final}: {e}")
        return 0
      
      
# Conexão com o banco de dados
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Consulta dos laudos
query_laudos = "SELECT * FROM p_laudo"
cursor.execute(query_laudos)
laudos = cursor.fetchall()

query_insert = """
INSERT INTO p_laudofastreport (
  p_idfastreport,
  p_idlaudo,
  p_diavar,
  p_dianum,
  p_tipocrise23,
  p_tipocrise18,
  p_tipocrise12,
  p_tipocrise06,
  p_tendenciaNirs23,
  p_tendenciaNirs18,
  p_tendenciaNirs12,
  p_tendenciaNirs06,
  p_temp23,
  p_temp18,
  p_temp12,
  p_temp06,
  p_spo223,
  p_spo218,
  p_spo212,
  p_spo206,
  p_pas23,
  p_pas18,
  p_pas12,
  p_pas06,
  p_pam23,
  p_pam18,
  p_pam12,
  p_pam06,
  p_pad23,
  p_pad18,
  p_pad12,
  p_pad06,
  p_obsNirs23,
  p_obsNirs18,
  p_obsNirs12,
  p_obsNirs06,
  p_momentocrise23,
  p_momentocrise18,
  p_momentocrise12,
  p_momentocrise06,
  p_limitesNormalidadeNirs23,
  p_limitesNormalidadeNirs18,
  p_limitesNormalidadeNirs12,
  p_limitesNormalidadeNirs06,
  p_horafrCicloSonoeVigilia23,
  p_horafrCicloSonoeVigilia18,
  p_horafrCicloSonoeVigilia12,
  p_horafrCicloSonoeVigilia06,
  p_horafrAtvEletricaBase23,
  p_horafrAtvEletricaBase18,
  p_horafrAtvEletricaBase12,
  p_horafrAtvEletricaBase06,
  p_horafr23,
  p_horafr18,
  p_horafr12,
  p_horafr06,
  p_fr23,
  p_fr18,
  p_fr12,
  p_fr06,
  p_fdeletado,
  p_fc23,
  p_fc18,
  p_fc12,
  p_fc06,
  p_dataupdate,
  p_dataregistro,
  p_classificacaocrise23,
  p_classificacaocrise18,
  p_classificacaocrise12,
  p_classificacaocrise06,
  p_cicloPredominante23,
  p_cicloPredominante18,
  p_cicloPredominante12,
  p_cicloPredominante06,
  p_basedPresente23,
  p_basedPresente18,
  p_basedPresente12,
  p_basedPresente06,
  p_basedPredominante23,
  p_basedPredominante18,
  p_basedPredominante12,
  p_basedPredominante06,
  p_basedAssimetria23,
  p_basedAssimetria18,
  p_basedAssimetria12,
  p_basedAssimetria06,
  p_atividadeepileptica23,
  p_atividadeepileptica18,
  p_atividadeepileptica12,
  p_atividadeepileptica06
) VALUES (
    NULL, 
    %s, 
    %s, 
    %s, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL,
    NULL,
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL,
    NULL,
    NULL,
    NULL,
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL,
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL,
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL,
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL,
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL,
    NULL, 
    NULL, 
    NULL, 
    NULL, 
    NULL
)
"""

log_falhas = []

for laudo in laudos:
    try:
        data_inicial = laudo[28] if laudo[28] else None
        data_final = laudo[31] if laudo[31] else None
        if data_inicial:
            dias_entre_datas = calcular_dia_laudo(data_inicial, data_final)
            if dias_entre_datas > 0:
                for i in range(1, dias_entre_datas + 1):
                    p_diavar = f'D{i}'
                    p_dianum = i
                    cursor.execute(query_insert, (laudo[0], p_diavar, p_dianum))
                print(f"Laudo ID {laudo[0]} inserido com sucesso {dias_entre_datas} vezes.")
            else:
                log_falhas.append((laudo[0], data_inicial, data_final, "Diferença de dias não é positiva"))
                print(f"Laudo ID {laudo[0]} não inserido: diferença de dias não é positiva.")
        else:
            log_falhas.append((laudo[0], data_inicial, data_final, "Data inicial inválida"))
            print(f"Laudo ID {laudo[0]} não inserido: data inicial inválida.")
    except Exception as e:
        log_falhas.append((laudo[0], data_inicial, data_final, str(e)))
        print(f"Laudo ID {laudo[0]} não inserido: erro - {e}")

conn.commit()

cursor.close()
conn.close()

print("\nLog de Falhas:")
for falha in log_falhas:
    print(f"Laudo ID {falha[0]}, Data Inicial: {falha[1]}, Data Final: {falha[2]}, Motivo: {falha[3]}")