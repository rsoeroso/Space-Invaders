import socket, pygame

host = '127.0.0.1'
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))

pygame.init()
pygame.display.set_caption(u'Keyboard events')
pygame.display.set_mode((120, 80))

while True:
  event = pygame.event.wait()

  if event.type == pygame.QUIT: # close button
    break

  if event.type == pygame.KEYDOWN:
    # key_name = pygame.key.name(event.key)
    # print('"{}" key pressed'.format(key_name))

    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
      break

    if event.key == pygame.K_LEFT:
      mySocket.send('LEFT'.encode())
    if event.key == pygame.K_RIGHT:
      mySocket.send('RIGHT'.encode())
    if event.key == pygame.K_UP:
      mySocket.send('UP'.encode())
    if event.key == pygame.K_DOWN:
      mySocket.send('DOWN'.encode())

mySocket.close()
pygame.quit()
