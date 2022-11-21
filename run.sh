docker stop $(docker ps -q --filter ancestor=scrabble_game)
docker build -t scrabble_game .
docker run -p 5678:5678 scrabble_game
