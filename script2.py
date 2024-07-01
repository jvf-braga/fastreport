import mysql.connector

# Configuração da conexão com o banco de dados
config = {
    'user': 'nomedouser@adb-mariadb-csi-hom',
    'password': 'pass',
    'host': 'adb-mariadb-csi-hom.mariadb.database.azure.com',
    'database': 'babytracking_homologacao'
}

conn = mysql.connector.connect(**config)
cursor = conn.cursor()

update_query_atvep = """
    UPDATE p_laudofastreport
    INNER JOIN p_laudo ON p_laudofastreport.p_idlaudo = p_laudo.p_idlaudo
    SET 
        p_laudofastreport.p_atividadeepileptica06 = p_laudo.p_atividadeepileptica,
        p_laudofastreport.p_momentocrise06 = p_laudo.p_momentocrise,
        p_laudofastreport.p_tipocrise06 = p_laudo.p_tipocrise,
        p_laudofastreport.p_classificacaocrise06 = p_laudo.p_classificacaocrise
    WHERE p_laudofastreport.p_idlaudo = p_laudo.p_idlaudo
        AND p_laudo.p_atividadeepileptica != ''
"""

cursor.execute(update_query_atvep)

# Iterar pelos campos de p_ciclod1predominante até p_ciclod10predominante
for i in range(1, 11):
    campo_ciclod = f'p_ciclod{i}predominante'
    
    # Consulta para atualizar o campo p_cicloPredominante06 na tabela p_laudofastreport
    update_query = f"""
        UPDATE p_laudofastreport
        INNER JOIN p_laudo ON p_laudofastreport.p_idlaudo = p_laudo.p_idlaudo
        SET p_laudofastreport.p_cicloPredominante06 = p_laudo.{campo_ciclod}
        WHERE p_laudofastreport.p_idlaudo = p_laudo.p_idlaudo
            AND p_laudofastreport.p_dianum = {i}
            AND p_laudo.{campo_ciclod} != ''
    """
    
    cursor.execute(update_query)
    
for i in range(1, 11):
    campo_based = f'p_based{i}predominante'
    
    # Consulta para atualizar o campo p_basedPredominante06 na tabela p_laudofastreport
    update_query = f"""
        UPDATE p_laudofastreport
        INNER JOIN p_laudo ON p_laudofastreport.p_idlaudo = p_laudo.p_idlaudo
        SET p_laudofastreport.p_basedPredominante06 = p_laudo.{campo_based}
        WHERE p_laudofastreport.p_idlaudo = p_laudo.p_idlaudo
            AND p_laudofastreport.p_dianum = {i}
            AND p_laudo.{campo_based} != ''
    """
    
    cursor.execute(update_query)
    
    
for i in range(1, 11):
    campo_based = f'p_based{i}presente'
    
    # Consulta para atualizar o campo p_basedPresente06 na tabela p_laudofastreport
    update_query = f"""
        UPDATE p_laudofastreport
        INNER JOIN p_laudo ON p_laudofastreport.p_idlaudo = p_laudo.p_idlaudo
        SET p_laudofastreport.p_basedPresente06 = p_laudo.{campo_based}
        WHERE p_laudofastreport.p_idlaudo = p_laudo.p_idlaudo
            AND p_laudofastreport.p_dianum = {i}
            AND p_laudo.{campo_based} != ''
    """
    
    cursor.execute(update_query)

conn.commit()

cursor.close()
conn.close()
