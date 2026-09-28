"""Dados compartilhados (§6.4). Texto canônico: não editar sem mudar o SPEC."""

CASES = {
 "bvba-surrealismo": dict(num="01", marca="BVBA Supply", titulo="O surrealismo", nome="BVBA Supply · O surrealismo",
   segmento="Moda", entregavel="Fashion film e editorial com IA", area="Audiovisual com IA",
   linha="Filme e editorial de coleção num museu que cede. Peça real no corpo real, sala construída com IA.",
   cover="/assets/cases/bvba-surrealismo/cover.jpg",
   cover_alt="Modelo caindo sobre uma vitrine de vidro que derrete, com um gato sentado no piso de um museu claro",
   servico="audiovisual-com-ia", ia_pessoa=False),
 "alumee-vela-mel": dict(num="02", marca="Alumee", titulo="vela Mel", nome="Alumee · vela Mel",
   segmento="Velas artesanais", entregavel="Campanha de lançamento com IA", area="Audiovisual com IA",
   linha="Cenas de lançamento criadas a partir do produto real, com rótulo, vidro e madeira preservados.",
   cover="/assets/cases/alumee-vela-mel/cover.jpg",
   cover_alt="Vela Mel da Alumee com mel escorrendo sobre a tampa de madeira, sobre pedra clara",
   servico="audiovisual-com-ia", ia_pessoa=False),
 "ana-lauren-modelo-ia": dict(num="03", marca="Ana Lauren", titulo="100% IA", nome="Ana Lauren · 100% IA",
   segmento="Criativo para anúncio", entregavel="Modelo sintética licenciável", area="IA",
   linha="Uma modelo que não existe, com o mesmo rosto em cada cena. Licenciável para anúncio e UGC (conteúdo no estilo de cliente).",
   cover="/assets/cases/ana-lauren-modelo-ia/cover.jpg",
   cover_alt="Ana Lauren, modelo criada por IA, sorrindo em close numa festa à noite",
   servico="audiovisual-com-ia", ia_pessoa=True),
 "iose-trafego-pago": dict(num="04", marca="IOSE", titulo="tráfego pago", nome="IOSE · tráfego pago",
   segmento="Educação técnica", entregavel="Gestão de tráfego pago", area="Tráfego pago",
   linha="Estrutura por curso, criativo por formato e leitura campanha por campanha.",
   cover="/assets/cases/iose-trafego-pago/cover.jpg",
   cover_alt="Anúncio vertical do IOSE para o curso Projeto de Linhas de Transmissão, com o professor em frente a uma torre",
   servico="trafego-pago", ia_pessoa=False, cover_fx=False),
}
ORDEM_CASES = ["bvba-surrealismo","alumee-vela-mel","ana-lauren-modelo-ia","iose-trafego-pago"]
SERVICES = {
 "trafego-pago": dict(titulo="Tráfego pago e performance", curto="Tráfego pago",
   linha="Meta Ads e Google Ads, lidos campanha por campanha, com a venda como régua.",
   marcadores=["Meta Ads e Google Ads","Estrutura, rastreamento e criativo por formato","Relatório que termina em decisão"],
   url="/servicos/trafego-pago/", service_type="Gestão de tráfego pago",
   # entregas: a mesma lista na home e em /servicos/trafego-pago/
   entregas=["Diagnóstico da conta que já roda",
             "Estrutura de campanha por oferta, com nomes padronizados",
             "Criativo em vídeo e imagem para cada formato",
             "Rastreamento do anúncio até o contato",
             "Leitura campanha por campanha, não pelo total do mês",
             "Relatório que termina em decisão: o que continua e o que sai"]),
 "audiovisual-com-ia": dict(titulo="Audiovisual com IA", curto="Audiovisual com IA",
   linha="Filme, campanha de produto e modelo sintética, com direção humana em cada quadro.",
   marcadores=["Fashion film e filme de marca","Campanha de produto a partir do real","Modelo sintética licenciável"],
   url="/servicos/audiovisual-com-ia/", service_type="Produção audiovisual com IA"),
 "marketing": dict(titulo="Marketing", curto="Marketing",
   linha="Página, formulário, oferta e mensagem que sustentam o anúncio.",
   marcadores=["Página de destino e site","Formulário e caminho para o WhatsApp","Oferta e mensagem"],
   url="/servicos/marketing/", service_type="Marketing de conversão"),
}
PILARES = [  # ordem canônica · não reordenar
 dict(nome="Performance", kanji=("磨","otimizar"), verbo="Otimizamos.", frase="Anúncio medido em resultado de caixa, não em curtida. A pergunta é sempre a mesma: quanto virou venda.", onde=("Tráfego pago e performance","/servicos/trafego-pago/")),
 dict(nome="Marketing", kanji=("築","construir"), verbo="Construímos.", frase="Página, formulário, oferta e mensagem que sustentam o anúncio. O clique chega num lugar pronto para vender.", onde=("Marketing","/servicos/marketing/")),
 dict(nome="IA", kanji=("知","saber · IA"), verbo="Dirigimos.", frase="IA é o ofício, não o produto. Entra no roteiro, no criativo e na leitura da campanha, sempre com direção humana.", onde=("Nos três serviços","/servicos/")),
 dict(nome="Tráfego pago", kanji=("展","escalar"), verbo="Escalamos.", frase="Gestão de campanhas em Meta Ads e Google Ads com a venda como régua. Verba lida campanha por campanha, não no total do mês.", onde=("Tráfego pago e performance","/servicos/trafego-pago/")),
 dict(nome="Audiovisual", kanji=("創","criar"), verbo="Criamos.", frase="Câmera, direção e movimento. Criativo em vídeo e imagem feito para anúncio e para ser assistido até o fim.", onde=("Audiovisual com IA","/servicos/audiovisual-com-ia/")),
]
PILARES_LINHA = "Performance · Marketing · IA · Tráfego pago · Audiovisual"
CLIENT_LOGOS = [  # arquivo em /assets/clients/ (tinta/*.webp sai de tools/logos.py; fonte: <nome>.png), alt, escala da altura base
 # escalas pela altura ótica (28/09): o emblema da Da Terrinha pede ~2,2×; nenhuma abaixo de 70% da média dos letreiros.
 # O Setor Elétrico em 0,7 (≈74% da média, ~210 px no 1440): nome e logo do IOSE estão em aberto com o Victor; não subir sem ele
 ("tinta/daterrinha.webp","Da Terrinha Alimentos",2.2),
 ("tinta/buyticket.webp","BuyTicket",0.95), ("tinta/ondaeco.webp","Onda Eco",0.95),
 ("tinta/osetor.webp","O Setor Elétrico",0.7),
 ("tinta/bvba.webp","BVBA Supply",1.1), ("tinta/uma.webp","UMA Raquel Blay",1.05),
]
