import io
import os
import textwrap

import streamlit as st
from dotenv import load_dotenv
from google import genai
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageColor


# Configuração inicial
st.set_page_config(
    page_title="OfertaFlow AI",
    page_icon="✨",
    layout="centered"
)

load_dotenv()


# Carrega uma fonte do Windows
def carregar_fonte(tamanho, negrito=False):
    if negrito:
        caminho = "C:/Windows/Fonts/arialbd.ttf"
    else:
        caminho = "C:/Windows/Fonts/arial.ttf"

    try:
        return ImageFont.truetype(caminho, tamanho)
    except OSError:
        return ImageFont.load_default()


# Centraliza um texto
def escrever_centralizado(desenho, texto, y, fonte, cor, largura):
    caixa = desenho.textbbox((0, 0), texto, font=fonte)
    tamanho_texto = caixa[2] - caixa[0]
    x = (largura - tamanho_texto) / 2
    desenho.text((x, y), texto, fill=cor, font=fonte)


# Quebra textos longos em linhas
def escrever_texto_quebrado(
    desenho,
    texto,
    y,
    fonte,
    cor,
    largura,
    caracteres=28
):
    linhas = textwrap.wrap(texto, width=caracteres)

    for linha in linhas[:3]:
        escrever_centralizado(
            desenho,
            linha,
            y,
            fonte,
            cor,
            largura
        )
        y += fonte.size + 12


# Cria a imagem da publicação
def criar_fundo_gradiente(largura, altura, cor_base):
    cor = ImageColor.getrgb(cor_base)

    cor_clara = tuple(
        min(255, valor + 115)
        for valor in cor
    )

    fundo = Image.new("RGB", (largura, altura))
    pixels = fundo.load()

    for y in range(altura):
        proporcao = y / altura

        cor_linha = tuple(
            int(
                cor_clara[i] * (1 - proporcao)
                + cor[i] * proporcao
            )
            for i in range(3)
        )

        for x in range(largura):
            pixels[x, y] = cor_linha

    return fundo
