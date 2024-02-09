let colors = [['black', '♠'], ['red', '♥'], ['black', '♣'], ['red', '♦']]
let levels = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
let jokers = [['black', 'J👻'], ['red', 'J🤡']]
let deck = []
for (let i of colors)
    for (let j of levels)
        deck.push([i[0], j + i[1]])
for (let i of jokers)
    deck.push(i)

export default deck