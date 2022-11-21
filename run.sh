docker stop $(docker ps -q --filter ancestor=scrabble_game)
docker build -t scrabble_game .
docker run -d -p 5678:5678 scrabble_game
