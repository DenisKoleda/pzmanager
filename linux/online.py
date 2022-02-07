from rcon import Client


# Отображение списка игроков в онлайне
with Client('109.195.19.162', 27015, passwd='8TNvxsxJDp') as client:
    online = client.run('players')

online = "\n".join(online.split('\n')[1:-1])

print(online)

# Отображение игроков в Array
with Client('109.195.19.162', 27015, passwd='8TNvxsxJDp') as client:
    online = client.run('players')

online = online.split('\n')[1:-1]

print(online)

# Отображение колличества игроков
with Client('109.195.19.162', 27015, passwd='8TNvxsxJDp') as client:
    online = client.run('players')

online = online.split('\n')[0].split(':')[0]

print(online)

# Отображение колличества игроков только число
with Client('109.195.19.162', 27015, passwd='8TNvxsxJDp') as client:
    online = client.run('players')

online = online.split(')')[0].split('(')[1]

print(online)