def criar_arte(
    nome_marca,
    nome_produto,
    preco,
    titulo,
    chamada,
    cor_principal,
    cor_secundaria,
    formato,
    possui_cupom,
    codigo_cupom,
    logo,
    foto_produto
):
    if formato == "Stories do Instagram — 1080 × 1920":
        largura = 1080
        altura = 1920

    elif formato == "Feed vertical — 1080 × 1350":
        largura = 1080
        altura = 1350

    else:
        largura = 1080
        altura = 1080

        imagem = criar_fundo_gradiente(
        largura,
        altura,
        cor_secundaria
    )

    desenho = ImageDraw.Draw(imagem) 
      
    fonte_marca = carregar_fonte(58, True)
    fonte_titulo = carregar_fonte(72, True)
    fonte_produto = carregar_fonte(48, True)
    fonte_preco = carregar_fonte(68, True)
    fonte_normal = carregar_fonte(42)
    fonte_cupom = carregar_fonte(46, True)

    # Nome da marca
    escrever_centralizado(
        desenho,
        nome_marca.upper(),
        75,
        fonte_marca,
        cor_principal,
        largura
    )

    # Logotipo
    if logo is not None:
        logo.seek(0)
        imagem_logo = Image.open(logo).convert("RGBA")
        imagem_logo.thumbnail((180, 180))

        imagem.paste(
            imagem_logo,
            (largura - imagem_logo.width - 50, 40),
            imagem_logo
        )

    # Título criado pela IA
    escrever_texto_quebrado(
        desenho,
        titulo,
        210,
        fonte_titulo,
        cor_principal,
        largura,
        23
    )

    # Área da imagem do produto
    margem = 90
    topo_foto = 470

    if altura == 1920:
        altura_foto = 720
    elif altura == 1350:
        altura_foto = 480
    else:
        altura_foto = 330

    caixa_foto = (
        margem,
        topo_foto,
        largura - margem,
        topo_foto + altura_foto
    )

    desenho.rounded_rectangle(
        caixa_foto,
        radius=45,
        fill="white",
        outline=cor_principal,
        width=8
    )

    if foto_produto is not None:
        foto_produto.seek(0)
        foto = Image.open(foto_produto).convert("RGB")

        tamanho_foto = (
            largura - (margem * 2) - 24,
            altura_foto - 24
        )

        foto = ImageOps.fit(
            foto,
            tamanho_foto,
            method=Image.Resampling.LANCZOS
        )

        imagem.paste(
            foto,
            (margem + 12, topo_foto + 12)
        )

    else:
        escrever_centralizado(
            desenho,
            "ESPAÇO PARA FOTO DO PRODUTO",
            topo_foto + (altura_foto // 2),
            fonte_normal,
            cor_principal,
            largura
        )

    # Nome do produto
    y_produto = topo_foto + altura_foto + 45

    escrever_texto_quebrado(
        desenho,
        nome_produto,
        y_produto,
        fonte_produto,
        cor_principal,
        largura,
        32
    )

    # Preço
    preco_formatado = (
        f"R$ {preco:.2f}"
        .replace(".", ",")
    )

    y_preco = y_produto + 130

    desenho.rounded_rectangle(
        (
            170,
            y_preco,
            largura - 170,
            y_preco + 120
        ),
        radius=40,
        fill=cor_principal
    )

    escrever_centralizado(
        desenho,
        preco_formatado,
        y_preco + 20,
        fonte_preco,
        "white",
        largura
    )

    # Cupom
    y_cupom = y_preco + 155

    if possui_cupom:
        desenho.rounded_rectangle(
            (
                140,
                y_cupom,
                largura - 140,
                y_cupom + 105
            ),
            radius=30,
            fill="white",
            outline=cor_principal,
            width=6
        )

        texto_cupom = f"CUPOM: {codigo_cupom.upper()}"

        escrever_centralizado(
            desenho,
            texto_cupom,
            y_cupom + 22,
            fonte_cupom,
            cor_principal,
            largura
        )

        y_chamada = y_cupom + 145

    else:
        y_chamada = y_cupom + 20

    # Chamada final
    escrever_texto_quebrado(
        desenho,
        chamada,
        y_chamada,
        fonte_normal,
        cor_principal,
        largura,
        38
    )

    # Salva a arte na memória
    arquivo = io.BytesIO()
    imagem.save(arquivo, format="PNG")
    arquivo.seek(0)

    return imagem, arquivo


# Cabeçalho do site
st.title("OfertaFlow AI")
st.subheader("Conteúdo inteligente para marcas que desejam se destacar")

st.write(
    "Crie publicações personalizadas para o Instagram utilizando "
    "a identidade visual da sua marca."
)

st.divider()


# Informações da marca
st.header("1. Informações da marca")

nome_marca = st.text_input(
    "Nome da marca",
    placeholder="Digite o nome que será exibido na publicação"
)

segmento = st.text_input(
    "Segmento de atuação",
    placeholder="Informe a principal área de atuação da marca"
)

publico_alvo = st.text_area(
    "Público-alvo",
    placeholder="Descreva o perfil das pessoas que a marca deseja alcançar"
)


# Identidade visual
st.header("2. Identidade visual")

estilo_visual = st.selectbox(
    "Estilo da marca",
    [
        "Minimalista",
        "Moderno",
        "Elegante",
        "Delicado",
        "Criativo",
        "Sofisticado",
        "Descontraído"
    ]
)

cor_principal = st.color_picker(
    "Cor principal",
    "#E75480"
)

cor_secundaria = st.color_picker(
    "Cor de fundo",
    "#FFF4E6"
)

logo = st.file_uploader(
    "Logotipo da marca",
    type=["png", "jpg", "jpeg"]
)


# Informações do produto
st.header("3. Informações do produto ou serviço")

nome_produto = st.text_input(
    "Nome do produto ou serviço"
)

descricao_produto = st.text_area(
    "Características ou benefícios",
    placeholder="Informe os principais diferenciais"
)

preco = st.number_input(
    "Preço",
    min_value=0.0,
    format="%.2f"
)

foto_produto = st.file_uploader(
    "Foto do produto ou serviço",
    type=["png", "jpg", "jpeg"]
)


# Formato
st.header("4. Formato da publicação")

formato = st.selectbox(
    "Escolha o formato",
    [
        "Stories do Instagram — 1080 × 1920",
        "Feed vertical — 1080 × 1350",
        "Feed quadrado — 1080 × 1080"
    ]
)

objetivo = st.selectbox(
    "Objetivo da publicação",
    [
        "Divulgar um produto ou serviço",
        "Promover uma oferta",
        "Aumentar as vendas",
        "Atrair novos clientes",
        "Fortalecer a marca",
        "Gerar engajamento"
    ]
)

possui_cupom = st.checkbox(
    "Adicionar cupom de desconto"
)

codigo_cupom = ""

if possui_cupom:
    codigo_cupom = st.text_input(
        "Código do cupom"
    )


# Geração
if st.button(
    "Gerar publicação",
    use_container_width=True
):
    campos_obrigatorios = (
        nome_marca
        and segmento
        and publico_alvo
        and nome_produto
        and descricao_produto
        and preco > 0
    )

    if not campos_obrigatorios:
        st.warning(
            "Preencha todas as informações obrigatórias."
        )

    elif possui_cupom and not codigo_cupom:
        st.warning(
            "Digite o código do cupom."
        )

    else:
        chave_api = os.getenv("GEMINI_API_KEY")

        if not chave_api:
            st.error(
                "A chave GEMINI_API_KEY não foi encontrada no arquivo .env."
            )

        else:
            with st.spinner("Criando o conteúdo e a arte..."):
                cliente = genai.Client(api_key=chave_api)

                prompt = f"""
                Crie conteúdo curto e profissional para uma publicação
                do Instagram.

                Marca: {nome_marca}
                Segmento: {segmento}
                Público-alvo: {publico_alvo}
                Produto ou serviço: {nome_produto}
                Características: {descricao_produto}
                Objetivo: {objetivo}
                Estilo da marca: {estilo_visual}

                Responda exatamente em duas linhas:
                TITULO: um título com no máximo 7 palavras
                CHAMADA: uma chamada para ação com no máximo 10 palavras
                """

                resposta = cliente.models.generate_content(
                    model="gemini-3.1-flash-lite",
                    contents=prompt
                )

                titulo = nome_produto
                chamada = "Saiba mais e aproveite esta oportunidade"

                for linha in resposta.text.splitlines():
                    if linha.upper().startswith("TITULO:"):
                        titulo = linha.split(":", 1)[1].strip()

                    if linha.upper().startswith("CHAMADA:"):
                        chamada = linha.split(":", 1)[1].strip()

                arte, arquivo = criar_arte(
                    nome_marca,
                    nome_produto,
                    preco,
                    titulo,
                    chamada,
                    cor_principal,
                    cor_secundaria,
                    formato,
                    possui_cupom,
                    codigo_cupom,
                    logo,
                    foto_produto
                )

                st.success("Publicação criada com sucesso!")

                st.image(
                    arte,
                    caption="Prévia da publicação",
                    use_container_width=True
                )

                st.download_button(
                    "Baixar imagem em PNG",
                    data=arquivo,
                    file_name="ofertaflow_publicacao.png",
                    mime="image/png",
                    use_container_width=True
                )

