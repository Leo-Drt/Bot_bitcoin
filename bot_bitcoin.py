import ssl
import json

import websocket
import bitstamp.client
import credenciais

def cliente():
    return bitstamp.client.Trading(username=credenciais.USERNAME, key=credenciais.KEY, secret= credenciais.SECRET)


def comprar(quantidade):
    trading_client= cliente()
    trading_client.buy_market_order(quantidade)

def vender(quantidade):
    trading_client= cliente()
    trading_client.sell_market_order(quantidade)

def ao_abrir(ws):
    print("ABRIU!")

    json_subscrible= """
     {
    "event": "bts:subscribe",
    "data": {
        "channel": "live_trades_btcusd"
    }
}   
"""
    ws.send(json_subscrible)
   
def ao_fechar(ws):
    print("FECHOU!")

def erro(ws,erro):
    print("ERRO!")
    print(erro)
    

def ao_receber_mensagem(ws, mensagem):
    try:
        print("MENSAGEM!")
        mensagem= json.loads(mensagem)
        print(mensagem['data']['price'])

        global preco
        preco= mensagem['data']['price']
        if preco > 17000:
            vender()
        elif preco < 16000:
            comprar()
        else:
            print("AGUARDAR!")

    except Exception as error:
        print(error)


if __name__== "__main__":
    
    ws = websocket.WebSocketApp("wss://ws.bitstamp.net",
                                on_open= ao_abrir,
                                on_message=ao_receber_mensagem,
                                on_close=ao_fechar,
                                on_error=erro)
    
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    