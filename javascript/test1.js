const Cube = require("./cube");
const Queue = require("queue");
const BFS = require("./BFS");



const target = new Cube();


const m1 = new Cube();
m1.move("U");

console.log(m1.state.join(""));
