from __future__ import unicode_literals

import sys
import json
import urllib
import requests
import datetime

class ContabilizeiApi(object):
    base_url = "https://appservices.contabilizei.com.br/rest"
    VERBOSE_QUIET = 0
    VERBOSE_NORMAL = 1
    VERBOSE_DEBUG = 2

    def __init__(self, verbose=1):
        self.request = requests.Session()
        self.login_data = None
        self.headers = {}
        self.verbose = verbose

    def _post(self, url, data={}):
        target_url = self.base_url + url
        r = self.request.post(target_url, data=data, headers=self.headers)
        if self.verbose >= self.VERBOSE_DEBUG:
            print("status_code: {}".format(r.status_code))
            if "application/json" in r.headers['content-type']:
                rj = r.json()
                print(json.dumps(rj, indent=2))
            else:
                print(r.text)
        return r

    def _get(self, url, payload={}):
        target_url = self.base_url + url
        r = self.request.get(target_url, params=payload, headers=self.headers)
        if self.verbose >= self.VERBOSE_DEBUG:
            print("status_code: {}".format(r.status_code))
            if "application/json" in r.headers['content-type']:
                rj = r.json()
                print(json.dumps(rj, indent=2))
            else:
                print(r.text)
        return r

    def _fixdate(self, ano, mes):
        mes_passado = datetime.datetime.now() - datetime.timedelta(days=30)
        if mes is None:
            mes = mes_passado.month
        if ano is None:
            ano = mes_passado.year
        return ano, mes

    def verbose_print(self, min_verbose_level, msg):
        if self.verbose >= min_verbose_level:
            print(msg)

    def login(self, email, password):
        self.request.auth = (email, password)
        login_json = {"email": email, "senha": password}
        target_url = "/public/login?keepConnected=true&login={}".format(urllib.quote_plus(json.dumps(login_json)))
        self.login_data = self._post(target_url).json()
        self.headers["strinfs-token"] = self.login_data["token"]
        self.headers["userId"] = self.login_data["userId"]
        self.verbose_print(self.VERBOSE_NORMAL, "Conectado ao contabilzei.com.br como [{}]".format(email))
        return self

    def get_print(self, url):
        r = self._get(url)
        if "application/json" in r.headers['content-type']:
            rj = r.json()
            print(json.dumps(rj, indent=2))
        else:
            print(r.text)
        print "-----------------------"
        return r

    def impostos_listar(self, mes=None, ano = None):
        ano, mes = self._fixdate(ano, mes)
        self.verbose_print(self.VERBOSE_NORMAL, "Obtendo lista de impostos para {:04}-{:02}...".format(ano, mes))
        url = "/impostopagar/list/{}/{}".format(mes, ano)
        output = c._get(url).json()
        return output

    def impostos_baixar_todos(self, mes=None, ano = None):
        ano, mes = self._fixdate(ano, mes)
        self.verbose_print(self.VERBOSE_NORMAL, "Baixando todos os impostos de {:04}-{:02}...".format(ano, mes))
        impostos_json = self.impostos_listar(mes, ano)
        for imposto in impostos_json:
            nome = "{}-{:02}_{}-{:.2f}.pdf".format(ano, mes, imposto["descGuia"].replace(" ", "_"), imposto["valorTotal"])
            self.impostos_baixar(imposto["id"], nome)
        self.verbose_print(self.VERBOSE_NORMAL, "Total de impostos de {:04}-{:02} baixados: {}".format(ano, mes, len(impostos_json)))

    def impostos_baixar(self, id, name="file.pdf"):
        print "Baixando [{}]".format(name)
        url = "{}/impostopagar/download/e772481e-2851-40aa-bc7e-ff241238bd72/{}".format(self.base_url, id)
        r = requests.get(url, stream=True)

        if r.status_code == 200:
            with open(name, 'wb') as f:
                for chunk in r:
                    f.write(chunk)



if len(sys.argv) < 3:
    print("uso: {} EMAIL_CADASTRADO_NO_CONTABILIZEI SENHA".format(sys.argv[0]))
    sys.exit(2)

c = ContabilizeiApi().login(sys.argv[1], sys.argv[2])
print "-------------"
# c.pega_impostos()
c.impostos_baixar_todos()
print "-----"


# c.get_print("/responsavel/verificalogin")
# c.get_print("/empresa/getEmpresaLogada")
# c.get_print("/socio/list")
# c.get_print("/mescontabil/historico")
# c.get_print("/mescontabil/resumo/3/2016")
# c.get_print("/notafiscal/list/6/2016")
# c.get_print("/impostopagar/list/5/2016")
# c.get_print("/impostopagar/list/4/2016")
# c.get_print("/impostopagar/list/5/2016")
# c.get_print("/impostopagar/list/6/2016")
# c.get_print("/movimentacaousuario/listextrato/5/2016")
# c.get_print("/movimentacaousuario/listcaixa/5/2016")

