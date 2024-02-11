let styles = [['black', '♠'], ['red', '♥'], ['black', '♣'], ['red', '♦']]
let colors = ['♠', '♥', '♣', '♦']
let levels = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
let jokers = [['black', 'J', '👻'], ['red', 'J', '🤡']]
let deck = []
for (let i of styles)
    for (let j of levels)
        deck.push([i[0], i[1], j])
for (let i of jokers)
    deck.push(i)

export default {
    styles,
    colors,
    levels,
    jokers,
    deck
}