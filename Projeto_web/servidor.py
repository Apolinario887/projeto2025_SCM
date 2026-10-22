from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pycomm3 import LogixDriver

app = FastAPI()

# Permite que a página web (Frontend) faça pedidos a este servidor (Backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ATENÇÃO: Coloque o IP e Slot que testou e funcionou
CLP_PATH = '192.168.23.143/1/2' 

# Estrutura de dados para receber o comando de ligar/desligar
class ComandoBomba(BaseModel):
    ligar: bool

@app.get("/api/dados")
def ler_dados():
    try:
        with LogixDriver(CLP_PATH) as plc:
            # Leitura das tags globais sem o prefixo de programa
            nivel = plc.read('Nivel_Tanque')
            status = plc.read('Liga_motor_M1')
            
            return {
                "sucesso": True,
                "nivel_tanque": round(nivel.value, 1) if nivel.value else 0,
                "bomba_ligada": status.value
            }
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}

@app.post("/api/bomba")
def controlar_bomba(comando: ComandoBomba):
    try:
        with LogixDriver(CLP_PATH) as plc:
            # Escrita direta na tag de status (para efeitos de teste web)
            plc.write('Liga_motor_M1', comando.ligar)
            return {"sucesso": True, "bomba_ligada": comando.ligar}
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}