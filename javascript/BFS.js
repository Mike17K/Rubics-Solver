const Queue = require('queue');
const Cube = require("./cube");

function BFS(obj_code, targetCode, history = Map()) {
  // create a new queue
  const node_queue = new Queue();

  // enqueue the initial object code
  node_queue.push(obj_code);
  while (node_queue.length!==0) {
    // dequeue the next object code
    const tmp_code = node_queue.shift();

    let obj = new Cube(tmp_code);
    
    for (let m of Cube.MOVES) {
      let tmp = obj.copy();
      tmp.move(m);

    if (history.has(tmp.code())==false) {
        // enqueue the new object code
        node_queue.push(tmp.code());
        history.set(tmp.code(), {"code":obj.code(), "move":m});
        
        //console.log(tmp.code());
        if (history.size % 1000 === 0) {
          console.log(history.size);
        }
      }
      if (tmp.code() === targetCode) {
        return 1;
      }
      
    }
  }
}

function BFS_2() {
  // implementation for BFS_2
}

module.exports = BFS;
