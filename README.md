# 📚 Objetivos / finalidade
Criar um dispositivo capaz de realizar medições contínuas de temperatura, pressão e altitude com a finalidade de fornecer ao usuário tais dados, para que o mesmo possa realizar inferências. As informações serão fornecidas pelo sensor _BMP280_, que há de comunicar-se com o _RP2040_ através do protocolo _I2C_. Além disso, o microcontrolador também processará e fornecerá as informações necessárias para display _LCD_, que por sua vez, realiza a exibição das informações periodicamente para o usuário. 

# Motivos da escolha dos componentes utilizados para resolver o problema:
- _RP2040_: A escolha do microcontrolador deu-se como sugestão do professor.
- _BMP280_: foi escolhido em contraproposta ao _BMP270_ pois o primeiro é menor e mais veloz, portanto mais eficiente.
- _LCD 16x2_: Para realizar uma exibição amigável dos dados de interesse para o usuário. 
- _PCF8574_: Nosso display _LCD_ não comunica-se utilizando _I2C_, então para normalizar a comunicação buscamos um CI para tal função.

# Problemas e dificuldades encontrados:
1. Testar o código: Como não possuímos o hardware em mãos, não tivemos como realizar testes concretos. Boa parte do nosso desenvolvimento baseou-se em exemplos de implementação de casos similares encontrados na internet. 
2. Encontrar circuito para realizar a comunicação _I2C_ entre o microcontrolador e o display
3. Realizar o roteamento da placa
