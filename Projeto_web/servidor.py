from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pycomm3 import LogixDriver

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CLP_PATH = '192.168.23.143/1/2' # Lembre-se de colocar o seu IP e Slot corretos

class ComandoBomba(BaseModel):
    ligar: bool

# Nova estrutura para o Setpoint
class ComandoSetpoint(BaseModel):
    valor: float

@app.get("/api/dados")
def ler_dados():
    try:
        with LogixDriver(CLP_PATH) as plc:
            nivel = plc.read('Nivel_Tanque')
            status = plc.read('Status_motor_M1')
            # Lemos também o setpoint atual para mostrar na tela, se desejar
            setpoint = plc.read('Setpoint_Tanque')
            
            return {
                "sucesso": True,
                "nivel_tanque": round(nivel.value, 1) if nivel.value else 0,
                "bomba_ligada": status.value,
                "setpoint_atual": round(setpoint.value, 1) if setpoint.value else 0
            }
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}

@app.post("/api/bomba")
def controlar_bomba(comando: ComandoBomba):
    try:
        with LogixDriver(CLP_PATH) as plc:
            plc.write('Status_motor_M1', comando.ligar)
            return {"sucesso": True, "bomba_ligada": comando.ligar}
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}

# Nova rota para enviar o Setpoint para o CLP
@app.post("/api/setpoint")
def escrever_setpoint(comando: ComandoSetpoint):
    try:
        with LogixDriver(CLP_PATH) as plc:
            plc.write('Setpoint_Tanque', comando.valor)
            return {"sucesso": True, "setpoint": comando.valor}
    except Exception as e:
        return {"sucesso": False, "erro": str(e)}