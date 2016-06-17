Esta é uma API para o site contabilizei.com.br

autor: marcos AT unitron DOT com DOT br
licensa: MIT

API para o site www.contabilizei.com.br

Por Que ?

A ideia de um contador por 50 reais por mês é fantástica.
Mas o site é muito chato de usar.

Com essa API pretendo autatizar o processo.

Atualmente já é possível baixar o PDF de todos os meus impostos em pouquíssimos segundos!


exemplo de uso:

mdiez@batman:~/code/contabilizei_api$ ./contabilizei_api.py EMAIL SENHA
Conectado ao contabilzei.com.br como [EMAIL]
-------------
Baixando todos os impostos de 2016-05...
Obtendo lista de impostos para 2016-05...
Baixando [2016-05_DAS_SIMPLES-200.00.pdf]
Baixando [2016-05_GPS_INSS-100.00.pdf]
Total de impostos de 2016-05 baixados: 2
-----


