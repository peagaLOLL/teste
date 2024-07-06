import sqlite3
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = '6865859266:AAGDK_osYYARn5K8A13L15kNLdPfVDD7iXU'  # Substitua com o token do seu bot

# Função para inicializar o banco de dados SQLite
def setup_database():
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0.0
        );
    ''')
    conn.commit()
    conn.close()

# Função para obter o saldo de um usuário
def get_balance(user_id):
    conn = sqlite3.connect('balances.db')
    cursor = conn.cursor()
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    else:
        return 0.0

# Handler para o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("▶️ Assistir aos anúncios", web_app=WebAppInfo(url='https://shiny-gingersnap-56d57d.netlify.app/'))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = (
        "Assista aos anúncios e ganhe dinheiro de verdade!\n\n"
        "Clique no botão abaixo para começar a assistir aos anúncios\n"
        "👇🏽"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text, reply_markup=reply_markup)

# Handler para o comando /menu
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("▶️ Assistir aos anúncios", web_app=WebAppInfo(url='https://shiny-gingersnap-56d57d.netlify.app/'))],
        [
            InlineKeyboardButton("💸 Saldo", callback_data='saldo'),
            InlineKeyboardButton("🤝 Parceiros", callback_data='parceiros')
        ],
        [
            InlineKeyboardButton("🎯 Desafio", callback_data='desafio'),
            InlineKeyboardButton("⚙️ Outros", callback_data='outros')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = "Escolha uma opção:"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text, reply_markup=reply_markup)

# Handler para o comando /saldo
async def saldo_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    current_balance = get_balance(user_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Seu saldo é: R$ {current_balance:.2f}")

# Handler para o comando /desafios
async def desafios(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = (
        "7️⃣ Como Funciona?\n"
        "Você pode se cadastrar nos meus programas de afiliados. Eles me remuneram e, com essa remuneração, "
        "eu repasso uma parte para você. Dessa forma, todos saem ganhando. Eu lhe pago com o que eles pagam e todos ganham.\n"
        "⚠️ Você não precisa jogar ou fazer depósito, faça por conta e risco.\n\n"
        "3️⃣ Qual é a taxa de pagamento atual?\n"
        "A taxa de pagamento atual é de R$ 5,12 a R$ 10,28 por contas cadastradas pelo link.\n\n"
        "4️⃣ Como faço pra pegar a recompensa?\n"
        "Me informe no atendimento ao cliente que irei creditar o valor no bot.\n\n"
        "7️⃣ Métodos de retirada de fundos?\n"
        "Pix, bancos brasileiros, Perfect Money, criptomoeda.\n\n"
        "8️⃣ O AdPlayy App é seguro?\n"
        "Sim, o AdPlayy segue todas as diretrizes de segurança para proteger seus dados e suas transações.\n\n"
        "Se você tiver mais perguntas, entre em contato com nosso suporte ao cliente."
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)

# Handler para o comando /parceiros
async def parceiros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Informações sobre parceiros...")

# Handler para o comando /outros
async def outros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Outras informações...")

# Handler para os botões inline
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    # Resposta específica para cada opção
    if data == 'assistir_anuncios':
        # Simulando escolha aleatória de vídeo (substitua com sua lógica real)
        videos = [
            {'https://www.youtube.com/watch?v=4Jx_8e1dlNA&pp=ygULYW51bmNpbyBiZXQ%3D': 0.27},
        ]
        video = random.choice(videos)

        # Construindo a mensagem com o vídeo
        message_text = (
            f"Assista ao vídeo para ganhar R$ {video['earnings']:.2f}\n\n"
            f"Clique no botão abaixo para assistir ao vídeo\n"
            f"👇🏽 [Assistir Vídeo]({video['url']})"
        )
        await query.edit_message_text(text=message_text, parse_mode='Markdown')

        # Enviando o Web View para o usuário
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Clique no botão abaixo para assistir ao vídeo:",
                                       reply_markup=InlineKeyboardMarkup([
                                           [InlineKeyboardButton("Assistir Vídeo", url=video['url'])]
                                       ]))

    elif data == 'saldo':
        await saldo_command(update, context)
    elif data == 'parceiros':
        await parceiros(update, context)
    elif data == 'desafio':
        await desafios(update, context)
    elif data == 'outros':
        await outros(update, context)

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    # Adicionando handlers para os comandos individuais e inline buttons
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("saldo", saldo_command))
    application.add_handler(CommandHandler("desafios", desafios))
    application.add_handler(CommandHandler("parceiros", parceiros))
    application.add_handler(CommandHandler("outros", outros))

    application.add_handler(CallbackQueryHandler(button))

    setup_database()  # Inicializa o banco de dados SQLite

    application.run_polling()

if __name__ == '__main__':
    main()
