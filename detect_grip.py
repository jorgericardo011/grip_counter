import cv2

# Define as variáveis globais que armazenam as coordenadas do retângulo
drawing = False
ix, iy = -1, -1

# Define a função de callback que será chamada quando ocorrer um evento do mouse
def draw_rectangle(event, x, y, flags, params):
    global ix, iy, drawing, img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Desenha um retângulo dinâmico enquanto o mouse é arrastado
            cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

        # Desenha o retângulo final na imagem
        cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

        # Armazena as coordenadas do retângulo
        global x_rect, y_rect, w_rect, h_rect
        x_rect, y_rect, w_rect, h_rect = ix, iy, x - ix, y - iy

# Carrega a imagem da parede de escalada
img = cv2.imread(".\img\parede.jpg")

# Cria uma janela para exibir a imagem
cv2.namedWindow('Imagem original')

# Define a função de callback para a janela
cv2.setMouseCallback('Imagem original', draw_rectangle)

# Exibe a imagem na janela e aguarda a interação do usuário
while True:
    cv2.imshow('Imagem original', img)
    key = cv2.waitKey(1) & 0xFF

    # Fecha a janela se o usuário pressionar a tecla 'q'
    if key == ord('q'):
        break

# Segmenta a imagem usando as coordenadas do retângulo
roi = img[y_rect:y_rect+h_rect, x_rect:x_rect+w_rect]

# import cv2

# # Carrega a imagem
# img = cv2.imread(".\img\parede.jpg")

# # Define as coordenadas do canto superior esquerdo do retângulo
# x, y = 100, 200

# # Define as dimensões do retângulo
# width, height = 50, 50

# # Desenha o retângulo na imagem
# cv2.rectangle(img, (x, y), (x + width, y + height), (0, 255, 0), 2)

# # Segmenta a imagem usando as coordenadas do retângulo
# roi = img[y:y+height, x:x+width]

# Converte a região de interesse para escala de cinza
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# Aplica um filtro Gaussiano para reduzir o ruído
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# Binariza a imagem com um limiar adaptativo
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Encontra os contornos na imagem binarizada
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Desenha os contornos na imagem original
cv2.drawContours(img, contours, -1, (0, 0, 255), 2)

# Exibe a imagem com os contornos na janela
cv2.imshow('Imagem com contornos', img)
cv2.waitKey(0)


# # Converte a imagem para escala de cinza
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# # Aplica uma operação de thresholding para binarizar a imagem
# _, thresh = cv2.threshold(gray, 0, 100, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# # Aplica uma operação de abertura para remover pequenos ruídos
# kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
# opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

# # Aplica uma operação de fechamento para preencher lacunas nas agarras
# closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

# # Encontra os contornos das agarras
# contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE )

# # Desenha os contornos das agarras na imagem original
# cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

# # Exibe a imagem resultante
# cv2.imshow('Agarras detectadas', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
