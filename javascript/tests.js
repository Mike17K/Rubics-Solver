const Cube = require("./cube");
const Queue = require("queue");
const BFS = require("./BFS");



const target = new Cube();


const m1 = new Cube();
m1.move("B U B U' R2");

let cube_states = new Map();

let status = BFS(m1.code(), target.code(), cube_states);

console.log(status);
console.log("Different states reached: " + cube_states.size);

// decript the solution
let movelist = [];
let prev_node_code = target.code();
while (true) {
    const s = cube_states.get(prev_node_code);

  const move = s.move;
  prev_node_code = s.code;

  movelist.push(move);

  if (prev_node_code === m1.code()) {
    break;
  }
}

// movelist.reverse();

console.log(movelist.reverse().join(" "));

