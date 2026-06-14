from groq import Groq
from django.conf import settings

client = Groq(
    api_key=settings.GROQ_API_KEY
)


def perguntar_ia(contexto, pergunta):

    resposta = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[

            {
                    "role": "system",
                    "content": """
                Você é o Assistente NexusHub.

                Sua função é responder utilizando somente os relatórios fornecidos.

                Regras:

                - Nunca invente informações.
                - Use apenas o conteúdo dos relatórios.
                - Se a resposta não existir, informe isso.
                - Cite o título dos relatórios utilizados.
                - Explique em passos simples.
                - Seja objetivo e profissional.
                """
            },

            {
                "role": "user",
                "content": f"""
RELATÓRIOS:

{contexto}

PERGUNTA:

{pergunta}
"""
            }

        ]

    )

    return resposta.choices[0].message.content