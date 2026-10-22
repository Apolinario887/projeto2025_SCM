from pycomm3 import LogixDriver

# O segredo está no "Path" (Caminho).
# Formato: IP_DO_SEU_PC/1/SLOT_DO_EMULATE
# Substitua '192.168.0.x' pelo IP da sua máquina na rede (ou tente '127.0.0.1').
# O '1' significa rotear para o backplane, e o '2' é o slot onde a CPU está no Emulate.
CLP_PATH = '192.168.23.143/1/2'

try:
    with LogixDriver(CLP_PATH) as plc:
        print("Conectado ao Emulate com sucesso!")
        
        # Lendo uma tag que você criou no Studio 5000
        valor_nivel = plc.read('Nivel_Tanque')
        Liga_motor = plc.read('Liga_motor_M1')
        Rele_Motor = plc.read('Liga_motor_M1')
        print(f"Nível do Tanque: {valor_nivel.value}")
        print(f"comando liga motor: {Liga_motor}")
        print(f"Status do modo antes do comando: {Rele_Motor}")
        
        # Escrevendo em uma tag
        if Liga_motor is False:
            plc.write('Liga_motor_M1', True)
            plc.write('Nivel_Tanque', 1200.50)
            
        else:
            plc.write('Liga_motor_M1', True) 
        

        print("Comando de ligar bomba enviado.")
except Exception as e:
    print(f"Erro ao conectar ou ler tags: {e}")