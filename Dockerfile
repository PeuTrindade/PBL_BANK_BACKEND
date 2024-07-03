FROM python

COPY . .

COPY requirements.txt .

# Instala as dependências especificadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Pede ao usuário para inserir a porta desejada no momento da execução do contêiner
CMD ["sh", "-c", "echo 'Informe a porta desejada:' && read PORT && python index.py $PORT"]

# Expõe a porta especificada pelo usuário
EXPOSE 4000